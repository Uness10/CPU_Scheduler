#pragma once 
#include "algorithm.h"

// priority scheduling + RR algorithm

class PschRR : public Algorithm {
    public : 
        PschRR(); 
        ~PschRR() override; 
        vector<int> execute(Process_Table& table) override; 
};

