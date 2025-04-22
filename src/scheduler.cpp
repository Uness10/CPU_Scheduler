#include "scheduler.h"

Scheduler::Scheduler() = default ; 
Scheduler::~Scheduler() = default ;

void Scheduler::setAlgorithm(Algorithm* algorithm) {
    this->algorithm = algorithm; 
}

void Scheduler::setProcessTable(Process_Table& table) {
    this->process_table = table; 
}

vector<int> Scheduler::run() {
    if (algorithm) 
        return algorithm->execute(process_table);
    return {}; 
}
