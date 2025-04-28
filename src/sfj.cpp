#include "sjf.h"


SJF::SJF()= default;
SJF::~SJF()= default;

vector<int> SJF::execute(Process_Table& table) {
    vector<int> order;
    vector<Process> processes = table.get_all();
    order.reserve(processes.size());

    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.get_burst_time() < b.get_burst_time();
    });

    for (const auto& p : processes) 
        order.push_back(p.get_pid());
    

    return order;
}
