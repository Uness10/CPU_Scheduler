<template>
  <div class="interactive-visualizer">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium">Interactive Visualization</h3>
      <div class="flex space-x-3">
        <button 
          @click="startSimulation"
          class="btn btn-primary"
          :disabled="loading || simulationHistory.length > 0"
        >
          Start Simulation
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      <p class="mt-2 text-gray-600">Running simulation...</p>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Simulation Controls -->
    <div v-if="simulationHistory.length > 0" class="mb-6">
      <div class="flex justify-between items-center bg-gray-50 p-4 rounded-lg">
        <div class="flex space-x-2">
          <button 
            @click="currentStep = 0" 
            class="btn btn-secondary"
            :disabled="currentStep === 0 || isPlaying"
          >
            <span class="text-lg">⏮</span>
          </button>
          <button 
            @click="previousStep" 
            class="btn btn-secondary"
            :disabled="currentStep === 0 || isPlaying"
          >
            <span class="text-lg">⏪</span>
          </button>
          <button 
            @click="togglePlayback" 
            class="btn btn-primary"
          >
            <span class="text-lg">{{ isPlaying ? '⏸' : '▶️' }}</span>
          </button>
          <button 
            @click="nextStep" 
            class="btn btn-secondary"
            :disabled="currentStep === simulationHistory.length - 1 || isPlaying"
          >
            <span class="text-lg">⏩</span>
          </button>
          <button 
            @click="currentStep = simulationHistory.length - 1" 
            class="btn btn-secondary"
            :disabled="currentStep === simulationHistory.length - 1 || isPlaying"
          >
            <span class="text-lg">⏭</span>
          </button>
        </div>
        <div class="flex items-center">
          <span class="mr-4">Speed: </span>
          <input 
            type="range" 
            min="1" 
            max="10" 
            v-model.number="playbackSpeed" 
            class="w-32"
          />
        </div>
        <div class="text-sm text-gray-700">
          Step {{ currentStep + 1 }} / {{ simulationHistory.length }}
          <span class="ml-2 text-gray-500">(Time: {{ currentState?.current_time || 0 }})</span>
        </div>
      </div>
    </div>

    <div v-if="simulationHistory.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left column - Current state -->
      <div class="lg:col-span-1 space-y-6">
        <div class="card">
          <h4 class="text-md font-medium mb-3">Current Time: {{ currentState?.current_time || 0 }}</h4>
          
          <h4 class="text-md font-medium mb-2">Ready Queue</h4>
          <div class="bg-gray-50 p-3 rounded-md mb-4 min-h-16">
            <div v-if="hasReadyQueue" class="flex flex-col space-y-2">
              <!-- Show priority queues for Priority RR algorithm -->
              <template v-if="algorithm === 'PriorityRR' && currentState?.priority_queues">
                <div v-for="(queue, priority) in currentState.priority_queues" :key="priority" class="mb-1">
                  <div class="text-sm font-medium mb-1">Priority {{ priority }}:</div>
                  <div class="flex flex-wrap items-center">
                    <div 
                      v-for="(process, index) in queue" 
                      :key="`${priority}-${process.process_id}`"
                      class="flex items-center mr-3 mb-2"
                    >
                      <div 
                        class="w-8 h-8 rounded-full flex items-center justify-center text-white font-medium"
                        :style="{ backgroundColor: getProcessColor(process.process_id) }"
                      >
                        P{{ process.process_id }}
                      </div>
                      <span class="ml-1 text-xs text-gray-600">({{ process.remaining_time }})</span>
                      <span v-if="index < queue.length - 1" class="mx-1">→</span>
                    </div>
                  </div>
                </div>
              </template>
              
              <!-- Show regular ready queue for other algorithms -->
              <template v-else>
                <div class="flex flex-wrap items-center">
                  <div 
                    v-for="(process, index) in currentState.ready_queue" 
                    :key="process.process_id"
                    class="flex items-center mr-3 mb-2"
                  >
                    <div 
                      class="w-8 h-8 rounded-full flex items-center justify-center text-white font-medium"
                      :style="{ backgroundColor: getProcessColor(process.process_id) }"
                    >
                      P{{ process.process_id }}
                    </div>
                    <span class="ml-1 text-xs text-gray-600">({{ process.remaining_time }})</span>
                    <span v-if="index < currentState.ready_queue.length - 1" class="mx-1">→</span>
                  </div>
                </div>
              </template>
            </div>
            <p v-else class="text-center text-gray-500 py-2">No processes in the ready queue</p>
          </div>
          
          <h4 class="text-md font-medium mb-2">Process States</h4>
          <div class="grid grid-cols-1 gap-2">
            <div 
              v-for="process in sortedProcesses" 
              :key="process.process_id"
              class="flex items-center p-2 rounded-md"
              :class="getProcessStateClass(process)"
            >
              <div 
                class="w-6 h-6 rounded-full flex items-center justify-center text-white font-medium text-xs mr-2"
                :style="{ backgroundColor: getProcessColor(process.process_id) }"
              >
                {{ process.process_id }}
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-center text-sm">
                  <span class="font-medium">Process {{ process.process_id }}</span>
                  <span class="text-xs bg-white bg-opacity-30 px-2 py-1 rounded">
                    {{ getProcessStateLabel(process) }}
                  </span>
                </div>
                <div class="text-xs mt-1 grid grid-cols-3 gap-1">
                  <div>Arrival: {{ process.arrival_time }}</div>
                  <div>Burst: {{ process.burst_time }}</div>
                  <div>Remaining: {{ process.remaining_time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right column - Visualization -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Process arrivals section -->
        <div v-if="getProcessArrivals().length > 0" class="card bg-blue-50">
          <h4 class="text-md font-medium mb-2">Process Arrivals</h4>
          <p class="text-gray-700">{{ getProcessArrivalsDescription() }}</p>
        </div>

        <!-- Current action explanation -->
        <div class="card bg-blue-50">
          <h4 class="text-md font-medium mb-2">Current Action</h4>
          <p class="text-gray-700">{{ getCurrentActionDescription() }}</p>
        </div>
        
        <!-- Gantt chart -->
        <div class="card">
          <GanttChart 
            :timeline="ganttChartData" 
            :currentTime="currentState?.current_time"
            :interactive="true"
            @block-click="handleGanttBlockClick"
          />
        </div>
        
        <!-- Performance metrics for current step -->
        <div class="card">
          <h4 class="text-md font-medium mb-3">Current Metrics</h4>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div class="bg-gray-50 p-3 rounded-lg">
              <h5 class="text-sm font-medium text-gray-700">Avg Waiting Time</h5>
              <p class="text-xl font-bold text-blue-600">{{ currentState?.metrics?.average_waiting_time?.toFixed(2) || '0.00' }}</p>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg">
              <h5 class="text-sm font-medium text-gray-700">Avg Turnaround Time</h5>
              <p class="text-xl font-bold text-blue-600">{{ currentState?.metrics?.average_turnaround_time?.toFixed(2) || '0.00' }}</p>
            </div>
            <div class="bg-gray-50 p-3 rounded-lg">
              <h5 class="text-sm font-medium text-gray-700">CPU Utilization</h5>
              <p class="text-xl font-bold text-blue-600">{{ currentState?.metrics?.cpu_utilization?.toFixed(2) || '0.00' }}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!simulationHistory.length && !loading" class="text-center py-8 text-gray-500">
      Click "Start Simulation" to see the step-by-step execution of the algorithm.
    </div>
  </div>
</template>

<script>
import GanttChart from '@/components/GanttChart.vue';
import api from '@/services/api';

export default {
  name: 'InteractiveVisualizer',
  components: {
    GanttChart
  },
  props: {
    processes: {
      type: Array,
      required: true
    },
    algorithm: {
      type: String,
      required: true
    },
    params: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      loading: false,
      error: null,
      simulationHistory: [],
      currentStep: 0,
      isPlaying: false,
      playbackSpeed: 5,
      playbackInterval: null,
      ganttChartData: []
    };
  },
  computed: {
    currentState() {
      return this.simulationHistory[this.currentStep] || null;
    },
    sortedProcesses() {
      if (!this.currentState) return [];
      
      // Combine all processes from active, waiting, and completed
      const allProcesses = [
        ...(this.currentState.active_processes || []),
        ...(this.currentState.waiting_processes || []),
        ...(this.currentState.completed_processes || [])
      ];
      
      // Sort by process ID for consistent display
      return [...allProcesses].sort((a, b) => a.process_id - b.process_id);
    },
    hasReadyQueue() {
      if (this.algorithm === 'PriorityRR') {
        return this.currentState?.priority_queues && 
               Object.keys(this.currentState.priority_queues).length > 0;
      } else {
        return this.currentState?.ready_queue && 
               this.currentState.ready_queue.length > 0;
      }
    }
  },
  watch: {
    currentStep(newStep) {
      this.updateGanttChart();
    },
    processes() {
      // Reset simulation when processes change
      this.resetSimulation();
    },
    algorithm() {
      // Reset simulation when algorithm changes
      this.resetSimulation();
    },
    params: {
      handler() {
        // Reset simulation when params change
        this.resetSimulation();
      },
      deep: true
    }
  },
  methods: {
    async startSimulation() {
      if (!this.processes.length) {
        this.error = "Please add at least one process to run the simulation.";
        return;
      }
      
      try {
        this.loading = true;
        this.error = null;
        console.log(this.processes);
        const response = await api.runInteractiveSimulation(
          this.algorithm,
          this.params,
          this.processes
        );
        
        this.simulationHistory = response.data.simulation_history || [];
        this.currentStep = 0;
        this.updateGanttChart();
        
        // Emit event to notify parent component
        this.$emit('simulation-started', this.simulationHistory);
      } catch (error) {
        this.error = `Error running simulation: ${error.response?.data?.error || error.message}`;
        console.error('Error running interactive simulation:', error);
      } finally {
        this.loading = false;
      }
    },
    
    resetSimulation() {
      this.stopPlayback();
      this.simulationHistory = [];
      this.currentStep = 0;
      this.ganttChartData = [];
      this.error = null;
    },
    
    previousStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    },
    
    nextStep() {
      if (this.currentStep < this.simulationHistory.length - 1) {
        this.currentStep++;
      } else {
        this.stopPlayback();
      }
    },
    
    togglePlayback() {
      if (this.isPlaying) {
        this.stopPlayback();
      } else {
        this.startPlayback();
      }
    },
    
    startPlayback() {
      if (this.currentStep >= this.simulationHistory.length - 1) {
        this.currentStep = 0;
      }
      
      this.isPlaying = true;
      
      // Calculate interval based on playback speed (1-10)
      // Faster values = shorter intervals
      const interval = 1100 - (this.playbackSpeed * 100);
      
      this.playbackInterval = setInterval(() => {
        this.nextStep();
        
        // Stop at the end
        if (this.currentStep >= this.simulationHistory.length - 1) {
          this.stopPlayback();
        }
      }, interval);
    },
    
    stopPlayback() {
      this.isPlaying = false;
      if (this.playbackInterval) {
        clearInterval(this.playbackInterval);
        this.playbackInterval = null;
      }
    },
    
    updateGanttChart() {
      if (!this.currentState) return;
      
      // Get the gantt chart up to the current step
      this.ganttChartData = this.currentState.gantt_chart || [];
    },
    
    getProcessColor(processId) {
      // Generate a deterministic color based on process ID
      // Match the colors used in GanttChart.vue
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
    
    getProcessStateClass(process) {
      switch (process.state) {
        case 'running':
          return 'bg-green-100 border border-green-200';
        case 'waiting':
          return 'bg-yellow-50 border border-yellow-100';
        case 'completed':
          return 'bg-gray-50 border border-gray-200';
        case 'not_arrived':
          return 'bg-blue-50 border border-blue-100';
        default:
          return 'bg-gray-50';
      }
    },
    
    getProcessStateLabel(process) {
      switch (process.state) {
        case 'running':
          return 'Running';
        case 'waiting':
          return 'Ready';
        case 'completed':
          return 'Completed';
        case 'not_arrived':
          return 'Not Arrived';
        default:
          return 'Unknown';
      }
    },
    
    getCurrentActionDescription() {
      if (!this.currentState) return "Simulation not started.";
      
      const timePoint = this.currentState.current_time;
      const ganttEntries = this.currentState.gantt_chart || [];
      
      // Collect all events happening at the current time
      const events = [];
      
      // If there are no Gantt entries yet, we're at the very beginning
      if (ganttEntries.length === 0) {
        return `Time ${timePoint}: Simulation initialized. Waiting for the first process.`;
      }
      
      // Find the current or most recent Gantt entry
      // (The one that contains the current time point or ended exactly at this time point)
      const currentEntry = ganttEntries.find(entry => 
        entry.start_time <= timePoint && entry.end_time > timePoint
      ) || ganttEntries.find(entry => entry.end_time === timePoint);
      
      // Find the previous Gantt entry (to detect transitions)
      const prevEntryIndex = ganttEntries.findIndex(entry => entry === currentEntry) - 1;
      const prevEntry = prevEntryIndex >= 0 ? ganttEntries[prevEntryIndex] : null;
      
      // Check if processes just completed
      const justCompleted = this.sortedProcesses.filter(p => 
        p.state === 'completed' && p.completion_time === timePoint
      );
      justCompleted.forEach(process => {
        events.push(`Process P${process.process_id} completed execution`);
      });

      // Check for idle CPU
      if (currentEntry && currentEntry.process_id === null) {
        const nextArrival = this.sortedProcesses
          .filter(p => p.arrival_time > timePoint)
          .sort((a, b) => a.arrival_time - b.arrival_time)[0];
          
        if (nextArrival) {
          events.push(`CPU is idle, waiting for Process P${nextArrival.process_id} to arrive at time ${nextArrival.arrival_time}`);
        } else {
          events.push(`CPU is idle`);
        }
      }
      
      // Check for quantum expiration (specific to RR and PriorityRR)
      if ((this.algorithm === 'RR' || this.algorithm === 'PriorityRR') && 
          prevEntry && currentEntry && prevEntry.process_id !== currentEntry.process_id) {
        const quantum = this.currentState.time_quantum || this.params.time_quantum || 2;
        
        // If the previous entry duration equals the quantum and that process isn't completed
        const prevProcess = this.sortedProcesses.find(p => p.process_id === prevEntry.process_id);
        if (prevEntry.duration === quantum && prevProcess && prevProcess.state !== 'completed') {
          if (this.algorithm === 'RR') {
            events.push(`Process P${prevEntry.process_id} used its time quantum and returned to the ready queue`);
          } else { // PriorityRR
            events.push(`Process P${prevEntry.process_id} (priority ${prevProcess.priority}) used its time quantum and returned to its priority queue`);
          }
        }
      }
      
      // Check for a currently running process
      const runningProcess = this.sortedProcesses.find(p => p.state === 'running');
      if (runningProcess) {
        // Check if this process just started its execution
        const justStarted = prevEntry && 
                           (prevEntry.process_id !== runningProcess.process_id || 
                            prevEntry.process_id === null);
                           
        let explanation = '';
        switch (this.algorithm) {
          case 'FCFS':
            explanation = 'following First-Come-First-Served policy';
            break;
          case 'SJF':
            explanation = 'having the shortest remaining burst time';
            break;
          case 'Priority':
            explanation = `having the highest priority (${runningProcess.priority})`;
            break;
          case 'RR':
            explanation = `with time quantum ${this.currentState.time_quantum || this.params.time_quantum || 2}`;
            break;
          case 'PriorityRR':
            explanation = `from priority level ${runningProcess.priority} with time quantum ${this.currentState.time_quantum || this.params.time_quantum || 2}`;
            break;
        }
        
        if (justStarted) {
          events.push(`Process P${runningProcess.process_id} started execution (${explanation})`);
        } else {
          events.push(`Process P${runningProcess.process_id} is executing (${explanation})`);
        }
      }
      
      // Check for process selection/context switch
      if (currentEntry && prevEntry && currentEntry.process_id !== prevEntry.process_id && 
          currentEntry.process_id !== null && prevEntry.process_id !== null) {
        events.push(`Switching from Process P${prevEntry.process_id} to Process P${currentEntry.process_id}`);
      }
      
      // If no specific events were detected but we have a current entry
      if (events.length === 0 && currentEntry) {
        if (currentEntry.process_id !== null) {
          events.push(`Process P${currentEntry.process_id} is running until time ${currentEntry.end_time}`);
        } else {
          events.push(`CPU is idle until time ${currentEntry.end_time}`);
        }
      }
      
      // If still no events (unlikely), provide a default message
      if (events.length === 0) {
        events.push('Simulation in progress');
      }
      
      // Format the output with all events
      return `Time ${timePoint}: ${events.join('; ')}`;
    },
    
    handleGanttBlockClick(block) {
      if (block && block.start_time !== undefined) {
        const stepIndex = this.simulationHistory.findIndex(
          step => step.current_time === block.start_time
        );
        if (stepIndex !== -1) {
          this.currentStep = stepIndex;
        }
      }
    },

    getProcessArrivals() {
      if (!this.currentState) return [];
      
      const currentTime = this.currentState.current_time;
      const ganttEntries = this.currentState.gantt_chart || [];
      
      // Find processes that arrive exactly at the current time
      const exactArrivals = this.sortedProcesses.filter(p => p.arrival_time === currentTime);
      
      // If we are at a time point after an execution block, also check for arrivals during that execution
      const currentEntry = ganttEntries.find(entry => entry.end_time === currentTime);
      if (currentEntry) {
        // Find processes that arrived during the execution period (after the last checked time)
        // This ensures we don't miss arrivals that occurred during execution
        const duringExecutionArrivals = this.sortedProcesses.filter(p => 
          p.arrival_time > currentEntry.start_time && 
          p.arrival_time <= currentEntry.end_time &&
          !exactArrivals.includes(p)  // Don't double count exact arrivals
        );
        
        // Return combined list of arrivals
        return [...exactArrivals, ...duringExecutionArrivals].sort((a, b) => a.arrival_time - b.process_id);
      }
      
      return exactArrivals;
    },

    getProcessArrivalsDescription() {
      const arrivals = this.getProcessArrivals();
      if (arrivals.length === 0) return '';
      
      // Group arrivals by their arrival time
      const groupedArrivals = {};
      arrivals.forEach(p => {
        if (!groupedArrivals[p.arrival_time]) {
          groupedArrivals[p.arrival_time] = [];
        }
        groupedArrivals[p.arrival_time].push(p);
      });
      
      // Generate description for each arrival time
      const descriptions = Object.entries(groupedArrivals).map(([time, processes]) => {
        const processIds = processes.map(p => `P${p.process_id}`).join(', ');
        return `New process(es) ${processIds} arrived at time ${time}`;
      });
      
      return descriptions.join('; ') + '.';
    }
  },
  beforeUnmount() {
    // Clean up any intervals when component is destroyed
    this.stopPlayback();
  }
}
</script>

<style scoped>
.min-h-16 {
  min-height: 4rem;
}
</style>