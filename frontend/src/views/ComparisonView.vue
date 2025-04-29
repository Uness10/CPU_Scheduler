<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">Algorithm Comparison</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left column for process management -->
      <div class="lg:col-span-1 space-y-6">
        <div class="card">
          <ProcessTable 
            :processes="processes" 
            @update="updateProcesses" 
            @generate="generateRandomProcesses"
          />
        </div>

        <div class="card">
          <h3 class="text-lg font-medium mb-4">Round Robin Time Quantum</h3>
          <div class="mb-4">
            <label for="quantum" class="form-label">Time Quantum</label>
            <input 
              id="quantum"
              type="number" 
              v-model.number="timeQuantum" 
              min="1"
              class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            />
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-medium mb-4">Actions</h3>
          <div class="flex space-x-3">
            <button 
              @click="runComparison" 
              class="btn btn-primary flex-1"
              :disabled="!canRunComparison || loading"
            >
              Compare Algorithms
            </button>
            <button 
              @click="resetComparison" 
              class="btn btn-secondary flex-1"
            >
              Reset
            </button>
          </div>
          
          <div v-if="loading" class="mt-4 text-center text-gray-600">
            Loading comparison data...
          </div>
          
          <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-md text-sm">
            {{ error }}
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
import ProcessTable from '@/components/ProcessTable.vue';
import api from '@/services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const CHART_COLORS = [
  'rgba(54, 162, 235, 0.7)',   // blue
  'rgba(75, 192, 192, 0.7)',   // green
  'rgba(255, 159, 64, 0.7)',   // orange
  'rgba(153, 102, 255, 0.7)',  // purple
  'rgba(255, 99, 132, 0.7)'    // red
];

export default {
  name: 'ComparisonView',
  components: {
    ProcessTable,
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
          backgroundColor: CHART_COLORS,
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
          backgroundColor: CHART_COLORS,
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
          backgroundColor: CHART_COLORS,
          borderWidth: 1
        }]
      };
    }
  },
  methods: {
    updateProcesses(processes) {
      this.processes = processes;
      // Reset comparison when processes change
      this.resetComparisonResults();
    },
    async generateRandomProcesses() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.generateProcesses();
        this.processes = response.data;
        
        // Reset comparison when new processes are generated
        this.resetComparisonResults();
      } catch (error) {
        this.error = `Error generating processes: ${error.response?.data?.error || error.message}`;
        console.error('Error generating processes:', error);
      } finally {
        this.loading = false;
      }
    },
    async runComparison() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.compareAlgorithms(this.processes);
        
        // Process response results
        this.comparisonResults = response.data.map(result => {
          // Apply time quantum configuration to RR and PriorityRR results
          if (result.algorithm.id === 'RR' || result.algorithm.id === 'PriorityRR') {
            // Update the algorithm name to include the time quantum
            result.algorithm.name += ` (TQ=${this.timeQuantum})`;
          }
          return result;
        });
        
        // Sort results by average waiting time for better visualization
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
    // Generate random processes when component mounts
    this.generateRandomProcesses();
  }
}
</script>