#shows how multiprocessing is quicker than running things linearly
#also shows how to use basic time functions

import time as t 
from multiprocessing import Process

import multiprocess as mul #importing the multiprocessing function


#iterates 100000000 times (takes about a second for each call on my machine)
def iter100000000():
    for _ in range(100000000):
        continue



startTime = t.time()
# iter100000000()
# iter100000000()
# iter100000000()
for _ in range(20):
    # iter100000000()
    t.sleep(1)
print("Elapsed nonparallel time:", t.time()-startTime)



startTime = t.time()
#setting up processes list
#base, customizable version: processes = [Process(target=iter100000000), Process(target=iter100000000), Process(target=iter100000000)]
processes = []
for _ in range(20):
    # processes.append(Process(target=iter100000000))
    # processes.append(Process(target=t.sleep)) #doesn't work bc no args
    processes.append(Process(target=t.sleep, args=(1,)))
mul.runProcesses(processes=processes)
print("Elapsed parallel time:", t.time()-startTime)


#notice how the more processes/calls of the function used, the larger the difference in the times