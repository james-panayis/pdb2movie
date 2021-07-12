'''
this contains some useful helper functions used throughout the project
'''

import os
import argparse

'''
parsing_args: takes all command-line arguments and parse them into a structure with argument fields

Inputs:
list sys_args: list of system arguments as received in the command line

Outputs:
structure args: structured object with fields corresponding to the possible parameters from command line
'''

def parsing_args(sys_args):

    # the argparse library takes care of all the parsing from a list of
    # command-line arguments to a structure
    parser = argparse.ArgumentParser(description='Runs simulations and generates videos for the most likely movement modes given a PDB file.',usage='%(prog)s pdbfile [options]')

    parser.add_argument('--keep',  nargs="+",
                        help='List of molecules to be kept')
    parser.add_argument('--output',  nargs=1,
                        help='Output directory')
    parser.add_argument('--res',  nargs=2, type=int, default=[640, 480], 
                        help='Video resolution (width, height), range [16, 8192]')
    parser.add_argument('--waters',  action='store_true',
                        help='Flag for keeping water molecules')
    parser.add_argument('--multiple',  action='store_true',
                        help='Keep multiple chains (default: uses only chain A)')
    parser.add_argument('--nomovie',  action='store_true',
                        help='Stop calculation after FRODA and before any attempt to generate images and movies')
    parser.add_argument('--combi',  action='store_true',
                        help='Combine both positive and negative directions into a single movie')
    parser.add_argument('--threed',  action='store_true',
                        help='Flag for generating anaglyph stereo movies')
    parser.add_argument('--confs',  nargs=1,
                        help='Total number of configurations to be calculated')
    parser.add_argument('--freq',  nargs=1,
                        help='Frequency of saving intermediate configurations')
    parser.add_argument('--step',  nargs=1,
                        help='Size of random step')
    parser.add_argument('--dstep',  nargs=1,
                        help='Size of directed step')
    parser.add_argument('--modes',  nargs="+",
                        help='Movement modes to be investigated')
    parser.add_argument('--ecuts',  nargs="+",
                        help='Energy cutoff values')
    parser.add_argument('--video',  nargs=1,
                        help='File with PyMOL or VMD commands to be run before generating video')
    parser.add_argument('pdbfile', metavar='PDB', type=str, nargs=1,
                        help='Initial PDB file')
    parser.add_argument('--videocodec', type=str, default="mp4", 
                        help="Use 'mp4' or 'hevc' to enode the videos, resulting in .mp4 or .mov files (defaults to mp4)")
    parser.add_argument('--drawingengine', type=str, default="pymol", 
                        help="Use 'vmd' or 'pymol' to render pdb files to frames (defaults to pymol for now)")
    parser.add_argument('--fps',  nargs=1, type=int, default=30,
                        help='Frames per second of the videos, range [1, 240]')

    # actually do the parsing for all system args other than 0
    # (which is the python script name) and return the structure generated
    args = parser.parse_args(sys_args[1:])

    #ensure pdbfile and output are full paths, not relative ones (so they are correct from here on, regardless of pwd)
    args.pdbfile[0] = os.path.abspath(args.pdbfile[0])
    if (args.output):
        args.output[0] = os.path.abspath(args.output[0])
    
    return args


'''
go_to_output_folder: creates or (if necessary) empties output folder and enters it,
                     and warns user before deletions if necessary

Inputs:
argument list args: object containing all command-line arguments as parsed by pdb2movie

Outputs:
None
'''

def go_to_output_folder(args):

    # make or (if necessary) empty the output folder, warning the user before any emptying occurs
    try:
        os.mkdir(args.output[0])
    except Exception:
        #try:
        #    userinput=raw_input("WARNING: everything in output folder will be deleted! Are you sure you want to continue? [y/N]   ")
        #except NameError:
        #    userinput=input("WARNING: everything in output folder will be deleted! Are you sure you want to continue? [y/N]   ")
        #if (userinput=="y"):
            os.system("rm -r -f "+args.output[0]+"/*")
        #else:
        #    quit()

    #enter the output folder
    os.chdir(args.output[0])
