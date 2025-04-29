<template>
  <div class="about">
    <h1 class="text-2xl font-bold mb-6">About CPU Scheduler Simulation</h1>
    
    <div class="card mb-6">
      <h2 class="text-xl font-bold text-blue-600 mb-3">Project Overview</h2>
      <p class="text-gray-700 mb-4">
        This CPU Scheduler Simulation is an educational tool designed to help students and professionals understand 
        how different CPU scheduling algorithms work in operating systems. The simulation allows users to visualize 
        the scheduling process and compare the performance of various algorithms using metrics like waiting time, 
        turnaround time, and CPU utilization.
      </p>
      <p class="text-gray-700">
        The project features both a Python backend that implements the scheduling algorithms and a Vue.js frontend 
        that provides an interactive visualization interface.
      </p>
    </div>
    
    <div class="card mb-6">
      <h2 class="text-xl font-bold text-blue-600 mb-3">CPU Scheduling Concepts</h2>
      <p class="text-gray-700 mb-4">
        CPU scheduling is a process that allows one process to use the CPU while the execution of another process is on hold due to unavailability of resources. 
        The aim of CPU scheduling is to make the system efficient, fast, and fair.
      </p>
      
      <div class="mb-4">
        <h3 class="font-bold text-gray-800 mb-1">Important Terms:</h3>
        <ul class="list-disc list-inside text-gray-700 space-y-2">
          <li><span class="font-medium">Arrival Time:</span> The time at which a process arrives in the ready queue</li>
          <li><span class="font-medium">Burst Time:</span> The time required by a process for CPU execution</li>
          <li><span class="font-medium">Completion Time:</span> The time at which a process completes its execution</li>
          <li><span class="font-medium">Turnaround Time:</span> Completion time - Arrival time</li>
          <li><span class="font-medium">Waiting Time:</span> Turnaround time - Burst time</li>
          <li><span class="font-medium">Priority:</span> A value that determines the priority of process scheduling (lower value typically means higher priority)</li>
        </ul>
      </div>
    </div>
    
    <div class="card mb-6">
      <h2 class="text-xl font-bold text-blue-600 mb-3">Scheduling Algorithms</h2>
      
      <div class="space-y-4">
        <div>
          <h3 class="font-bold text-gray-800 mb-1">First-Come, First-Served (FCFS)</h3>
          <p class="text-gray-700">
            The simplest scheduling algorithm that schedules processes in the order they arrive in the ready queue.
            It's easy to implement but can lead to the "convoy effect" where short processes wait for a long process to finish.
          </p>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Shortest Job First (SJF)</h3>
          <p class="text-gray-700">
            Schedules processes based on their CPU burst time. The process with the shortest burst time is scheduled first.
            It's optimal for minimizing average waiting time but requires knowledge of burst time in advance.
          </p>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Priority Scheduling</h3>
          <p class="text-gray-700">
            Schedules processes based on their priority. Higher priority processes are executed first.
            It can lead to starvation of lower priority processes if higher priority processes keep arriving.
          </p>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Round Robin (RR)</h3>
          <p class="text-gray-700">
            Each process gets a small unit of CPU time (time quantum) in a cyclic way. After the time quantum expires,
            the process is preempted and added to the back of the ready queue. It's fair but sensitive to the time quantum size.
          </p>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Priority Round Robin</h3>
          <p class="text-gray-700">
            Combines priority scheduling with round robin. Processes are organized by priority,
            and within each priority level, round robin scheduling is used.
          </p>
        </div>
      </div>
    </div>
    
    <div class="card">
      <h2 class="text-xl font-bold text-blue-600 mb-3">How to Use This Simulation</h2>
      
      <div class="space-y-4">
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Visualization Tab</h3>
          <ol class="list-decimal list-inside text-gray-700 space-y-1">
            <li>Add processes manually or generate random processes</li>
            <li>Select a scheduling algorithm and configure any parameters</li>
            <li>Click "Run Simulation" to see the Gantt chart visualization</li>
            <li>View the performance metrics for the selected algorithm</li>
          </ol>
        </div>
        
        <div>
          <h3 class="font-bold text-gray-800 mb-1">Comparison Tab</h3>
          <ol class="list-decimal list-inside text-gray-700 space-y-1">
            <li>Add processes manually or generate random processes</li>
            <li>Configure the Round Robin time quantum if needed</li>
            <li>Click "Compare Algorithms" to run all algorithms on the same processes</li>
            <li>View performance charts and the detailed comparison table</li>
          </ol>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.card {
  @apply bg-white rounded-lg shadow-md p-6 mb-6;
}
</style>
