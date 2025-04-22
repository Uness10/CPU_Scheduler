#pragma once 
#include "process.h"
#include <vector>
#include <algorithm>
#include <map>
#include <iostream>

using namespace std ; 
class Process_Table {
    map<int,Process> table ;

public:
    Process_Table() ; 
    ~Process_Table() ;
    int add_process(int arrival_time, int burst_time, int priority) ;
    int remove_process(int pid) ;

    const Process* get_process(int pid) const  ;
    vector<Process> get_all() const ;
    int get_size() const ;

    void set_process_state(int pid, State new_state) ;
    void set_process_burst_time(int pid, int new_burst_time) ;
    void set_process_priority(int pid, int new_priority) ;

    void print_process_table() const ;

};