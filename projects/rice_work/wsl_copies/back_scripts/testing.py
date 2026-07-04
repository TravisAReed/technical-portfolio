print('testing')

root = '/home/treed777/'

# #general testing
# import xyzFuncs as xyz
# print(xyz.trajs)






# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

# with PdfPages('output.pdf') as pdf:
#     plt.figure()
#     plt.plot([1, 2, 3], [4, 5, 6])
#     plt.title('Example Plot')
#     pdf.savefig()   # Saves the current figure into the PDF
#     plt.close()








# import matplotlib.pyplot as plt

# plt.plot([1, 2, 3], [4, 5, 6])
# plt.title("TIFF Example")
# # plt.savefig("my_figure.tiff")
# plt.savefig("my_figure.tiff", dpi=300, bbox_inches='tight')



# #multiple plots in one figure
# import matplotlib.pyplot as plt
# import numpy as np
# import os

# # Example data
# x = np.linspace(0, 2 * np.pi, 100)
# y1 = np.sin(x)
# y2 = np.cos(x)

# # Create figure and subplots
# fig, axs = plt.subplots(2, 1, figsize=(6, 8))  # 2 rows, 1 column

# # First plot
# axs[0].plot(x, y1, label='sin(x)', color='blue')
# axs[0].set_title('Sine Wave')
# axs[0].legend()

# # Second plot
# axs[1].plot(x, y2, label='cos(x)', color='green')
# axs[1].set_title('Cosine Wave')
# axs[1].legend()

# # Adjust layout
# plt.tight_layout()

# # Ensure output directory exists
# output_path = "figures/SineCosine.tiff"
# os.makedirs(os.path.dirname(output_path), exist_ok=True)

# # Save the figure as a TIFF file
# fig.savefig(output_path, dpi=300, bbox_inches='tight')

# print(f"✅ Figure saved to {output_path}")



# #mutable examples
# list = [1, 2, 3, 4, 5]
# print(list)

# listCopy = list
# print(listCopy)
# # listCopy = [6,7,8]
# listCopy[0] = 6
# listCopy[1] = 7
# listCopy[2] = 8
# listCopy[3] = 9
# listCopy[4] = 10

# print(list)

# print(listCopy)



# # Create a list
# original = [1, 2, 3]
# print("Original list:", original)

# # Assign the same list to another variable
# copy = original

# # Modify the second variable
# copy[0] = 99

# # Print both lists
# print("Modified copy:", copy)
# print("Original after modification:", original)





# import time

# start = time.time()

# # Code you want to time
# for _ in range(1000000):
#     pass

# end = time.time()
# print(f"Elapsed time: {end - start:.4f} seconds")







# #racing np method vs .split + .append method #decided not to do np method bc have to use .split on the csv anyway #actually changed my mind
# import timeit

# s = "-0.67481078, 2.4199698,3.65742276" * 10000

# # split
# t1 = timeit.timeit(lambda: [float(x) for x in s.split(",")], number=100)

# # numpy
# import numpy as np
# t2 = timeit.timeit(lambda: np.fromstring(s, sep=",").tolist(), number=100)

# print(f"split: {t1:.4f}s, numpy: {t2:.4f}s")








# #manually creating cndb file. Precusor to basically transposing frames and sims I don't have to modify the cndbTools functions
# import h5py
# import numpy as np

# # === Parameters ===
# filename = "manual_trajectory.cndb"
# N_frames = 10
# N_beads = 100



# # === Create the file ===
# with h5py.File(filename, "w") as f:
#     # Create bead types (e.g., "A" or "B" for each bead)
#     chromatin_types = np.random.choice([b"A", b"B"], size=N_beads)
#     f.create_dataset("types", data=chromatin_types)

#     # Create frames: each frame is an N_beads x 3 array of coordinates
#     for i in range(N_frames):
#         coords = np.random.rand(N_beads, 3) * 10  # scale to 3D space
#         f.create_dataset(str(i), data=coords)

# print(f"✅ Created {filename}")




# #testing 
# print(np.arange(1000).size)







# #generating Hi-C map using sim1's nucleus 0 and 1


# from OpenMiChroM.CndbTools import cndbTools
# import numpy as np

# def load_coords(cndb_path, frame=0):
#     traj = cndbTools().load(cndb_path)
#     coords = np.array(traj.cndb[str(frame)])
#     return coords

# coords0 = load_coords("/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_1.cndb")
# coords1 = load_coords("/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_1.cndb")

# print(coords0)
# print(coords1)

# coords = np.vstack((coords0, coords1))  # shape: (N_beads_total, 3)

# # from OpenMiChroM.HiC_gen import computeHiC

# # hic_map = computeHiC(coords, cutoff=1.5)  # adjust cutoff if needed

# # import matplotlib.pyplot as plt

# # plt.imshow(hic_map, cmap="Reds", origin="lower")
# # plt.colorbar(label="Contact Frequency")
# # plt.title("Hi-C Contact Map (combined trajectories)")
# # plt.xlabel("Bead Index")
# # plt.ylabel("Bead Index")
# # plt.show()


# def compute_hic(coords, cutoff=1.5):
#     N = coords.shape[0]
#     hic = np.zeros((N, N), dtype=int)

#     for i in range(N):
#         for j in range(i+1, N):
#             dist = np.linalg.norm(coords[i] - coords[j])
#             if dist < cutoff:
#                 hic[i, j] += 1
#                 hic[j, i] += 1
#     return hic

# import matplotlib.pyplot as plt
# import matplotlib as mpl

# hic_map = compute_hic(coords, cutoff=1.5)

# # plt.imshow(hic_map, cmap="Reds", origin="lower")
# plt.matshow(hic_map, norm=mpl.colors.LogNorm(vmin=0.001, vmax=hic_map.max()), cmap="Reds")

# plt.colorbar(label="Contact Count")
# plt.title("Hi-C Contact Map")
# plt.xlabel("Bead Index")
# plt.ylabel("Bead Index")
# plt.show()


# # #counting number of data points plotted
# # hic[i, j] += 1
# # hic[j, i] += 1




# #plotting both files generated in sim from theory #now works I think
# from OpenMiChroM.CndbTools import cndbTools
# import numpy as np
# import matplotlib.pyplot as plt

# def load_coords(file, frame=0):
#     traj = cndbTools().load(file)
#     return np.array(traj.cndb[str(frame)])

# # === Load both trajectories ===
# coords0 = load_coords("/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus0_1.cndb", frame=0)
# coords1 = load_coords("/home/treed777/cluster_runs/split/splitMid/output_nucleus5/locTrajs5/nucleus1_1.cndb", frame=0)






# # === Combine coordinates ===
# coords = np.vstack((coords0, coords1))
# # print(coords0[0],coords0[-1])
# # print(coords1[0],coords1[-1])
# # print(coords[0], coords[-1])
# print(coords)

# # # === Compute Hi-C map ===
# # def compute_hic(coords, cutoff=1.5):
# #     N = len(coords)
# #     print(N)
# #     hic = np.zeros((N, N), dtype=int)
# #     for i in range(N):
# #         for j in range(i+1, N):
# #             if np.linalg.norm(coords[i] - coords[j]) < cutoff:
# #                 hic[i, j] = 1
# #                 hic[j, i] = 1
# #     return hic

# # hic_map = compute_hic(coords)
# import matplotlib as mpl
# # === Plot ===
# cndbTools = cndbTools() #this line needed to make hic plot
# print(type(coords))
# print(np.array(coords).shape)

# funcFormat = np.array([coords]) #only using one frame but changes this single frame into proper format to be plotted on hic map

# hic_map = cndbTools.traj2HiC(xyz=funcFormat)



# # plt.imshow(hic_map, cmap="Reds", origin="lower")
# plt.matshow(hic_map, norm=mpl.colors.LogNorm(vmin=0.001, vmax=hic_map.max()), cmap="Reds")

# plt.colorbar(label="Contact (1 = within cutoff)")
# plt.title("Hi-C Map (nucleus0 + nucleus1, Frame 0)")
# plt.xlabel("Bead Index")
# plt.ylabel("Bead Index")
# plt.show() #looks like this worked







# #plotting columns of csvs
# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv("testFiles/pandasTest.csv")#right bc there is a header

# # Plot column 3 vs column 1
# plt.plot(df[df.columns[0]], df[df.columns[2]], marker='o')

# plt.xlabel(df.columns[0])   # e.g., "Time"
# plt.ylabel(df.columns[2])   # e.g., "Separation"
# plt.title(f"{df.columns[2]} vs {df.columns[0]}")
# plt.grid(True)
# plt.show()



# #plotting CombinedFrames.csv
# import pandas as pd
# import matplotlib.pyplot as plt

# # df = pd.read_csv(f"{root}/cluster_runs/split/splitMid/output_nucleus5/SepCsvs5/CombinedFrames.csv")#right bc there is a header
# df = pd.read_csv(f"{root}/move/CombinedFrames.csv")#right bc there is a header

# # Plot column 3 vs column 1
# # plt.plot(df[df.columns[0]], df[df.columns[2]], marker='o')
# # plt.plot(df[df.columns[0]], df[df.columns[1]])
# # plt.plot(df[df.columns[0]], df[df.columns[2]])
# # plt.plot(df[df.columns[0]], df[df.columns[3]])

# sims = range(1,101)
# for sim in sims:
#     plt.plot(df[df.columns[0]], df[df.columns[sim]])


# plt.xlabel(df.columns[0])   # e.g., "Time"
# plt.ylabel(df.columns[2])   # e.g., "Separation"
# plt.title(f"{df.columns[2]} vs {df.columns[0]}")
# # plt.grid(True)
# plt.show()








# #learning multithreading (and time a bit better)
# import threading
# import time


# #finding nums of threads
# import os
# print(os.cpu_count())  # Total number of threads (logical CPUs) #pretty sure best one
# import multiprocessing
# print(multiprocessing.cpu_count())  # Total number of threads (logical CPUs)
# activeThreads = threading.active_count()
# print(activeThreads)
# allThreads = threading.enumerate()
# print(allThreads)

# # def first(let):
# #     time.sleep(5)
# #     print('1', let)

# def second(let1, let2):
#     time.sleep(2)
#     print('2', let1, let2)

# # def third():
# #     time.sleep(1)
# #     print('3')

# # task1 = threading.Thread(target=first, args=("A",)) #need the comma at the end to show it's tuple (must be tuple)
# # task1.start()

# task2 = threading.Thread(target=second, kwargs={"let2": "E", "let1": "B"}) #passing specific args
# task2.start()

# task3 = threading.Thread(target=third)
# task3.start()

# #waits for all tasks to finish
# task1.join()
# task2.join()
# task3.join()
# print('all chores are complete')

# # first()
# # takeOutTrash()
# # getMail()

# #threading on one func with different parameters
# import threading
# import time

# def first(let):
#     time.sleep(5)
#     print('1', let)



# start = time.time()

# task1 = threading.Thread(target=first, args=("A",)) #need the comma at the end to show it's tuple (must be tuple)
# task1.start()

# task2 = threading.Thread(target=first, args=("D",))
# task2.start()


# task1.join()
# task2.join()

# end = time.time()
# print(f"Elapsed time for event: {end - start:.4f} seconds", flush=True)




# #checking if list was passed in or not
# def argNone(lst=None):
#     if lst == None:
#         l = [0,1,2]
#     else:
#         l = lst
    
#     print(l)

# argNone()
# argNone(lst=[3,4,5])


#trying to find distance 2 away from diagonal
import numpy as np

# # Example 5x5 array (replace with your real simHiC)
# simHiC = np.random.rand(5, 5)

# arrList = [
#     [5,0,0,3,0],
#     [0,5,5,0,0],
#     [0,0,5,0,0],
#     [0,0,1,5,0],
#     [0,0,5.3,0,5],
# ]
# arrList = [
#     [5,0,0,3.5,0],
#     [0,5,5,0,0],
#     [0,0,5,0,0],
#     [0,0,1,5,0],
#     [0,0,0,0,5],
# ]
# simHiC = np.array(arrList)


# # Create a mask that excludes values where |i - j| < 2
# mask = np.fromfunction(lambda i, j: np.abs(i - j) >= 2, simHiC.shape, dtype=int)

# # Apply mask: set invalid entries to -inf so they won't affect argmax
# masked_simHiC = np.where(mask, simHiC, -np.inf)

# # Find index of max in masked data
# max_index = np.unravel_index(np.argmax(masked_simHiC), simHiC.shape)

# print("Max location:", max_index)
# print("Max value:", simHiC[max_index])

# #putting as func
# def findMaxNotOnDiag(arr, dist):
#     # Create a mask that excludes values where |i - j| < dist
#     mask = np.fromfunction(lambda i, j: np.abs(i - j) >= dist, arr.shape, dtype=int)

#     # Apply mask: set invalid entries to -inf so they won't affect argmax
#     masked_arr = np.where(mask, arr, -np.inf)

#     # Find index of max in masked data
#     max_index = np.unravel_index(np.argmax(masked_arr), arr.shape)

#     print("Max location:", max_index)
#     print("Max value:", arr[max_index])


# arrList = [
#     [5,0,0,3,0],
#     [0,5,5,0,0],
#     [0,0,5,0,0],
#     [0,0,1,5,0],
#     [0,0,5.3,0,5],
# ]
# # arrList = [
# #     [5,0,0,3.5,0],
# #     [0,5,5,0,0],
# #     [0,0,5,0,0],
# #     [0,0,1,5,0],
# #     [0,0,0,0,5],
# # ]

# simHiC = np.array(arrList)

# findMaxNotOnDiag(simHiC,2)
# findMaxNotOnDiag(simHiC,1)



# #modifies matrix of all values that are less than 1 with +1 higher
import numpy as np

arrList = [
    [5,0,0,3,0],
    [0,5,5,0,0],
    [0,0,5,0,0],
    [0,0,1,5,0],
    [0,0,5.3,0,5],
]


arr = np.array(arrList)

# # arr[arr < 1] += 1

# # print(arr)

# # def myAdd(arr, lowBound):
# #     arr[arr < lowBound] += lowBound
    
# # myAdd(arr, 10**-5)
# # print(arr)


# def myLog(arr, lowBound):
#     arr[arr < lowBound] += lowBound
#     return np.log(arr)
    
# print(myLog(arr, 10**-5))
# print(arr)


# #plotting marker over plotted data
# import matplotlib.pyplot as plt
# import numpy as np

# # Matrix data
# data = np.random.rand(10, 10)
# nrows, ncols = data.shape

# # Custom intersection point
# row = 8
# col = 8

# # Plot matrix
# plt.matshow(data, cmap='Reds')

# # Plot the plus sign at (row, col)
# #cutoff
# plt.plot([col, col], [0, nrows-1], color='lime', linewidth=2)  # vertical
# plt.plot([0, ncols-1], [row, row], color='lime', linewidth=2)  # horizontal
# #at ends
# # plt.plot([col, col], [-0.5, nrows-0.5], color='lime', linewidth=2)  # vertical
# # plt.plot([-0.5, ncols-0.5], [row, row], color='lime', linewidth=2)  # horizontal

# plt.show()



#printing box around location
import numpy as np

# def print_3x3_box_around(matrix, row, col):
#     """
#     Prints a 3x3 box of values centered at (row, col).
#     Values outside the bounds are skipped.
#     """
#     nrows, ncols = matrix.shape
#     print(f"3x3 box around ({row}, {col}):\n")

#     for r in range(row - 1, row + 2):
#         line = []
#         for c in range(col - 1, col + 2):
#             if 0 <= r < nrows and 0 <= c < ncols:
#                 line.append(f"{matrix[r, c]}")
#             else:
#                 line.append("   ")  # Placeholder for out-of-bounds
#         print("  ".join(line))

# # Example usage
# data = arr  # or load your Hi-C matrix here
# split_row = 3
# split_col = 3

# print_3x3_box_around(data, split_row, split_col)



#more similar to hic integration
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

# Example usage
data = arr  # or load your Hi-C matrix here
splitLoc = 2
sideLen = 5

print_box_around(data, splitLoc, sideLen)
