from process import Process
from random import randint


def main():
    processNum = 5
    processes = []
    for process in range(processNum):
        processes.append(Process(process, randint(0 ,10), randint(1, 10),randint(1,5)))
    print(processes)

if __name__ == "__main__":
    main()