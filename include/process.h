#pragma once
#include "state.h"
#include <iostream>
using namespace std ;
class Process {
        int pid;
        int arrival_time;
        int burst_time;
        int priority;
        State state;
    
    public:
        Process(int pid, int arrival_time, int burst_time, int priority);
        Process();

        ~Process();
    
        int get_pid() const;
        int get_arrival_time() const;
        int get_burst_time() const;
        int get_priority() const;
        State get_state() const;
        void print_process() const; 

        void set_state(State new_state);        
        void set_burst_time(int new_burst_time);
        void set_priority(int new_priority);
};