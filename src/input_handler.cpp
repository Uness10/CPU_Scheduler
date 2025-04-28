#include "input_handler.h"



InputHandler::InputHandler() {
    // Seed the random number generator with current time
    unsigned seed = chrono::system_clock::now().time_since_epoch().count();
    rng = mt19937(seed);
    
    // Initialize distributions with default ranges
    arrival_dist = uniform_int_distribution<int>(0, 20);
    burst_dist = uniform_int_distribution<int>(1, 10);
    priority_dist = uniform_int_distribution<int>(0, 10);
}

Process_Table InputHandler::generate_random_processes(int num_processes, 
                                                    int min_arrival, int max_arrival,
                                                    int min_burst, int max_burst,
                                                    int min_priority, int max_priority) {
    Process_Table table;
    
    // Update distributions with provided ranges
    arrival_dist = uniform_int_distribution<int>(min_arrival, max_arrival);
    burst_dist = uniform_int_distribution<int>(min_burst, max_burst);
    priority_dist = uniform_int_distribution<int>(min_priority, max_priority);
    
    for (int i = 0; i < num_processes; i++) {
        int arrival_time = arrival_dist(rng);
        int burst_time = burst_dist(rng);
        int priority = priority_dist(rng);
        
        table.add_process(arrival_time, burst_time, priority);
    }
    
    return table;
}

Process_Table InputHandler::read_processes_from_file(const string& filename) {
    Process_Table table;
    ifstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return table;
    }
    
    string line;
    int line_num = 0;
    
    // Skip header line if exists
    getline(file, line);
    line_num++;
    
    // Check if the first line is a header or data
    bool is_header = line.find_first_not_of("0123456789, \t") != string::npos;
    if (!is_header) {
        // If not a header, reset file to beginning to read the first line again
        file.clear();
        file.seekg(0);
        line_num = 0;
    }
    
    while (getline(file, line)) {
        line_num++;
        istringstream iss(line);
        int arrival_time, burst_time, priority;
        
        // Try to parse the line with format: arrival_time burst_time priority
        if (iss >> arrival_time >> burst_time >> priority) {
            table.add_process(arrival_time, burst_time, priority);
        } else {
            cerr << "Warning: Could not parse line " << line_num << ": " << line << endl;
        }
    }
    
    file.close();
    return table;
}

bool InputHandler::write_processes_to_file(const Process_Table& table, const string& filename) {
    ofstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << " for writing" << endl;
        return false;
    }
    
    // Write header
    file << "arrival_time burst_time priority" << endl;
    
    // Write each process
    for (const auto& process : table.get_all()) {
        file << process.get_arrival_time() << " "
             << process.get_burst_time() << " "
             << process.get_priority() << endl;
    }
    
    file.close();
    return true;
}