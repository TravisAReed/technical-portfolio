#!/usr/bin/env python
# coding: utf8


################################################################
#
# Trajectories file *.cndb to Nucleome Data Bank format .ndb and/or .pdb
#
# usage:
#  ./cndb2pdb.py -f file.cndb -n name_NDB_file
#
################################################################



"""
Convert a .cndb (HDF5) trajectory file to an .pdb text format for Nucleome Data Bank.

to run:
python3 cndb2pdb.py -f <filename>.cndb -n <output_filename>
*just do the output filename, it will add .pdb automatically and will be located in the same directory as the input file.
"""



import argparse
import subprocess




def convert(inp, newFile='', cndbExists=True, onlyNdb=False, delNdb=True):

    print('converting', inp, '...')

    pathLoc = inp.rfind('/')
    inDir = inp[:pathLoc+1] if pathLoc != -1 else './'


    if len(newFile) == 0:
        newFile = inp[pathLoc+1:].split('.')[0]

    # print(newFile)
    print('inputDirectory:', inDir+newFile)

    #convert cndb to ndb
    # cmd = 'PROMPT:       '+       f"python3 cndb2ndb.py -f {inp} -n {newFile}"
    # # cmd = 'PROMPT:       '+       f"python3 ndb2pdb.py -f {inDir+newFile}.ndb -n {inDir+newFile}"
    # print(cmd)
    if cndbExists:
        subprocess.run(f"python3 cndb2ndb.py -f {inp} -n {newFile}", shell=True, check=True)
    # else:
    #     newFile = inp
    #convert ndb to pdb if wanted
    if onlyNdb:
        return
    subprocess.run(f"python3 ndb2pdb.py -f {newFile}.ndb -n {inDir+newFile}", shell=True, check=True)
    #delete the ndb file after conversion
    if delNdb:
        subprocess.run(f"rm {newFile}.ndb", shell=True, check=True)





def convFiles(inputs):
    for inp in inputs:
        convert(inp=inp, newFile=newFile, delNdb=False)





parser = argparse.ArgumentParser(description="Convert CNDB to NDB format")
parser.add_argument("-f", required=True, help="Input .cndb HDF5 file")
parser.add_argument("-n", default="", help="Base name for output .ndb file")



try:
    args = parser.parse_args()
    inp = args.f
    newFile = args.n
    print('no inputs were given in argument')
except:
    # inp = '../move/nucleus1_80.cndb'
    # inp = '/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb'
    newFile = ''





# pathLoc = args.f.rfind('/')
# path = args.f[:pathLoc+1] if pathLoc != -1 else './'
# pathN = path + args.n
# print('pathN:', pathN)




# inp = args.f
# pathLoc = inp.rfind('/')
# inDir = inp[:pathLoc+1] if pathLoc != -1 else './'


# if len(newFile) == 0:
#     newFile = inp[pathLoc+1:].split('.')[0]

# # print(newFile)
# print('inputDirectory:', inDir+newFile)









# convert(inp=inp, newFile=newFile, delNdb=False)
# convert(inp=inp, newFile=newFile, delNdb=True)
# convert(inp=inp, newFile=newFile, onlyNdb=True)
# convert(inp=inp, newFile=newFile, cndbExists=False, delNdb=False)



# convFiles([
#     '../move/nucleus0_12.cndb',
#     '../move/nucleus1_12.cndb',
#     '../move/nucleus0_80.cndb',
#     '../move/nucleus1_80.cndb'
#     ])

# convFiles([
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_1.cndb',
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_2.cndb',
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_3.cndb',
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_1.cndb',
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_2.cndb',
#     '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_3.cndb',
    
#     ])




def convNdb2Pdb(inp,newFile=''):

    pathLoc = inp.rfind('/')
    inDir = inp[:pathLoc+1] if pathLoc != -1 else './'

    if len(newFile) == 0:
        newFile = inp[pathLoc+1:].split('.')[0]

    subprocess.run(f"python3 ndb2pdb.py -f {inp} -n {inDir+newFile}", shell=True, check=True)

# inp = '/home/treed777/cluster_runs/collapsed/OpenMiChroM_step0.ndb'
# inp = '/home/treed777/move/C1.ndb'
# inp = '/home/treed777/move/C2.ndb'
inp = '/home/treed777/move/nucleus_0_step100000.ndb'
inp = '/home/treed777/move/nucleus_1_step100000.ndb'


convNdb2Pdb(inp)










# import argparse
# import numpy as np
# import h5py
# import time
# from pathlib import Path

# # ------------------------- Argument Parser -------------------------
# parser = argparse.ArgumentParser(description="Convert CNDB to NDB format")
# parser.add_argument("-f", required=True, help="Input .cndb HDF5 file")
# parser.add_argument("-n", default="output", help="Base name for output .ndb file")
# parser.add_argument("-res", default=50000, type=int, help="Resolution in bp")
# parser.add_argument("-chroID", default="C", help="Chromosome chain ID")
# parser.add_argument("-sigma", default=0.000, type=float, help="Fluctuation sigma")
# parser.add_argument("-scale", default=1.000, type=float, help="Distance scale")
# args = parser.parse_args()

# start_time = time.time()

# # ------------------------ Load .cndb File --------------------------
# cndb_file = Path(args.f)
# if not cndb_file.exists():
#     raise FileNotFoundError(f"Input file not found: {args.f}")

# f = h5py.File(cndb_file, "r")
# types = list(f["types"].asstr())

# try:
#     loops = np.array(f["loops"])
#     has_loops = True
# except KeyError:
#     has_loops = False

# frames = sorted(k for k in f.keys() if k.isdigit())


# #Travis additions
# # print('args.f:', args.f)
# # print('args.n:', args.n)

# pathLoc = args.f.rfind('/')
# path = args.f[:pathLoc+1] if pathLoc != -1 else './'
# pathN = path + args.n
# print('pathN:', pathN)




# # ---------------------- Write .ndb Header --------------------------
# # with open(args.n + ".ndb", "w") as out:
# with open(pathN + ".ndb", "w") as out:
#     out.write("HEADER    Converted from CNDB\n")
#     out.write("TITLE     Generated by cndb2ndb.py\n")
#     out.write("AUTHOR    Auto-generated\n")
#     out.write("EXPDTA    Simulated\n")

#     # Write SEQCHR entries
#     for i, chunk in enumerate([types[x:x+23] for x in range(0, len(types), 23)]):
#         out.write(f"SEQCHR {i+1:3d} {args.chroID:2s} {len(types):5d}  {' '.join(chunk):69s}\n")

#     # ------------------ Write Each Frame ----------------------
#     for frame_id in frames:
#         data = np.array(f[frame_id])
#         out.write(f"MODEL     {int(frame_id):4d}\n")

#         for i, (x, y, z) in enumerate(data):
#             subtype = types[i] if i < len(types) else 'UN'
#             start = i * args.res + 1
#             end = (i + 1) * args.res
#             out.write(f"CHROM  {i+1:8d} {subtype:2s}       {args.chroID:4s} {i+1:8d} {x:8.3f} {y:8.3f} {z:8.3f} {start:10d} {end:10d} {args.sigma:8.3f}\n")

#         out.write(f"TER   {len(data)+1:8d} {subtype:2s}        {args.chroID}\n")
#         out.write("ENDMDL\n")

#     # ------------------ Write Loops --------------------------
#     if has_loops:
#         for i, j in loops:
#             out.write(f"LOOPS  {i:8d} {j:8d}\n")

#     out.write("END\n")

# print(f"Converted {len(frames)} frames from {args.f} to {args.n}.ndb")
# print("Elapsed time: %.2f seconds" % (time.time() - start_time))


# #run exit() if trying to do cndb2ndb
# # exit()

# ##to make it convert straight from cndb to pdb
# import subprocess
# subprocess.run(f"python3 ~/back_scripts/ndb2pdb.py -f {pathN}.ndb -n {pathN}", shell=True, check=True)
# #delete the ndb file after conversion
# # subprocess.run(f"rm -r {pathN}.ndb", shell=True, check=True)
