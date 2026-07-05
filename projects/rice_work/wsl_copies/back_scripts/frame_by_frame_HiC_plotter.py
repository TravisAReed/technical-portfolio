print('Make sure all trajectories are stored in the format: chain{chain}sim{sim}.cndb')



from OpenMiChroM.CndbTools import cndbTools
# cndbTools = cndbTools() #this line needed to make hic plot
import matplotlib.pyplot as plt
import numpy as np
import xyzFuncs
import os
from multiprocessing import Process


def loadTraj(file):
    '''
    Loads trajectory without having to be ran many times
    '''
    return cndbTools().load(file)


trajs = {} #global variable that stores all loaded trajectories and will be a property after void defTrajs is called. Better than deleting each file after it's loaded and reloading it for every frame.
def loadTrajs(sims, trajFolder): #move this under 
    '''
    restructures a multi-dimensional list of the trajectories for each simulation
    access by trajs[sim][0 or 1 (chain number)]
    '''
    print('loading trajectories ...', flush=True)
    global trajs
    trajs = {} #clearing trajs every time this loadTrajs is called

    for sim in sims: #made dict so sim number used as key without needing to subtract 1
        trajs[sim] = [loadTraj(f'{trajFolder}/chain0sim{sim}.cndb'), loadTraj(f'{trajFolder}/chain1sim{sim}.cndb')]


scriptDir = os.path.dirname(os.path.abspath(__file__))
HiCPath=f'{scriptDir}/HiCMaps'


import argparse

# parser = argparse.ArgumentParser()

# parser.add_argument("--endFrames", type=int, required=False) #needed for generating differences HiC maps
# parser.add_argument("--initTraj", type=str, required=False) #needed for generating differences HiC maps
# parser.add_argument("--mu", type=float, required=True, default=3.22)
# parser.add_argument("--rc", type=float, required=True, default=1.78)

# args = parser.parse_args()
# num = args.split


# trajFolder = input('Trajectory folder (where the cndb trajectries are stored): ')
# simSelectionInp = input('Sims to use (ex 1,2,3 for using sims 1,2, and 3 Return no text for using all sims): ')
# frameSelectionInp = input('Frames to plot (ex 0,1,2 for plotting frames 0,1, and 2. Return no text for plotting all frames): ')
# frameSteps = int(input('The number of steps that occur between frames in the sim: '))
# doDiffsInp = input('Plot differences HiC maps? (y/n): ').upper()
# doParallelInp = input('Run HiC map plotting in parallel? (y/n): ').upper() #generates plots must faster but is still being developed

#for testing
trajFolder = '/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5'
simSelectionInp = ''
frameSelectionInp = ''
frameSteps = 100
doDiffsInp = 'Y'
doParallelInp = 'N'

#finding simSelection
if len(simSelectionInp) < 1:
    highestSim = 0
    for file in os.listdir(trajFolder):
        if file.startswith('chain') and file.endswith('.cndb'):
            highestSim = max(highestSim, int(file.split('sim')[1].split('.')[0]))
    simSelection = np.arange(1, highestSim + 1)
else:
    simSelection = np.array(simSelectionInp.split(','), dtype=int)

print(simSelection)

#finding frameSelection
if len(frameSelectionInp) < 1: #creates list of frames to plot assumes all trajectories in the trajectory folder have the same number of frames which needs to be true for program to work correctly
    for file in os.listdir(trajFolder):
        if file.startswith('chain') and file.endswith('.cndb'):
            frameSelection = np.arange(loadTraj(f'{trajFolder}/{file}').Nframes)
            break
else:
    frameSelection = np.array(frameSelectionInp.split(','), dtype=int)


#finding doDiffs
if doDiffsInp == 'Y':
    doDiffs = True
elif doDiffsInp == 'N':
    doDiffs = False
else:
    print('Invalid input for doDiffs.  Exiting.')
    exit()

#finding doParallel
if doParallelInp == 'Y':
    doParallel = True
elif doParallelInp == 'N':
    doParallel = False
else:
    print('Invalid input for doParallel. Exiting.')
    exit()





def safeLog(arr, lowBound):
    arr[arr < lowBound] += lowBound
    return np.log(arr)

def overSimsXYZ(frame, sims):
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
        


        if beadSelection == None: 
            selection = np.arange(traj.Nbeads)
        else:
            selection = np.array(beadSelection)
        
        return np.take(np.take(np.array(traj.cndb[str(frame)]), selection, axis=0), XYZ, axis=1) 
        


    sim_list = []
    for sim in sims:       
        coords0 = xyzSub(traj=xyzFuncs.trajs[sim][0], frame=frame, XYZ=[0, 1, 2]) #using loadTrajs
        coords1 = xyzSub(traj=xyzFuncs.trajs[sim][1], frame=frame, XYZ=[0, 1, 2]) #using loadTrajs

        sim_list.append(np.vstack((coords0, coords1)))

    return np.array(sim_list)


def plotHiC(frame, sims, initHiC=[], mu=3.22, rc=1.78):
    '''
    Plots Hi-C map using the given XYZ coordinates
    '''
    print('plotting frame', frame, flush=True)


    simHiC = cndbTools().traj2HiC(overSimsXYZ(frame=frame, sims=sims), mu=mu, rc=rc)

    if len(initHiC) == 0: #plotting with no matrix subtraction (all red)
        plt.matshow(safeLog(simHiC, 10**-5), cmap="Reds")
        tag = 'Reds'
    else: #plotting with matrix subtraction (red and blue)
        
        diff = safeLog(simHiC, 10**-5) - safeLog(initHiC, 10**-5)
        tag = 'Diffs'

        abs_max = np.max(np.abs(diff))  # Get max magnitude for symmetric color scaling
        plt.matshow(diff, cmap='seismic', vmin=-abs_max, vmax=abs_max)
        # plt.matshow(diff, cmap='seismic', vmin=-12, vmax=12) #manually put max values on colorbar in so the formatting of the image wouldn't get messed up every time. Needed for generating smooth videos.
    


 
    plt.colorbar()
    
    plt.title(f'Hi-C {tag} Map at\nStep {(frame+1)*frameSteps}', fontsize=21)


    plt.savefig(f'{HiCPath}/frame{frame}HiC{tag}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file

    plt.show()
    plt.close() #takes the HiC plot out of memory so program won't crash. Does not do anything about loaded trajectory files.
    


#generates initial Hi-C matrix using end of setup sim
def init_HiC(initTraj, endFrames, mu=3.22, rc=1.78):
        '''
        Returns the HiC matrix of the first frame
        '''
        traj = xyzFuncs.defTraj(initTraj)       
        return cndbTools().traj2HiC(traj.xyz(frames=range(traj.Nframes-endFrames,traj.Nframes), XYZ=[0, 1, 2]), mu=mu, rc=rc)
        

def plotHiCs(sims, frameSelection, doDiffs=False, doParallel=False, mu=3.22, rc=1.78):
    '''
    Plots Hi-C maps for given frames
    '''

    
    
    if len(trajs) == 0: #checks if trajectories have already been loaded
        loadTrajs(sims,trajFolder=trajFolder)

    #creates folder if it doesn't exist
    os.makedirs(HiCPath, exist_ok=True)


    
    if doDiffs: #defining initHiC #plotting with matrix subtraction (red and blue)
        endFrames = 50
        initTraj = '/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb'
        initHiC = init_HiC(endFrames=endFrames, initTraj=initTraj)
        # initHiC = init_HiC(initTraj=args.initTraj, endFrames=args.endFrames)
    else: #plotting with no matrix subtraction (all red)
        initHiC = []


    if doParallel:
        processes = []
        for frame in frameSelection:
            p = Process(target=plotHiC, kwargs={"frame": frame, "sims": sims, "initHiC": initHiC, "mu": mu, "rc": rc})
            processes.append(p)
            # p.start()
    
     
        return processes #returns for both plot types
    else:
        for frame in frameSelection:
            plotHiC(frame=frame, sims=sims, initHiC=initHiC, mu=mu, rc=rc)
        


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
            print('There are not enough threads on this machine to run the selected amount of threads') 

    #makes sure there aren't more threads than processes
    if len(processes) < threads:
        threads = len(processes)

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





import time

start = time.time()

if doParallel:
    runProcesses(plotHiCs(sims=simSelection, doDiffs=doDiffs, doParallel=True, frameSelection=frameSelection))
else:
    plotHiCs(sims=simSelection, doDiffs=doDiffs, doParallel=False, frameSelection=frameSelection)

end = time.time()
print(f"Elapsed time to plot HiC Maps: {end - start:.4f} seconds", flush=True)


