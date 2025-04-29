# CS 3202 Project 2: CPU Scheduling Simulator

This project simulates and compares different CPU scheduling algorithms using Python.  
It collects performance metrics and visualizes the results across various test cases.

## Implemented Algorithms
- **First Come First Serve (FCFS)**  
- **Highest Response Ratio Next (HRRN)**  
- **Shortest Job First (SJF)**  
- **Shortest Remaining Time First (SRTF)**  

## Features
- Calculates:
  - Average Waiting Time (AWT)
  - Average Turnaround Time (ATT)
  - CPU Utilization (%)
  - Throughput (Processes per unit time)
- Supports small manual tests, large random tests, and edge case scenarios.
- Generates comparison tables and bar graphs using `tabulate` and `matplotlib`.

## How to Run
1. Install required libraries:
    ```bash
        pip install matplotlib tabulate
    ```
2. To run the simulation:
    ```python 
        python main.py
    ```

3. Output:
    - Console tables
    - Comparison graphs
    - Performance metrics

## Requirements
- Python 3,10+
- Libraries:
    - matplotlib
    - tabulate

If you need to download matplotlib or tabulate, run these commands in the terminal:
```bash
pip install matplotlib
```
```bash
pip install tabulate
```

## Notes:
- Burst times, arrival times, and priorities are randomly generated.
- Some algorithms (like SJF and SRTF) assume knowledge of burst times for simplicity.
- Priorities are included but not actively used in this project since all four algorithms doesn't involve priorities.