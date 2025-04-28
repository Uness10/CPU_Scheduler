#pragma once
#include "process_table.h"
#include <string>
#include <random>
#include <fstream>

class InputHandler {
private:
    // Random number generation
    std::mt19937 rng;
    std::uniform_int_distribution<int> arrival_dist;
    std::uniform_int_distribution<int> burst_dist;
    std::uniform_int_distribution<int> priority_dist;

public:
    InputHandler();
    
    // Generate random processes
    Process_Table generate_random_processes(int num_processes, 
                                           int min_arrival = 0, int max_arrival = 20,
                                           int min_burst = 1, int max_burst = 10,
                                           int min_priority = 0, int max_priority = 10);
    
    // Read processes from file
    Process_Table read_processes_from_file(const std::string& filename);
    
    // Write processes to file (utility function)
    bool write_processes_to_file(const Process_Table& table, const std::string& filename);
};