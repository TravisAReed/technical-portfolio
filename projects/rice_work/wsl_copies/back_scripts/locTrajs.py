print('localizing trajectory cndb files...')


import os
import subprocess


num = '5'

script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
if script_dir.startswith('/home'):
    # print('wsl')
    path = f'/home/treed777/cluster_runs/split/splitMid/output_nucleus{num}'
else:
    # print('nots')
    path = f'/scratch/tr63/Real/output_nucleus{num}'


#check if the folder exists
if os.path.isdir(f"{path}/locTrajs{num}"):
    print("Folder exists!")
else:
    print("Folder does not exist.")
    subprocess.run(f"mkdir {path}/locTrajs{num}",shell=True, check=True)



def clearLocTrajs():
    print("clearing locStats directory ...")
    try:
        subprocess.run(f"rm {path}/locTrajs{num}/*.cndb",shell=True, check=True)
    except:
        print("No files to clear in locStats directory.")

def locTrajs(n):
    #clearing the locTrajs directory before copying new files (not mv so won't replace existing files)
    clearLocTrajs()
    for sim in range(1, n+1):
        print("copying sim", sim, "...")
        # print(f"cp {path}/sim{sim}/*.cndb {path}/locTrajs{num}/nucleus{sim}*.cndb")
        subprocess.run(f"cp {path}/sim{sim}/nucleus_0.cndb {path}/locTrajs{num}/nucleus0_{sim}.cndb",shell=True, check=True)
        subprocess.run(f"cp {path}/sim{sim}/nucleus_1.cndb {path}/locTrajs{num}/nucleus1_{sim}.cndb",shell=True, check=True)






locTrajs(100)

