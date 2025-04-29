import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Service for making API calls to the CPU Scheduler Simulation backend
 */
export default {
  /**
   * Get a list of available scheduling algorithms
   * @returns {Promise} Promise object with algorithm data
   */
  getAlgorithms() {
    return axios.get(`${API_BASE_URL}/algorithms`);
  },

  /**
   * Generate random processes based on parameters
   * @param {Object} params - Parameters for random process generation
   * @returns {Promise} Promise object with generated processes
   */
  generateProcesses(params = {}) {
    const defaultParams = {
      count: 5,
      min_arrival_time: 0,
      max_arrival_time: 10,
      min_burst_time: 1,
      max_burst_time: 10,
      min_priority: 1,
      max_priority: 10
    };
    
    return axios.post(`${API_BASE_URL}/generate-processes`, { ...defaultParams, ...params });
  },

  /**
   * Upload a file with process data
   * @param {File} file - The file containing process data
   * @returns {Promise} Promise object with parsed processes
   */
  uploadProcessFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return axios.post(`${API_BASE_URL}/upload-processes`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  /**
   * Run a simulation with specific algorithm and processes
   * @param {string} algorithm - The algorithm ID to use
   * @param {Object} params - Algorithm-specific parameters (e.g., time_quantum)
   * @param {Array} processes - Array of process objects
   * @returns {Promise} Promise object with simulation results
   */
  runSimulation(algorithm, params, processes) {
    let data = axios.post(`${API_BASE_URL}/run-simulation`, {
        algorithm,
        params,
        processes
      });
    console.log(data);
    
    return data
  },

  /**
   * Compare performance of all scheduling algorithms with the same processes
   * @param {Array} processes - Array of process objects
   * @returns {Promise} Promise object with comparison results
   */
  compareAlgorithms(processes) {
    return axios.post(`${API_BASE_URL}/performance-comparison`, {
      processes
    });
  }
}