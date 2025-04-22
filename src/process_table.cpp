#include "process_table.h"


Process_Table::Process_Table() = default ;
Process_Table::~Process_Table() = default ;

int Process_Table::add_process(int arrivale_time,int burst_time, int priority){
    int pid = table.size();
    Process p = Process(pid, arrivale_time, burst_time, priority) ;
    table[pid]= p  ;
    return pid;
}

int Process_Table::remove_process(int pid){
    auto it = table.find(pid) ;
    if (it != table.end()) {
        table.erase(it);
        return 0 ; 
    } else {
        return -1 ; 
    }
}

const Process* Process_Table::get_process(int pid) const {
    auto it = table.find(pid);
    return (it != table.end()) ? &(it->second) : nullptr;
}

const map<int, Process>& Process_Table::get_all() const {
    return table;
}

int Process_Table::get_size() const {
    return table.size();
}

void Process_Table::set_process_state(int pid, State new_state) {
    auto it = table.find(pid);
    if (it != table.end()) 
        it->second.set_state(new_state);
    
}
void Process_Table::set_process_burst_time(int pid, int new_burst_time) {
    auto it = table.find(pid);
    if (it != table.end())
        it->second.set_burst_time(new_burst_time);
    
}

void Process_Table::set_process_priority(int pid, int new_priority) {
    auto it = table.find(pid);
    if (it != table.end()) 
        it->second.set_priority(new_priority);
    
}
void Process_Table::print_process_table() const {
    for (const auto& pair : table) {
        const Process& p = pair.second;
        p.print_process();
        cout <<"\n"; 
    }
}

 