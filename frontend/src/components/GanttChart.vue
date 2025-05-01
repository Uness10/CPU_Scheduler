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
            :class="{ 'gantt-block-current': isCurrentBlock(item) }"
            :style="{
              width: `${item.duration * 50}px`, 
              backgroundColor: getProcessColor(item.process_id)
            }"
            @click="$emit('block-click', item)"
          >
            <div class="gantt-content">{{ item.process_id !== null ? `P${item.process_id}` : 'Idle' }}</div>
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
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          <div 
            v-for="processId in uniqueProcessIds" 
            :key="processId" 
            class="flex items-center"
          >
            <div 
              class="w-4 h-4 rounded mr-2" 
              :style="{backgroundColor: getProcessColor(processId)}"
            ></div>
            <span>{{ processId !== null ? `Process ${processId}` : 'Idle' }}</span>
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
    },
    currentTime: {
      type: Number,
      default: null
    },
    interactive: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    uniqueProcessIds() {
      return [...new Set(this.timeline.map(item => item.process_id))];
    }
  },
  methods: {
    getProcessColor(processId) {
      // Handle idle time differently
      if (processId === null) {
        return '#CBD5E0'; // gray-400 for idle time
      }
      
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
    
    isCurrentBlock(block) {
      if (!this.interactive || this.currentTime === null) {
        return false;
      }
      
      // Check if current time falls within this block
      return this.currentTime >= block.start_time && this.currentTime < block.end_time;
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
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.gantt-block:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.gantt-block-current {
  box-shadow: 0 0 0 2px #3182CE, 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 20;
  transform: translateY(-2px);
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