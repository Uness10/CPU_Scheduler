#pragma once 
#include "algorithm.h"
#include "process_table.h"
#include <vector>

using namespace std ;


class Scheduler {
    Algorithm* algorithm;
    Process_Table process_table;
    public:
        Scheduler() ; 
        ~Scheduler(); 
        vector<int> run();
        void setAlgorithm(Algorithm* algorithm); 
        void setProcessTable(Process_Table& table);
};