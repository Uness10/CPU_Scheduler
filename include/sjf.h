#pragma once 
#include "algorithm.h"

// shortest job first (SJF) scheduling algorithm
class SJF :public Algorithm {
    public :
        SJF() = default; 
        ~SJF() override = default; 
        void run() override;
};

