<template>
  <div class="about-view">
    <h1 class="text-2xl font-bold mb-6">About CPU Scheduling Algorithms</h1>
    
    <div class="mb-6">
      <p class="text-gray-600">
        CPU scheduling is the process of determining which process in the ready queue gets allocated to the CPU. The scheduler assigns resources to different processes based on a specific scheduling algorithm.
      </p>
    </div>
    
    <!-- Algorithm Selector Tabs -->
    <div class="mb-6">
      <div class="flex flex-wrap border-b border-gray-200">
        <button 
          v-for="algorithm in algorithms" 
          :key="algorithm.id"
          @click="selectedAlgorithm = algorithm.id"
          class="px-4 py-2 text-sm font-medium border-b-2 -mb-px focus:outline-none"
          :class="selectedAlgorithm === algorithm.id 
            ? 'border-blue-500 text-blue-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
        >
          {{ algorithm.name }}
        </button>
      </div>
    </div>
    
    <!-- Algorithm Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Content -->
      <div class="lg:col-span-2">
        <div class="card">
          <template v-for="algorithm in algorithms" :key="algorithm.id">
            <div v-if="selectedAlgorithm === algorithm.id">
              <h2 class="text-xl font-bold mb-4">{{ algorithm.name }}</h2>
              
              <div class="prose max-w-none">
                <div v-html="algorithm.description"></div>
                
                <h3 class="text-lg font-medium mt-6 mb-2">How It Works</h3>
                <div v-html="algorithm.howItWorks"></div>
                
                <h3 class="text-lg font-medium mt-6 mb-2">Advantages</h3>
                <ul class="list-disc pl-6 mb-4">
                  <li v-for="(advantage, idx) in algorithm.advantages" :key="idx" class="mb-1">
                    {{ advantage }}
                  </li>
                </ul>
                
                <h3 class="text-lg font-medium mt-6 mb-2">Disadvantages</h3>
                <ul class="list-disc pl-6 mb-4">
                  <li v-for="(disadvantage, idx) in algorithm.disadvantages" :key="idx" class="mb-1">
                    {{ disadvantage }}
                  </li>
                </ul>

                <h3 class="text-lg font-medium mt-6 mb-2">Use Cases</h3>
                <div v-html="algorithm.useCases"></div>
              </div>
            </div>
          </template>
        </div>
      </div>
      
      <!-- Sidebar -->
      <div class="lg:col-span-1 space-y-6">
        <!-- Key Metrics -->
        <div class="card">
          <h3 class="text-lg font-medium mb-4">Key Performance Metrics</h3>
          <div class="space-y-4">
            <div>
              <h4 class="font-medium text-gray-800">Waiting Time</h4>
              <p class="text-sm text-gray-600">The time a process spends waiting in the ready queue.</p>
            </div>
            <div>
              <h4 class="font-medium text-gray-800">Turnaround Time</h4>
              <p class="text-sm text-gray-600">The time taken to complete a process (waiting time + burst time).</p>
            </div>

            <div>
              <h4 class="font-medium text-gray-800">CPU Utilization</h4>
              <p class="text-sm text-gray-600">The percentage of time the CPU is actively executing processes.</p>
            </div>
            <div>
              <h4 class="font-medium text-gray-800">Throughput</h4>
              <p class="text-sm text-gray-600">The number of processes completed per unit time.</p>
            </div>
          </div>
        </div>
        
        <!-- Visualization Link -->
        <div class="card bg-blue-50">
          <h3 class="text-lg font-medium mb-4">Try it Yourself</h3>
          <p class="text-sm text-gray-600 mb-4">
            See how different CPU scheduling algorithms perform with your own custom processes or generated test cases.
          </p>
          <div class="flex flex-col space-y-2">
            <router-link to="/processes" class="btn btn-outline">
              Create Processes
            </router-link>
            <router-link to="/visualization" class="btn btn-primary">
              View Visualizations
            </router-link>
          </div>
        </div>
        
        <!-- Resources -->
        <div class="card">
          <h3 class="text-lg font-medium mb-4">Additional Resources</h3>
          <ul class="space-y-2">
            <li>
              <a href="https://en.wikipedia.org/wiki/Scheduling_(computing)" target="_blank" class="text-blue-600 hover:underline flex items-center">
                <span>Wikipedia: CPU Scheduling</span>
                <svg class="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                  <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"></path>
                </svg>
              </a>
            </li>
            <li>
              <a href="https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/" target="_blank" class="text-blue-600 hover:underline flex items-center">
                <span>GeeksforGeeks: CPU Scheduling</span>
                <svg class="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                  <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"></path>
                </svg>
              </a>
            </li>
            <li>
              <a href="https://www.tutorialspoint.com/operating_system/os_process_scheduling.htm" target="_blank" class="text-blue-600 hover:underline flex items-center">
                <span>TutorialsPoint: Process Scheduling</span>
                <svg class="w-4 h-4 ml-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"></path>
                  <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"></path>
                </svg>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      selectedAlgorithm: 'fcfs',
      algorithms: [
        {
          id: 'fcfs',
          name: 'First-Come, First-Served (FCFS)',
          description: `
            <p>First-Come, First-Served (FCFS) is the simplest CPU scheduling algorithm. In this scheme, the process that requests the CPU first is allocated the CPU first. The implementation of the FCFS policy is easily managed with a FIFO (First-In, First-Out) queue.</p>
            <p>When a process enters the ready queue, its PCB (Process Control Block) is linked to the tail of the queue. When the CPU is free, it is allocated to the process at the head of the queue.</p>
          `,
          howItWorks: `
            <p>FCFS works exactly as its name implies:</p>
            <ol class="list-decimal pl-6 mb-4">
              <li>Processes are executed in the order they arrive in the ready queue</li>
              <li>Once a process gets CPU time, it runs to completion</li>
              <li>Non-preemptive algorithm - the currently running process can't be interrupted</li>
              <li>Easy to implement and understand</li>
            </ol>
            <p>For example, if we have processes P1, P2, and P3 arriving at times 0, 1, and 2 with burst times of 5, 3, and 8 respectively, FCFS would execute them in order: P1 (0-5), P2 (5-8), P3 (8-16).</p>
          `,
          advantages: [
            'Simple and easy to implement',
            'FIFO queue data structure is easy to program',
            'Fair in the sense that processes are executed in the order they arrive',
            'No starvation, as every process eventually gets CPU time'
          ],
          disadvantages: [
            'Can lead to the "convoy effect" where short processes wait for long processes to complete',
            'Poor performance as average waiting time can be high',
            'Not responsive for interactive systems',
            'No prioritization, important tasks have to wait their turn'
          ],
          useCases: `
            <p>FCFS is suitable for:</p>
            <ul class="list-disc pl-6 mb-4">
              <li>Batch systems where interactive performance is not important</li>
              <li>Simple task queues where fairness in order is more important than efficiency</li>
              <li>Systems with similar-length processes where convoy effect is minimal</li>
            </ul>
          `
        },
        {
          id: 'sjf',
          name: 'Shortest Job First (SJF)',
          description: `
            <p>Shortest Job First (SJF) is a scheduling algorithm where the process with the smallest execution time (burst time) is selected for execution next. This can be either preemptive or non-preemptive.</p>
            <p>In the non-preemptive variant, once a process begins execution, it must run to completion. In the preemptive variant (also known as Shortest Remaining Time First or SRTF), a running process can be preempted if a new process arrives with a smaller burst time.</p>
          `,
          howItWorks: `
            <p>SJF works by selecting the process with the shortest burst time:</p>
            <ol class="list-decimal pl-6 mb-4">
              <li>Processes are scheduled according to their burst time</li>
              <li>The process with the shortest burst time is selected for execution</li>
              <li>In case of a tie, FCFS can be used as a tie-breaker</li>
              <li>In preemptive mode (SRTF), if a new process arrives with burst time less than remaining time of current process, the CPU switches to the new process</li>
            </ol>
            <p>For example, with processes P1, P2, P3 with burst times 6, 3, 8, SJF would execute them in order: P2 (3 units), P1 (6 units), P3 (8 units).</p>
          `,
          advantages: [
            'Provides minimum average waiting time among all scheduling algorithms',
            'Gives optimal results in terms of average waiting time',
            'Good for batch systems where burst times are known in advance',
            'Reduces the waiting time for processes with short bursts'
          ],
          disadvantages: [
            'Hard to implement in practical systems because predicting burst time is difficult',
            'May cause starvation for processes with longer burst times',
            'Cannot be implemented without knowing the burst time in advance',
            'Performance depends heavily on accurate burst time predictions'
          ],
          useCases: `
            <p>SJF is suitable for:</p>
            <ul class="list-disc pl-6 mb-4">
              <li>Batch systems where burst times are known or can be accurately predicted</li>
              <li>Systems that benefit from minimizing average waiting time</li>
              <li>Scenarios where shorter jobs should be given preference (e.g., query processing)</li>
            </ul>
          `
        },
        {
          id: 'priority',
          name: 'Priority Scheduling',
          description: `
            <p>Priority Scheduling is a scheduling algorithm that allocates the CPU to processes based on their priority values. Each process is assigned a priority, and the process with the highest priority is executed first.</p>
            <p>This can be implemented in both preemptive and non-preemptive versions. In preemptive priority scheduling, if a process with higher priority arrives, the current process is preempted (interrupted) and the CPU is allocated to the higher priority process.</p>
          `,
          howItWorks: `
            <p>Priority scheduling operates as follows:</p>
            <ol class="list-decimal pl-6 mb-4">
              <li>Each process is assigned a priority value</li>
              <li>Processes are sorted in the ready queue based on their priorities</li>
              <li>The CPU is allocated to the process with the highest priority</li>
              <li>When processes have the same priority, FCFS can be used to break the tie</li>
              <li>In preemptive mode, a running process is interrupted if a higher-priority process arrives</li>
            </ol>
            <p>Priorities can be defined internally (e.g., time limits, memory requirements) or externally (e.g., importance of the process, department, payment).</p>
          `,
          advantages: [
            'Allows system to prioritize important or time-critical processes',
            'Can be implemented with or without preemption for flexibility',
            'Suitable for real-time systems where certain tasks must be executed promptly',
            'Adaptable to different system requirements by adjusting priority assignment'
          ],
          disadvantages: [
            'Can lead to starvation of low-priority processes if many high-priority processes keep arriving',
            'Need for aging mechanism to prevent indefinite blocking of low-priority processes',
            'Priority assignment may be subjective or difficult to determine',
            'Additional overhead in constantly checking and updating priorities'
          ],
          useCases: `
            <p>Priority Scheduling is suitable for:</p>
            <ul class="list-disc pl-6 mb-4">
              <li>Real-time systems where some processes must be executed promptly</li>
              <li>Multi-user environments where process importance varies</li>
              <li>Systems that must respond differently to different types of events</li>
              <li>Mission-critical systems where certain operations take precedence</li>
            </ul>
          `
        },
        {
          id: 'rr',
          name: 'Round Robin (RR)',
          description: `
            <p>Round Robin is a CPU scheduling algorithm that is designed specifically for time-sharing systems. It is similar to FCFS but with preemption to switch between processes. Each process is assigned a fixed time slice called a quantum.</p>
            <p>Once a process has executed for the given time quantum, it is preempted and added to the end of the ready queue, allowing another process to execute. This ensures fair distribution of CPU time and improved response time.</p>
          `,
          howItWorks: `
            <p>Round Robin works with a time-sharing approach:</p>
            <ol class="list-decimal pl-6 mb-4">
              <li>A fixed time quantum (typically 10-100 milliseconds) is defined</li>
              <li>The ready queue is treated as a circular queue</li>
              <li>The scheduler assigns CPU to each process for a time interval of one time quantum</li>
              <li>After the quantum expires, the process is preempted and added to the end of the ready queue</li>
              <li>If a process completes before its quantum expires, the CPU selects the next process from the ready queue</li>
            </ol>
            <p>The performance of RR depends heavily on the size of the time quantum. Too large a quantum makes it similar to FCFS, while too small a quantum increases context switching overhead.</p>
          `,
          advantages: [
            'Fair allocation of CPU time among processes',
            'Better response time for short processes compared to FCFS',
            'No starvation as each process gets a fair share of CPU',
            'Ideal for time-sharing environments where interactive response is important'
          ],
          disadvantages: [
            'Higher context-switching overhead compared to non-preemptive algorithms',
            'Average waiting time and turnaround time can be high for varying burst times',
            'Performance heavily dependent on time quantum selection',
            'Not suitable for processes with widely varying CPU burst requirements'
          ],
          useCases: `
            <p>Round Robin is suitable for:</p>
            <ul class="list-disc pl-6 mb-4">
              <li>Time-sharing systems requiring fair CPU allocation</li>
              <li>Interactive systems where quick response is needed for multiple users</li>
              <li>Systems where predictable response times are needed</li>
              <li>General purpose operating systems serving multiple users/applications</li>
            </ul>
          `
        },
        {
          id: 'priority-rr',
          name: 'Priority Round Robin (PRR)',
          description: `
            <p>Priority Round Robin (PRR) is a hybrid scheduling algorithm that combines the features of both Priority Scheduling and Round Robin. It organizes processes into multiple priority queues and applies Round Robin scheduling within each priority level.</p>
            <p>This algorithm aims to address the disadvantages of both Priority Scheduling (potential starvation) and Round Robin (equal treatment of processes with different importance).</p>
          `,
          howItWorks: `
            <p>Priority Round Robin operates as follows:</p>
            <ol class="list-decimal pl-6 mb-4">
              <li>Processes are grouped into different priority queues</li>
              <li>Higher priority queues are served first</li>
              <li>Within each priority level, processes are scheduled using Round Robin with a time quantum</li>
              <li>Only when a higher priority queue is empty will processes from lower priority queues be served</li>
              <li>Aging mechanism can be implemented to prevent starvation of low-priority processes</li>
            </ol>
            <p>This approach provides the responsiveness of Round Robin while still respecting process priorities, making it a good compromise for many systems.</p>
          `,
          advantages: [
            'Combines benefits of both Priority Scheduling and Round Robin',
            'Respects process priorities while ensuring CPU time distribution within same priority',
            'Better response time for high-priority processes',
            'More flexible than simple Round Robin for complex systems'
          ],
          disadvantages: [
            'More complex to implement than either Priority or Round Robin alone',
            'Without aging, may still lead to starvation of low-priority processes',
            'Increased overhead due to managing multiple queues',
            'Requires careful tuning of both priorities and time quantum'
          ],
          useCases: `
            <p>Priority Round Robin is suitable for:</p>
            <ul class="list-disc pl-6 mb-4">
              <li>Complex systems requiring both priority handling and time-sharing</li>
              <li>Real-time systems with different categories of tasks</li>
              <li>Multi-user systems where both user priority and fair CPU sharing are important</li>
              <li>Enterprise systems running both background and interactive applications</li>
            </ul>
          `
        }
      ]
    };
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

/* Additional styling for HTML content */
.prose h3 {
  @apply text-lg font-medium mt-6 mb-2;
}

.prose p {
  @apply mb-4;
}

.prose a {
  @apply text-blue-600 hover:underline;
}
</style>
