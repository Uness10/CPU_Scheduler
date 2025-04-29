<template>
  <div>
    <h3 class="text-lg font-medium mb-4">Gantt Chart</h3>
    <div v-if="timeline.length > 0" class="gantt-container">
      <div class="gantt-chart">
        <div class="gantt-row flex">
          <div 
            v-for="(item, index) in timeline" 
            :key="index" 
            class="gantt-block" 
            :style="{
              width: `${item.duration * 50}px`, 
              backgroundColor: getProcessColor(item.process_id)
            }"
          >
            <div class="gantt-content">P{{ item.process_id }}</div>
          </div>
        </div>
        <div class="gantt-timeline flex">
          <div 
            v-for="(item, index) in timeline" 
            :key="index" 
            class="gantt-time" 
            :style="{width: `${item.duration * 50}px`}"
          >
            <div class="gantt-time-marker">{{ item.start_time }}</div>
            <div 
              v-if="index === timeline.length - 1" 
              class="gantt-time-marker" 
              style="position: absolute; right: 0;"
            >
              {{ item.start_time + item.duration }}
            </div>
          </div>
        </div>
      </div>

      <div class="process-legend mt-8">
        <h4 class="text-md font-medium mb-2">Legend</h4>
        <div class="grid grid-cols-4 gap-4">
          <div 
            v-for="processId in uniqueProcessIds" 
            :key="processId" 
            class="flex items-center"
          >
            <div 
              class="w-4 h-4 rounded mr-2" 
              :style="{backgroundColor: getProcessColor(processId)}"
            ></div>
            <span>Process {{ processId }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-8 text-gray-500">
      Run a simulation to see the Gantt chart.
    </div>
  </div>
</template>

<script>
export default {
  name: 'GanttChart',
  props: {
    timeline: {
      type: Array,
      required: true
    }
  },
  computed: {
    uniqueProcessIds() {
      return [...new Set(this.timeline.map(item => item.process_id))];
    }
  },
  methods: {
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
    }
  }
}
</script>

<style scoped>
.gantt-container {
  overflow-x: auto;
}

.gantt-block {
  position: relative;
  height: 40px;
  border-right: 1px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 500;
}

.gantt-time {
  position: relative;
  height: 20px;
  border-right: 1px solid #e2e8f0;
}

.gantt-time-marker {
  position: absolute;
  top: 0;
  left: 0;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: #4a5568;
}
</style>