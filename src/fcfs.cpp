#include "fcfs.h"

FCFS::FCFS() = default;
FCFS::~FCFS() = default;

vector<int> FCFS::execute(Process_Table& table){
    vector<int> order ; 
    vector<Process> processes = table.get_all();
    order.reserve(processes.size());

    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.get_arrival_time() < b.get_arrival_time();
    });
    for (const auto& p : processes)
        order.push_back(p.get_pid());

    
    return order;
}

