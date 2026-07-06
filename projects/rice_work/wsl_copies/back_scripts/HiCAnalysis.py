print('analyzing HiC ...')

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