"""
Round Robin (RR) Scheduler Implementation.
"""

from scheduler import Scheduler
from collections import deque

class RoundRobinScheduler(Scheduler):
    """
    Round Robin (RR) scheduling algorithm.
    Processes are executed in a circular queue with a fixed time quantum.
    This is a preemptive algorithm.
    """
    
    def __init__(self, time_quantum=1):
        """
        Initialize the RR scheduler with a time quantum.
        
        Args:
            time_quantum (int): Maximum time slice allocated to each process
        """
        super().__init__()
        self.time_quantum = time_quantum
        # For simulation state tracking
        self.ready_queue_state = []
    
    def set_time_quantum(self, quantum):
        """
        Set the time quantum for the Round Robin scheduler.
        
        Args:
            quantum (int): Time quantum value
        """
        self.time_quantum = max(1, quantum)  # Ensure time quantum is at least 1
    
    def schedule(self):
        """
        Execute the Round Robin scheduling algorithm.
        """
        if not self.processes:
            return
        
        # Reset simulation history before starting
        self.simulation_step = 0
        self.simulation_history = []
        
        # Create a copy of processes to work with during scheduling
        remaining_processes = self.processes.copy()
        # Queue for ready processes
        ready_queue = deque()
        
        # Save initial state
        self._capture_queue_state(ready_queue)
        self.save_simulation_state()
        
        while remaining_processes or ready_queue:
            # Check for new process arrivals
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            # Save state after arrivals if queue changed
            if newly_arrived:
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
            
            if not ready_queue:
                # No processes in ready queue, advance time to next arrival
                if remaining_processes:
                    next_arrival_time = min(p.arrival_time for p in remaining_processes)
                    self.update_gantt_chart(None, self.current_time, next_arrival_time)
                    self.current_time = next_arrival_time
                    # Save state after advancing time
                    self._capture_queue_state(ready_queue)
                    self.save_simulation_state()
                    continue
                else:
                    break  # No more processes to schedule
            
            # Get the next process from the ready queue
            current_process = ready_queue.popleft()
            
            # Save state after selecting process
            self._capture_queue_state(ready_queue)
            self.save_simulation_state()
            
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
            
            # Save state after execution
            self._capture_queue_state(ready_queue)
            self.save_simulation_state()
            
            # Check for new arrivals during this quantum
            newly_arrived = [
                p for p in remaining_processes 
                if p.arrival_time <= self.current_time
            ]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            # Save state if new arrivals came during execution
            if newly_arrived:
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
            
            # Handle process completion or re-queue
            if current_process.remaining_time <= 0:
                # Process completed
                current_process.completion_time = self.current_time
                current_process.calculate_turnaround_time()
                current_process.calculate_waiting_time()
                self.completion_order.append(current_process)
                
                # Save state after process completion
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
            else:
                # Process needs more time, put it back in the queue
                ready_queue.append(current_process)
                
                # Save state after putting process back in queue
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
        
        return {
            'performance_metrics': self.get_performance_metrics(),
            'simulation_history': self.get_simulation_history()
        }
    
    def _capture_queue_state(self, ready_queue):
        """
        Capture the current state of the ready queue for simulation tracking.
        """
        self.ready_queue_state = [
            {
                'process_id': p.process_id,
                'remaining_time': p.remaining_time
            } for p in ready_queue
        ]
    
    def get_simulation_state(self):
        """
        Enhanced simulation state that includes ready queue information.
        
        Returns:
            dict: The current simulation state with ready queue details
        """
        state = super().get_simulation_state()
        
        # Add ready queue information
        state['ready_queue'] = self.ready_queue_state
        state['time_quantum'] = self.time_quantum
        
        return state