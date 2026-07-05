




#only will be run on wsl
from OpenMiChroM.CndbTools import cndbTools
# cndbTools = cndbTools() #I was wrong. This line caused it to overwrite itself. I can't create new objects of this class when this line is used. #this line may be worthless but I think it's the constructor
# import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import os

# num = 5
# num = 4
 

root = "/home/treed777"
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(f'{script_dir}/masterVars.csv', 'r') as r: #getting manually defined variable(s) from a file
    lines = r.readlines()[1]
    masterNum = int(lines.split(',')[1])

    num = masterNum


item = os.environ.get('item')
if item != None:
    num = item



if script_dir.startswith('/home'): #run in wsl
    path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"


#temp
# import time



def defTraj(file):
    '''
    Loads trajectory without having to be ran many times
    '''
    # print(f'loading {file} ...')
    # return cndbTools.load(file) #was used when cndbTools = cndbTools() not commented out and made traj always overwrite itself
    return cndbTools().load(file)

trajs = {} #global variable that stores all loaded trajectories and will be a property after void defTrajs is called. Better than deleting each file after it's loaded and reloading it for every frame.
def defTrajs(sims=range(1,101), num=masterNum): #move this under 
    '''
    restructures a multi-dimensional list of the trajectories for each simulation
    access by trajs[sim][0 or 1 (chain number)]
    '''
    print('loading trajectories ...', flush=True)
    global trajs
    trajs = {} #clearing it every time this is called

    if script_dir.startswith('/home'): #run in wsl
        path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
    else: #run in nots
        path = f"/scratch/tr63/Real/output_nucleus{num}"

    print('for checking it works: ')
    print('defTrajs num:', num, flush=True)
    print(f'{path}/locTrajs{num}/nucleus0_1.cndb',flush=True)

    # print(sims)
    for sim in sims: #made dict so sim number used as key without needing to subtract 1
        # trajs[sim] = [defTraj(f'{root}/cluster_runs/split/splitMid/output_nucleus{num}/locTrajs{num}/nucleus0_{sim}.cndb'), defTraj(f'{root}/cluster_runs/split/splitMid/output_nucleus{num}/locTrajs{num}/nucleus1_{sim}.cndb')]
        trajs[sim] = [defTraj(f'{path}/locTrajs{num}/nucleus0_{sim}.cndb'), defTraj(f'{path}/locTrajs{num}/nucleus1_{sim}.cndb')]
        # print(trajs)
        # print('lenth of trajs:', len(trajs))

#if used bead index is -1, returns last bead's xyz (though we're using real bead number not bead indexes)
# so if bead arg is 0, will return last bead in frame
def findXYZ(traj, frame, bead):
    '''
    returns XYZ coordinates of a single bead with given trajectory, frame, and bead
    '''
    return traj.cndb[str(frame)][bead-1] #quickest method I know


def printXYZ(traj, frame, bead):
    '''
    prints XYZ coordinates with given trajectory, frame, and bead    
    '''
    print(f"Bead {bead} at frame {frame}:", findXYZ(traj,frame,bead))



def dist(pt1, pt2, metric='euclidean'):
    '''returns distance two points of split are from each other'''
    return distance.cdist([pt1], [pt2], metric)[0][0]


# # collapseTraj = defTraj('/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb')
# sim1traj0 = defTraj('/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_1.cndb')
# sim1traj1 = defTraj('/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_1.cndb')

# printXYZ(sim1traj0,frame=0, bead=1356)
# printXYZ(sim1traj1,frame=0, bead=1)

# print(dist(findXYZ(sim1traj0,frame=0, bead=1356),findXYZ(sim1traj1,frame=0, bead=1)))


# traj0 = defTraj('/home/treed777/cluster_runs/split/nucleus0_1.cndb')
# traj1 = defTraj('/home/treed777/cluster_runs/split/nucleus1_1.cndb')

# printXYZ(traj0,frame=0, bead=-1)
# printXYZ(traj1,frame=0, bead=1)

# print(dist(findXYZ(traj0,frame=0, bead=-1),findXYZ(traj1,frame=0, bead=1)))



# traj0loc = defTraj('/home/treed777/cluster_runs/split/nucleus_0.cndb')
# traj1loc = defTraj('/home/treed777/cluster_runs/split/nucleus_1.cndb')

# printXYZ(traj0loc,frame=0, bead=1356)
# printXYZ(traj1loc,frame=0, bead=1)

# print(dist(findXYZ(traj0loc,frame=0, bead=1356),findXYZ(traj1loc,frame=0, bead=1)))



# for frame in range(100):
#     printXYZ(collapseTraj,frame=frame, bead=1)
# print()








# printXYZ(collapseTraj,frame=0, bead=1)
# printXYZ(collapseTraj,frame=99, bead=1)
# printXYZ(sim1traj,frame=0, bead=1)


# collapseTraj_xyz = collapseTraj.xyz(frames=range(0,100), XYZ=[0, 1, 2])
# Rgs = collapseTraj.compute_RG(collapseTraj_xyz)
# print(Rgs)


# for i in range(len(Rgs)):
#     print(i, Rgs[i])
# print()

