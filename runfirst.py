# -*- coding: utf-8 -*-

'''
runfirst.py - functions to run FIRST simulations, analyzing rigidity in proteins
'''


import os


'''
firstsim - main function for running FIRST analysis on a protein

Inputs:
- string exec_folder: folder where the python scripts are located (full path)
- string cleanpdb: full path to PDB file after cleaning (by extension, also includes path to where all outputs are)

Outputs:
- string hydropdb: full path to PDB file after addition of hydrogens 

'''


def firstsim(exec_folder,cleanpdb):

    print ("---------------------------------------------------------------")
    print ("firstsim:")
    print ("----------------------------------------------------------------")

    # now, we need to run reduce to add hydrogens to protein residues - this generates a PDB file with hydrogens

    print ("---------------------------------------------------------------")
    print ("firstsim: calling reduce.3.23.130521")
    print ("----------------------------------------------------------------")

    # print              "./reduce.3.23.130521 -DB "+exec_folder+"/reduce_het_dict.txt -build "+cleanpdb+" > "+cleanpdb[:-9]+ "hydro.pdb"
    os.system(exec_folder+"/reduce.3.23.130521 -DB "+exec_folder+"/reduce_het_dict.txt -build "+cleanpdb+" > "+cleanpdb[:-9]+"hydro.pdb")

    # now, we call an external function to renumber the atoms taking the hydrogens into account
    renum_atoms(cleanpdb[:-9]+"hydro.pdb")

    # finally we run FIRST with the PDB after hydrogen addition!

    print ("---------------------------------------------------------------")
    print ("firstsim: running FIRST with new PDB file after hydrogens added")
    print ("----------------------------------------------------------------")

    os.system(exec_folder+"/FIRST-190916-SAW/src/FIRST "+cleanpdb[:-9]+"hydro.pdb -non -dil 1 -E -0 -covout -hbout -phout -srout -L "+exec_folder+"/FIRST-190916-SAW")

    # finally, return the hydro-added PDB path
    return cleanpdb[:-9]+"hydro.pdb"


'''
renum_atoms: renumber the atoms in a PDB file to make sure they're in order and without gaps

Inputs:
string filename: path to origin PDB file

'''


def renum_atoms(filename):

    # open the input file and a temp file
    inputfile=open(filename,'r')
    tempfile=open("tmp.pdb",'w')

    # let's learn how to count!
    counter=1

    print ("---------------------------------------------------------------")
    print ("renum_atoms:")
    print ("----------------------------------------------------------------")

    # looping over every line in the input file
    for line in inputfile:

        # if line is an atom...
        if (line[0:6].strip()=='ATOM' or line[0:6].strip()=='HETATM'):

            # we chop up the line, cutting out the current atom number and putting the value of counter as atom number
            line=line[:6]+format(counter, '05d')+line[11:]

            # write it to temp file and increase counter
            tempfile.write(line)
            counter=counter+1

    # now we can close them both
    inputfile.close()
    tempfile.close()

    # finally, we replace the original file with the temporary one
    os.system("rm "+filename)
    os.system("mv tmp.pdb "+filename)
