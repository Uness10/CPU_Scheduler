<template>
  <div class="processes-view">
    <h1 class="text-2xl font-bold mb-6">Create Processes</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Process Creation Section -->
      <div class="lg:col-span-2">
        <div class="card mb-6">
          <h2 class="text-xl font-semibold mb-4">Process List</h2>
          <div class="mb-6 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
            <div class="flex gap-2">
              <button class="btn btn-primary" @click="addNewProcess">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Add Process
              </button>
              <button class="btn btn-outline" @click="generateRandomProcesses">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
                Generate Random
              </button>
            </div>
            <div class="flex gap-2">
              <button class="btn btn-outline" @click="importProcesses">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
                </svg>
                Import
              </button>
              <button class="btn btn-outline" @click="exportProcesses">
                <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                </svg>
                Export
              </button>
            </div>
          </div>

          <!-- Process Table -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th class="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Arrival Time</th>
                  <th class="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Burst Time</th>
                  <th class="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                  <th class="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Color</th>
                  <th class="px-4 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-if="processes.length === 0">
                  <td colspan="6" class="px-4 py-8 text-center text-gray-500">
                    No processes available. Add one or generate random processes.
                  </td>
                </tr>
                <tr v-for="(process, index) in processes" :key="process.process_id" class="hover:bg-gray-50">
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="font-medium">P{{ process.process_id }}</span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <input 
                      type="number" 
                      v-model.number="process.arrival_time" 
                      min="0" 
                      class="input-field"
                    />
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <input 
                      type="number" 
                      v-model.number="process.burst_time" 
                      min="1" 
                      class="input-field"
                    />
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <input 
                      type="number" 
                      v-model.number="process.priority" 
                      min="1" 
                      max="10" 
                      class="input-field"
                    />
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <div class="w-6 h-6 rounded" :style="{ backgroundColor: getProcessColor(process.process_id) }"></div>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap text-right">
                    <button 
                      @click="deleteProcess(index)" 
                      class="text-red-600 hover:text-red-800 transition focus:outline-none"
                      title="Delete process"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="mt-6 flex justify-between items-center">
            <span class="text-sm text-gray-500">{{ processes.length }} Processes</span>
            <div>
              <button 
                @click="resetProcesses" 
                class="btn btn-outline text-red-600 border-red-300 hover:bg-red-50"
              >
                Clear All
              </button>
            </div>
          </div>
        </div>

        <div class="card" v-if="processes.length > 0">
          <h2 class="text-xl font-semibold mb-4">Process Generation Settings</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-group">
              <label class="form-label" for="processCount">Process Count</label>
              <input
                id="processCount"
                type="number"
                v-model.number="generatorSettings.processCount"
                min="1"
                max="20"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label" for="maxArrivalTime">Maximum Arrival Time</label>
              <input
                id="maxArrivalTime"
                type="number"
                v-model.number="generatorSettings.maxArrivalTime"
                min="0"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label" for="minBurstTime">Minimum Burst Time</label>
              <input
                id="minBurstTime"
                type="number"
                v-model.number="generatorSettings.minBurstTime"
                min="1"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label" for="maxBurstTime">Maximum Burst Time</label>
              <input
                id="maxBurstTime"
                type="number"
                v-model.number="generatorSettings.maxBurstTime"
                min="1"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label" for="minPriority">Minimum Priority</label>
              <input
                id="minPriority"
                type="number"
                v-model.number="generatorSettings.minPriority"
                min="1"
                class="form-input"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label" for="maxPriority">Maximum Priority</label>
              <input
                id="maxPriority"
                type="number"
                v-model.number="generatorSettings.maxPriority"
                min="1"
                class="form-input"
              />
            </div>
          </div>
          
          <div class="mt-6">
            <button class="btn btn-primary" @click="generateCustomProcesses">
              Generate with These Settings
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Process Preview Card -->
        <div class="card">
          <h2 class="text-lg font-semibold mb-4">Process Preview</h2>
          <div class="space-y-2">
            <div v-for="process in processes.slice(0, 5)" :key="process.process_id" class="p-3 rounded-lg flex items-center gap-3" :style="{ backgroundColor: getProcessColorLight(process.process_id) }">
              <div class="w-8 h-8 rounded-full flex items-center justify-center font-medium text-white" :style="{ backgroundColor: getProcessColor(process.process_id) }">
                {{ process.process_id }}
              </div>
              <div>
                <div class="text-sm font-medium">Process {{ process.process_id }}</div>
                <div class="text-xs text-gray-600">
                  Arrival: {{ process.arrival_time }} | Burst: {{ process.burst_time }} | Priority: {{ process.priority }}
                </div>
              </div>
            </div>
            <div v-if="processes.length > 5" class="text-center text-sm text-gray-500 pt-2">
              + {{ processes.length - 5 }} more processes
            </div>
            <div v-if="processes.length === 0" class="text-center text-gray-500 py-6">
              No processes to preview
            </div>
          </div>
        </div>

        <!-- Actions Card -->
        <div class="card bg-blue-50">
          <h3 class="text-lg font-semibold mb-4">Next Steps</h3>
          <p class="text-sm text-gray-600 mb-4">
            Once you've created your processes, you can visualize how they'll be scheduled using different algorithms.
          </p>
          <router-link to="/visualization" class="btn btn-primary w-full">
            View Visualization
          </router-link>
        </div>

        <!-- Help Card -->
        <div class="card">
          <h3 class="text-lg font-semibold mb-4">Understanding Process Parameters</h3>
          
          <div class="space-y-4">
            <div>
              <h4 class="font-medium text-gray-800">Arrival Time</h4>
              <p class="text-sm text-gray-600">When the process arrives and becomes ready for execution.</p>
            </div>
            
            <div>
              <h4 class="font-medium text-gray-800">Burst Time</h4>
              <p class="text-sm text-gray-600">The total CPU time required by the process to complete execution.</p>
            </div>
            
            <div>
              <h4 class="font-medium text-gray-800">Priority</h4>
              <p class="text-sm text-gray-600">Used by priority-based schedulers. Lower values typically indicate higher priority.</p>
            </div>
          </div>
          
          <div class="mt-4">
            <router-link to="/about" class="text-blue-600 hover:underline text-sm flex items-center">
              <span>Learn more about scheduling algorithms</span>
              <svg class="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
              </svg>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- File Input (hidden) -->
    <input
      type="file"
      ref="fileInput"
      accept=".json"
      style="display: none"
      @change="handleFileImport"
    />
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/services/api';

export default {
  name: 'ProcessesView',
  data() {
    return {
      processes: [],
      loading: false,
      error: null,
      generatorSettings: {
        processCount: 5,
        maxArrivalTime: 10,
        minBurstTime: 1,
        maxBurstTime: 10,
        minPriority: 1,
        maxPriority: 10
      }
    };
  },
  methods: {
    addNewProcess() {
      const newId = this.processes.length > 0 
        ? Math.max(...this.processes.map(p => p.process_id)) + 1 
        : 1;
        
      this.processes.push({
        process_id: newId,
        arrival_time: 0,
        burst_time: 5,
        priority: 1,
        remaining_time: 5  // Same as burst_time initially
      });
      
      // Save to localStorage
      this.saveProcesses();
    },
    
    deleteProcess(index) {
      this.processes.splice(index, 1);
      this.saveProcesses();
    },
    
    resetProcesses() {
      if (confirm('Are you sure you want to clear all processes?')) {
        this.processes = [];
        this.saveProcesses();
      }
    },
    
    async generateRandomProcesses() {
      try {
        this.loading = true;
        this.error = null;
        
        const response = await api.generateProcesses();
        this.processes = response.data;
        
        this.saveProcesses();
      } catch (error) {
        this.error = `Error generating processes: ${error.response?.data?.error || error.message}`;
        console.error('Error generating processes:', error);
      } finally {
        this.loading = false;
      }
    },
    
    generateCustomProcesses() {
      const { processCount, maxArrivalTime, minBurstTime, maxBurstTime, minPriority, maxPriority } = this.generatorSettings;
      
      // Generate new processes based on settings
      const newProcesses = [];
      for (let i = 1; i <= processCount; i++) {
        const burstTime = Math.floor(Math.random() * (maxBurstTime - minBurstTime + 1)) + minBurstTime;
        newProcesses.push({
          process_id: i,
          arrival_time: Math.floor(Math.random() * (maxArrivalTime + 1)),
          burst_time: burstTime,
          priority: Math.floor(Math.random() * (maxPriority - minPriority + 1)) + minPriority,
          remaining_time: burstTime // Same as burst_time initially
        });
      }
      
      this.processes = newProcesses;
      this.saveProcesses();
    },
    
    importProcesses() {
      this.$refs.fileInput.click();
    },
    
    handleFileImport(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedProcesses = JSON.parse(e.target.result);
          if (Array.isArray(importedProcesses)) {
            this.processes = importedProcesses;
            this.saveProcesses();
          } else {
            alert('Invalid process data format. Expected an array.');
          }
        } catch (error) {
          alert('Error parsing JSON file: ' + error.message);
        }
        // Reset file input
        event.target.value = '';
      };
      reader.readAsText(file);
    },
    
    exportProcesses() {
      if (this.processes.length === 0) {
        alert('No processes to export.');
        return;
      }
      
      const data = JSON.stringify(this.processes, null, 2);
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = 'processes.json';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    saveProcesses() {
      localStorage.setItem('cpu_scheduler_processes', JSON.stringify(this.processes));
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
  mounted() {
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
  @apply bg-white shadow rounded-lg p-6;
}

.input-field {
  @apply block w-24 text-sm border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500;
}

.form-group {
  @apply flex flex-col;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-input {
  @apply block w-full text-sm border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500;
}
</style>