<template>
  <div class="card">
    <h3 class="text-lg font-medium mb-4">Algorithm Configuration</h3>
    
    <div class="mb-4">
      <label for="algorithm" class="form-label">Scheduling Algorithm</label>
      <select 
        id="algorithm"
        v-model="selectedAlgorithm" 
        @change="updateSelection"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option 
          v-for="algorithm in algorithms" 
          :key="algorithm.id" 
          :value="algorithm.id"
        >
          {{ algorithm.name }}
        </option>
      </select>
    </div>

    <div v-if="needsQuantum" class="mb-4">
      <label for="quantum" class="form-label">Time Quantum</label>
      <input 
        id="quantum"
        type="number" 
        v-model.number="timeQuantum" 
        @change="updateSelection"
        min="1"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      />
      <p class="text-xs text-gray-500 mt-1">Note: Quantum value must be greater than or equal to 1</p>
    </div>

    <div class="mt-4 bg-gray-50 p-4 rounded-md">
      <h4 class="text-sm font-medium text-gray-700 mb-2">Algorithm Description</h4>
      <p class="text-sm text-gray-600">{{ algorithmDescription }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlgorithmSelector',
  data() {
    return {
      selectedAlgorithm: 'FCFS',
      timeQuantum: 2,
      algorithms: [
        { id: 'FCFS', name: 'First-Come, First-Served (FCFS)', description: 'Processes are executed in the order they arrive. Simple but can lead to long waiting times.' },
        { id: 'SJF', name: 'Shortest Job First (SJF)', description: 'Processes with the shortest burst time are executed first. Optimal for minimizing average waiting time.' },
        { id: 'Priority', name: 'Priority Scheduling', description: 'Processes with higher priority are executed first. Can lead to starvation of lower priority processes.' },
        { id: 'RR', name: 'Round Robin (RR)', description: 'Each process gets a small unit of CPU time (time quantum), and processes are executed in a circular queue.' },
        { id: 'PriorityRR', name: 'Priority Round Robin', description: 'Combines priority scheduling with round robin. Processes are organized by priority, and within each priority level, round robin is used.' }
      ]
    };
  },
  computed: {
    algorithmDescription() {
      const algorithm = this.algorithms.find(algo => algo.id === this.selectedAlgorithm);
      return algorithm ? algorithm.description : '';
    },
    needsQuantum() {
      return this.selectedAlgorithm === 'RR' || this.selectedAlgorithm === 'PriorityRR';
    }
  },
  methods: {
    updateSelection() {
      this.$emit('update', {
        algorithm: this.selectedAlgorithm,
        params: this.needsQuantum ? { time_quantum: this.timeQuantum } : {}
      });
    }
  },
  mounted() {
    // Initialize with the default selection
    this.updateSelection();
  }
}
</script>