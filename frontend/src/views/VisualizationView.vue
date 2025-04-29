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
              <span v-if="loading">Running...</span>
              <span v-else>Run Simulation</span>
            </button>
            <button 
              @click="resetSimulation" 
              class="btn btn-secondary flex-1"
            >
              Reset
            </button>
          </div>
          
          <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded-md text-sm">
            {{ error }}
          </div>
        </div>
      </div>
      
      <!-- Right column for visualization and results -->
      <div class="lg:col-span-2 space-y-6">
        <div class="card">
          <GanttChart :timeline="timeline" />
        </div>
        
        <PerformanceMetrics :metrics="metrics" />
      </div>
    </div>
  </div>
</template>

<script>
import ProcessTable from '@/components/ProcessTable.vue';
import AlgorithmSelector from '@/components/AlgorithmSelector.vue';
import GanttChart from '@/components/GanttChart.vue';
import PerformanceMetrics from '@/components/PerformanceMetrics.vue';
import api from '@/services/api';

export default {
  name: 'VisualizationView',
  components: {
    ProcessTable,
    AlgorithmSelector,
    GanttChart,
    PerformanceMetrics
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
      loading: false
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
        this.timeline = visData.gantt_chart?.map(item => ({
          process_id: item.process_id,
          start_time: item.start_time,
          duration: item.end_time - item.start_time
        })) || [];
        
        // Generate process metrics if not explicitly provided in the API
        // This creates a process_metrics array with completion time, turnaround time, and waiting time for each process
        const processMetrics = [];
        if (this.processes && visData.gantt_chart) {
          // Create a map to track the latest end time for each process (completion time)
          const completionTimes = {};
          
          // Populate completion times
          visData.gantt_chart.forEach(item => {
            const pid = item.process_id;
            const endTime = item.end_time;
            
            // Update completion time if this is the latest end time for the process
            if (!completionTimes[pid] || endTime > completionTimes[pid]) {
              completionTimes[pid] = endTime;
            }
          });
          
          // Create process metrics for each process
          this.processes.forEach(process => {
            const pid = process.process_id;
            const arrivalTime = process.arrival_time;
            const burstTime = process.burst_time;
            const completionTime = completionTimes[pid] || 0;
            
            // Calculate metrics
            const turnaroundTime = completionTime - arrivalTime;
            const waitingTime = turnaroundTime - burstTime;
            
            processMetrics.push({
              process_id: pid,
              completion_time: completionTime,
              turnaround_time: turnaroundTime,
              waiting_time: waitingTime
            });
          });
        }
        
        // Set the metrics data using the correct fields from performance_metrics
        this.metrics = {
          avg_turnaround_time: perfMetrics.average_turnaround_time || 0,
          avg_waiting_time: perfMetrics.average_waiting_time || 0,
          cpu_utilization: perfMetrics.cpu_utilization || 0,
          throughput: perfMetrics.throughput || 0,
          total_time: visData.total_time || 0,
          // Use API-provided process_metrics if available, otherwise use our calculated metrics
          process_metrics: perfMetrics.process_metrics || processMetrics
        };
        
        console.log('Processed timeline:', this.timeline);
        console.log('Processed metrics:', this.metrics);
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