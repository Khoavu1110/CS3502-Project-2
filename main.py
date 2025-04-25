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



def main():
    processNum = 5
    processes = []
    for process in range(processNum):
        processes.append(Process(process+1, randint(0 ,10), randint(1, 10),randint(1,5)))
    print(processes)
    print(f"FCFS:  {simulateFCFS(processes)}")

    updated_processes = simulateFCFS(processes)

    averageWaitTime = calculateAverageWaitTime(updated_processes)
    averageTurnaroundTime = calculateAverageTurnaroundTime(updated_processes)

    print(f"Average Waiting Time: {averageWaitTime:.2f}")
    print(f"Average Turnaround Time: {averageTurnaroundTime:.2f}")


if __name__ == "__main__":
    main()