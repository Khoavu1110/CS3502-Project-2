class Process:
    '''
    class Process:
        attribute:
            identifier
            arrivalTime
            burstTime
            priority
            startTime
            completionTime
            waitingTime
            turnaroundTime
    '''
    def __init__(self, pid, arrivalTime, burstTime, priority):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        self.startTime = None
        self.completionTime = None
        self.waitingTime = None
        self.turnaroundTime = None
        self.isCompleted = False

        

    def __repr__(self):
        return (f"Process(pid={self.pid}, AT={self.arrivalTime}, BT={self.burstTime}, PR={self.priority}, "
                f"ST={self.startTime}, CT={self.completionTime}, WT={self.waitingTime}, TAT={self.turnaroundTime})")
