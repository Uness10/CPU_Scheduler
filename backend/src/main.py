"""
API Endpoints for the CPU Scheduler Simulation.
Provides REST API endpoints for frontend integration.
"""
import os
import json
import tempfile
from models.process import Process
from utils.process_generator import ProcessGenerator
from controllers.simulation_controller import SimulationController

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create a simulation controller instance
controller = SimulationController()

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Return a list of available scheduling algorithms."""
    return jsonify(controller.get_available_algorithms())

@app.route('/api/generate-processes', methods=['POST'])
def generate_processes():
    """Generate random processes based on the provided parameters."""
    try:
        params = request.json
        processes = controller.load_processes('random', params)
        return jsonify([p.to_dict() for p in processes])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/upload-processes', methods=['POST'])
def upload_processes_file():
    """Handle uploaded process data file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Save the uploaded file to a temporary location
        _, temp_path = tempfile.mkstemp(suffix=os.path.splitext(file.filename)[1])
        file.save(temp_path)
        
        # Load processes from the file
        processes = controller.load_processes(temp_path)
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return jsonify([p.to_dict() for p in processes])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    """Run a simulation with the specified algorithm and processes."""
    try:
        data = request.json
        algorithm = data.get('algorithm')
        processes_data = data.get('processes')
        params = data.get('params', {})
        interactive = data.get('interactive', False)  # New parameter for interactive mode
        
        if not algorithm:
            return jsonify({'error': 'No algorithm specified'}), 400
            
        # Set the scheduler based on the algorithm
        controller.set_scheduler(algorithm, params)
        
        # If processes are provided, use them
        if processes_data:
            processes = []
            for p_data in processes_data:
                process = Process(
                    p_data.get('process_id'),
                    p_data.get('arrival_time'),
                    p_data.get('burst_time'),
                    p_data.get('priority', 0)
                )
                processes.append(process)
            
            controller.processes = processes
        
        # Run the simulation
        result = controller.run_simulation()
        
        # If interactive mode is requested, include the simulation history
        if interactive:
            # Add the simulation history to the result
            if hasattr(controller.scheduler, 'get_simulation_history'):
                result['simulation_history'] = controller.scheduler.get_simulation_history()
                
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/performance-comparison', methods=['POST'])
def get_performance_comparison():
    """Compare performance of all algorithms using the same set of processes."""
    try:
        processes_data = request.json.get('processes')
        if not processes_data:
            return jsonify({'error': 'No processes provided'}), 400
            
        # Convert JSON data to Process objects
        processes = []
        for p_data in processes_data:
            process = Process(
                p_data.get('process_id'),
                p_data.get('arrival_time'),
                p_data.get('burst_time'),
                p_data.get('priority', 0)
            )
            processes.append(process)
        
        # Get all available algorithms
        algorithms = controller.get_available_algorithms()
        
        # Run simulation for each algorithm
        results = []
        for algo_info in algorithms:
            algo_id = algo_info['id']
            
            # Set parameters for algorithms that need them
            params = {}
            if algo_id in ['RR', 'PriorityRR']:
                params = {'time_quantum': 2}  # Default time quantum
                
            # Set the scheduler and run simulation
            controller.processes = processes.copy()  # Use a copy to avoid modifying the original
            controller.set_scheduler(algo_id, params)
            result = controller.run_simulation()
            
            # Add algorithm info to the result
            result['algorithm'] = algo_info
            results.append(result)
            
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/interactive-simulation', methods=['POST'])
def get_interactive_simulation():
    """
    Get detailed simulation history for interactive visualization.
    Returns the entire simulation history with state information at each step.
    """
    try:
        data = request.json
        algorithm = data.get('algorithm')
        processes_data = data.get('processes')
        params = data.get('params', {})
        
        if not algorithm:
            return jsonify({'error': 'No algorithm specified'}), 400
            
        # Set the scheduler based on the algorithm
        controller.set_scheduler(algorithm, params)
        
        # If processes are provided, use them
        if processes_data:
            processes = []
            for p_data in processes_data:
                process = Process(
                    p_data.get('process_id'),
                    p_data.get('arrival_time'),
                    p_data.get('burst_time'),
                    p_data.get('priority', 0)
                )
                processes.append(process)
            
            controller.processes = processes
        
        # Run the simulation
        controller.run_simulation()
        
        # Get the simulation history with detailed state information
        simulation_history = []
        if hasattr(controller.scheduler, 'get_simulation_history'):
            simulation_history = controller.scheduler.get_simulation_history()
            
        # Get final performance metrics
        performance_metrics = controller.get_performance_metrics()
            
        return jsonify({
            'simulation_history': simulation_history,
            'performance_metrics': performance_metrics,
            'total_steps': len(simulation_history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)