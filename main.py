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



'''
simulateSRTF(processes) function:
Initialize currentTime = 0
While not all processes are completed:
    Find all processes that have arrived (arrivalTime <= current_time) and are not finished.
    From ready processes, pick the one with the **smallest remaining time**.
    Run that process for 1 unit of time (simulate small steps!).
    Decrease its remaining time by 1.
    If a process finishes (remaining time == 0):
        Set completionTime, waitingTime, turnaroundTime
        Mark process as completed
    Increase current_time by 1
'''
def simulateSRTF (processes):
    currentTime = 0
    # Initialize remaining time for all processes
    for process in processes:
        process.remainingTime = process.burstTime

    while not all (process.isCompleted for process in processes):
        readyProcesses = []
        smallestRemainingTime = math.inf
        selectedProcess = None

        for process in processes:
            if not process.isCompleted and process.arrivalTime <= currentTime:
                readyProcesses.append(process)
                if process.remainingTime < smallestRemainingTime:
                    smallestRemainingTime = process.remainingTime
                    selectedProcess = process
        
        # If no process is ready
        if selectedProcess is None:
            currentTime += 1
            continue

        # Execute the selected process for 1 unit of time
        selectedProcess.remainingTime -= 1

        # If the process is finished
        if selectedProcess.remainingTime == 0:
            selectedProcess.isCompletd = True
            selectedProcess.completionTime = currentTime + 1
            selectedProcess.turnaroundTime = selectedProcess.completionTime - selectedProcess.arrivalTime
            selectedProcess.waitingTime = selectedProcess.turnaroundTime - selectedProcess.burstTime
            if selectedProcess.startTime is None:
                selectedProcess.startTime = currentTime

        # Update time
        currentTime += 1

    return processes
                



    pass


'''
CPU Utilization = (Total CPU Busy Time / Total Time) × 100
'''
def calculateCPUUtilization(processes):
    CPUUtilization = 0
    totalCPUBusyTime = 0
    for process in processes:
        totalCPUBusyTime = totalCPUBusyTime + process.burstTime
    totalTime = max(process.completionTime for process in processes)

    CPUUtilization = float((totalCPUBusyTime / totalTime) *100)
    return CPUUtilization



'''
Throughput = Total number of processes completed / total time taken
'''
def calculateThroughput(processes):
    totalTime = max(process.completionTime for process in processes)
    return len(processes)/totalTime
    


def main():
    processNum = 50
    processes = []

    # Generate random processes
    for process in range(processNum):
        # pid, arrivalTime, burstTime, priority
        processes.append(Process(process+1, randint(0, 10), randint(1, 50), randint(1, 5)))
    # print(f"Original Processes:\n{processes}\n")
    print("Original Process: ")
    for process in processes:
        print(f"{process}\n")

    # Make deep copies for each algorithm so original data is untouched
    processes_fcfs = copy.deepcopy(processes)
    processes_hrrn = copy.deepcopy(processes)
    processes_sjf = copy.deepcopy(processes)
    processes_srtf = copy.deepcopy(processes)

    # Run FCFS simulation
    FCFS_UpdatedProcesses = simulateFCFS(processes_fcfs)
    FCFS_averageWaitTime = calculateAverageWaitTime(FCFS_UpdatedProcesses)
    FCFS_averageTurnaroundTime = calculateAverageTurnaroundTime(FCFS_UpdatedProcesses)
    FCFS_CPUUtilization = calculateCPUUtilization(FCFS_UpdatedProcesses)
    FCFS_Throughput = calculateThroughput(FCFS_UpdatedProcesses)

    # Run HRRN simulation
    HRRN_UpdatedProcesses = simulateHRRN(processes_hrrn)
    HRRN_averageWaitTime = calculateAverageWaitTime(HRRN_UpdatedProcesses)
    HRRN_averageTurnaroundTime = calculateAverageTurnaroundTime(HRRN_UpdatedProcesses)
    HRRN_CPUUtilization = calculateCPUUtilization(HRRN_UpdatedProcesses)
    HRRN_Throughput = calculateThroughput(HRRN_UpdatedProcesses)

    # Run SJF simulation
    SJF_UpdatedProcesses = simulateSJF(processes_sjf)
    SJF_averageWaitTime = calculateAverageWaitTime(SJF_UpdatedProcesses)
    SJF_averageTurnaroundTime = calculateAverageTurnaroundTime(SJF_UpdatedProcesses)
    SJF_CPUUtilization = calculateCPUUtilization(SJF_UpdatedProcesses)
    SJF_Throughput = calculateThroughput(SJF_UpdatedProcesses)

    # Run SRTF
    SRTF_UpdatedProcesses = simulateSJF(processes_srtf)
    SRTF_averageWaitTime = calculateAverageWaitTime(SRTF_UpdatedProcesses)
    SRTF_averageTurnaroundTime = calculateAverageTurnaroundTime(SRTF_UpdatedProcesses)
    SRTF_CPUUtilization = calculateCPUUtilization(SRTF_UpdatedProcesses)
    SRTF_Throughput = calculateThroughput(SRTF_UpdatedProcesses)

    # Create table with tabulate
    data = [
        ["FCFS", FCFS_averageWaitTime, FCFS_averageTurnaroundTime, FCFS_CPUUtilization, FCFS_Throughput],
        ["HRRN", HRRN_averageWaitTime, HRRN_averageTurnaroundTime, HRRN_CPUUtilization, HRRN_Throughput],
        ["SJF", SJF_averageWaitTime, SJF_averageTurnaroundTime, SJF_CPUUtilization, SJF_Throughput],
        ["SRTF", SRTF_averageWaitTime, SRTF_averageTurnaroundTime, SRTF_CPUUtilization, SRTF_Throughput]

    ]

    headers = ["Algorithm", "Avg Wait Time", "Avg Turnaround Time", "CPU Utilization (%)", "Throughput (processes/unit time)"]
    print(tabulate(data, headers=headers, tablefmt="github"))

    # Plotting the result
    algorithms = ["FCFS", "HRRN", "SJF", "SRTF"]
    avgWaitTime = [FCFS_averageWaitTime, HRRN_averageWaitTime, SJF_averageWaitTime, SRTF_averageWaitTime]
    avgTurnaroundTime = [FCFS_averageTurnaroundTime, HRRN_averageTurnaroundTime, SJF_averageTurnaroundTime, SRTF_averageTurnaroundTime]

    x = range(len(algorithms))
    barWidth = 0.35

    plt.bar(x, avgWaitTime, width=barWidth, label="Average Wait Time")
    plt.bar([i + barWidth for i in x], avgTurnaroundTime, width=barWidth, label="Average Turnaround Time")

    # Add labels and title
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Time (units)')
    plt.title('FCFS vs HRRN vs SJF vs SRTF Performance')
    plt.xticks([i + barWidth / 2 for i in x], algorithms)
    plt.legend()

    # Save the plot as image (optional)
    plt.savefig('scheduling_comparison.png')

    # Show the graph
    plt.show()

if __name__ == "__main__":
    main()