print('localizing stats ...')

import os
import subprocess


num = '1'

script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
if script_dir.startswith('/home'):
    # print('wsl')
    # path = '/home/treed777/cluster_runs/split/splitMid'
    path = f'/home/treed777/cluster_runs/split/splitMid/output_nucleus{num}/'
    # path = f'/home/treed777/cluster_runs/split/splitMid/'

else:
    # print('nots')
    path = f'/scratch/tr63/Real/output_nucleus{num}/'
    # path = f'/scratch/tr63/Real/'



#check if the folder exists
if os.path.isdir(f"{path}/locStats{num}"):
    print("Folder exists!")
else:
    print("Folder does not exist.")
    subprocess.run(f"mkdir {path}/locStats{num}",shell=True, check=True)




def clearLocStats():
    print("clearing locStats directory ...")
    try:
        subprocess.run(f"rm {path}/locStats{num}/statistics*.txt",shell=True, check=True)
    except:
        print("No files to clear in locStats directory.")

def locStats(n):
    #clearing the locStats directory before copying new files (not mv so won't replace existing files)
    clearLocStats()
    for sim in range(1, n+1):
        print("copying sim", sim, "...")
        # subprocess.run(f"cp {path}/sim{sim}/statistics.txt {path}/locStats{num}/statistics{sim}.txt",shell=True, check=True)
        subprocess.run(f"cp {path}/sim{sim}/statistics.txt {path}/locStats{num}/statistics{sim}.txt",shell=True, check=True)
        




# clearLocStats()
# locStats(2)
locStats(100)

