from process import Process
from random import randint

'''
Your Task: simulate_fcfs(processes)

Write a function that:
    Sorts the processes by arrivalTime
    Initializes a current_time = 0
    Loops through each process:
        If current_time < arrivalTime, advance time to arrivalTime (CPU waits)
            Set startTime = current_time
            Set completionTime = startTime + burstTime
            Set waitingTime = startTime - arrivalTime
            Set turnaroundTime = completionTime - arrivalTime
    Update current_time = completionTime
'''

def simulateFCFS(processes):
    # Sorting the process by its arrivalTime
    sorted_processes = sorted(processes, key=lambda p: p.arrivalTime)
    currentTime = 0
    for process in sorted_processes:
        if currentTime < process.arrivalTime:
            currentTime = process.arrivalTime

        process.startTime = currentTime
        process.completionTime = process.startTime + process.burstTime
        process.waitingTime = process.startTime - process.arrivalTime
        process.turnaroundTime = process.completionTime - process.arrivalTime
        currentTime = process.completionTime
    return sorted_processes
    

# Return average waiting time
def calculateAverageWaitTime(processes):
    totalWaitTime = 0.0
    for process in processes:
        totalWaitTime += process.waitingTime
    return (totalWaitTime/len(processes))


# Return average turnaround time
def calculateAverageTurnaroundTime(processes):
    totalTurnaroundTime = 0.0
    for process in processes:
        totalTurnaroundTime += process.turnaroundTime
    return (totalTurnaroundTime/len(processes))


'''
Write a simulate_hrrn(processes) function:
    Initialize current_time = 0
    While not all processes are completed:
        Find all ready processes (arrivalTime <= current_time)
        Calculate response ratio for each ready process: (waitingTime + burstTime) / burstTime
        Pick the process with the highest response ratio
        Set startTime
        Set completionTime
        Set waitingTime
        Set turnaroundTime
        Update current_time to completionTime
        Mark process as completed
    Return the updated process list
'''
def simulateHRRN(processes):
    currentTime = 0
    while not all(process.isCompleted for process in processes):
        readyProcesses = []
        highestResponseRatio = -1

        for process in processes:
            if not process.isCompleted and process.arrivalTime <= currentTime:
                readyProcesses.append(process)
                currentProcessResponseRatio = ((currentTime - process.arrivalTime) + process.burstTime) / process.burstTime
                if currentProcessResponseRatio > highestResponseRatio:
                    highestResponseRatio = currentProcessResponseRatio
                    readyProcess = process
        
        if highestResponseRatio == -1:
            nextArrival = min(p.arrivalTime for p in processes if not p.isCompleted)
            currentTime = nextArrival
            continue

        readyProcess.startTime = currentTime
        readyProcess.completionTime = readyProcess.startTime + readyProcess.burstTime
        readyProcess.turnaroundTime = readyProcess.completionTime - readyProcess.arrivalTime
        readyProcess.waitingTime = readyProcess.startTime - readyProcess.arrivalTime
        readyProcess.isCompleted = True
        currentTime = readyProcess.completionTime
    return processes


def main():
    processNum = 5
    processes = []
    for process in range(processNum):
        processes.append(Process(process+1, randint(0 ,10), randint(1, 10),randint(1,5)))
    print(f"{processes}\n")
    print(f"FCFS:  {simulateFCFS(processes)}/n")

    updated_processes = simulateFCFS(processes)

    averageWaitTime = calculateAverageWaitTime(updated_processes)
    averageTurnaroundTime = calculateAverageTurnaroundTime(updated_processes)

    print(f"Average Waiting Time: {averageWaitTime:.2f}\n")
    print(f"Average Turnaround Time: {averageTurnaroundTime:.2f}\n")

    updated_processes = simulateHRRN(processes)
    print(f"HRRN: {updated_processes}\n")



if __name__ == "__main__":
    main()