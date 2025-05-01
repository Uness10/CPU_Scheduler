<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">CPU Scheduler Visualization</h1>
    
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
        
        <AlgorithmSelector @update="updateAlgorithm" />

        <div class="card">
          <h3 class="text-lg font-medium mb-4">Actions</h3>
          <div class="flex space-x-3">
            <button
              @click="runSimulation"
              class="btn btn-primary flex-1"
              :disabled="!canRunSimulation || loading"
            >
              Run Simulation
            </button>
            <button
              @click="resetSimulation"
              class="btn btn-secondary flex-1"
            >
              Reset
            </button>
          </div>

          <div v-if="loading" class="mt-4 text-center text-gray-600">
            Running simulation...
          </div>
          
          <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-md">
            {{ error }}
          </div>
        </div>
      </div>
      
      <!-- Right column for visualization and results -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Visualization mode tabs -->
        <div class="border-b border-gray-200">
          <nav class="flex -mb-px">
            <button 
              @click="visualizationMode = 'basic'"
              class="px-4 py-2 font-medium text-sm border-b-2 transition-colors duration-150 ease-in-out"
              :class="visualizationMode === 'basic' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
            >
              Basic Visualization
            </button>
            <button 
              @click="visualizationMode = 'interactive'"
              class="ml-8 px-4 py-2 font-medium text-sm border-b-2 transition-colors duration-150 ease-in-out"
              :class="visualizationMode === 'interactive' 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
            >
              Interactive Visualization
            </button>
          </nav>
        </div>

        <!-- Basic visualization content -->
        <div v-if="visualizationMode === 'basic'">
          <div class="card">
            <GanttChart :timeline="timeline" />
          </div>
          
          <PerformanceMetrics :metrics="metrics" />
        </div>

        <!-- Interactive visualization content -->
        <div v-if="visualizationMode === 'interactive'">
          <InteractiveVisualizer 
            :processes="processes" 
            :algorithm="algorithm.algorithm"
            :params="algorithm.params"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProcessTable from '@/components/ProcessTable.vue';
import AlgorithmSelector from '@/components/AlgorithmSelector.vue';
import GanttChart from '@/components/GanttChart.vue';
import PerformanceMetrics from '@/components/PerformanceMetrics.vue';
import InteractiveVisualizer from '@/components/InteractiveVisualizer.vue';
import api from '@/services/api';

export default {
  name: 'VisualizationView',
  components: {
    ProcessTable,
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
        params: {}
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
    updateProcesses(processes) {
      this.processes = processes;
      // Reset results when processes change
      this.resetResults();
    },
    updateAlgorithm(algorithmData) {
      this.algorithm = algorithmData;
      // Reset results when algorithm changes
      this.resetResults();
    },
    async generateRandomProcesses() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.generateProcesses();
        this.processes = response.data;
        
        // Reset results when new processes are generated
        this.resetResults();
      } catch (error) {
        this.error = `Error generating processes: ${error.response?.data?.error || error.message}`;
        console.error('Error generating processes:', error);
      } finally {
        this.loading = false;
      }
    },
    async runSimulation() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.runSimulation(
          this.algorithm.algorithm,
          this.algorithm.params,
          this.processes
        );
        
        console.log('API response:', response.data);
        
        // Extract data from the correct response structure
        const perfMetrics = response.data.performance_metrics || {};
        const visData = response.data.visualization_data || {};
        
        // Process the timeline data for the Gantt chart from the gantt_chart field
        this.timeline = visData.gantt_chart || [];
        
        // Generate process metrics if not explicitly provided in the API
        const processMetrics = [];
        for (const process of this.processes) {
          // Find the matching completed process
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
        
        // Set the metrics data using the correct fields from performance_metrics
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
      this.processes = [];
      this.resetResults();
    },
    resetResults() {
      this.timeline = [];
      this.metrics = null;
      this.error = null;
    }
  },
  mounted() {
    // Load sample processes when component mounts
    this.generateRandomProcesses();
  }
}
</script>