"""
Main entry point for the CPU Scheduler Simulation application.
"""

import os
import sys
import argparse
from simulation_controller import SimulationController
from process_generator import ProcessGenerator
from process import Process

def main():
    """
    Main entry point for the CPU scheduler simulation application.
    Provides a command-line interface for running simulations.
    """
    parser = argparse.ArgumentParser(description="CPU Scheduler Simulation")
    
    # Define command-line arguments
    parser.add_argument(
        "--algorithm", "-a",
        choices=["FCFS", "SJF", "Priority", "RR", "PriorityRR"],
        default="FCFS",
        help="Scheduling algorithm to use"
    )
    
    parser.add_argument(
        "--processes", "-p",
        choices=["random", "file"],
        default="random",
        help="Process source (random generation or from file)"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="Input file path (CSV or JSON) for processes"
    )
    
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=5,
        help="Number of random processes to generate"
    )
    
    parser.add_argument(
        "--burst-min",
        type=int,
        default=1,
        help="Minimum burst time for random processes"
    )
    
    parser.add_argument(
        "--burst-max",
        type=int,
        default=10,
        help="Maximum burst time for random processes"
    )
    
    parser.add_argument(
        "--arrival-min",
        type=int,
        default=0,
        help="Minimum arrival time for random processes"
    )
    
    parser.add_argument(
        "--arrival-max",
        type=int,
        default=10,
        help="Maximum arrival time for random processes"
    )
    
    parser.add_argument(
        "--priority-min",
        type=int,
        default=1,
        help="Minimum priority for random processes"
    )
    
    parser.add_argument(
        "--priority-max",
        type=int,
        default=5,
        help="Maximum priority for random processes"
    )
    
    parser.add_argument(
        "--time-quantum", "-q",
        type=int,
        default=2,
        help="Time quantum for RR and PriorityRR algorithms"
    )
    
    parser.add_argument(
        "--compare-all", "-ca",
        action="store_true",
        help="Compare all scheduling algorithms using the same processes"
    )
    
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Start the web server for frontend access"
    )

    # Parse arguments
    args = parser.parse_args()
    
    # Start web server if requested
    if args.web:
        from api_endpoints import app
        app.run(debug=True, port=5000)
        return
    
    # Initialize controller
    controller = SimulationController()
    
    # Load processes
    if args.processes == "file":
        if not args.file:
            print("Error: File path must be provided when using '--processes file'")
            return 1
        
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found")
            return 1
            
        processes = controller.load_processes(args.file)
    else:  # random generation
        processes = controller.load_processes("random", {
            "count": args.count,
            "burst_range": (args.burst_min, args.burst_max),
            "arrival_range": (args.arrival_min, args.arrival_max),
            "priority_range": (args.priority_min, args.priority_max)
        })
    
    # Print process information
    print("\nProcesses:")
    print(f"{'ID':^5} {'Arrival':^10} {'Burst':^10} {'Priority':^10}")
    print("-" * 40)
    for p in processes:
        print(f"{p.process_id:^5} {p.arrival_time:^10} {p.burst_time:^10} {p.priority:^10}")
    print()
    
    # Compare all algorithms if requested
    if args.compare_all:
        # Get all available algorithms
        algorithms = ["FCFS", "SJF", "Priority", "RR", "PriorityRR"]
        
        # Collect results
        results = []
        for algorithm in algorithms:
            params = {}
            if algorithm in ["RR", "PriorityRR"]:
                params = {"time_quantum": args.time_quantum}
                
            controller.set_scheduler(algorithm, params)
            controller.processes = processes.copy()  # Use a copy to avoid modification
            controller.run_simulation()
            metrics = controller.get_performance_metrics()
            metrics["algorithm"] = algorithm
            results.append(metrics)
        
        # Print comparison table
        print("\nAlgorithm Comparison:")
        print(f"{'Algorithm':^15} {'Avg Wait':^15} {'Avg Turn':^15} {'Avg Response':^15} {'CPU Util %':^15}")
        print("-" * 75)
        
        for r in results:
            print(
                f"{r['algorithm']:^15} "
                f"{r['average_waiting_time']:^15.2f} "
                f"{r['average_turnaround_time']:^15.2f} "
                f"{r['average_response_time']:^15.2f} "
                f"{r['cpu_utilization']:^15.2f}"
            )
    else:
        # Run single algorithm simulation
        params = {}
        if args.algorithm in ["RR", "PriorityRR"]:
            params = {"time_quantum": args.time_quantum}
            
        controller.set_scheduler(args.algorithm, params)
        controller.run_simulation()
        
        # Print Gantt chart
        print(f"\nGantt Chart ({args.algorithm}):")
        gantt = controller.scheduler.get_gantt_chart()
        print("-" * 50)
        for slot in gantt:
            pid = slot["process_id"] if slot["process_id"] is not None else "IDLE"
            print(f"| {pid:^4} ", end="")
        print("|")
        print("-" * 50)
        
        current_time = 0
        for slot in gantt:
            print(f"| {current_time:^4} ", end="")
            current_time = slot["end_time"]
        print(f"| {current_time:^4} |")
        print("-" * 50)
        
        # Print metrics
        metrics = controller.get_performance_metrics()
        print("\nPerformance Metrics:")
        print(f"Average Waiting Time: {metrics['average_waiting_time']:.2f}")
        print(f"Average Turnaround Time: {metrics['average_turnaround_time']:.2f}")
        print(f"Average Response Time: {metrics['average_response_time']:.2f}")
        print(f"CPU Utilization: {metrics['cpu_utilization']:.2f}%")
        print(f"Total Execution Time: {metrics['total_execution_time']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())