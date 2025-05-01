<template>
  <div class="w-full max-w-full mx-auto px-4">
    <!-- Header with algorithm selection -->
    <div class="mb-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2">
          <h1 class="text-2xl font-bold">CPU Scheduler Visualization</h1>
          <p class="text-gray-600 mt-1">Visualize and compare different CPU scheduling algorithms</p>
          <div class="card p-4">
          <h3 class="text-lg font-medium mb-3">Visualization</h3>
          <div class="flex flex-col space-y-4">
            <div>
              <div class="text-sm text-gray-600 mb-2">Visualization Mode</div>
              <div class="inline-flex shadow-sm rounded-md w-full">
                <button 
                  @click="visualizationMode = 'basic'"
                  class="px-4 py-2 text-sm font-medium flex-1 rounded-l-md"
                  :class="visualizationMode === 'basic' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 border'"
                >
                  Basic
                </button>
                <button 
                  @click="visualizationMode = 'interactive'"
                  class="px-4 py-2 text-sm font-medium flex-1 rounded-r-md"
                  :class="visualizationMode === 'interactive' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50 border'"
                >
                  Interactive
                </button>
              </div>
            </div>
            
            <button
              @click="runSimulation"
              class="btn btn-primary w-full"
              :disabled="!canRunSimulation || loading"
            >
              <span v-if="loading" class="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
              {{ loading ? 'Running...' : 'Run Simulation' }}
            </button>
            
            <button
              @click="resetSimulation"
              class="btn btn-outline w-full"
              :disabled="loading"
            >
              Reset Results
            </button>
          </div>
        </div>
        </div>
        
        <div class="card p-4">
          <h3 class="text-lg font-medium mb-3">Algorithm Selection</h3>
          <AlgorithmSelector 
            @update="updateAlgorithm" 
            :selected-algorithm="algorithm.algorithm" 
            class="w-full"
          />
        </div>
      </div>
    </div>
    
    <!-- Main content area (now using full width) -->
    <div class="w-full">
      <!-- Loading indicator -->
      <div v-if="loading" class="card flex flex-col items-center justify-center py-12">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
        <p class="mt-4 text-gray-600">Running simulation...</p>
      </div>

      <!-- Error display -->
      <div v-else-if="error" class="card bg-red-50 border border-red-200 p-4">
        <h3 class="text-lg font-medium text-red-800 mb-2">Error</h3>
        <p class="text-red-700">{{ error }}</p>
        <button @click="resetSimulation" class="mt-4 btn btn-outline border-red-300 text-red-700 hover:bg-red-50">Try Again</button>
      </div>

      <!-- Basic Visualization -->
      <template v-else-if="visualizationMode === 'basic'">
        <div v-if="timeline.length > 0" class="space-y-6">
          <div class="card p-4">
            <GanttChart :timeline="timeline" />
          </div>
          
          <div class="card p-4" v-if="metrics">
            <PerformanceMetrics :metrics="metrics" />
          </div>
        </div>
        
        <div class="card text-center p-12 text-gray-500" v-else>
          <div class="mb-4">
            <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <p class="mb-4">Select an algorithm and run the simulation to visualize the scheduling process.</p>
          <button
            @click="runSimulation"
            class="btn btn-primary"
            :disabled="!canRunSimulation || loading"
          >
            Run Simulation
          </button>
        </div>
      </template>

      <!-- Interactive Visualization -->
      <template v-else-if="visualizationMode === 'interactive'">
        <div class="card p-4">
          <InteractiveVisualizer 
            :processes="processes" 
            :algorithm="algorithm.algorithm"
            :params="algorithm.params"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import AlgorithmSelector from '@/components/AlgorithmSelector.vue';
import GanttChart from '@/components/GanttChart.vue';
import PerformanceMetrics from '@/components/PerformanceMetrics.vue';
import InteractiveVisualizer from '@/components/InteractiveVisualizer.vue';
import api from '@/services/api';

export default {
  name: 'VisualizationView',
  components: {
    AlgorithmSelector,
    GanttChart,
    PerformanceMetrics,
    InteractiveVisualizer
  },
  data() {
    return {
      processes: [],
      algorithm: {
        algorithm: 'FCFS',
        params: {
          timeQuantum: 2
        }
      },
      timeline: [],
      metrics: null,
      error: null,
      loading: false,
      visualizationMode: 'basic'  // 'basic' or 'interactive'
    };
  },
  computed: {
    canRunSimulation() {
      return this.processes.length > 0 && !this.loading;
    }
  },
  methods: {
    updateAlgorithm(algorithmData) {
      this.algorithm = algorithmData;
      this.resetResults();
    },
    
    async runSimulation() {
      if (this.visualizationMode === 'basic') {
        await this.runBasicSimulation();
      } else {
        // The interactive simulation is handled by the InteractiveVisualizer component
      }
    },
    
    async runBasicSimulation() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.runSimulation(
          this.algorithm.algorithm,
          this.algorithm.params,
          this.processes
        );
        
        // Extract data from the response structure
        const perfMetrics = response.data.performance_metrics || {};
        const visData = response.data.visualization_data || {};
        
        // Process the timeline data for the Gantt chart
        this.timeline = visData.gantt_chart || [];
        
        // Generate process metrics if not explicitly provided in the API
        const processMetrics = [];
        for (const process of this.processes) {
          const completedProcess = (visData.completion_order || []).find(p => p.process_id === process.process_id);
          if (completedProcess) {
            processMetrics.push({
              process_id: process.process_id,
              completion_time: completedProcess.completion_time,
              turnaround_time: completedProcess.turnaround_time,
              waiting_time: completedProcess.waiting_time
            });
          }
        }
        
        // Set the metrics data using the correct fields
        this.metrics = {
          avg_waiting_time: perfMetrics.average_waiting_time || 0,
          avg_turnaround_time: perfMetrics.average_turnaround_time || 0,
          avg_response_time: perfMetrics.average_response_time || 0,
          cpu_utilization: perfMetrics.cpu_utilization || 0,
          throughput: (this.processes.length / (visData.total_time || 1)) || 0,
          total_time: visData.total_time || 0,
          process_metrics: processMetrics
        };
        
      } catch (error) {
        this.error = `Error running simulation: ${error.response?.data?.error || error.message}`;
        console.error('Error running simulation:', error);
      } finally {
        this.loading = false;
      }
    },
    
    resetSimulation() {
      this.resetResults();
    },
    
    resetResults() {
      this.timeline = [];
      this.metrics = null;
      this.error = null;
    },
    

    
    getProcessColor(processId) {
      // Generate a deterministic color based on process ID
      const colors = [
        '#4299E1', // blue-500
        '#48BB78', // green-500
        '#ED8936', // orange-500
        '#9F7AEA', // purple-500
        '#F56565', // red-500
        '#38B2AC', // teal-500
        '#ECC94B', // yellow-500
        '#667EEA', // indigo-500
        '#ED64A6', // pink-500
        '#A0AEC0'  // gray-500
      ];
      
      return colors[processId % colors.length];
    },
    
    getProcessColorLight(processId) {
      // Generate lighter background colors for process cards
      const colors = [
        '#EBF8FF', // blue-100
        '#F0FFF4', // green-100
        '#FFFAF0', // orange-100
        '#FAF5FF', // purple-100
        '#FFF5F5', // red-100
        '#E6FFFA', // teal-100
        '#FFFFF0', // yellow-100
        '#EBF4FF', // indigo-100
        '#FFF5F7', // pink-100
        '#F7FAFC'  // gray-100
      ];
      
      return colors[processId % colors.length];
    }
  },
  created() {
    // Load processes from localStorage if available
    const savedProcesses = localStorage.getItem('cpu_scheduler_processes');
    if (savedProcesses) {
      try {
        this.processes = JSON.parse(savedProcesses);
      } catch (e) {
        console.error('Error loading saved processes:', e);
      }
    }
    

  }
};
</script>

<style scoped>
.btn {
  @apply inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.btn-outline {
  @apply bg-white text-gray-700 border-gray-300 hover:bg-gray-50;
}

.card {
  @apply bg-white shadow rounded-lg p-4;
}
</style>