# -*- coding: utf-8 -*-

'''
cleanpdb.py - removes rotamers and non-protein molecules

'''


import sys
import os

import helpers
try:
    from exceptions import RuntimeError
except ImportError:
    from builtins import RuntimeError

'''
remove_rotamers: uses pymol to keep a single rotamer from the pdb file

Inputs:
string output_filename: a filename (full path) where the pdb file with rotamers is located
string exec_folder: location where the python scripts are located

Outputs:
structure args: structured object with fields corresponding to the possible parameters from command line
'''
def remove_rotamers(output_filename,exec_folder):
    # calls pymol using remove_rotamers.py - for details on this, see that file!
    os.system('pymol -qc '+exec_folder+'/remove_rotamers.py '+output_filename)


'''
cleanPDB: 

Inputs: 
argument list args: object containing all command-line arguments as parsed by pdb2movie

Outputs:
string output_filename: a filename (full path) where the clean pdb file will be located

'''
def cleanPDB(args):

    # opens the input file received as one of the arguments for reading
    inputfile=open(args.pdbfile[0],'r')

    # set args.keep as a list of molecules that need to be kept, based on the arguments received
    # if there are any to keep, make/move to a folder for them, named after them in alphabetical order
    if (args.keep==None):
        args.keep=[]
    if args.waters:
        args.keep.append('HOH')
    if (args.keep!=[]):
        print("Keeping the following molecules: ")
        for i in args.keep:
            print(i)
        args.keep.sort()
        os.system("mkdir -p " + '_'.join(args.keep))
        os.chdir('_'.join(args.keep))

    # initialise a list of residues
    residues=[]

    # set output filename based on arguments received and open that file for writing
    output_filename="./"+args.pdbfile[0].rsplit("/",1)[1][:-4]+"_clean.pdb"
    print(output_filename)
    output=open(output_filename,'w')

    # goes over every single line from tge 
    for line in inputfile:
        #print(line)
        # only looks at atoms in the PDB file
        if (line[0:6].strip()=='ATOM'):


            # if there are multiple chains and the "multiple" flag has not been set, only use the first chain
            if ((line[21]!='A' and line[21]!=' ') and not(args.multiple)):

                continue

            # add the residue number to the list of residues
            residues.append(int(line[23:26].strip()))


        # this section looks at the HETATM lines in the file
        if (line[0:6]=='HETATM'):

            # if any extraneous molecules need to be kept, check whether this HETATM is part of one of them and keep it or not
            if args.keep:

                if line[17:20].strip() in args.keep:

                    output.write(line)
                    #print("printing line" +line)
            continue

        # if you didn't hit a continue, you get here and that line is kept
        #print("printing line" +line)
        output.write(line)

    # takes only unique values of residues list
    residues=list(set(residues))

    # check whether there are missing residues by comparing the list with a range
    try:
	    for i in range(residues[0],residues[-1]):
	        if (not(i in residues)):
	            print("WARNING: residue "+str(i)+" is missing!")
    except:
	    raise RuntimeError("cleanpdb: chain A seems to be empty/non-existent! --- aborting")

    # close files
    inputfile.close()
    output.close()

    # calls pymol to remove remaining rotamers
    #remove_rotamers(output_filename,exec_folder)

    #done!
    return output_filename


#calling this as a single script will probably not work, I think?
if __name__ == "__main__":
    # parse commmand-line arguments
    args=helpers.parsing_args(sys.argv)

    # set the output folder if not specified
    if (not args.output):
        args.output = [args.pdbfile[0][:-4]]

    # change directory to the output folder
    helpers.go_to_output_folder(args)

    cleanPDB(args)
