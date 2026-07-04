print('finding separation distances ...', flush=True)





import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xyzFuncs as xyz



# num = 5
# num = 4
num = xyz.masterNum
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
else: #run in nots
    path = f"/scratch/tr63/Real/output_nucleus{num}"
    numSims = 100


frames = range(xyz.defTraj(f'{path}/locTrajs{num}/nucleus0_1.cndb').Nframes) #assuming all trajectories have the same number of frames which should always be true


csvFolder = f'{path}/SepCsvs{num}'

# print(f'path: {path}/locTrajs{num}/nucleus0_1.cndb', flush=True)



#creates folder if it doesn't exist
os.makedirs(csvFolder, exist_ok=True)





def clearFile(frame): #may just be needed for testing
    '''clears a file defined by its frame'''
    # print(csvFolder) #ig don't have to define as global if only using not modifying
    with open(f'{csvFolder}/frame{frame}.csv', 'w') as w:
        pass

def outRelCoords (sim):
    '''outputs the coordinates of the relavant beads'''
    #load the trajectory
    # traj0 = defTraj(f'{path}/locTrajs{num}/nucleus0_{sim}.cndb') #I'm pretty sure both won't work at once #maybe can do two imports (one for each)
    # traj1 = defTraj(f'{path}/locTrajs{num}/nucleus1_{sim}.cndb') #yeah this line breaks it
    # traj0 = defTraj(f'{path}/locTrajs{num}/nucleus0_{sim}.cndb') #I'm pretty sure both won't work at once #maybe can do two imports (one for each)
    #using trajs dict
    # print(xyz.trajs)
    traj0 = xyz.trajs[sim][0]
    traj1 = xyz.trajs[sim][1]

    for frame in frames:
        with open(f'{csvFolder}/frame{frame}.csv', 'a') as a:
            # coords0 = xyz.findXYZ(traj0, frame, 1356) #Python index for bead 1356 (last bead) in given frame of nucleus 0
            coords0 = xyz.findXYZ(traj0, frame, -1) #Python index for bead 1356 (last bead) in given frame of nucleus 0
            coords1 = xyz.findXYZ(traj1, frame, 1) #Python index for bead 1 (first bead) in given frame of nucleus 1
            # print(coords0) #right output for sim 1 frame 0 nucleus 0 is [-0.67481078  2.4199698   3.65742276]
            # print(coords[0]) 
            # a.write(f'{sim},{coords0[0]},{coords0[1]},{coords0[2]},{coords1[0]},{coords1[1]},{coords1[2]}\n')
            # a.write(f'{sim},{coords0},{coords1}\n')
            a.write(f'{sim},{coords0},{coords1},{xyz.dist(coords0, coords1)}\n')
        #may need to clear the trajectories from memory each iteration to prevent memory issues (I think overflow)
    

def formatOutCoords(sims):
    '''manages the output of the coordinates of the relavant beads'''
    #clearing previous files' data and writing headers
    for frame in frames:
        with open(f'{csvFolder}/frame{frame}.csv', 'w') as w:
            # w.write('#Sim,X,Y,Z (for nucleus 0),X,Y,Z (for nucleus 1)\n\n')
            # w.write('#Sim,Nucleus 0 Coordinates,Nucleus 1 Coordinates\n\n')
            w.write('#Sim,Nucleus 0 Coordinates,Nucleus 1 Coordinates, Separation between Chains\n\n')
    #calling outRelCoords for each sim
    for sim in sims:
        outRelCoords(sim)
                


           

def sep(sim, frame):
    '''returns distance the endpoints are separated by'''
    with open(f'{csvFolder}/frame{frame}.csv', 'r') as r:
        ln = r.readlines()[sim+1].split(',')
        # print(line)
        # print(line[0])
        # print(line[1])
        # print(line[2].rstrip())

        # return dist(
        #     np.fromstring(ln[1].strip("[]"), sep=" "),
        #     np.fromstring(ln[2].rstrip().strip("[]"), sep=" "))

        return float(ln[3])
        


    
    # return xyz.dist(xyz.findXYZ(trajs[sim][0], frame=frame, bead=1356), xyz.findXYZ(trajs[sim][1], frame=frame, bead=1))
    # return xyz.dist(xyz.findXYZ(trajs[sim][0], frame=0, bead=1356), xyz.findXYZ(trajs[sim][1], frame=0, bead=1))




def locFrames(sims): #localizes frames csvs but probably just for testing
    with open(f'{csvFolder}/CombinedFrames.csv', 'w') as w:
        # w.write('#Frame v and #Sim >')
        w.write('#Relative timestep v and #Sim >')
        for sim in sims:
            w.write(f',{sim}')
        w.write('\n')
        # w.flush()

        for frame in frames:
            w.write(f'{frame}')
            for sim in sims:
                w.write(f',{sep(sim,frame)}')
            w.write('\n')
            # w.flush()
                




def avgSep(frame):
    '''
    n is the number of 
    '''
    df = pd.read_csv(f'{csvFolder}/frame{frame}.csv')#right bc there is a header
    # print(df[df.columns[3]])

    return np.mean(df[df.columns[3]])





def writeSep(sims, frames=1000): #again assuming Nframes = 1000


    with open(f'{path}/SepAvgs.csv', "w") as w:
        w.write('#Frame,Separation of Endpoints\n\n')
        for frame in range(frames):
            # print(frame)
            w.write(f'{frame},{avgSep(frame)}\n')




def plotSep(sims): #assumes the RgAvgs.csv file is up-to-date

    
    timeSteps = []
    for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
        timeSteps.append((frame+1)*10**(pow-3))
    # print(timeSteps)

    df = pd.read_csv(f"{path}/SepAvgs.csv")#right bc there is a header

    plt.plot(timeSteps, df[df.columns[1]],color='purple')

    plt.xlabel('Step')
    plt.ylabel('Average Separation')
    plt.title('Average Separation vs Step')

   
    # plt.figure(figsize=(10, 8))
    plt.tight_layout()




    os.makedirs(f'{path}/Figs{num}', exist_ok=True)
    # plt.savefig(f'{path}/Figs{num}/SepPlot{num}.tiff',dpi=500)
    plt.savefig(f'{path}/Figs{num}/SepPlot{num}.pdf',dpi=500)

    # plt.show()
    plt.close()




def plotSeps(sims): #assumes the RgAvgs.csv file is up-to-date
    nums = [1356,1722,2012,2363]
    dict = {}
    dict[1356] = 'magenta'
    dict[1722] = 'lime'
    dict[2012] = 'blue'
    dict[2363] = 'black'


    timeSteps = []
    for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
        timeSteps.append((frame+1)*10**(pow-3))
    # print(timeSteps)


    for num in nums:
        path = f"/scratch/tr63/Real/output_nucleus{num}/"
        df = pd.read_csv(f"{path}/SepAvgs.csv")#right bc there is a header

        plt.plot(timeSteps, df[df.columns[1]],label=f'{num}',color=dict[num])



    
    
    
    plt.xlabel('Step', fontsize=18)
    plt.ylabel('Average Separation', fontsize=18)
    plt.title('Average Separation vs Step', fontsize=21)
    plt.legend(loc='lower right', fontsize=15)
   
    # plt.figure(figsize=(10, 8))
    plt.tight_layout()




    plt.savefig(f'{script_dir}/SepPlots.tiff')  # Save the current figure to the PDF

    plt.show()
    plt.close()






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
    plt.savefig(f'{path}/Figs{num}/SepCM{num}.tiff')  # Save the current figure to the PDF

    # plt.show()



def plotSepCMs(sims):
    nums = [1356,1722,2012,2363]
    dict = {}
    dict[1356] = 'magenta'
    dict[1722] = 'lime'
    dict[2012] = 'blue'
    dict[2363] = 'black'

    timeSteps = []
    for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
        timeSteps.append((frame+1)*10**(pow-3))

    for num in nums:
        xyz.defTrajs(sims=sims,num=num)

        all_distances = findSepCM(sims)
        print(all_distances[0][0])

        # Compute and plot average CM separation
        avg_distances = np.mean(all_distances, axis=0)
        plt.plot(timeSteps, avg_distances, label=f'{num}', color=dict[num])
    plt.xlabel("Step") #fix units later
    # bot.set_ylabel("Average CM Separation (nm)") #idk about those nm
    plt.ylabel("Average Separation of Centers of Mass")
    plt.title("Average Separation of Centers of Mass vs Steps")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{script_dir}/SepCMs.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file

    plt.show()




import time
# numSims = 3
sims = range(1,numSims+1)
# sims = [12]


# start = time.time()
# xyz.defTrajs(sims=sims, num=num)
# end = time.time()
# print(f"Elapsed time for defTrajs: {end - start:.4f} seconds", flush=True)

# start = time.time()
# formatOutCoords(sims=sims)
# end = time.time()
# print(f"Elapsed time for formatOutCoords: {end - start:.4f} seconds", flush=True)


# start = time.time()
# locFrames(sims=sims)
# end = time.time()
# print(f"Elapsed time for localizing frames: {end - start:.4f} seconds", flush=True)


# start = time.time()
# writeSep(sims)
# end = time.time()
# print(f"Elapsed time for write Sep: {end - start:.4f} seconds", flush=True)

# start = time.time()
# plotSep(sims)
# end = time.time()
# print(f"Elapsed time for plotSep: {end - start:.4f} seconds", flush=True)

start = time.time()
plotSeps(sims)
end = time.time()
print(f"Elapsed time for plotSeps: {end - start:.4f} seconds", flush=True)


# start = time.time()
# all_dists = findSepCM(sims)
# # print(all_dists[1][1])
# end = time.time()
# print(f"Elapsed time for findSepCM: {end - start:.4f} seconds", flush=True)

# start = time.time()
# plotSepCM(all_dists)
# end = time.time()
# print(f"Elapsed time for plotSepCM: {end - start:.4f} seconds", flush=True)

# start = time.time()
# plotSepCMs(sims)
# end = time.time()
# print(f"Elapsed time for plotSepCMs: {end - start:.4f} seconds", flush=True)







# print(avgSep(0))
# print(avgSep(999))













#Deprecated function
# def avgSep(frame, sims):
#     '''
#     n is the number of 
#     '''
#     sum = 0
#     for sim in sims:
#         sum += sep(sim, frame)
#     return sum / len(sims)



#Deprecated function
# def plotSep(sims): #assumes the RgAvgs.csv file is up-to-date

#     # Create two subplots that share the x-axis
#     fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))


#     # steps = []
#     # frames = np.arange(1000) #again assuming 1000 frames per traj #prolly should change this to steps later
#     timeSteps = []
#     for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
#         timeSteps.append((frame+1)*10**(pow-3))
#     # print(timeSteps)

#     # Plot on second subplot (bottom graph)

#     with open(f'{path}/SepAvgs.csv', "r") as r:
#         lns = r.readlines()[2:]
#         avgSeps = []
#         for ln in lns:
#             ln = ln.rstrip().split(',')
#             # steps.append(int(ln[0]))
#             avgSeps.append(float(ln[1]))





#     # ax2.plot(steps, avgSeps, label='Average Rgs', color='green')
#     # ax2.set_xlabel('Step')
#     # ax2.plot(frames, avgSeps, label='Average Rgs', color='green')
#     ax2.plot(timeSteps, avgSeps, label='Average Seps', color='green')
#     ax2.set_xlabel('Step')
#     ax2.set_ylabel('Average Separation')
#     # ax2.legend()

    



#     # Plot on first subplot (top graph)
#     # sepLines = []
#     # for sim in range(1,sims+1):


#     #     seps = []
#     #     for frame in frames:
#     #         seps.append(sep(sim, frame))
#     #     sepLines.append(seps)


#     #using CombinedFrames.csv


#     # df = pd.read_csv(f"{root}/cluster_runs/split/splitMid/output_nucleus5/SepCsvs5/CombinedFrames.csv")#right bc there is a header
#     # df = pd.read_csv(f"{root}/move/CombinedFrames.csv")#right bc there is a header
#     df = pd.read_csv(f'{csvFolder}/CombinedFrames.csv')

#     for sim in sims:
#         # ax1.plot(df[df.columns[0]], df[df.columns[sim]])
#         ax1.plot(timeSteps, df[df.columns[sim]])







#     # # Plot all n lines on the top graph
#     # for sim, y in enumerate(sepLines):
#     #     ax1.plot(frames, y, label=f'Line {sim+1}')  # add a label for the legend

#     ax1.set_ylabel('Separation')
#     # ax1.legend()

#     # Title and layout
#     fig.suptitle('Separation of Endpoints vs Steps')
#     plt.tight_layout()

#     # plt.show()

#     #creating file and saving the figure
#     os.makedirs(f'{path}/Figs{num}', exist_ok=True)
#     fig.savefig(f'{path}/Figs{num}/SepPlot{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file





#DEPRECATED
# def plotSepCM(all_distances):
#     timeSteps = []
#     for frame in range(1000): #again assuming 1000 frames per traj #prolly should change this to steps later
#         timeSteps.append((frame+1)*10**(pow-3))




#     fig, (top, bot) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

#     #plotting each sim's CM separations
#     for sim, dist_list in enumerate(all_distances):
#         # top.plot(dist_list, label=f"Sim {sim+1}")
#         top.plot(timeSteps, dist_list, label=f"Sim {sim+1}")
#     # top.set_ylabel("CM Separation (nm)")
#     top.set_ylabel("CM Separation")


#     # Compute and plot average CM separation
#     avg_distances = np.mean(all_distances, axis=0)
#     # bot.plot(avg_distances, label="Average", color='black', linewidth=2)
#     bot.plot(timeSteps, avg_distances, label="Average", color='black', linewidth=2)
#     bot.set_xlabel("Step") #fix units later
#     # bot.set_ylabel("Average CM Separation (nm)") #idk about those nm
#     bot.set_ylabel("Average CM Separation")




#     fig.suptitle("Separation of Centers of Mass vs Steps")
#     plt.tight_layout()
#     os.makedirs(f'{path}/Figs{num}', exist_ok=True)
#     plt.savefig(f'{path}/Figs{num}/SepCM{num}.tiff', dpi=300, bbox_inches='tight')  # Save the figure as a TIFF file

#     plt.show()
