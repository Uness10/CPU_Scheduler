"""
Priority Round Robin Scheduler Implementation.
A hybrid algorithm that combines priority scheduling with Round Robin.
"""

from scheduler import Scheduler
from collections import deque

class PriorityRRScheduler(Scheduler):
    """
    Priority Round Robin scheduling algorithm.
    Processes are grouped by priority, with Round Robin applied within each priority group.
    Higher priority (lower priority number) processes are executed before lower priority ones.
    """
    
    def __init__(self, time_quantum=1):
        """
        Initialize the Priority RR scheduler with a time quantum.
        
        Args:
            time_quantum (int): Maximum time slice allocated to each process
        """
        super().__init__()
        self.time_quantum = time_quantum
    
    def set_time_quantum(self, quantum):
        """
        Set the time quantum for the Round Robin component.
        
        Args:
            quantum (int): Time quantum value
        """
        self.time_quantum = max(1, quantum)  # Ensure time quantum is at least 1
    
    def schedule(self):
        """
        Execute the Priority Round Robin scheduling algorithm.
        """
        if not self.processes:
            return
        
        # Create a copy of processes to work with during scheduling
        remaining_processes = self.processes.copy()
        
        # Dictionary to hold queues for each priority level
        priority_queues = {}
        
        while remaining_processes or any(priority_queues.values()):
            # Check for new arrivals and add them to their priority queues
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in newly_arrived:
                if process.priority not in priority_queues:
                    priority_queues[process.priority] = deque()
                priority_queues[process.priority].append(process)
                remaining_processes.remove(process)
            
            # If no processes are ready, advance time to the next arrival
            if not any(priority_queues.values()):
                if remaining_processes:
                    next_arrival_time = min(p.arrival_time for p in remaining_processes)
                    self.update_gantt_chart(None, self.current_time, next_arrival_time)
                    self.current_time = next_arrival_time
                    continue
                else:
                    break  # No more processes to schedule
            
            # Get the highest priority non-empty queue
            current_priority = min([p for p in priority_queues.keys() if priority_queues[p]])
            current_queue = priority_queues[current_priority]
            
            # Get the next process from the queue
            current_process = current_queue.popleft()
            
            # Set start time if this is the first execution of the process
            if current_process.start_time is None:
                current_process.start_time = self.current_time
                current_process.calculate_response_time()
            
            # Calculate execution time for this quantum
            execution_time = min(self.time_quantum, current_process.remaining_time)
            execution_start = self.current_time
            self.current_time += execution_time
            current_process.remaining_time -= execution_time
            
            # Update Gantt chart with this execution segment
            self.update_gantt_chart(current_process, execution_start, self.current_time)
            
            # Check for new arrivals during this quantum
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in newly_arrived:
                if process.priority not in priority_queues:
                    priority_queues[process.priority] = deque()
                priority_queues[process.priority].append(process)
                remaining_processes.remove(process)
            
            # Handle process completion or re-queue
            if current_process.remaining_time <= 0:
                # Process completed
                current_process.completion_time = self.current_time
                current_process.calculate_turnaround_time()
                current_process.calculate_waiting_time()
                self.completion_order.append(current_process)
            else:
                # Process needs more time, put it back in the queue
                current_queue.append(current_process)
            
            # If the queue is now empty, remove it from the dictionary
            if not current_queue:
                del priority_queues[current_priority]
        
        return self.get_performance_metrics()