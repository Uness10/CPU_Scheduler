"""
Process module for CPU Scheduler Simulation.
Defines the Process class that represents a process in the operating system.
"""

class Process:
    """
    Represents a process with all relevant attributes and methods for scheduling.
    """
    
    def __init__(self, process_id, arrival_time, burst_time, priority=0):
        """
        Initialize a new Process instance.
        
        Args:
            process_id (int): Unique identifier for the process
            arrival_time (int): Time at which the process arrives in the ready queue
            burst_time (int): Total CPU time required by the process
            priority (int, optional): Priority of the process (lower value means higher priority). Defaults to 0.
        """
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Tracking execution
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        
        # Performance metrics
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
    
    def calculate_waiting_time(self):
        """
        Calculate the waiting time for this process.
        Waiting Time = Turnaround Time - Burst Time
        """
        if self.completion_time is not None:
            self.waiting_time = self.turnaround_time - self.burst_time
            return self.waiting_time
        return None
    
    def calculate_turnaround_time(self):
        """
        Calculate the turnaround time for this process.
        Turnaround Time = Completion Time - Arrival Time
        """
        if self.completion_time is not None:
            self.turnaround_time = self.completion_time - self.arrival_time
            return self.turnaround_time
        return None
    
    def calculate_response_time(self):
        """
        Calculate the response time for this process.
        Response Time = Start Time - Arrival Time
        """
        if self.start_time is not None:
            self.response_time = self.start_time - self.arrival_time
            return self.response_time
        return None
    
    def reset(self):
        """Reset the process to its initial state for rerunning simulations."""
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None
    
    def __str__(self):
        """String representation of the process."""
        return (f"Process {self.process_id}: arrival={self.arrival_time}, "
                f"burst={self.burst_time}, priority={self.priority}")
    
    def to_dict(self):
        """Convert the process to a dictionary for JSON serialization."""
        return {
            'process_id': self.process_id,
            'arrival_time': self.arrival_time,
            'burst_time': self.burst_time,
            'priority': self.priority,
            'remaining_time': self.remaining_time,
            'start_time': self.start_time,
            'completion_time': self.completion_time,
            'waiting_time': self.waiting_time,
            'turnaround_time': self.turnaround_time,
            'response_time': self.response_time
        }