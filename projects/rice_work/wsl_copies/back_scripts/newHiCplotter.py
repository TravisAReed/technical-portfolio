print('plotting Hi-C map(s) ...')



from OpenMiChroM.CndbTools import cndbTools
cndbTools = cndbTools() #this line needed to make hic plot
import matplotlib.pyplot as plt
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

from matplotlib.font_manager import FontProperties



root = "/home/treed777"
script_dir = os.path.dirname(os.path.abspath(__file__))


if script_dir.startswith('/home'): #run in wsl
    path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
    numSims = 3
    # numSims = 1
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"
    numSims = 100

print(numSims, flush=True)

HiCPath=f'{path}/Figs{num}/HiCMaps{num}'

frames = range(cndbTools.load(f'{path}/locTrajs{num}/nucleus0_1.cndb').Nframes) #assuming all trajectories have the same number of frames which should always be true



def xyz(frame, sims):
    R'''
    Returns XYZ coordinates for all beads in a given frame from a given file number

    Args:
        frame (int, required):
            The frame to extract the XYZ coordinates from.
        sims (list, optional):
            The simulations to extract the XYZ coordinates from.)
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
        


    sim_list = []
    for sim in sims: #or sim in trajs

        # print('looping through sim', sim, flush=True)

        # ret = xyzSub(xyzFuncs.defTraj(f'{root}/cluster_runs/split/splitMid/output_nucleus{num}/locTrajs{num}/nucleus{fileNum}_{sim}.cndb'), frame=frame, XYZ=[0, 1, 2])
        # print('hi', xyzFuncs.trajs[1][0])
        coords0 = xyzSub(traj=xyzFuncs.trajs[sim][0], frame=frame, XYZ=[0, 1, 2]) #using defTrajs
        coords1 = xyzSub(traj=xyzFuncs.trajs[sim][1], frame=frame, XYZ=[0, 1, 2]) #using defTrajs

        # print(ret)
        # print('-----------',ret[0],ret[3],ret[4],ret[-3],ret[-1],ret[1355])
        sim_list.append(np.vstack((coords0, coords1)))



    # print(sim_list)
    # print(sim_list[0]) #sim_list[0] contains the data of the first sim in the specified frame
    # print(sim_list[2]) #index error
    return np.array(sim_list)

def findMaxNotOnDiag(arr, dist): #for finding stuff primarily (won't be used often)
    '''
    outputs maximum value and its location of 2D numpy array
    '''
    # Create a mask that excludes values where |i - j| < dist
    mask = np.fromfunction(lambda i, j: np.abs(i - j) >= dist, arr.shape, dtype=int)

    # Apply mask: set invalid entries to -inf so they won't affect argmax
    masked_arr = np.where(mask, arr, -np.inf)

    # Find index of max in masked data
    max_index = np.unravel_index(np.argmax(masked_arr), arr.shape)

    print("Max location:", max_index)
    print("Max value:", arr[max_index])



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


def plotProbVsDist(simHiC, initHiC, midMonomer):
    # xVals = []
    # yVals = []
    # # for beadInd in range(midMonomer-50,midMonomer-50len(mat)):
    # for beadInd in range(midMonomer-50,midMonomer-50):
    #     # xVals.append(midMonomer-beadInd-1)
    #     xVals.append(beadInd-midMonomer+1)
    #     # print(f'bead {beadInd+1} value: {mat[beadInd][midMonomer-1]}')
    #     yVals.append(mat[beadInd][midMonomer-1])

    # # print(xVals[1356-1])
    # plt.plot(xVals,yVals)
    # plt.savefig(f'{script_dir}/ProbVsDistPlot{midMonomer}split{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    # plt.show()


    print(len(xyzFuncs.trajs), flush=True)
    

    xVals = []
    simYVals = []
    initYVals = []

    for beadInd in range(len(simHiC)):
    # for beadInd in range(midMonomer-50,midMonomer-50):
        # xVals.append(midMonomer-beadInd-1)
        xVals.append(beadInd-midMonomer+1)
        # print(f'bead {beadInd+1} value: {mat[beadInd][midMonomer-1]}')
        simYVals.append(simHiC[beadInd][midMonomer-1])
        initYVals.append(initHiC[beadInd][midMonomer-1])

    # print(xVals[1356-1], simYVals[1356-1])
    # print(xVals[0], simYVals[0])
    # print(len(xVals), len(simYVals))

    # plt.figure(figsize=(12.8, 9.6))

    plt.plot(xVals[midMonomer-50:midMonomer+50],initYVals[midMonomer-50:midMonomer+50], label="Unbroken", color = 'blue')
    plt.plot(xVals[midMonomer-50:midMonomer+50],simYVals[midMonomer-50:midMonomer+50], label="Split Average", color = 'lime')

    # plt.legend(loc='upper right', fontsize=20)
    # plt.xlabel(f'Genomic Displacement from Bead {midMonomer} (Beads)', fontsize=20)
    # plt.ylabel('Contact Probability', fontsize=20)
    # plt.title(f'Contact Probability vs Genomic Displacement from Bead {midMonomer}', fontsize=24)
    
    # plt.legend(loc='upper right', fontsize=7)
    plt.legend(loc='upper right', fontsize=15)
    plt.xlabel(f'Genomic Displacement from\nBead {midMonomer} (Beads)', fontsize=18)
    plt.ylabel('Contact Probability', fontsize=18)
    plt.title(f'Contact Probability vs Genomic Displacement\nfrom Bead {midMonomer} at end of sim', fontsize=21)
    
    print(f'saving in {script_dir}/ProbVsDistPlot{midMonomer}split{num}.tiff ...', flush=True)
    plt.savefig(f'{script_dir}/ProbVsDistPlot{midMonomer}split{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    
    plt.show()
    plt.close()








def safeLog(arr, lowBound):
    arr[arr < lowBound] += lowBound
    return np.log(arr)

def plotHiC(frame, sims, initHiC=[], mu=3.22, rc=1.78):
    '''
    Plots Hi-C map using the given XYZ coordinates
    '''
    print('plotting frame', frame, flush=True)


    # simHiC = cndbTools.traj2HiC(xyz(frame=frame, sims=sims), mu=mu, rc=rc)
    # simHiC = cndbTools.traj2HiC(xyz(frame=frame, sims=range(4,sims+1)), mu=mu, rc=rc)
    simHiC = cndbTools.traj2HiC(xyz(frame=frame, sims=sims), mu=mu, rc=rc)
    

    # findMaxNotOnDiag(simHiC,100) #finds index where max value is



    



    if len(initHiC) == 0: #plotting with no matrix subtraction (all red)
        # plt.matshow(simHiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=simHiC.max()), cmap="Reds")
        plt.matshow(safeLog(simHiC, 10**-5), cmap="Reds")
        tag = 'Red'
    else: #plotting with matrix subtraction (red and blue)
        # plt.matshow(simHiC-initHiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=simHiC.max()), cmap="Reds")
        
        # diff = simHiC - np.log(initHiC)
        diff = safeLog(simHiC, 10**-5) - safeLog(initHiC, 10**-5)
        tag = 'Diff'

        # #finds index where max value is #agrees with other one
        # max_index = np.unravel_index(np.argmax(diff), diff.shape)
        # print(f"Max value is at: {max_index}")
        # print(f"Max value is: {diff[max_index]}")



        abs_max = np.max(np.abs(diff))  # Get max magnitude for symmetric color scaling
        # plt.matshow(diff, cmap='seismic', vmin=-abs_max, vmax=abs_max)
        # plt.matshow(diff, cmap='seismic', vmin=-9, vmax=9) #manually put max values on colorbar in so the formatting of the image wouldn't get messed up every time
        plt.matshow(diff, cmap='seismic', vmin=-12, vmax=12) #manually put max values on colorbar in so the formatting of the image wouldn't get messed up every time
        # plt.matshow(diff, cmap='seismic', vmin=-11, vmax=11) #manually put max values on colorbar in so the formatting of the image wouldn't get messed up every time
    
    #plotting lime cross
    # splitLoc = num
    splitLoc = 1356
    # splitLoc = 1722
    plt.plot([splitLoc, splitLoc], [0, 2711], color='lime', linewidth=2)  # vertical
    plt.plot([0, 2711], [splitLoc, splitLoc], color='lime', linewidth=2)  # horizontal


    # print_box_around(diff, splitLoc=splitLoc, sideLen=11) #printing matrix vals in 11 by 11 area around splitLoc
    
    # for yBead in range(1,2712):
    #     if yBead in range(splitLoc-6+1,splitLoc+5+1):

    #         print(f'{yBead}: {simHiC[yBead-1][splitLoc-6:splitLoc+5]}')
    #         # print(f'{yBead}: {initHiC[yBead-1][splitLoc-6:splitLoc+5]}')
    #         # print(f'{yBead}: {diff[yBead-1][splitLoc-6:splitLoc+5]}')
    #     # if yBead in range():
    #     #     print()



    # print()
    # print(initHiC==simHiC)
    # print(simHiC)
    # print(diff)

    # start = time.time()
    # plt.matshow(sim_HiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=sim_HiC.max()), cmap="Reds")
    # end = time.time()
    # print(f"Elapsed time for matshow: {end - start:.4f} seconds", flush=True)

    # plt.matshow(sim_HiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=sim_HiC.max()), cmap="Reds")
    plt.colorbar()
    # plt.title(f'Hi-C map for chromosome 10 at frame {frame}') #can change frame to timestep by reading through statistics.txt files
    
    plt.title(f'Hi-C Map for Split {num}\nat Step {(frame+1)*10**(pow-3)}', fontsize=21)
    # plt.show()

    

    # start = time.time()
    # np.savetxt(f"{path}/Figs5/HiCMaps5/frame{frame}HiC.csv", sim_HiC, delimiter=",", fmt="%.5f")
    # end = time.time()
    # print(f"Elapsed time for matshow: {end - start:.4f} seconds", flush=True)



    # start = time.time()
    # plt.savefig(f'{path}/Figs{num}/HiCMaps{num}/HiC{frame}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    # # plt.savefig(f'{path}/Figs{num}/HiCMaps{num}/HiC{frame}.png', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    # end = time.time()
    # print(f"Elapsed time for savefig: {end - start:.4f} seconds", flush=True)
    # print(start, end)

    # p = Process(target=plt.savefig, kwargs={"fname": numSims, "dpi": 300, "bbox_inches": "tight"})
    # print(p)
    # p.start()

    # os.makedirs(f'{path}/Figs{num}/HiCMaps{num}', exist_ok=True) #now being run in plotHiCs
    # np.savetxt(f"{HiCPath}/frame{frame}HiC.csv", simHiC, delimiter=",", fmt="%.5f") #saves hic map as text file
    # plt.savefig(f'{HiCPath}/frame{frame}HiC{tag}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    plt.savefig(f'{HiCPath}/frame{frame}HiCDiffBigTitle.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file


    # plt.show()
    plt.close() #takes the HiC plot out of memory so program won't crash. Does not do anything about loaded files.


    # if script_dir.startswith('/home'): #run in wsl
    #     splitLoc = 1356
    # else: #run in nots
    #     splitLoc = int(num)
    # plotProbVsDist(simHiC, initHiC, splitLoc)

    # plotProbVsDist(simHiC, 1722)
    # plotProbVsDist(initHiC, splitLoc)
    # plotProbVsDist(initHiC, 1722)
    



def init_HiC(mu=3.22, rc=1.78):
        '''
        Returns the HiC matrix of the first frame
        '''

        
        if script_dir.startswith('/home'): #run in wsl
            traj = xyzFuncs.defTraj('/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb')
            
        else: #run in nots
            traj = xyzFuncs.defTraj(f'/scratch/tr63/Real/collapsed/traj_chr10_0.cndb')
        
        

        

        
        # traj = xyzFuncs.defTraj('/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb')
        # print(traj.Nframes)
        # return cndbTools.traj2HiC(traj.xyz(frames=range(90,100), XYZ=[0, 1, 2]), mu=mu, rc=rc)
        # return cndbTools.traj2HiC(traj.xyz(frames=range(50,100), XYZ=[0, 1, 2]), mu=mu, rc=rc)
        return cndbTools.traj2HiC(traj.xyz(frames=range(50,100), XYZ=[0, 1, 2]), mu=mu, rc=rc)
        p
        # return cndbTools.traj2HiC(traj.xyz(frames=[99], XYZ=[0, 1, 2]), mu=mu, rc=rc)

# def plotHiCs(sims, frameSelection=None, doSub=False, doParallel=False, initHiC=None, mu=3.22, rc=1.78):
def plotHiCs(sims=range(1,numSims+1), frameSelection=None, doSub=False, doParallel=False, mu=3.22, rc=1.78):
    '''
    Plots Hi-C maps for given frames
    '''

    
    
    if len(xyzFuncs.trajs) == 0: #checks if trajectories have already been loaded
        xyzFuncs.defTrajs(sims,num=num)

    #creates folder if it doesn't exist
    os.makedirs(HiCPath, exist_ok=True)


    if frameSelection == None:
        selection = np.array(frames) #if no frame selection, select all frames
    else:
        selection = np.array(frameSelection)

    
    if doSub: #defining initHiC #plotting with matrix subtraction (red and blue)
        initHiC = init_HiC()
        # findMaxNotOnDiag(initHiC, 100) #finding max value in initial frame at least 100 off diag
    else: #plotting with no matrix subtraction (all red)
        # initHiC = None
        initHiC = []


    if doParallel:
        processes = []
        # if doSub: 
        for frame in selection:
            p = Process(target=plotHiC, kwargs={"frame": frame, "sims": sims, "initHiC": initHiC})
            processes.append(p)
            # p.start()
    
        # else: 
        #     for frame in selection:
        #         # plotHiC(frame=frame, sims=sims, mu=mu, rc=rc)
        #         p = Process(target=plotHiC, kwargs={"frame": frame, "sims": sims})
        #         processes.append(p)

        return processes #returns for both plot types
    else:
        for frame in selection:
            plotHiC(frame=frame, sims=sims, initHiC=initHiC)






        ########
        # else: #plotting with no matrix subtraction (all red)
            
        #     #make mods where plotHiC added to process and run certain amount of processes once added to list (plotHiCs returns list of processes rather than runs plotHiC)
        #     for frame in selection:
        #         plotHiC(frame=frame, sims=sims, initHiC=initHiC, mu=mu, rc=rc)


    # if doSub == False: #plotting with no matrix subtraction (all red)
    #     for frame in selection:
    #         plotHiC(frame=frame, sims=sims, mu=mu, rc=rc)
    # else: #plotting with no matrix subtraction (all red)
    #     # if initHiC.any() == None:
    #     if initHiC == None:
    #         initHiC = init_HiC(sims) #python highlighted it yellow thinking it's a constructor but it's not and it runs right
        
    #     #make mods where plotHiC added to process and run certain amount of processes once added to list (plotHiCs returns list of processes rather than runs plotHiC)
    #     for frame in selection:
    #         plotHiC(frame=frame, sims=sims, initHiC=initHiC, mu=mu, rc=rc)
        







# #Generate Hi-C map
# print("Generating the contact probability matrix...")
# sim_HiC = cndbTools.traj2HiC(xyz(0, 0, 2))
# plt.matshow(sim_HiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=sim_HiC.max()), cmap="Reds")
# plt.colorbar()
# plt.show()


import time

start = time.time()


# plotHiC(frame=0, sims=3) #frames is the frame number (0-999)
# plotHiCs(frameSelection=range(0,10), sims=2) #frames is the frame number (0-10)
# plotHiCs(sims=numSims, doSub=True)
# plotHiCs(sims=numSims, doSub=True, frameSelection=[999])
# plotHiCs(sims=numSims, doSub=True, frameSelection=[0,1,2,3])
# plotHiCs(sims=range(1,numSims+1), doSub=True, frameSelection=[0]) #frame does matter

# xyzFuncs.defTrajs([1,2,3])
# plotHiCs(sims=[1], doSub=True, frameSelection=[0,999]) #frame does matter
# plotHiCs(sims=[2], doSub=True, frameSelection=[999]) #frame does matter
# plotHiCs(sims=[3], doSub=True, frameSelection=[999]) #frame does matter
# plotHiCs(sims=[100], doSub=True, frameSelection=[999]) #frame does matter
# plotHiCs(doSub=True, frameSelection=[999]) #frame does matter
# plotHiCs(sims=100)

# lst = plotHiCs(sims=numSims, doSub=False, doParallel=True, frameSelection=[0,1,2,3])
# lst = plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=[0,1,2,3,4,5,6,7,8,9])
# lst = plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=[0,1,2,3,4,5,6,7,8,9,10])
# lst = plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=None)
lst = plotHiCs(sims=range(1,numSims+1), doSub=True, doParallel=False, frameSelection=[0,100,999])
# lst = plotHiCs(sims=numSims, doSub=False, doParallel=False, frameSelection=[999])
# lst = plotHiCs(sims=3, doSub=True, doParallel=False, frameSelection=[0,15])
# lst = plotHiCs(sims=numSims, doSub=True, doParallel=False, frameSelection=[0,1,15,999])

# print(lst)
# print(len(lst))

# #running tasks
# for task in lst:
#     task.start()
# #broken up so all tasks are started first
# for task in lst:
#     task.join()





end = time.time()
print(f"Elapsed time for event: {end - start:.4f} seconds", flush=True)

# print(xyz())

































def runProcesses(processes, threads=None):

    def findNumRunningProcesses(processes):
        return sum(p.is_alive() for p in processes)
    
    def findCurRunningProcesses(processes):
        curProcesses = []
        for p in processes:
            if p.is_alive():
                curProcesses.append(p)
        return curProcesses



    if threads == None:
        threads = os.cpu_count() - 3 
    else:
        if threads >= os.cpu_count():
            print('there are not enough threads on this machine to run the selected amount of threads') 

    #makes sure there aren't more threads than processes
    if len(processes) < threads:
        threads = len(processes)


    threads /= 2 #just hoping this makes the nots code work

    print(f'running processes on {threads} threads ...')



    for frame in range(len(processes)):
        # print(frame)
        while True: #runs until new process starts
            if findNumRunningProcesses(processes) < threads:
                print(f'starting process {frame}')
                processes[frame].start()
                break


    print('waiting for processes to finish ...')
    for p in findCurRunningProcesses(processes): #making sure processes finish
        p.join()




    


# plotHiCs(sims=numSims, doSub=True, doParallel=False, frameSelection=[2,101,651,998])
# plotHiCs(sims=range(1,numSims+1), doSub=True, doParallel=False)

# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=[999]))
# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=[990,991,992,993,994,995,996,997,998,999]))
# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=range(20)))

# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=[0, 1, 15, 100, 300, 650, 999]))


# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=range(0,333)))
# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=range(333,667)))
# runProcesses(plotHiCs(sims=numSims, doSub=True, doParallel=True, frameSelection=range(667,1000)))
