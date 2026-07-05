print('finding Rgs ...', flush=True)


# num = 4  #used for locStats directory




# repInt = 100 #steps between each report
# repInt = 10 #steps between each report

#determining if on cluster or pc
import os
import matplotlib.pyplot as plt
import pandas as pd
from xyzFuncs import masterNum



num = masterNum
frames = 1000

pow = 5
repInt = int(10**pow / frames)



import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", type=str, required=True)
    args = parser.parse_args()
    num = args.split
except:
    print('not passed as arg likely')

print(num, flush=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
# print(script_dir)
if script_dir.startswith('/home/treed777'):
    # print('wsl')
    path = f"/home/treed777/cluster_runs/split/splitMid/output_nucleus{num}/"
else:
    # print('nots')
    path = f"/scratch/tr63/Real/output_nucleus{num}/"

#for debugging
expSims = []


#time t=1 equates to step {repInt} in the statistics.txt file
def Rg(t, sim):
    # print(sim)
    step = str(repInt * t)

    # with open(f"{path}/sim{run}/statistics.txt", "r") as r:
    with open(f"{path}/locStats{num}/statistics{sim}.txt", "r") as r:
        r.readline()
        r.readline()

        for line in r:
            # print(line)
            if line.startswith(step):
                ln = line.rstrip().split(',')
                #finding which sims exploded
                if float(ln[1]) > 1000:
                    # print(f"Simulation {run} exploded.")                    
                    if not sim in expSims:
                        expSims.append(sim)
                        
                return float(ln[1])
            
    #returns -1 if the step is not found            
    return -1.0

# print(Rg(1, 1))


def avgRg(t, sims):
    sum = 0
    for sim in range(sims):
        # if Rg(t, sim+1) == -1: #there were no errors and this takes time to compute
        #     print('error')
        sum += Rg(t, sim+1)
    return sum / sims




def writeAvgRg(sims, steps=1000):
    with open(f"{path}/RgAvgs.csv", "w") as w:
        w.write('#Step,RG\n\n')
        for t in range(1,steps+1):
            w.write(f'{repInt * t},{avgRg(t,sims)}\n')






def plotRg(n): #assumes the RgAvgs.csv file is up-to-date
    


    df = pd.read_csv(f"{path}/RgAvgs.csv")#right bc there is a header

    plt.plot(df[df.columns[0]], df[df.columns[1]],color='lime')
    
    plt.xlabel('Step')
    plt.ylabel('Average Radius of Gyration')
    plt.title('Average Radius of Gyration vs Step')

   
    # plt.figure(figsize=(10, 8))
    plt.tight_layout()
    plt.show()




    os.makedirs(f'{path}/Figs{num}', exist_ok=True)
    plt.savefig(f'{path}/Figs{num}/RgPlot{num}.tiff')  # Save the current figure to the PDF

    # plt.show()
    plt.close()


def plotRgs(n): #only run this in nots
    nums = [1356,1722,2012,2363]
    dict = {}
    dict[1356] = 'magenta'
    dict[1722] = 'lime'
    dict[2012] = 'blue'
    dict[2363] = 'black'

    for num in nums:
        path = f"/scratch/tr63/Real/output_nucleus{num}/"
        df = pd.read_csv(f"{path}/RgAvgs.csv")#right bc there is a header

        plt.plot(df[df.columns[0]], df[df.columns[1]], label=f'{num}', color=dict[num])
    
    plt.xlabel('Step', fontsize=18)
    plt.ylabel('Average Radius of Gyration', fontsize=18)
    plt.title('Average Radius of Gyration vs Step', fontsize=21)
    plt.legend(fontsize=15)

   
    # plt.figure(figsize=(10, 8))
    plt.tight_layout()
    plt.show()




    plt.savefig(f'{script_dir}/RgPlots.tiff')  # Save the current figure to the PDF

    # plt.show()
    plt.close()







simsPlotted = 100
# writeAvgRg(simsPlotted)
# plotRg(simsPlotted)
plotRgs(simsPlotted)


if len(expSims) > 0:
    print(expSims) #printing any sims that exploded
else:
    print('No sims exploded')




#DEPRECATED: plots each sim's value and avg value
# def plotRg(n): #assumes the RgAvgs.csv file is up-to-date
    

#     # Create two subplots that share the x-axis
#     fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))


#     steps = []
    
#     # Plot on second subplot (bottom graph)
#     with open(f"{path}/RgAvgs.csv", "r") as r:
#         lns = r.readlines()[2:]
#         avgRgs = []
#         for ln in lns:
#             ln = ln.rstrip().split(',')
#             steps.append(float(ln[0]))
#             avgRgs.append(float(ln[1]))
#     # print(steps, '\n', avgRgs)
#     ax2.plot(steps, avgRgs, label='Average Rgs', color='green')
#     ax2.set_xlabel('Step')
#     ax2.set_ylabel('Average Rg')
#     # ax2.legend()



#     # Plot on first subplot (top graph)
#     rgLines = []
#     for sim in range(1,n+1):
#         # with open(f"{path}/sim{sim}/statistics.txt", "r") as r:
#         with open(f"{path}/locStats{num}/statistics{sim}.txt", "r") as r:
#             lns = r.readlines()[2:]
#             Rgs = []
#             for ln in lns:
#                 ln = ln.rstrip().split(',')
#                 # steps.append(int(ln[0]))
#                 Rgs.append(float(ln[1]))
#         rgLines.append(Rgs)

#         # ax2.plot(steps, avgRgs, label='Average Rgs', color='green')
#         # print(len(steps), len(Rgs))

