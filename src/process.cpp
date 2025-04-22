#include "process.h"

Process::Process()  = default ; 
Process::Process(int pid, int arrival_time, int burst_time, int priority) 
    : pid(pid), arrival_time(arrival_time), burst_time(burst_time), priority(priority), state(State::READY) {}

Process::~Process()  = default ; 

int Process::get_pid() const {
    return pid;
}
int Process::get_arrival_time() const {
    return arrival_time;
}
int Process::get_burst_time() const {
    return burst_time;
}
int Process::get_priority() const{ 
    return priority;
}
State Process::get_state() const {
    return state;
}
void Process::set_state(State new_state) {
    state = new_state;
}
void Process::set_burst_time(int new_burst_time) {
    burst_time = new_burst_time;
}
void Process::set_priority(int new_priority) {
    priority = new_priority;
}
void Process::print_process() const {
    cout << "PID: " << pid << ", Arrival Time: " << arrival_time
         << ", Burst Time: " << burst_time << ", Priority: " << priority
         << ", State: " << (state == State::RUNNING ? "RUNNING" : (state == State::BLOCKED ? "BLOCKED" : "READY")) 
     << "\n";
}