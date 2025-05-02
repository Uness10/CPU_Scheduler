"""
Simulation Controller for CPU Scheduler Simulation.
Centralizes control over the scheduling simulation process.
"""

from utils.process_generator import ProcessGenerator
from schedulers.fcfs_scheduler import FCFSScheduler
from schedulers.sjf_scheduler import SJFScheduler
from schedulers.priority_scheduler import PriorityScheduler
from schedulers.round_robin_scheduler import RoundRobinScheduler
from schedulers.priority_rr_scheduler import PriorityRRScheduler

class SimulationController:
    """
    Controls the simulation of various CPU scheduling algorithms.
    Manages processes and schedulers, runs simulations, and collects performance metrics.
    """
    
    def __init__(self):
        """Initialize the simulation controller."""
        self.scheduler = None
        self.processes = []
        self.process_generator = ProcessGenerator()
        
    def load_processes(self, source, params=None):
        """
        Load processes from a file or generate random processes.
        
        Args:
            source (str): 'random' for random generation or a file path
            params (dict): Parameters for random generation or None
        
        Returns:
            list: The loaded processes
        """
        if source == 'random':
            if not params:
                params = {
                    'count': 5,
                    'burst_range': (1, 10),
                    'arrival_range': (0, 10),
                    'priority_range': (1, 5)
                }
            
            self.processes = self.process_generator.generate_random_processes(
                params.get('count', 5),
                params.get('burst_range', (1, 10)),
                params.get('arrival_range', (0, 10)),
                params.get('priority_range', (1, 5))
            )
        else:
            # Assume source is a file path
            self.processes = self.process_generator.load_processes_from_file(source)
            
        return self.processes
        
    def set_scheduler(self, algorithm, params=None):
        """
        Set the scheduler algorithm to use for the simulation.
        
        Args:
            algorithm (str): The name of the algorithm to use
                ('FCFS', 'SJF', 'Priority', 'RR', 'PriorityRR')
            params (dict): Additional parameters for the scheduler (e.g., time_quantum)
        
        Returns:
            bool: True if the scheduler was set successfully
        """
        if not params:
            params = {}
            
        if algorithm == 'FCFS':
            self.scheduler = FCFSScheduler()
        elif algorithm == 'SJF':
            self.scheduler = SJFScheduler()
        elif algorithm == 'Priority':
            self.scheduler = PriorityScheduler()
        elif algorithm == 'RR':
            self.scheduler = RoundRobinScheduler()
            if 'time_quantum' in params:
                self.scheduler.set_time_quantum(params['time_quantum'])
        elif algorithm == 'PriorityRR':
            self.scheduler = PriorityRRScheduler()
            if 'time_quantum' in params:
                self.scheduler.set_time_quantum(params['time_quantum'])
        else:
            raise ValueError(f"Unknown scheduling algorithm: {algorithm}")
            
        return True
    
    def run_simulation(self):
        """
        Run the simulation using the current scheduler and processes.
        
        Returns:
            dict: Simulation results including performance metrics and visualization data
        """
        if not self.scheduler:
            raise ValueError("No scheduler set. Use set_scheduler before running simulation.")
            
        if not self.processes:
            raise ValueError("No processes loaded. Use load_processes before running simulation.")
            
        # Set processes for the scheduler and run it
        self.scheduler.set_processes(self.processes)
        self.scheduler.schedule()
        
        # Collect and return results
        return {
            'performance_metrics': self.get_performance_metrics(),
            'visualization_data': self.get_visualization_data()
        }
    
    def get_performance_metrics(self):
        """
        Get the performance metrics from the last simulation run.
        
        Returns:
            dict: Performance metrics
        """
        if not self.scheduler:
            return {}
            
        return self.scheduler.get_performance_metrics()
    
    def get_visualization_data(self):
        """
        Get data needed for visualization of the simulation.
        
        Returns:
            dict: Visualization data including Gantt chart and completion order
        """
        if not self.scheduler:
            return {}
            
        # Convert processes to dictionaries for JSON serialization
        completion_order = [p.to_dict() for p in self.scheduler.get_completion_order()]
        
        return {
            'gantt_chart': self.scheduler.get_gantt_chart(),
            'completion_order': completion_order,
            'total_time': self.scheduler.current_time
        }
        
    def get_available_algorithms(self):
        """
        Get a list of available scheduling algorithms.
        
        Returns:
            list: List of available algorithms and their descriptions
        """
        return [
            {
                'id': 'FCFS',
                'name': 'First-Come, First-Served',
                'description': 'Processes are executed in the order they arrive',
                'type': 'batch',
                'params': []
            },
            {
                'id': 'SJF',
                'name': 'Shortest Job First',
                'description': 'Processes with the shortest burst time are executed first',
                'type': 'batch',
                'params': []
            },
            {
                'id': 'Priority',
                'name': 'Priority Scheduling',
                'description': 'Processes with higher priority (lower value) are executed first',
                'type': 'batch',
                'params': []
            },
            {
                'id': 'RR',
                'name': 'Round Robin',
                'description': 'Processes are executed in a circular queue with a fixed time quantum',
                'type': 'interactive',
                'params': [
                    {
                        'name': 'time_quantum',
                        'type': 'int',
                        'default': 2,
                        'description': 'Maximum time slice allocated to each process'
                    }
                ]
            },
            {
                'id': 'PriorityRR',
                'name': 'Priority with Round Robin',
                'description': 'Priority scheduling with Round Robin for processes of same priority',
                'type': 'interactive',
                'params': [
                    {
                        'name': 'time_quantum',
                        'type': 'int',
                        'default': 2,
                        'description': 'Maximum time slice allocated to each process'
                    }
                ]
            }
        ]