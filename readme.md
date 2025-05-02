# CPU Scheduling Algorithms Simulation

This project implements a comprehensive CPU scheduling algorithms simulation with both backend and frontend components. The simulation allows users to visualize and compare different CPU scheduling algorithms, understand their behavior, and analyze their performance metrics.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Project Structure](#project-structure)
5. [Scheduling Algorithms](#scheduling-algorithms)
6. [Classes and Functions](#classes-and-functions)
7. [Performance Metrics](#performance-metrics)
8. [Visualization](#visualization)
9. [Usage Instructions](#usage-instructions)
10. [Implementation Details](#implementation-details)

## Project Overview

This project simulates various CPU scheduling algorithms commonly studied in operating systems courses. It provides a visual and interactive way to understand how different scheduling algorithms work and how they affect the performance of a system.

The simulation allows users to:
- Generate random processes or load them from files
- Choose among different scheduling algorithms
- Visualize the execution of processes using Gantt charts
- Compare performance metrics across algorithms
- Step through the execution of algorithms to understand their behavior

## Features

- **Multiple Scheduling Algorithms**: FCFS, SJF, Priority, Round Robin, Priority Round Robin
- **Interactive Visualization**: Gantt charts and step-by-step execution
- **Performance Metrics**: Waiting time, turnaround time, response time, and CPU utilization
- **Process Generation**: Random process generation or loading from files
- **Comparison Tools**: Compare metrics across algorithms
- **Responsive UI**: User-friendly interface for interacting with the simulation

## System Architecture

The project follows a client-server architecture with a clear separation of concerns:

### Backend (Python)
- Process representation and management
- Scheduling algorithm implementations
- Performance metric calculations
- Simulation state tracking
- Data processing and validation

### Frontend (Vue.js)
- User interface for controlling the simulation
- Visualization of scheduling algorithms
- Display of performance metrics
- Interactive components for process management
- Algorithm comparison tools

## Project Structure

The project is organized into backend and frontend directories:

### Backend Structure
```
backend/
├── requirements.txt            # Python dependencies
└── src/                        # Source code directory
    ├── main.py                 # Main API endpoints and entry point
    ├── controllers/            # Controllers directory
    │   └── simulation_controller.py  # Manages simulation process
    ├── models/                 # Data models directory
    │   └── process.py          # Process representation
    ├── schedulers/             # Scheduling algorithms
    │   ├── scheduler.py        # Abstract base scheduler
    │   ├── fcfs_scheduler.py   # First-Come, First-Served
    │   ├── sjf_scheduler.py    # Shortest Job First
    │   ├── priority_scheduler.py  # Priority Scheduling
    │   ├── round_robin_scheduler.py  # Round Robin
    │   └── priority_rr_scheduler.py  # Priority Round Robin
    └── utils/                  # Utility functions
        └── process_generator.py  # Process generation functions
```

### Frontend Structure
```
frontend/
├── package.json               # NPM dependencies
├── babel.config.js            # Babel configuration
├── vue.config.js              # Vue configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── public/                    # Public assets
│   ├── index.html             # HTML entry point
│   └── favicon.ico            # Website favicon
└── src/                       # Source code directory
    ├── main.js                # Vue application entry point
    ├── App.vue                # Main application component
    ├── assets/                # Static assets
    │   ├── logo.png           # Application logo
    │   └── tailwind.css       # Tailwind CSS styles
    ├── components/            # Reusable Vue components
    │   ├── AlgorithmSelector.vue  # Algorithm selection component
    │   ├── GanttChart.vue     # Gantt chart visualization
    │   ├── ProcessTable.vue   # Process data table
    │   ├── PerformanceMetrics.vue  # Metrics display
    │   └── InteractiveVisualizer.vue  # Step-by-step visualization
    ├── router/                # Vue Router configuration
    │   └── index.js           # Routing definitions
    ├── services/              # External services
    │   └── api.js             # Backend API client
    └── views/                 # Application views/pages
        ├── HomeView.vue       # Home page
        ├── ProcessesView.vue  # Process management page
        ├── VisualizationView.vue  # Algorithm visualization page
        └── ComparisonView.vue  # Algorithm comparison page
```

## Scheduling Algorithms

The following scheduling algorithms are implemented:

### 1. First-Come, First-Served (FCFS)
- **Type**: Non-preemptive
- **Description**: Processes are executed in the order they arrive
- **Implementation**: `FCFSScheduler` class

### 2. Shortest Job First (SJF)
- **Type**: Non-preemptive
- **Description**: Processes with the shortest burst time are executed first
- **Implementation**: `SJFScheduler` class

### 3. Priority Scheduling
- **Type**: Non-preemptive
- **Description**: Processes with higher priority (lower value) are executed first
- **Implementation**: `PriorityScheduler` class

### 4. Round Robin (RR)
- **Type**: Preemptive
- **Description**: Processes are executed in a circular queue with a fixed time quantum
- **Implementation**: `RoundRobinScheduler` class
- **Parameters**: Time quantum (default: 2)

### 5. Priority with Round Robin (Priority RR)
- **Type**: Preemptive
- **Description**: Priority scheduling with Round Robin for processes of same priority
- **Implementation**: `PriorityRRScheduler` class
- **Parameters**: Time quantum (default: 2)

## Classes and Functions

### Core Classes

#### `Process` (`process.py`)
Represents a process with all relevant attributes and methods for scheduling.

**Attributes**:
- `process_id`: Unique identifier for the process
- `arrival_time`: Time at which the process arrives in the ready queue
- `burst_time`: Total CPU time required by the process
- `priority`: Priority of the process (lower value means higher priority)
- `remaining_time`: Remaining execution time
- `start_time`: Time when the process first starts execution
- `completion_time`: Time when the process completes execution
- `waiting_time`: Total time spent waiting in the ready queue
- `turnaround_time`: Total time from arrival to completion
- `response_time`: Time from arrival to first execution

**Methods**:
- `calculate_waiting_time()`: Calculate waiting time (Turnaround Time - Burst Time)
- `calculate_turnaround_time()`: Calculate turnaround time (Completion Time - Arrival Time)
- `calculate_response_time()`: Calculate response time (Start Time - Arrival Time)
- `reset()`: Reset process state for rerunning simulations
- `to_dict()`: Convert process to dictionary for JSON serialization

#### `Scheduler` (`scheduler.py`)
Abstract base class for all scheduling algorithms, providing common functionality.

**Attributes**:
- `processes`: List of processes to be scheduled
- `current_time`: Current simulation time
- `completion_order`: Order in which processes complete execution
- `gantt_chart`: Representation of the execution timeline
- `simulation_step`: Current step in the simulation
- `simulation_history`: History of simulation states

**Methods**:
- `set_processes(processes)`: Set the processes for scheduling
- `schedule()`: Abstract method for executing the scheduling algorithm
- `get_average_waiting_time()`: Calculate average waiting time
- `get_average_turnaround_time()`: Calculate average turnaround time
- `get_average_response_time()`: Calculate average response time
- `get_cpu_utilization()`: Calculate CPU utilization percentage
- `get_gantt_chart()`: Get the Gantt chart data
- `get_completion_order()`: Get the order of process completion
- `update_gantt_chart(process, start, end)`: Update the Gantt chart
- `get_performance_metrics()`: Get all performance metrics
- `get_simulation_state()`: Get the current state of the simulation
- `save_simulation_state()`: Save the current state to history
- `get_simulation_history()`: Get the complete simulation history

#### `SimulationController` (`simulation_controller.py`)
Controls the simulation process, manages processes and schedulers, and collects results.

**Attributes**:
- `scheduler`: The current scheduler algorithm
- `processes`: List of processes for the simulation
- `process_generator`: Generator for creating processes

**Methods**:
- `load_processes(source, params=None)`: Load processes from a file or generate random ones
- `set_scheduler(algorithm, params=None)`: Set the scheduler algorithm to use
- `run_simulation()`: Run the simulation with current scheduler and processes
- `get_performance_metrics()`: Get performance metrics from the simulation
- `get_visualization_data()`: Get data for visualization
- `get_available_algorithms()`: Get list of available scheduling algorithms

### Scheduler Implementations

#### `FCFSScheduler` (`fcfs_scheduler.py`)
Implements the First-Come, First-Served scheduling algorithm.

**Key Methods**:
- `schedule()`: Execute FCFS scheduling
- `_capture_queue_state(ready_queue)`: Track ready queue state
- `get_simulation_state()`: Get enhanced simulation state

#### `SJFScheduler` (`sjf_scheduler.py`)
Implements the Shortest Job First scheduling algorithm.

**Key Methods**:
- `schedule()`: Execute SJF scheduling
- `_capture_queue_state(ready_queue)`: Track ready queue state
- `get_simulation_state()`: Get enhanced simulation state

#### `PriorityScheduler` (`priority_scheduler.py`)
Implements the Priority scheduling algorithm.

**Key Methods**:
- `schedule()`: Execute Priority scheduling
- `_capture_queue_state(ready_queue)`: Track ready queue state
- `get_simulation_state()`: Get enhanced simulation state

#### `RoundRobinScheduler` (`round_robin_scheduler.py`)
Implements the Round Robin scheduling algorithm.

**Attributes**:
- `time_quantum`: Maximum time slice for each process execution

**Key Methods**:
- `set_time_quantum(quantum)`: Set the time quantum value
- `schedule()`: Execute Round Robin scheduling
- `_capture_queue_state(ready_queue)`: Track ready queue state
- `get_simulation_state()`: Get enhanced simulation state

#### `PriorityRRScheduler` (`priority_rr_scheduler.py`)
Implements the Priority Round Robin scheduling algorithm.

**Attributes**:
- `time_quantum`: Maximum time slice for each process execution
- `priority_queues_state`: State of queues for different priority levels

**Key Methods**:
- `set_time_quantum(quantum)`: Set the time quantum value
- `schedule()`: Execute Priority Round Robin scheduling
- `_process_new_arrivals(remaining_processes, priority_queues)`: Process newly arrived processes
- `_advance_to_next_arrival(remaining_processes)`: Advance time when no processes are ready
- `_execute_process(current_queue, priority, priority_queues)`: Execute a process for one time quantum
- `_capture_queue_state(priority_queues)`: Track priority queue states
- `_has_queue_state_changed(priority_queues)`: Check if queue state has changed
- `get_simulation_state()`: Get enhanced simulation state

### Support Classes

#### `ProcessGenerator` (`process_generator.py`)
Generates processes for the simulation, either randomly or from files.

**Methods**:
- `generate_random_processes(count, burst_range, arrival_range, priority_range)`: Create random processes
- `load_processes_from_file(filepath)`: Load processes from CSV or JSON files

## Performance Metrics

The simulation calculates the following performance metrics for each scheduling algorithm:

1. **Average Waiting Time**: Average time processes spend in the ready queue
   - Formula: `(Sum of Waiting Times) / (Number of Processes)`

2. **Average Turnaround Time**: Average time from arrival to completion
   - Formula: `(Sum of Turnaround Times) / (Number of Processes)`

3. **Average Response Time**: Average time from arrival to first execution
   - Formula: `(Sum of Response Times) / (Number of Processes)`

4. **CPU Utilization**: Percentage of time the CPU was busy
   - Formula: `(Sum of Burst Times) / (Total Execution Time) * 100`

## Visualization

The simulation provides the following visualization tools:

1. **Gantt Chart**: Visual representation of process execution timeline
   - Shows which process is executing at each time unit
   - Highlights CPU idle times
   - Displays process completion order

2. **Process Table**: Tabular view of all processes and their attributes
   - Process ID, Arrival Time, Burst Time, Priority
   - Completion Time, Turnaround Time, Waiting Time, Response Time

3. **Interactive Visualizer**: Step-by-step execution of scheduling algorithms
   - Displays the ready queue at each step
   - Shows the currently executing process
   - Updates performance metrics in real-time



## Usage Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the simulation:
   ```
   python src/main.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run serve
   ```

4. Access the web interface at `http://localhost:8080`

## Implementation Details

### Simulation Flow
1. User selects or generates processes
2. User chooses a scheduling algorithm and sets parameters
3. The simulation controller runs the selected algorithm
4. Results are calculated and displayed through the UI

### State Tracking
- The simulation maintains a history of states for step-by-step replay
- Each state includes ready queue information, current process, performance metrics

### Algorithm Comparison
- Users can run multiple algorithms on the same process set
- Performance metrics are displayed side by side for comparison
- Gantt charts can be compared to visualize execution differences

### File Formats
- **CSV**: Simple format with columns for Process ID, Arrival Time, Burst Time, and Priority
---

Project Created by: Youness Anouar, Abdeljalil Otman
Last Updated: May 1, 2025
