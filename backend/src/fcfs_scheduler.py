"""
First-Come, First-Served (FCFS) Scheduler Implementation.
"""

from scheduler import Scheduler

class FCFSScheduler(Scheduler):
    """
    First-Come, First-Served (FCFS) scheduling algorithm.
    Processes are executed in the order they arrive.
    This is a non-preemptive algorithm.
    """
    
    def __init__(self):
        """Initialize the FCFS scheduler."""
        super().__init__()
        self.ready_queue_state = []
    
    def schedule(self):
        """
        Execute the FCFS scheduling algorithm.
        """
        if not self.processes:
            return
        
        # Reset simulation history before starting
        self.simulation_step = 0
        self.simulation_history = []
            
        # Create a copy of processes to work with during scheduling
        remaining_processes = self.processes.copy()
        
        # Initialize ready queue
        ready_queue = []
        
        # Save initial state
        self._capture_queue_state(ready_queue)
        self.save_simulation_state()
        
        while remaining_processes:
            # Find the processes that have arrived by the current time
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            
            # Add newly arrived processes to the ready queue
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            # Save state after arrivals if queue changed
            if newly_arrived:
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
            
            if not ready_queue:
                # No processes available, advance time to the next arrival
                next_arrival_time = min(p.arrival_time for p in remaining_processes)
                # Add idle time to Gantt chart
                self.update_gantt_chart(None, self.current_time, next_arrival_time)
                self.current_time = next_arrival_time
                # Save state after advancing time
                self._capture_queue_state(ready_queue)
                self.save_simulation_state()
                continue
                
            # Get the first arrived process (FCFS)
            current_process = min(ready_queue, key=lambda p: p.arrival_time)
            ready_queue.remove(current_process)
            
            # Save state after selecting process
            self._capture_queue_state(ready_queue)
            self.save_simulation_state()
            
            # Set start time if this is the first execution of the process
            if current_process.start_time is None:
                current_process.start_time = self.current_time
                current_process.calculate_response_time()
            
            # Execute the entire process
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
            
            # Save state after execution
            self._capture_queue_state(ready_queue)
            self.save_simulation_state()
            
            # Check for any new arrivals during the execution
            newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
            for process in newly_arrived:
                ready_queue.append(process)
                remaining_processes.remove(process)
            
            # Save state if new arrivals came during execution
            if newly_arrived:
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
                'arrival_time': p.arrival_time,
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
        
        return state