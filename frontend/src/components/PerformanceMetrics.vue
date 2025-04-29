<template>
  <div class="card">
    <h3 class="text-lg font-medium mb-4">Performance Metrics</h3>
    
    <!-- Debug Info - will help identify if metrics are being received correctly -->
    <div v-if="metrics" class="mb-4 p-2 bg-yellow-50 border border-yellow-200 rounded-md text-xs">
      Data received: {{ dataReceived ? 'Yes' : 'No' }} | 
      Process metrics length: {{ metrics.process_metrics ? metrics.process_metrics.length : 0 }}
    </div>
    
    <div v-if="metrics" class="grid grid-cols-2 md:grid-cols-3 gap-4">
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700">Average Turnaround Time</h4>
        <p class="text-xl font-bold text-blue-600">{{ metrics.avg_turnaround_time.toFixed(2) }}</p>
      </div>
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700">Average Waiting Time</h4>
        <p class="text-xl font-bold text-blue-600">{{ metrics.avg_waiting_time.toFixed(2) }}</p>
      </div>
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700">CPU Utilization</h4>
        <p class="text-xl font-bold text-blue-600">{{ metrics.cpu_utilization.toFixed(2) }}%</p>
      </div>
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700">Throughput</h4>
        <p class="text-xl font-bold text-blue-600">{{ metrics.throughput.toFixed(4) }} processes/unit time</p>
      </div>
      <div class="bg-gray-50 p-4 rounded-lg">
        <h4 class="text-sm font-medium text-gray-700">Total Time</h4>
        <p class="text-xl font-bold text-blue-600">{{ metrics.total_time }}</p>
      </div>
    </div>
    
    <!-- Chart Visualization with explicit sizing -->
    <div v-if="metrics && metrics.process_metrics && metrics.process_metrics.length > 0" class="mt-6">
      <h4 class="text-md font-medium mb-3">Metrics Visualization</h4>
      <div style="height: 300px; position: relative;" class="border border-gray-200 rounded-md p-2">
        <Bar
          v-if="chartDataReady"
          :data="chartData"
          :options="chartOptions"
        />
      </div>
    </div>
    
    <div v-if="metrics && metrics.process_metrics" class="mt-6">
      <h4 class="text-md font-medium mb-3">Process Details</h4>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Process ID</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Completion Time</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Turnaround Time</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Waiting Time</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="process in metrics.process_metrics" :key="process.process_id">
              <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ process.process_id }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ process.completion_time }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ process.turnaround_time }}
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                {{ process.waiting_time }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-if="!metrics" class="text-center py-8 text-gray-500">
      Run a simulation to see the performance metrics.
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

// Register Chart.js components - ensure this happens
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'PerformanceMetrics',
  components: {
    Bar
  },
  props: {
    metrics: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      dataReceived: false,
      chartDataReady: false
    }
  },
  computed: {
    chartData() {
      if (!this.metrics || !this.metrics.process_metrics || this.metrics.process_metrics.length === 0) {
        return {
          labels: [],
          datasets: []
        }
      }

      // Sort processes by ID for consistent display
      const sortedProcesses = [...this.metrics.process_metrics].sort((a, b) => a.process_id - b.process_id);
      
      return {
        labels: sortedProcesses.map(p => `Process ${p.process_id}`),
        datasets: [
          {
            label: 'Waiting Time',
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            data: sortedProcesses.map(p => p.waiting_time)
          },
          {
            label: 'Turnaround Time',
            backgroundColor: 'rgba(255, 99, 132, 0.7)',
            data: sortedProcesses.map(p => p.turnaround_time)
          },
          {
            label: 'Completion Time',
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
            data: sortedProcesses.map(p => p.completion_time)
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top'
          },
          title: {
            display: true,
            text: 'Process Metrics Comparison'
          }
        }
      }
    }
  },
  watch: {
    metrics: {
      handler(newVal) {
        this.dataReceived = !!newVal;
        
        // Use setTimeout to ensure the DOM is updated before rendering the chart
        if (newVal && newVal.process_metrics && newVal.process_metrics.length > 0) {
          setTimeout(() => {
            this.chartDataReady = true;
          }, 100);
        } else {
          this.chartDataReady = false;
        }
      },
      immediate: true
    }
  },
  mounted() {
    console.log('PerformanceMetrics component mounted', this.metrics);
  }
}
</script>