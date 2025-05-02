"""
ProcessGenerator module for CPU Scheduler Simulation.
Provides functionality to generate and manage process data.
"""

import random
import csv
import json
from models.process import Process

class ProcessGenerator:
    """
    Handles creating sets of processes for scheduling simulations.
    Can generate random processes or load them from files.
    """
    
    @staticmethod
    def generate_random_processes(count, burst_range=(1, 10), arrival_range=(0, 20), priority_range=(1, 10)):
        """
        Generate a list of random processes for simulation.
        
        Args:
            count (int): Number of processes to generate
            burst_range (tuple): Range of burst times (min, max)
            arrival_range (tuple): Range of arrival times (min, max)
            priority_range (tuple): Range of priorities (min, max)
            
        Returns:
            list: List of Process objects
        """
        processes = []
        for i in range(count):
            process_id = i + 1
            arrival_time = random.randint(arrival_range[0], arrival_range[1])
            burst_time = random.randint(burst_range[0], burst_range[1])
            priority = random.randint(priority_range[0], priority_range[1])
            
            processes.append(Process(process_id, arrival_time, burst_time, priority))
        
        # Sort processes by arrival time (this is just for cleaner display)
        processes.sort(key=lambda p: p.arrival_time)
        
        # Re-assign process IDs to match the sorted order
        for i, process in enumerate(processes):
            process.process_id = i + 1
            
        return processes
    
    @staticmethod
    def load_processes_from_file(filename):
        """
        Load processes from a file (supports CSV and JSON).
        
        Args:
            filename (str): Path to the file containing process data
            
        Returns:
            list: List of Process objects
        """
        processes = []
        file_extension = filename.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                with open(filename, 'r') as file:
                    reader = csv.DictReader(file)
                    
                    # Map field names to standardized names
                    field_mapping = {
                        'process_id': ['process_id', 'pid', 'id', 'process id', 'process_number', 'process-id'],
                        'arrival_time': ['arrival_time', 'arrival', 'arrival-time', 'at', 'arrival time', 'start'],
                        'burst_time': ['burst_time', 'burst', 'burst-time', 'bt', 'burst time', 'cpu time', 'execution_time', 'execution time'],
                        'priority': ['priority', 'prio', 'pri', 'priority_value', 'priority-value']
                    }
                    
                    # Create a mapping for the actual CSV columns to our standardized names
                    column_map = {}
                    headers = reader.fieldnames
                    
                    for std_field, possible_names in field_mapping.items():
                        for header in headers:
                            clean_header = header.strip().lower()
                            if clean_header in [name.lower() for name in possible_names]:
                                column_map[header] = std_field
                                break
                    
                    # Reset file pointer to read data with new mapping
                    file.seek(0)
                    # Skip header line
                    next(file)
                    
                    for i, row in enumerate(csv.DictReader(file, fieldnames=headers)):
                        # Extract values using the column mapping
                        process_id = i + 1  # Default value
                        arrival_time = 0    # Default value
                        burst_time = 1      # Default value
                        priority = 1        # Default value
                        
                        for header, value in row.items():
                            if header in column_map:
                                if column_map[header] == 'process_id' and value.strip():
                                    process_id = int(value)
                                elif column_map[header] == 'arrival_time' and value.strip():
                                    arrival_time = int(value)
                                elif column_map[header] == 'burst_time' and value.strip():
                                    burst_time = int(value)
                                elif column_map[header] == 'priority' and value.strip():
                                    priority = int(value)
                        
                        processes.append(Process(process_id, arrival_time, burst_time, priority))
            
            elif file_extension == 'json':
                with open(filename, 'r') as file:
                    data = json.load(file)
                    for i, proc_data in enumerate(data):
                        process_id = int(proc_data.get('process_id', i + 1))
                        arrival_time = int(proc_data.get('arrival_time', 0))
                        burst_time = int(proc_data.get('burst_time', 1))
                        priority = int(proc_data.get('priority', 0))
                        
                        processes.append(Process(process_id, arrival_time, burst_time, priority))
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
            # Sort processes by arrival time
            processes.sort(key=lambda p: p.arrival_time)
            
        except Exception as e:
            print(f"Error loading processes from file: {e}")
            return []
            
        return processes
    
    @staticmethod
    def save_processes_to_file(processes, filename):
        """
        Save a list of processes to a file (CSV or JSON).
        
        Args:
            processes (list): List of Process objects
            filename (str): Output file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_extension = filename.split('.')[-1].lower()
            
            if file_extension == 'csv':
                with open(filename, 'w', newline='') as file:
                    fieldnames = ['process_id', 'arrival_time', 'burst_time', 'priority']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for process in processes:
                        writer.writerow({
                            'process_id': process.process_id,
                            'arrival_time': process.arrival_time,
                            'burst_time': process.burst_time,
                            'priority': process.priority
                        })
                        
            elif file_extension == 'json':
                process_data = []
                for process in processes:
                    process_data.append({
                        'process_id': process.process_id,
                        'arrival_time': process.arrival_time,
                        'burst_time': process.burst_time,
                        'priority': process.priority
                    })
                    
                with open(filename, 'w') as file:
                    json.dump(process_data, file, indent=4)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
            return True
            
        except Exception as e:
            print(f"Error saving processes to file: {e}")
            return False