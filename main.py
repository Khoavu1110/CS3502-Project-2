from process import Process
from random import randint
from tabulate import tabulate
import matplotlib.pyplot as plt
import copy
import math



'''
simulateFCFS (processes) function:
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
simulateHRRN(processes) function:
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



'''
simulateSJF(processes) function:
    Initialize current_time = 0
    While not all processes are completed:
        Find all ready processes (arrivalTime <= current_time)
        Among ready processes, select the one with the smallest burstTime
        If no process is ready, advance current_time to the next arrival
        Set startTime
        Set completionTime
        Set waitingTime
        Set turnaroundTime
        Update current_time to completionTime
        Mark process as completed
    Return the updated process list
'''
def simulateSJF(processes):
    currentTime = 0
    while not all(process.isCompleted for process in processes):
        readyProcesses = []
        smallestBurstTime = math.inf

        for process in processes:
            if not process.isCompleted and process.arrivalTime <= currentTime:
                readyProcesses.append(process)
                currentBurstTime = process.burstTime
                if currentBurstTime < smallestBurstTime:
                    smallestBurstTime = currentBurstTime
                    readyProcess = process

        # Check if no process was ready
        if smallestBurstTime == math.inf:
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

    # Generate random processes
    for process in range(processNum):
        processes.append(Process(process+1, randint(0, 10), randint(1, 10), randint(1, 5)))
    print(f"Original Processes:\n{processes}\n")

    # Make deep copies for each algorithm so original data is untouched
    processes_fcfs = copy.deepcopy(processes)
    processes_hrrn = copy.deepcopy(processes)
    processes_sjf = copy.deepcopy(processes)

    # Run FCFS simulation
    FCFS_UpdatedProcesses = simulateFCFS(processes_fcfs)
    FCFS_averageWaitTime = calculateAverageWaitTime(FCFS_UpdatedProcesses)
    FCFS_averageTurnaroundTime = calculateAverageTurnaroundTime(FCFS_UpdatedProcesses)

    # Run HRRN simulation
    HRRN_UpdatedProcesses = simulateHRRN(processes_hrrn)
    HRRN_averageWaitTime = calculateAverageWaitTime(HRRN_UpdatedProcesses)
    HRRN_averageTurnaroundTime = calculateAverageTurnaroundTime(HRRN_UpdatedProcesses)

    # Run SJF simulation
    SJF_UpdatedProcesses = simulateSJF(processes_sjf)
    SJF_averageWaitTime = calculateAverageWaitTime(SJF_UpdatedProcesses)
    SJF_averageTurnaroundTime = calculateAverageTurnaroundTime(SJF_UpdatedProcesses)

    # Create table with tabulate
    data = [
        ["FCFS", FCFS_averageWaitTime, FCFS_averageTurnaroundTime],
        ["HRRN", HRRN_averageWaitTime, HRRN_averageTurnaroundTime],
        ["SJF", SJF_averageWaitTime, SJF_averageTurnaroundTime]
    ]
    headers = ["Algorithm", "Average Wait Time", "Average Turnaround Time"]
    print(tabulate(data, headers=headers, tablefmt="github"))

    # Plotting the result
    algorithms = ["FCFS", "HRRN", "SJF"]
    avgWaitTime = [FCFS_averageWaitTime, HRRN_averageWaitTime, SJF_averageWaitTime]
    avgTurnaroundTime = [FCFS_averageTurnaroundTime, HRRN_averageTurnaroundTime, SJF_averageTurnaroundTime]

    x = range(len(algorithms))
    barWidth = 0.35

    plt.bar(x, avgWaitTime, width=barWidth, label="Average Wait Time")
    plt.bar([i + barWidth for i in x], avgTurnaroundTime, width=barWidth, label="Average Turnaround Time")

    # Add labels and title
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Time (units)')
    plt.title('FCFS vs HRRN vs SJF Performance')
    plt.xticks([i + barWidth / 2 for i in x], algorithms)
    plt.legend()

    # Save the plot as image (optional)
    plt.savefig('scheduling_comparison.png')

    # Show the graph
    plt.show()

if __name__ == "__main__":
    main()