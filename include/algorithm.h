#pragma once 
#include "process_table.h"
#include <vector>
#include <algorithm>
class Algorithm {
    public:
        virtual vector<int> execute(Process_Table& table) = 0; 
        virtual ~Algorithm() = default; 
    };