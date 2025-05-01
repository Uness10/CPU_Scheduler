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
  emits: ['update', 'generate', 'add', 'remove'], // Add 'add' and 'remove'
  methods: {
    addProcess() {
      const maxId = this.processes.length > 0 
        ? Math.max(...this.processes.map(p => parseInt(p.process_id) || 0)) // Ensure IDs are numbers
        : 0;
      
      const newProcess = {
        process_id: maxId + 1,
        arrival_time: 0,
        burst_time: 5,
        priority: 1
      };
      
      // Emit an event for the parent to handle adding
      this.$emit('add', newProcess); 
      // Do not push directly: this.processes.push(newProcess);
      // Do not emit update here for add: this.$emit('update', this.processes);
    },
    removeProcess(index) {
      // Emit an event for the parent to handle removal
      this.$emit('remove', index);
      // Do not splice directly: this.processes.splice(index, 1);
      // Do not emit update here for remove: this.$emit('update', this.processes);
    }
  }
}
</script>