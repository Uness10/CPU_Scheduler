#pragma once
#include "process_table.h"
#include <string>
#include <random>
#include <fstream>
#include <iostream>
#include <sstream>
#include <chrono>

using namespace std;
class InputHandler {
private:
    // Random number generation
    mt19937 rng;
    uniform_int_distribution<int> arrival_dist;
    uniform_int_distribution<int> burst_dist;
    uniform_int_distribution<int> priority_dist;

public:
    InputHandler();
    
    // Generate random processes
    Process_Table generate_random_processes(int num_processes, 
                                           int min_arrival = 0, int max_arrival = 20,
                                           int min_burst = 1, int max_burst = 10,
                                           int min_priority = 0, int max_priority = 10);
    
    // Read processes from file
    Process_Table read_processes_from_file(const string& filename);
    
    // Write processes to file (utility function)
    bool write_processes_to_file(const Process_Table& table, const string& filename);
};