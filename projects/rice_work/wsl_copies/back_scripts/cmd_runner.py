print('running commands ...')

import subprocess

# subprocess.run(f"scp nots:/scratch/tr63/back_scripts/RgPlots.tiff /mnt/c/Users/treed/Downloads/Figures/temp7",shell=True, check=True)
# subprocess.run(f"scp nots:/scratch/tr63/back_scripts/SepPlots.tiff /mnt/c/Users/treed/Downloads/Figures/temp7",shell=True, check=True)



def scpNums(nums, frames=None):
    for num in nums:
        print('running commands on split', num, '...')
        if frames != None:
            for frame in frames:
                # subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/Figs{num}/HiCMaps{num}/frame{frame}HiCDiff.tiff /mnt/c/Users/treed/Downloads/Figures/temp11/frame{frame}HiCDiff{num}.tiff",shell=True, check=True)
                subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/Figs{num}/HiCMaps{num}/frame{frame}HiCDiffBigTitle.tiff /mnt/c/Users/treed/Downloads/Figures/temp11/frame{frame}HiCDiffBigTitle{num}.tiff",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/back_scripts/SepCM{num}.tiff /mnt/c/Users/treed/Downloads/Figures/temp9/",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/Figs{num}/HiCMaps{num}/HiCDiffsVid{num}.mp4 /mnt/c/Users/treed/Downloads/Figures/temp9/HiCDiffsVid{num}.mp4",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/Figs{num}/HiCMaps{num}/HiCDiffsVid{num}Fixed.mp4 /mnt/c/Users/treed/Downloads/Figures/temp9/HiCDiffsVid{num}Fixed.mp4",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/back_scripts/ProbVsDistPlot{num}split{num}.tiff /mnt/c/Users/treed/Downloads/Figures/temp9/",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/sim1/nucleus_0_step100000.ndb /home/treed777/move",shell=True, check=True)
        # subprocess.run(f"scp nots:/scratch/tr63/Real/output_nucleus{num}/sim1/nucleus_1_step100000.ndb /home/treed777/move",shell=True, check=True)


nums = [1356,1722,2012,2363]
# nums = [2012,2363]
# nums = [1356, 1722]
nums = [1356]
# nums = [2363]

# scpNums(nums)
# scpNums(nums, [2,101,651,998])
# scpNums(nums, [999])
# scpNums(nums, [700])
# scpNums(nums, [0, 1, 15, 100, 300, 650, 999])
# scpNums(nums, [0, 100, 500, 999])
scpNums(nums, [0, 100, 999])



def managePhotos(inp):

    fName = inp.split('.')[0]


    subprocess.run(f"convert {inp} {fName}.png",shell=True, check=True)
    subprocess.run(f"scp {fName}.png /mnt/c/Users/treed/Downloads/Figures/temp10",shell=True, check=True)

# managePhotos('/home/treed777/cluster_runs/collapsed/')
# managePhotos('/home/treed777/move/postSplit.tga')
# managePhotos('/home/treed777/move/endSim.tga')