#pragma once 
#include "algorithm.h" 

// priority scheduling algorithm
class Psch : public Algorithm {
    public : 
        Psch() ; 
        ~Psch() override; 
        vector<int> execute(Process_Table& table) override; 
};

