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
from scipy.spatial import distance

num = 5  #used for locStats directory
# num = xyzFuncs.masterNum
pow = 5

root = "/home/treed777"
script_dir = os.path.dirname(os.path.abspath(__file__))

# splitLoc = 1356
splitLoc = 1356


if script_dir.startswith('/home'): #run in wsl
    path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
    numSims = 3
    # numSims = 1
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"
    numSims = 100

HiCPath=f'{path}/Figs{num}/HiCMaps{num}'

frames = range(cndbTools.load(f'{path}/locTrajs{num}/nucleus0_1.cndb').Nframes) #assuming all trajectories have the same number of frames which should always be true



def print_box_around(matrix, splitLoc, sideLen):

    """
    Prints a box of values centered at (row, col).
    Values outside the bounds are skipped.
    """
    row = splitLoc
    col = splitLoc
    nrows, ncols = matrix.shape
    print(f"box around ({row}, {col}):\n")

    for r in range(row - (sideLen//2), row +1 +(sideLen//2)):
        line = []
        for c in range(col - (sideLen//2), col +1 +(sideLen//2)):
            if 0 <= r < nrows and 0 <= c < ncols:
                line.append(f"{matrix[r, c]}")
            else:
                line.append("   ")  # Placeholder for out-of-bounds
        print("  ".join(line))


def xyz(frame, sims=100):
    R'''
    Returns XYZ coordinates for all beads in a given frame from a given file number

    Args:
        frame (int, required):
            The frame to extract the XYZ coordinates from.
        sims (int, optional):
            The number of simulations to extract the XYZ coordinates from. (Default value: `100`)
    '''

    def xyzSub(traj, frame, beadSelection=None, XYZ=[0,1,2]): #check if works for ndb also
        R""" 
        Get the selected beads' 3D position from a **cndb** or **ndb** for a frame.
        
        Args:
            frame (int, required):
                Define which frame to extract the position of the selected beads.
            beadSelection (list of ints, required):
                List of beads to extract the 3D position for each frame. The list is defined by `beadSelection=[0,1,2,...,N-1]`. (Default value: `None`, all beads) 
            XYZ (list, required):
                List of the axis in the Cartesian coordinate system that the position of the bead will get extracted for each frame. The list is defined by `XYZ=[0,1,2]`. where 0, 1 and 2 are the axis X, Y and Z, respectively. (Default value: `XYZ=[0,1,2]`) 

        Returns:
            Returns a list of numpy arrays containing the 3D position of the selected beads for the given frame.
        """
        


        if beadSelection == None: #I was right #I think I'll leave beadSelection alone bc seems to be localized to each frame which is consistent with both versions
            # print(traj.Nbeads)
            selection = np.arange(traj.Nbeads)
        else:
            # print(beadSelection)
            selection = np.array(beadSelection)
        #selection appears to be a numpy array with all the bead indices to print out
        
        # print(np.array(traj.cndb[str(sim)]))

        # xyzFuncs.printXYZ(traj, frame, 1)

        # return np.take(np.take(np.array(traj.cndb[str(frame)]), selection, axis=0), XYZ, axis=1) #currently only using one traj #I think I just need to modify this line
        return np.take(np.take(np.array(traj.cndb[str(frame)]), selection, axis=0), XYZ, axis=1) 
        

    
    with open(f'{script_dir}/boxVals.txt', 'a') as a:
        a.write(f'Frame {frame}\n')


        sim_list = []
        # for sim in range(1, sims+1) :#or sim in trajs
        for sim in sims :#or sim in trajs
            print(f'printing sim {sim} ...', flush=True)
            a.write(f'Sim {sim}\n')
            a.flush()
            # ret = xyzSub(xyzFuncs.defTraj(f'{root}/cluster_runs/split/splitMid/output_nucleus{num}/locTrajs{num}/nucleus{fileNum}_{sim}.cndb'), frame=frame, XYZ=[0, 1, 2])
            # print('hi', xyzFuncs.trajs[1][0])
            coords0 = xyzSub(traj=xyzFuncs.trajs[sim][0], frame=frame, XYZ=[0, 1, 2]) #using defTrajs
            coords1 = xyzSub(traj=xyzFuncs.trajs[sim][1], frame=frame, XYZ=[0, 1, 2]) #using defTrajs

            # print(ret)
            # print('-----------',ret[0],ret[3],ret[4],ret[-3],ret[-1],ret[1355])

            mat = np.vstack((coords0, coords1))
            # print(mat)
            # print(mat[1355])
            highList = range(splitLoc-6,splitLoc+5)
            # highList = [1351,1352,1353,1354,1355,1356,1357,1358,1359,1360,1361]
            for bead in highList:
                a.write(f'bead {bead}: {mat[bead-1]}\n')
                # print(mat[bead-1])
            # print_box_around(mat, splitLoc=1356, sideLen=11) #printing matrix vals in 11 by 11 area around splitLoc
            # print(xyzFuncs.dist(mat[1351-1],mat[1353-1]))
            
            def calc_prob(data, mu, rc):
                print(distance.cdist(data, data, 'euclidean'))
                return 0.5 * (1.0 + np.tanh(mu * (rc - distance.cdist(data, data, 'euclidean'))))
            
            P = calc_prob(data=mat[splitLoc-6:splitLoc+5],mu=3.22,rc=1.78)
            # print(P)
            # sim_list.append(np.vstack((coords0, coords1)))

            # print(len(mat[splitLoc-6:splitLoc+5]))

            sim_list.append(mat[splitLoc-6:splitLoc+5])



    # print(sim_list)
    # print(sim_list[0]) #sim_list[0] contains the data of the first sim in the specified frame
    # print(sim_list[2]) #index error
    # print(sim_list)
    return np.array(sim_list)
    # return np.array(sim_list[splitLoc-5:splitLoc+6])



xyzFuncs.defTrajs(range(1,numSims+1))

# xyzFuncs.printXYZ(xyzFuncs.trajs[1][1],0,1)
with open(f'{script_dir}/boxVals.txt', 'w') as w: #clears file
    pass

# simHiC0 = cndbTools.traj2HiC(xyz(frame=0, sims=numSims),mu=3.22,rc=1.78)
# simHiC15 = cndbTools.traj2HiC(xyz(frame=15, sims=numSims,mu=3.22,rc=1.78))

# simHiC0 = cndbTools.traj2HiC(xyz(frame=0, sims=1),mu=3.22,rc=1.78)
# simHiC15 = cndbTools.traj2HiC(xyz(frame=15, sims=1),mu=3.22,rc=1.78)

#using new xyz with list input
simHiC0 = cndbTools.traj2HiC(xyz(frame=0, sims=range(1,numSims+1)),mu=3.22,rc=1.78)
simHiC15 = cndbTools.traj2HiC(xyz(frame=15, sims=range(1,numSims+1)),mu=3.22,rc=1.78)

# simHiC0 = cndbTools.traj2HiC(xyz(frame=0, sims=[3]),mu=3.22,rc=1.78)
# simHiC15 = cndbTools.traj2HiC(xyz(frame=15, sims=[3]),mu=3.22,rc=1.78)





# print(simHiC0)
# print()
print(simHiC15)

# print(range(1351,1362))
# print(range(1356-5,1356+6))


def loadMorrisonCalculatedVals(file):
    lst = []
    # with open(f'/mnt/c/Users/treed/Downloads/av{frame}.txt', 'r') as r:
    with open(file, 'r') as r:
        lns = r.readlines()

    lst = lns

    return lst



# morrison0 = loadMorrisonCalculatedVals(0)
# morrison15 = loadMorrisonCalculatedVals(15)
morrisonValsPath = '/mnt/c/Users/treed/Downloads'
# morrisonValsPath = '/scratch/tr63/back_scripts/morrisonVals'
morrison0 = loadMorrisonCalculatedVals(f'{morrisonValsPath}/av0.txt')
morrison15 = loadMorrisonCalculatedVals(f'{morrisonValsPath}/av15.txt')


def myLog(arr, lowBound):
    arr[arr < lowBound] += lowBound
    return np.log(arr)

myDiffs = myLog(simHiC15, 10**-5) - myLog(simHiC0, 10**-5)

morrisonDiffs = loadMorrisonCalculatedVals(f'{morrisonValsPath}/difflog.txt')


# print('\n\n\n\n-------------------------------------------\n')
# for row in range(11):
#     print(simHiC0[row])
#     print()
#     print(morrison0[row])
#     print('-------------------------------------------\n')






# print('\n\n\n\n-------------------------------------------\n')
# for row in range(11):
#     print(simHiC15[row])
#     print()
#     print(morrison15[row])
#     print('-------------------------------------------\n')










with open(f'{script_dir}/CompareHiCAvgs.txt', 'w') as w:
    


    w.write('writing frame 0 info')
    w.write('\n\n\n\n-------------------------------------------\n\n')
    for row in range(11):
        w.write(f'{simHiC0[row]}\n')
        w.write('\n')
        w.write(f'{morrison0[row]}\n')
        w.write('-------------------------------------------\n\n')





    w.write('writing frame 15 info')
    w.write('\n\n\n\n-------------------------------------------\n\n')
    for row in range(11):
        w.write(f'{simHiC15[row]}\n')
        w.write('\n')
        w.write(f'{morrison15[row]}\n')
        w.write('-------------------------------------------\n\n')




    


    w.write('writing diffs info')
    w.write('\n\n\n\n-------------------------------------------\n\n')
    for row in range(11):
        w.write(f'{myDiffs[row]}\n')
        w.write('\n')
        w.write(f'{morrisonDiffs[row]}\n')
        w.write('-------------------------------------------\n\n')