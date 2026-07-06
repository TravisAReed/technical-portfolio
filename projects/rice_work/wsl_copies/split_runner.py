##setup
print('running cmd_runner.py ...')

import os
import subprocess
import argparse
import time

##to change the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

##defining the functions
def splitChromosome(initFile, pyLoc="", splitLoc=-1): #eventually need to modify this to be able to split multiple times (either recursion on another decent-sized function)
    '''
    runs the scripts to split a chromosome at a split location.

    number of splits does not matter if split location (splitLoc) is manually specified.
    '''
    if len(pyLoc) > 0:
        pyLoc = pyLoc + '/'

    # #determine the split location. If it is negative, it will split the chromosome in half
    # if splitLoc < 0:
    #     with open(initFile, "r") as r:
    #         #read the first line after the 6th line
    #         for i in range(6):
    #             r.readline()
    #         ln = r.readline()[15:19]  # reads the 7th line, which contains the chromosome length, assuming length is 4 digits
    #         # splitLoc = int(ln) // splits+1  # sets the split location to half the chromosome length #more complex to get into 3 parts than just replacing the 2 with the 3 but may still be useful to calculate. I'll probably make there be an optional function call on how many times to split.
    #         splitLoc = int(ln) // splits+1  # sets the split location to a third the chromosome length #more complex to get into 3 parts than just replacing the 2 with the 3 but may still be useful to calculate. I'll probably make there be an optional function call on how many times to split.
    #         print(ln)
            
    cmds = [
        f"python {pyLoc}ndb2pdb_mod.py -f {initFile} -n toSplit",
        f"python {pyLoc}chop.py -f toSplit.pdb -n isSplit.pdb -l {splitLoc}",
        f"python {pyLoc}pdb2ndb_mod.py -f isSplit.pdb -n isSplit",
        f"python {pyLoc}split.py -f isSplit.ndb"

        
        
    ]

    for cmd in cmds:
        print(f"\nRunning: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print("STDOUT:\n", result.stdout)
            # subprocess.run("ls")
        except subprocess.CalledProcessError as e:
            print("ERROR OCCURRED:")
            print("Command:", e.cmd)
            print("Return code:", e.returncode)
            print("STDOUT:\n", e.stdout)
            print("STDERR:\n", e.stderr)
            raise
    #delete the files created in the process
    print('deleting files created in the process ...')
    subprocess.run(f"rm /home/treed777/toSplit.pdb",shell=True, check=True)
    subprocess.run(f"rm /home/treed777/isSplit.pdb",shell=True, check=True)
    subprocess.run(f"rm /home/treed777/isSplit.ndb",shell=True, check=True)
    #moving C1.ndb and C2.ndb to the move directory
    print('moving C1.ndb and C2.ndb ...')
    subprocess.run(f"mv C1.ndb move",shell=True, check=True)
    subprocess.run(f"mv C2.ndb move",shell=True, check=True)
    # subprocess.run(f"python {pyLoc}columnizer.py",shell=True, check=True) #not needed for right file inputs
    print('finished')







#executing the functions
# splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splitLoc=1356)
# splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters')
# splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splitLoc=1722)
# splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splitLoc=2012)
# splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splitLoc=2363)
splitChromosome(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splitLoc=1356)



def splitMult(initFile, pyLoc="", splits=1):


    # #copying initFile as C2
    # subprocess.run(f"cp {initFile} move/C{2+split}",shell=True, check=True)

    with open(initFile, "r") as r:\
        #finding the location that every file needs to be split at
        #read the first line after the 6th line
        for i in range(6):
            r.readline()
        chrLen = int(r.readline()[15:19])  # reads the 7th line, which contains the chromosome length, assuming length is 4 digits

        splitLoc = chrLen // (splits + 1)


        #start using original file of full chromosome
        splitChromosome(initFile, pyLoc, splitLoc)
        subprocess.run(f"cp move/C1.ndb move/Chr1.ndb",shell=True, check=True)
        subprocess.run(f"cp move/C2.ndb move/prevC2.ndb",shell=True, check=True)


        for split in range(2, splits+1):
            # divisor = splits + 1


            splitChromosome("move/prevC2.ndb", pyLoc, splitLoc)
            subprocess.run(f"cp move/C1.ndb move/Chr{split}.ndb",shell=True, check=True)
            subprocess.run(f"cp move/C2.ndb move/prevC2.ndb",shell=True, check=True)
        
        #cleanup after the last split
        subprocess.run(f"mv move/C2.ndb move/Chr{splits+1}.ndb",shell=True, check=True)
        subprocess.run(f"rm move/C1.ndb",shell=True, check=True)




# splitMult(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splits=1)
# splitMult(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splits=2)
# splitMult(initFile='/home/treed777/cluster_runs/collapsed/collapsed.ndb', pyLoc='/home/treed777/back_scripts/splitters', splits=3)
