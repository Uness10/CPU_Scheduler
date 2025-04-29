<template>
  <div class="homepage">
    <div class="max-w-3xl mx-auto text-center mb-12">
      <h1 class="text-3xl font-bold text-blue-600 mb-4">CPU Scheduler Simulation</h1>
      <p class="text-xl text-gray-700 mb-6">
        An interactive visualization tool for understanding CPU scheduling algorithms
      </p>
      <div class="flex justify-center space-x-4">
        <router-link to="/visualization" class="btn btn-primary px-6 py-3">
          Try the Visualization
        </router-link>
        <router-link to="/comparison" class="btn btn-secondary px-6 py-3">
          Compare Algorithms
        </router-link>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
      <div class="card">
        <h2 class="text-xl font-bold text-blue-600 mb-3">Interactive Visualization</h2>
        <p class="text-gray-700 mb-4">
          Visualize how different CPU scheduling algorithms work with a dynamic Gantt chart representation.
          See processes being scheduled in real-time.
        </p>
        <div class="mt-auto">
          <router-link to="/visualization" class="text-blue-600 hover:text-blue-800 font-medium">
            Launch Visualizer →
          </router-link>
        </div>
      </div>

      <div class="card">
        <h2 class="text-xl font-bold text-blue-600 mb-3">Algorithm Comparison</h2>
        <p class="text-gray-700 mb-4">
          Compare different scheduling algorithms side by side using the same set of processes.
          Analyze performance metrics like average waiting time, turnaround time, and CPU utilization.
        </p>
        <div class="mt-auto">
          <router-link to="/comparison" class="text-blue-600 hover:text-blue-800 font-medium">
            Compare Algorithms →
          </router-link>
        </div>
      </div>

      <div class="card">
        <h2 class="text-xl font-bold text-blue-600 mb-3">Educational Tool</h2>
        <p class="text-gray-700 mb-4">
          Perfect for students learning about operating systems and CPU scheduling.
          Generate random processes or create your own to see how different algorithms perform.
        </p>
        <div class="mt-auto">
          <router-link to="/about" class="text-blue-600 hover:text-blue-800 font-medium">
            Learn More →
          </router-link>
        </div>
      </div>
    </div>

    <div class="card mb-12">
      <h2 class="text-2xl font-bold text-blue-600 mb-4">Available Scheduling Algorithms</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="p-4 border rounded-lg bg-gray-50">
          <h3 class="font-bold text-gray-800 mb-1">First-Come, First-Served (FCFS)</h3>
          <p class="text-sm text-gray-600">
            Processes are executed in the order they arrive. Simple but can lead to long waiting times.
          </p>
        </div>
        
        <div class="p-4 border rounded-lg bg-gray-50">
          <h3 class="font-bold text-gray-800 mb-1">Shortest Job First (SJF)</h3>
          <p class="text-sm text-gray-600">
            Processes with the shortest burst time are executed first. Optimal for minimizing average waiting time.
          </p>
        </div>
        
        <div class="p-4 border rounded-lg bg-gray-50">
          <h3 class="font-bold text-gray-800 mb-1">Priority Scheduling</h3>
          <p class="text-sm text-gray-600">
            Processes with higher priority are executed first. Can lead to starvation of lower priority processes.
          </p>
        </div>
        
        <div class="p-4 border rounded-lg bg-gray-50">
          <h3 class="font-bold text-gray-800 mb-1">Round Robin (RR)</h3>
          <p class="text-sm text-gray-600">
            Each process gets a small unit of CPU time (time quantum), and processes are executed in a circular queue.
          </p>
        </div>
        
        <div class="p-4 border rounded-lg bg-gray-50">
          <h3 class="font-bold text-gray-800 mb-1">Priority Round Robin</h3>
          <p class="text-sm text-gray-600">
            Combines priority scheduling with round robin. Processes are organized by priority, and within each priority level, round robin is used.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.card {
  @apply bg-white rounded-lg shadow-md p-6 flex flex-col h-full;
}
</style>
