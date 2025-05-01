"""
Priority Round Robin Scheduler Implementation.
A hybrid algorithm that combines priority scheduling with Round Robin.
"""

from scheduler import Scheduler
from collections import deque

class PriorityRRScheduler(Scheduler):
    """
    Priority Round Robin scheduling algorithm.
    
    This scheduler combines two scheduling concepts:
    1. Priority-based scheduling - processes with higher priority (lower priority number) execute first
    2. Round Robin - within each priority level, processes are executed in a time-sliced manner
    
    The algorithm works by:
    - Maintaining separate round robin queues for each priority level
    - Always executing from the highest priority non-empty queue first
    - Applying time quantum-based execution within each priority level
    - Only moving to a lower priority queue when all higher priority queues are empty
    - Following queue discipline: newly arrived processes and processes that haven't
      finished execution are always placed at the back of their respective priority queues
    """
    def __init__(self, time_quantum=1):
        """
        Initialize the Priority RR scheduler with a time quantum.
        
        Args:
            time_quantum (int): Maximum time slice allocated to each process
        """
        super().__init__()
        self.time_quantum = time_quantum
        # For simulation state tracking
        self.priority_queues_state = {}
    
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
        
        # Reset simulation history before starting
        self.simulation_step = 0
        self.simulation_history = []
        
        # Create a copy of processes to work with during scheduling
        remaining_processes = self.processes.copy()
        
        # Dictionary to hold queues for each priority level
        # Each queue is a deque data structure that maintains FIFO order
        priority_queues = {}
        
        # Save initial state
        self._capture_queue_state(priority_queues)
        self.save_simulation_state()
        
        while remaining_processes or any(priority_queues.values()):
            # Process any new arrivals and add them to the back of their respective priority queues
            self._process_new_arrivals(remaining_processes, priority_queues)
            
            # Save state after arrivals
            if self._has_queue_state_changed(priority_queues):
                self._capture_queue_state(priority_queues)
                self.save_simulation_state()
            
            # If no processes are ready, advance time to the next arrival
            if not any(priority_queues.values()):
                if remaining_processes:
                    self._advance_to_next_arrival(remaining_processes)
                    # Save state after advancing time
                    self._capture_queue_state(priority_queues)
                    self.save_simulation_state()
                    continue
                else:
                    break  # No more processes to schedule
            
            # Get the highest priority non-empty queue
            current_priority = min([p for p in priority_queues.keys() if priority_queues[p]])
            current_queue = priority_queues[current_priority]
            
            # Execute one process from the front of the highest priority queue
            self._execute_process(current_queue, current_priority, priority_queues)
            
            # Save state after execution
            self._capture_queue_state(priority_queues)
            self.save_simulation_state()
            
            # Process any new arrivals that might have come during execution
            self._process_new_arrivals(remaining_processes, priority_queues)
            
            # Save state if new arrivals came during execution
            if self._has_queue_state_changed(priority_queues):
                self._capture_queue_state(priority_queues)
                self.save_simulation_state()
        
        return {
            'performance_metrics': self.get_performance_metrics(),
            'simulation_history': self.get_simulation_history()
        }
    
    def _process_new_arrivals(self, remaining_processes, priority_queues):
        """
        Check for newly arrived processes and add them to appropriate priority queues.
        Newly arrived processes are always added to the back of their priority queue.
        
        Args:
            remaining_processes (list): List of processes that haven't arrived yet
            priority_queues (dict): Dictionary of priority queues
        """
        # Find processes that have arrived by the current time
        newly_arrived = [p for p in remaining_processes if p.arrival_time <= self.current_time]
        
        # Add newly arrived processes to their respective priority queues
        for process in newly_arrived:
            if process.priority not in priority_queues:
                priority_queues[process.priority] = deque()
            
            # Add to back of queue (maintaining FIFO order)
            priority_queues[process.priority].append(process)
            remaining_processes.remove(process)
    
    def _advance_to_next_arrival(self, remaining_processes):
        """
        Advance time to the next process arrival when no processes are ready.
        
        Args:
            remaining_processes (list): List of processes that haven't arrived yet
        """
        next_arrival_time = min(p.arrival_time for p in remaining_processes)
        self.update_gantt_chart(None, self.current_time, next_arrival_time)
        self.current_time = next_arrival_time
    
    def _execute_process(self, current_queue, priority, priority_queues):
        """
        Execute a single process from the given queue for one time quantum.
        
        Args:
            current_queue (deque): The queue containing the process to execute
            priority (int): The priority level of the current queue
            priority_queues (dict): Dictionary of all priority queues
        """
        # Get the next process from the front of the queue (FIFO order)
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
        
        # Handle process completion or re-queue
        if current_process.remaining_time <= 0:
            # Process completed
            current_process.completion_time = self.current_time
            current_process.calculate_turnaround_time()
            current_process.calculate_waiting_time()
            self.completion_order.append(current_process)
        else:
            # Process needs more time, put it back at the end of the queue (maintaining FIFO order)
            current_queue.append(current_process)
        
        # If the queue is now empty, remove it from the dictionary
        if not current_queue:
            priority_queues.pop(priority, None)
    
    def _capture_queue_state(self, priority_queues):
        """
        Capture the current state of all priority queues for simulation tracking.
        """
        queue_state = {}
        for priority, queue in priority_queues.items():
            queue_state[priority] = [
                {
                    'process_id': p.process_id,
                    'remaining_time': p.remaining_time,
                    'priority': p.priority
                } for p in queue
            ]
        self.priority_queues_state = queue_state
    
    def _has_queue_state_changed(self, priority_queues):
        """
        Check if the queue state has changed since the last capture.
        """
        # Quick check for different priorities
        if set(priority_queues.keys()) != set(self.priority_queues_state.keys()):
            return True
        
        # Check for differences in queue contents
        for priority, queue in priority_queues.items():
            if priority not in self.priority_queues_state:
                return True
                
            old_queue = self.priority_queues_state[priority]
            if len(queue) != len(old_queue):
                return True
                
            for i, process in enumerate(queue):
                if i >= len(old_queue) or process.process_id != old_queue[i]['process_id'] or \
                   process.remaining_time != old_queue[i]['remaining_time']:
                    return True
        
        return False
    
    def get_simulation_state(self):
        """
        Enhanced simulation state that includes priority queue information.
        
        Returns:
            dict: The current simulation state with priority queue details
        """
        state = super().get_simulation_state()
        
        # Add priority queue information
        state['priority_queues'] = self.priority_queues_state
        state['time_quantum'] = self.time_quantum
        
        return state