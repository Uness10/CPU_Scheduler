"""
Test file to demonstrate the behavior of the Priority Round Robin Scheduler.
"""

from process import Process
from priority_rr_scheduler import PriorityRRScheduler

def print_gantt_chart(gantt_chart):
    """Print a simple representation of a Gantt chart."""
    print("\nGantt Chart:")
    print("Time | Process")
    print("-----+---------")
    
    for item in gantt_chart:
        process_id = "IDLE" if item['process_id'] is None else f"P{item['process_id']}"
        print(f"{item['start_time']:4d} | {process_id}")
        print(f"{item['end_time']:4d} | ")
        
def test_priority_rr_scheduler():
    """
    Test the Priority Round Robin scheduler with a set of processes.
    
    This test creates processes with different priorities and checks if the scheduler
    correctly executes them according to priority with round robin within each priority level.
    """
    # Create test processes
    processes = [
        # Process(id, arrival_time, burst_time, priority)
        Process(1, 0, 5, 2),  # P1: medium priority
        Process(2, 1, 4, 1),  # P2: high priority
        Process(3, 0, 3, 3),  # P3: low priority
        Process(4, 2, 6, 1),  # P4: high priority, arrives later
        Process(5, 4, 2, 2),  # P5: medium priority, arrives even later
    ]
    
    # Print the initial process list
    print("Initial Process List:")
    for p in processes:
        print(f"P{p.process_id}: Priority={p.priority}, Arrival={p.arrival_time}, Burst={p.burst_time}")
    print("\n")
    
    # Initialize scheduler with time quantum of 2 and enable debug output
    scheduler = PriorityRRScheduler(time_quantum=2)
    scheduler.set_processes(processes)
    
    # Run the scheduler with debugging
    print("=== Execution Trace ===")
    result = scheduler.schedule()
    
    # Print processes
    print("\nProcess Details After Execution:")
    for p in processes:
        print(f"P{p.process_id}: Priority={p.priority}, Arrival={p.arrival_time}, Burst={p.burst_time}, " + 
              f"Completion={p.completion_time}, Turnaround={p.turnaround_time}, Waiting={p.waiting_time}")
    
    # Print Gantt chart
    print_gantt_chart(scheduler.get_gantt_chart())
    
    # Print performance metrics
    metrics = scheduler.get_performance_metrics()
    print("\nPerformance Metrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
            
if __name__ == "__main__":
    test_priority_rr_scheduler()