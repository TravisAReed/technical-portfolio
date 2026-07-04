import os #part of standard library

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


    # threads /= 2 #just hoping this makes the nots code work

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