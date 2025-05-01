"""
Scheduler module for CPU Scheduler Simulation.
Defines the abstract base class for all scheduling algorithms.
"""

from abc import ABC, abstractmethod
import copy

class Scheduler(ABC):
    """
    Abstract base class for all CPU scheduling algorithms.
    Provides common functionality and defines the interface that all schedulers must implement.
    """
    
    def __init__(self):
        """Initialize the scheduler with empty state."""
        self.processes = []
        self.current_time = 0
        self.completion_order = []
        self.gantt_chart = []
        # Add tracking for simulation state
        self.simulation_step = 0
        self.simulation_history = []
    
    def set_processes(self, processes):
        """
        Set the list of processes to be scheduled.
        Makes deep copies to avoid modifying the original process objects.
        
        Args:
            processes (list): List of Process objects
        """
        self.processes = copy.deepcopy(processes)
        # Reset scheduler state
        self.current_time = 0
        self.completion_order = []
        self.gantt_chart = []
        
        # Sort processes by arrival time to ensure correct execution
        self.processes.sort(key=lambda p: p.arrival_time)
    
    @abstractmethod
    def schedule(self):
        """
        Execute the scheduling algorithm.
        This method must be implemented by all concrete scheduler classes.
        """
        pass
    
    def get_average_waiting_time(self):
        """
        Calculate the average waiting time for all processes.
        
        Returns:
            float: Average waiting time
        """
        if not self.completion_order:
            return 0
            
        total_waiting_time = sum(p.waiting_time for p in self.completion_order)
        return total_waiting_time / len(self.completion_order)
    
    def get_average_turnaround_time(self):
        """
        Calculate the average turnaround time for all processes.
        
        Returns:
            float: Average turnaround time
        """
        if not self.completion_order:
            return 0
            
        total_turnaround_time = sum(p.turnaround_time for p in self.completion_order)
        return total_turnaround_time / len(self.completion_order)
    
    def get_average_response_time(self):
        """
        Calculate the average response time for all processes.
        
        Returns:
            float: Average response time
        """
        if not self.completion_order:
            return 0
            
        total_response_time = sum(p.response_time for p in self.completion_order)
        return total_response_time / len(self.completion_order)
    
    def get_cpu_utilization(self):
        """
        Calculate CPU utilization as the percentage of time the CPU was busy.
        
        Returns:
            float: CPU utilization percentage (0-100)
        """
        if not self.completion_order or self.current_time == 0:
            return 0
            
        total_burst_time = sum(p.burst_time for p in self.completion_order)
        return (total_burst_time / self.current_time) * 100
    
    def get_gantt_chart(self):
        """
        Get the Gantt chart representing the execution timeline.
        
        Returns:
            list: List of dictionaries, each representing a time slot in the Gantt chart
        """
        return self.gantt_chart
    
    def get_completion_order(self):
        """
        Get the order in which processes completed execution.
        
        Returns:
            list: List of Process objects in order of completion
        """
        return self.completion_order
    
    def update_gantt_chart(self, process, start, end):
        """
        Update the Gantt chart with a new execution segment.
        
        Args:
            process: The Process object that was executed
            start (int): Start time of execution
            end (int): End time of execution
        """
        if process is None:
            # CPU idle time
            self.gantt_chart.append({
                'process_id': None,
                'start_time': start,
                'end_time': end,
                'duration': end - start
            })
        else:
            self.gantt_chart.append({
                'process_id': process.process_id,
                'start_time': start,
                'end_time': end,
                'duration': end - start
            })
            
    def get_performance_metrics(self):
        """
        Get all performance metrics for this scheduling algorithm.
        
        Returns:
            dict: Dictionary containing all performance metrics
        """
        return {
            'algorithm': self.__class__.__name__,
            'average_waiting_time': self.get_average_waiting_time(),
            'average_turnaround_time': self.get_average_turnaround_time(),
            'average_response_time': self.get_average_response_time(),
            'cpu_utilization': self.get_cpu_utilization(),
            'total_execution_time': self.current_time,
            'processes_completed': len(self.completion_order)
        }
    
    def get_simulation_state(self):
        """
        Get the current state of the simulation for interactive visualization.
        This provides all details needed for the frontend to render the current state.
        
        Returns:
            dict: A dictionary containing the current simulation state
        """
        active_processes = []
        waiting_processes = []
        completed_processes = []
        
        for process in self.processes:
            process_state = process.to_dict()
            
            # Add more detailed state information
            process_state['state'] = 'completed' if process in self.completion_order else \
                                    'running' if process.start_time is not None and process.remaining_time > 0 else \
                                    'waiting' if process.arrival_time <= self.current_time else \
                                    'not_arrived'
            
            # Organize processes by their state
            if process in self.completion_order:
                completed_processes.append(process_state)
            elif process.arrival_time <= self.current_time:
                waiting_processes.append(process_state)
            else:
                active_processes.append(process_state)
        
        return {
            'current_time': self.current_time,
            'active_processes': active_processes,
            'waiting_processes': waiting_processes,
            'completed_processes': completed_processes,
            'gantt_chart': self.gantt_chart,
            'step': self.simulation_step,
            'metrics': {
                'average_waiting_time': self.get_average_waiting_time(),
                'average_turnaround_time': self.get_average_turnaround_time(),
                'average_response_time': self.get_average_response_time(),
                'cpu_utilization': self.get_cpu_utilization()
            }
        }
        
    def save_simulation_state(self):
        """
        Save the current simulation state to the history for step-by-step replay.
        """
        self.simulation_history.append(self.get_simulation_state())
        self.simulation_step += 1
        
    def get_simulation_history(self):
        """
        Get the complete simulation history for interactive replay.
        
        Returns:
            list: List of simulation states at each step
        """
        return self.simulation_history