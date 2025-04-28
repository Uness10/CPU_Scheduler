#include <iostream>
#include <string>
#include "process_table.h"
#include "fcfs.h"
#include "sjf.h"
#include "psch.h"
#include "scheduler.h"
#include "input_handler.h"

using namespace std; 

// Function to run the scheduler with a table and display results for all algorithms
void run_and_display_results(Process_Table& pt) {
    Scheduler scheduler;
    vector<int> order;
    Algorithm* algo;
    
    // Display the process table
    cout << "\nProcess Table:" << endl;
    pt.print_process_table();
    
    // Run FCFS algorithm
    algo = new FCFS();
    scheduler.setAlgorithm(algo);
    scheduler.setProcessTable(pt);
    order = scheduler.run();
    
    cout << "\nExecution order (FCFS):" << endl;
    for (int pid : order) {
        cout << "P" << pid << " ";
    }
    cout << endl;
    delete algo;
    
    // Run SJF algorithm
    algo = new SJF();
    scheduler.setAlgorithm(algo);
    order = scheduler.run();    
    cout << "\nExecution order (SJF):" << endl;
    for (int pid : order) {
        cout << "P" << pid << " ";
    }
    cout << endl;
    delete algo;
    
    // Run Priority Scheduling algorithm
    algo = new Psch();
    scheduler.setAlgorithm(algo);
    order = scheduler.run();
    cout << "\nExecution order (Priority):" << endl;
    for (int pid : order) {
        cout << "P" << pid << " ";
    }
    cout << endl;
    delete algo;
}

int main() {
    InputHandler input_handler;
    Process_Table pt;
    int choice;
    
    cout << "CPU Scheduler Simulation" << endl;
    cout << "------------------------" << endl;
    cout << "1. Use hardcoded processes" << endl;
    cout << "2. Generate random processes" << endl;
    cout << "3. Read processes from file" << endl;
    cout << "4. Generate random processes and save to file" << endl;
    cout << "Enter your choice: ";
    cin >> choice;
    
    switch (choice) {
        case 1: {
            // Hardcoded processes
            pt.add_process(0, 10, 1);
            pt.add_process(1, 0, 2);
            pt.add_process(2, 8, 3);
            pt.add_process(3, 6, 0);
            pt.add_process(4, 7, 5);
            run_and_display_results(pt);
            break;
        }
        
        case 2: {
            // Generate random processes
            int num_processes;
            cout << "Enter number of processes to generate: ";
            cin >> num_processes;
            
            int min_arrival, max_arrival, min_burst, max_burst, min_priority, max_priority;
            
            cout << "Enter arrival time range (min max): ";
            cin >> min_arrival >> max_arrival;
            
            cout << "Enter burst time range (min max): ";
            cin >> min_burst >> max_burst;
            
            cout << "Enter priority range (min max): ";
            cin >> min_priority >> max_priority;
            
            pt = input_handler.generate_random_processes(
                num_processes, min_arrival, max_arrival, 
                min_burst, max_burst, min_priority, max_priority
            );
            
            run_and_display_results(pt);
            break;
        }
        
        case 3: {
            // Read processes from file
            string filename;
            cout << "Enter filename to read processes from: ";
            cin >> filename;
            
            pt = input_handler.read_processes_from_file(filename);
            
            if (pt.get_size() == 0) {
                cout << "No processes were read from the file or file could not be opened." << endl;
                return 1;
            }
            
            run_and_display_results(pt);
            break;
        }
        
        case 4: {
            // Generate and save to file
            int num_processes;
            cout << "Enter number of processes to generate: ";
            cin >> num_processes;
            
            int min_arrival, max_arrival, min_burst, max_burst, min_priority, max_priority;
            
            cout << "Enter arrival time range (min max): ";
            cin >> min_arrival >> max_arrival;
            
            cout << "Enter burst time range (min max): ";
            cin >> min_burst >> max_burst;
            
            cout << "Enter priority range (min max): ";
            cin >> min_priority >> max_priority;
            
            pt = input_handler.generate_random_processes(
                num_processes, min_arrival, max_arrival, 
                min_burst, max_burst, min_priority, max_priority
            );
            
            string filename;
            cout << "Enter filename to save processes to: ";
            cin >> filename;
            
            if (input_handler.write_processes_to_file(pt, filename)) {
                cout << "Processes successfully saved to " << filename << endl;
            }
            
            run_and_display_results(pt);
            break;
        }
        
        default:
            cout << "Invalid choice!" << endl;
            return 1;
    }
    
    return 0;
}