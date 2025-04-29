<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium">Process Table</h3>
      <div class="flex space-x-2">
        <button @click="addProcess" class="btn btn-secondary">
          Add Process
        </button>
        <button @click="$emit('generate')" class="btn btn-primary">
          Generate Random
        </button>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Process ID
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Arrival Time
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Burst Time
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Priority
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(process, index) in processes" :key="index" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              {{ process.process_id }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <input 
                type="number" 
                min="0"
                v-model.number="process.arrival_time" 
                class="w-20 border rounded px-2 py-1"
                @change="$emit('update', processes)"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <input 
                type="number" 
                min="1"
                v-model.number="process.burst_time" 
                class="w-20 border rounded px-2 py-1"
                @change="$emit('update', processes)"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <input 
                type="number" 
                min="1"
                v-model.number="process.priority" 
                class="w-20 border rounded px-2 py-1"
                @change="$emit('update', processes)"
              />
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="removeProcess(index)" class="text-red-600 hover:text-red-900">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="processes.length === 0" class="text-center py-4 text-gray-500">
      No processes available. Add processes or generate random ones.
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProcessTable',
  props: {
    processes: {
      type: Array,
      required: true
    }
  },
  emits: ['update', 'generate'],
  methods: {
    addProcess() {
      const maxId = this.processes.length > 0 
        ? Math.max(...this.processes.map(p => p.process_id)) 
        : 0;
      
      const newProcess = {
        process_id: maxId + 1,
        arrival_time: 0,
        burst_time: 5,
        priority: 1
      };
      
      this.processes.push(newProcess);
      this.$emit('update', this.processes);
    },
    removeProcess(index) {
      this.processes.splice(index, 1);
      this.$emit('update', this.processes);
    }
  }
}
</script>