<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Algorithm Comparison</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left column for controls -->
      <div class="space-y-6">
        <div class="card">
          <h3 class="text-lg font-medium mb-4">Comparison Controls</h3>
          
          <div v-if="processes.length === 0" class="mb-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-700">
            <p>No processes available. Add processes in the Processes tab first.</p>
            <router-link to="/processes" class="btn btn-primary mt-3">
              Go to Process Creation
            </router-link>
          </div>
          
          <div v-else>
            <div class="mb-4">
              <label class="form-label" for="timeQuantum">Time Quantum for RR algorithms</label>
              <input
                id="timeQuantum"
                type="number"
                v-model.number="timeQuantum"
                min="1"
                class="form-input"
              />
              <p class="text-xs text-gray-500 mt-1">Note: Quantum value must be greater than or equal to 1</p>
            </div>
            
            <div class="mb-4">
              <label class="form-label">Processes to Compare</label>
              <div class="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                {{ processes.length }} processes loaded from your process list
              </div>
            </div>
            
            <div class="space-y-3">
              <button 
                @click="runComparison" 
                :disabled="!canRunComparison" 
                class="btn btn-primary w-full"
                :class="{'opacity-50 cursor-not-allowed': !canRunComparison}"
              >
                <span v-if="loading">Comparing...</span>
                <span v-else>Compare Algorithms</span>
              </button>
              
              <button 
                @click="resetComparisonResults" 
                class="btn btn-outline w-full"
                :disabled="comparisonResults.length === 0 || loading"
                :class="{'opacity-50 cursor-not-allowed': comparisonResults.length === 0 || loading}"
              >
                Clear Results
              </button>
            </div>
          </div>
          
          <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
            {{ error }}
          </div>
        </div>
        
        <div class="card" v-if="processes.length > 0">
          <h3 class="text-lg font-medium mb-4">Processes Preview</h3>
          <div class="max-h-96 overflow-y-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Arrival</th>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Burst</th>
                  <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="process in processes.slice(0, 10)" :key="process.process_id" class="hover:bg-gray-50">
                  <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-900">{{ process.process_id }}</td>
                  <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500">{{ process.arrival_time }}</td>
                  <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500">{{ process.burst_time }}</td>
                  <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500">{{ process.priority }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="processes.length > 10" class="text-sm text-gray-500 text-center mt-2">
              + {{ processes.length - 10 }} more processes
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right column for comparison charts -->
      <div class="lg:col-span-2 space-y-6">
        <div class="card" v-if="comparisonResults.length > 0">
          <h3 class="text-lg font-medium mb-4">Average Wait Time Comparison</h3>
          <div class="h-80">
            <Bar
              :data="waitTimeChartData"
              :options="chartOptions"
            />
          </div>
        </div>
        
        <div class="card" v-if="comparisonResults.length > 0">
          <h3 class="text-lg font-medium mb-4">Average Turnaround Time Comparison</h3>
          <div class="h-80">
            <Bar
              :data="turnaroundTimeChartData"
              :options="chartOptions"
            />
          </div>
        </div>
        
        <div class="card" v-if="comparisonResults.length > 0">
          <h3 class="text-lg font-medium mb-4">CPU Utilization Comparison</h3>
          <div class="h-80">
            <Bar
              :data="cpuUtilizationChartData"
              :options="chartOptions"
            />
          </div>
        </div>
        
        <div class="card" v-if="comparisonResults.length > 0">
          <h3 class="text-lg font-medium mb-4">Detailed Comparison</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Algorithm</th>
                  <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg. Waiting Time</th>
                  <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg. Turnaround Time</th>
                  <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CPU Utilization</th>
                  <th class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Throughput</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="result in comparisonResults" :key="result.algorithm.id" class="hover:bg-gray-50">
                  <td class="px-3 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ result.algorithm.name }}
                  </td>
                  <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ result.avg_waiting_time.toFixed(2) }}
                  </td>
                  <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ result.avg_turnaround_time.toFixed(2) }}
                  </td>
                  <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ result.cpu_utilization.toFixed(2) }}%
                  </td>
                  <td class="px-3 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ result.throughput.toFixed(4) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-if="!comparisonResults.length" class="card">
          <div class="text-center py-12 text-gray-500">
            No comparison data available yet. Click "Compare Algorithms" to run the comparison.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import api from '@/services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ALGORITHM_COLORS = {
  'FCFS': 'rgba(54, 162, 235, 0.7)',     // Blue
  'SJF': 'rgba(75, 192, 192, 0.7)',      // Green
  'Priority': 'rgba(255, 159, 64, 0.7)', // Orange
  'RR': 'rgba(153, 102, 255, 0.7)',      // Purple
  'PriorityRR': 'rgba(255, 99, 132, 0.7)' // Red
};

export default {
  name: 'ComparisonView',
  components: {
    Bar
  },
  data() {
    return {
      processes: [],
      comparisonResults: [],
      timeQuantum: 2,
      error: null,
      loading: false,
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          legend: {
            display: false
          }
        }
      }
    };
  },
  computed: {
    canRunComparison() {
      return this.processes.length > 0 && !this.loading;
    },
    waitTimeChartData() {
      return {
        labels: this.comparisonResults.map(result => result.algorithm.name),
        datasets: [{
          label: 'Average Waiting Time',
          data: this.comparisonResults.map(result => result.avg_waiting_time),
          backgroundColor: this.comparisonResults.map(result => ALGORITHM_COLORS[result.algorithm.id]),
          borderWidth: 1
        }]
      };
    },
    turnaroundTimeChartData() {
      return {
        labels: this.comparisonResults.map(result => result.algorithm.name),
        datasets: [{
          label: 'Average Turnaround Time',
          data: this.comparisonResults.map(result => result.avg_turnaround_time),
          backgroundColor: this.comparisonResults.map(result => ALGORITHM_COLORS[result.algorithm.id]),
          borderWidth: 1
        }]
      };
    },
    cpuUtilizationChartData() {
      return {
        labels: this.comparisonResults.map(result => result.algorithm.name),
        datasets: [{
          label: 'CPU Utilization (%)',
          data: this.comparisonResults.map(result => result.cpu_utilization),
          backgroundColor: this.comparisonResults.map(result => ALGORITHM_COLORS[result.algorithm.id]),
          borderWidth: 1
        }]
      };
    }
  },
  methods: {
    loadProcessesFromLocalStorage() {
      const savedProcesses = localStorage.getItem('cpu_scheduler_processes');
      if (savedProcesses) {
        try {
          this.processes = JSON.parse(savedProcesses);
        } catch (e) {
          console.error('Error loading saved processes:', e);
          this.processes = []; 
        }
      } else {
        this.processes = [];
      }
    },

    async runComparison() {
      try {
        this.loading = true;
        this.error = null;
        
        // Prepare algorithms with their parameters
        const algorithms = [
          { id: 'FCFS', name: 'First-Come, First-Served' },
          { id: 'SJF', name: 'Shortest Job First' },
          { id: 'Priority', name: 'Priority Scheduling' },
          { 
            id: 'RR', 
            name: 'Round Robin',
            params: { time_quantum: this.timeQuantum }
          },
          { 
            id: 'PriorityRR', 
            name: 'Priority Round Robin',
            params: { time_quantum: this.timeQuantum }
          }
        ];
        
        // Run each algorithm and collect results
        this.comparisonResults = [];
        
        for (const algo of algorithms) {
          try {
            const params = algo.params || {};
            // Fix the parameter order: (algorithm, params, processes) instead of (processes, algorithm, params)
            const response = await api.runSimulation(algo.id, params, this.processes);
            
            // Access the performance metrics from the nested structure
            const perfMetrics = response.data.performance_metrics || {};
            
            // Add the result with algorithm info
            this.comparisonResults.push({
              algorithm: {
                id: algo.id,
                name: algo.name + (params.time_quantum ? ` (TQ=${params.time_quantum})` : '')
              },
              avg_waiting_time: perfMetrics.average_waiting_time || 0,
              avg_turnaround_time: perfMetrics.average_turnaround_time || 0,
              cpu_utilization: perfMetrics.cpu_utilization || 0, // Already in percentage
              throughput: perfMetrics.processes_completed / (perfMetrics.total_execution_time || 1) || 0
            });
          } catch (algoError) {
            console.error(`Error running ${algo.name}:`, algoError);
            // Continue with other algorithms if one fails
          }
        }
        
        // Sort by average waiting time (most efficient first)
        this.comparisonResults.sort((a, b) => a.avg_waiting_time - b.avg_waiting_time);
        
      } catch (error) {
        this.error = `Error running comparison: ${error.response?.data?.error || error.message}`;
        console.error('Error running comparison:', error);
      } finally {
        this.loading = false;
      }
    },
    
    resetComparison() {
      this.processes = [];
      this.resetComparisonResults();
    },
    
    resetComparisonResults() {
      this.comparisonResults = [];
      this.error = null;
    }
  },
  mounted() {
    this.loadProcessesFromLocalStorage();
  }
}
</script>