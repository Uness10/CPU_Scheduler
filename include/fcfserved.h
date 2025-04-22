#pragma once 
#include "algorithm.h"

// First-Come, First-Served (FCFS) scheduling algorithm
class FCFS : public Algorithm {
    public:
        FCFS(); 
        ~FCFS() override ; 
        vector<int> execute(Process_Table& table) override;

};