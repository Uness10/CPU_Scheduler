"""
Priority Scheduler Implementation.
"""

from scheduler import Scheduler

class PriorityScheduler(Scheduler):
    """
    Priority scheduling algorithm.
    Processes are executed based on their priority, with lower priority value indicating higher priority.
    This is a non-preemptive algorithm.
    """
    
    def schedule(self):
        """
        Execute the Priority scheduling algorithm.
        """
        if not self.processes:
            return
        
        # Create a copy of processes to work with during scheduling
        remaining_processes = self.processes.copy()
        
        while remaining_processes:
            # Find processes that have arrived by the current time
            ready_processes = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            if not ready_processes:
                # No processes available, advance time to the next arrival
                next_arrival_time = min(p.arrival_time for p in remaining_processes)
                # Add idle time to Gantt chart
                self.update_gantt_chart(None, self.current_time, next_arrival_time)
                self.current_time = next_arrival_time
                continue
            
            # Select the process with the highest priority (lowest priority value)
            current_process = min(ready_processes, key=lambda p: p.priority)
            
            # Set start time if this is the first execution of the process
            if current_process.start_time is None:
                current_process.start_time = self.current_time
                current_process.calculate_response_time()
            
            # Execute the entire process (non-preemptive)
            execution_start = self.current_time
            self.current_time += current_process.remaining_time
            current_process.remaining_time = 0
            
            # Update completion information
            current_process.completion_time = self.current_time
            current_process.calculate_turnaround_time()
            current_process.calculate_waiting_time()
            
            # Add to completion order and update Gantt chart
            self.completion_order.append(current_process)
            self.update_gantt_chart(current_process, execution_start, self.current_time)
            
            # Remove the completed process from remaining processes
            remaining_processes.remove(current_process)
        
        return self.get_performance_metrics()