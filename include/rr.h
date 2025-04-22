#pragma once
#include "algorithm.h"

// round robin algorithm
class RR : public Algorithm {
    public:
        RR() ;
        ~RR() override ;
        vector<int> execute(Process_Table& table) override;
};

