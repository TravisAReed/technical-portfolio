import os
import numpy as np
import matplotlib.pyplot as plt
# import xyzFuncs
import xyzFuncs as xyz
import time


print('plotting Hi-C map(s) ...')



from OpenMiChroM.CndbTools import cndbTools
cndbTools = cndbTools() #this line needed to make hic plot
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xyzFuncs
import os
# import threading
from multiprocessing import Process

num = 5  #used for locStats directory
num = xyzFuncs.masterNum
pow = 5


import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", type=str, required=True)
    args = parser.parse_args()
    num = args.split
except:
    print('not passed as arg likely')

print(num, flush=True)

root = "/home/treed777"
script_dir = os.path.dirname(os.path.abspath(__file__))


if script_dir.startswith('/home'): #run in wsl
    path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
    numSims = 3
    # numSims = 1
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"
    numSims = 100

HiCPath=f'{path}/Figs{num}/HiCMaps{num}'

frames = range(cndbTools.load(f'{path}/locTrajs{num}/nucleus0_1.cndb').Nframes) #assuming all trajectories have the same number of frames which should always be true


def findSepCM(sims):
    all_distances = []

    for sim in sims:
        print('finding sep of CMs for sim ...', sim, flush=True)

        frames0 = xyz.trajs[sim][0].xyz(frames=range(min(xyz.trajs[sim][0].Nframes, xyz.trajs[sim][0].Nframes)))
        frames1 = xyz.trajs[sim][1].xyz(frames=range(min(xyz.trajs[sim][1].Nframes, xyz.trajs[sim][1].Nframes)))

        distances = []
        for f0, f1 in zip(frames0, frames1):
            com0 = np.mean(f0, axis=0)
            com1 = np.mean(f1, axis=0)
            dist = np.linalg.norm(com0 - com1)
            distances.append(dist)

        all_distances.append(distances)
    # print(all_distances[0][0])
    return all_distances


def plotSepCM(all_distances):
    timeSteps = []
    for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
        timeSteps.append((frame+1)*10**(pow-3))

    print(len(all_distances))
    print(len(all_distances[0]))
    # print(all_distances[0][0])
    # Compute and plot average CM separation
    avg_distances = np.mean(all_distances, axis=0)
    # bot.plot(avg_distances, label="Average", color='black', linewidth=2)
    plt.plot(timeSteps, avg_distances, label="Average", color='black', linewidth=2)
    plt.xlabel("Step") #fix units later
    # bot.set_ylabel("Average CM Separation (nm)") #idk about those nm
    plt.ylabel("Average Separation of Centers of Mass")




    plt.title("Average Separation of Centers of Mass vs Steps")
    plt.tight_layout()
    os.makedirs(f'{path}/Figs{num}', exist_ok=True)
    plt.savefig(f'{path}/Figs{num}/SepCM{num}.tiff')  
    plt.savefig(f'{script_dir}/SepCM{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure to back_scripts for easy checking


    # plt.show()



def plotSepCMs(sims):
    nums = [1356,1722,2012,2363]


    timeSteps = []
    for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
        timeSteps.append((frame+1)*10**(pow-3))

    for num in nums:
        xyz.defTrajs(sims=sims,num=num)

        all_distances = findSepCM(sims)
        print(all_distances[0][0])

        # Compute and plot average CM separation
        avg_distances = np.mean(all_distances, axis=0)
        plt.plot(timeSteps, avg_distances, label=f'{num}')
    plt.xlabel("Step") #fix units later
    # bot.set_ylabel("Average CM Separation (nm)") #idk about those nm
    plt.ylabel("Average Separation of Centers of Mass")
    plt.title("Average Separation of Centers of Mass vs Steps")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{script_dir}/SepCMs.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file

    plt.show()
    plt.close()


























sims = range(1,numSims+1)


start = time.time()
xyz.defTrajs(sims=sims, num=num)
end = time.time()
print(f"Elapsed time for defTrajs: {end - start:.4f} seconds", flush=True)

start = time.time()
all_dists = findSepCM(sims)
# print(all_dists[1][1])
end = time.time()
print(f"Elapsed time for findSepCM: {end - start:.4f} seconds", flush=True)

start = time.time()
plotSepCM(all_dists)
end = time.time()
print(f"Elapsed time for plotSepCM: {end - start:.4f} seconds", flush=True)

# start = time.time()
# plotSepCMs(sims)
# end = time.time()
# print(f"Elapsed time for plotSepCMs: {end - start:.4f} seconds", flush=True)



























# # replica_ids = ['1', '2', '3', '4', '5']
# # replica_ids = ['1']


# # === Setup ===
# # base_path = "/scratch/ho25/multi_chr_example"

# # num = 5
# num = num = xyzFuncs.masterNum

# root = "/home/treed777"
# script_dir = os.path.dirname(os.path.abspath(__file__))


# if script_dir.startswith('/home'): #run in wsl
#     base_path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
#     numSims = 3
# else: #run in nots
#     base_path = f"/scratch/tr63/Real/output_nucleus{num}"
#     numSims = 100





# # === Store distances for each replica ===


# def findCMSeps(sims):
#     all_distances = []

#     for sim in sims:
#         print('finding sep of CMs for sim', sim, flush=True)

#         frames0 = xyzFuncs.trajs[sim][0].xyz(frames=range(min(xyzFuncs.trajs[sim][0].Nframes, xyzFuncs.trajs[sim][0].Nframes)))
#         frames1 = xyzFuncs.trajs[sim][1].xyz(frames=range(min(xyzFuncs.trajs[sim][1].Nframes, xyzFuncs.trajs[sim][1].Nframes)))

#         distances = []
#         for f0, f1 in zip(frames0, frames1):
#             com0 = np.mean(f0, axis=0)
#             com1 = np.mean(f1, axis=0)
#             dist = np.linalg.norm(com0 - com1)
#             distances.append(dist)

#         all_distances.append(distances)
#     # print(all_distances[0][0])
#     return all_distances


# def plotCM(all_distances):
    
#     fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

#     #plotting each sim's CM seperations
#     for sim, dist_list in enumerate(all_distances):
#         top.plot(dist_list, label=f"Sim {sim+1}")
#     top.set_ylabel("CM Separation (nm)")


#     # Compute and plot average CM separation
#     avg_distances = np.mean(all_distances, axis=0)
#     bot.plot(avg_distances, label="Average", color='black', linewidth=2)
#     bot.set_xlabel("Frame (Time)") #fix units later
#     bot.set_ylabel("Average CM Separation (nm)")




#     fig.suptitle("Distance Between Chain 0 and Chain 1 Centers of Mass vs Frame (change to timestep later)")
#     plt.tight_layout()
#     plt.show()
#     os.makedirs(f'{base_path}/Figs{num}', exist_ok=True)
#     plt.savefig(f'{base_path}/Figs{num}/CMsep{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file



# sims = range(1,numSims+1)
# xyzFuncs.defTrajs(sims)
# plotCM(findCMSeps(sims))