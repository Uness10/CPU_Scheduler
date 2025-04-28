#pragma once 
#include "algorithm.h"
#include "process_table.h"
// shortest job first (SJF) scheduling algorithm
class SJF :public Algorithm {
    public :
        SJF() ; 
        ~SJF() override ; 
        vector<int> execute(Process_Table& table) override;
};

