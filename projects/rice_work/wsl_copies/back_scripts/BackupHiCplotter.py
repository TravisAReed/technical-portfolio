print('plotting Hi-C map(s) ...')



from OpenMiChroM.CndbTools import cndbTools
cndbTools = cndbTools() #this line needed to make hic plot
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xyzFuncs
import os

# num = 5  #used for locStats directory
num = xyzFuncs.masterNum

root = "/home/treed777"
script_dir = os.path.dirname(os.path.abspath(__file__))


if script_dir.startswith('/home'): #run in wsl
    path = f"{root}/cluster_runs/split/splitMid/output_nucleus{num}"
    # numSims = 3
    numSims = 1
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"
    numSims = 100

HiCPath=f'{path}/Figs{num}/HiCMaps{num}'

frames = range(cndbTools.load(f'{path}/locTrajs{num}/nucleus0_1.cndb').Nframes) #assuming all trajectories have the same number of frames which should always be true



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
        


    sim_list = []
    for sim in range(1, sims+1): #or sim in trajs
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



def plotHiC(frame, sims, initHiC=[], mu=3.22, rc=1.78):
    '''
    Plots Hi-C map using the given XYZ coordinates
    '''
    # print("Generating the contact probability matrix...")
    simHiC = cndbTools.traj2HiC(xyz(frame=frame, sims=sims), mu=mu, rc=rc)
    
    if len(initHiC) == 0: #plotting with no matrix subtraction (all red)
        plt.matshow(simHiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=simHiC.max()), cmap="Reds")
    else: #plotting with matrix subtraction (red and blue)
        # plt.matshow(simHiC-initHiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=simHiC.max()), cmap="Reds")
        diff = simHiC - initHiC
        abs_max = np.max(np.abs(diff))  # Get max magnitude for symmetric color scaling
        plt.matshow(diff, cmap='seismic', vmin=-abs_max, vmax=abs_max)
    


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
    plt.title(f'Hi-C map for chromosome 10 at frame {frame}') #can change frame to timestep by reading through statistics.txt files
    # plt.show()

    # start = time.time()
    # os.makedirs(f'{path}/Figs{num}/HiCMaps{num}', exist_ok=True)
    # end = time.time()
    # print(f"Elapsed time for makedirs: {end - start:.4f} seconds", flush=True)

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

    # os.makedirs(f'{path}/Figs{num}/HiCMaps{num}', exist_ok=True) #now being run in plotHiCs
    np.savetxt(f"{HiCPath}/frame{frame}HiC.csv", simHiC, delimiter=",", fmt="%.5f") #saves hic map as text file
    plt.savefig(f'{HiCPath}/frame{frame}HiC.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file
    plt.close() #takes the HiC plot out of memory so program won't crash. Does not do anything about loaded files.




def plotHiCs(sims, frameSelection=None, doSub=False, mu=3.22, rc=1.78):
    '''
    Plots Hi-C maps for given frames
    '''

    def initHiC(mu=3.22, rc=1.78):
        '''
        Returns the HiC matrix of the first frame
        '''
        return cndbTools.traj2HiC(xyz(frame=0, sims=sims), mu=mu, rc=rc)
    

    xyzFuncs.defTrajs(range(1,sims+1))

    #creates folder if it doesn't exist
    os.makedirs(HiCPath, exist_ok=True)


    if frameSelection == None:
        selection = np.array(frames) #if no frame selection, select all frames
    else:
        selection = np.array(frameSelection)



    if doSub == False: #plotting with no matrix subtraction (all red)
        for frame in selection:
            print('plotting frame', frame, flush=True)
            plotHiC(frame=frame, sims=sims, mu=mu, rc=rc)
    else: #plotting with no matrix subtraction (all red)
        initHiC = initHiC() #python highlighted it yellow thinking it's a constructor but it's not and it runs right
        for frame in selection:
            print('plotting frame', frame, flush=True)
            plotHiC(frame=frame, sims=sims, initHiC=initHiC, mu=mu, rc=rc)
        








# #Generate Hi-C map
# print("Generating the contact probability matrix...")
# sim_HiC = cndbTools.traj2HiC(xyz(0, 0, 2))
# plt.matshow(sim_HiC, norm=mpl.colors.LogNorm(vmin=0.001, vmax=sim_HiC.max()), cmap="Reds")
# plt.colorbar()
# plt.show()


import time

start = time.time()


# plotHiC(frame=0, sims=2) #frames is the frame number (0-999)
# plotHiCs(frameSelection=range(0,10), sims=2) #frames is the frame number (0-10)
plotHiCs(sims=numSims, doSub=True)
# plotHiCs(sims=numSims, doSub=True, frameSelection=[999])
# plotHiCs(sims=100)

end = time.time()
print(f"Elapsed time for formatOutCoords: {end - start:.4f} seconds", flush=True)

# print(xyz())