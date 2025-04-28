#include "psch.h"


Psch::Psch() = default;
Psch::~Psch() = default;
vector<int> Psch::execute(Process_Table& table) {
    vector<int> order;
    vector<Process> processes = table.get_all();
    order.reserve(processes.size());

    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        // Higher number means lower priority
        return a.get_priority() < b.get_priority(); 
    });

    for (const auto& p : processes) 
        order.push_back(p.get_pid());

    return order;
}