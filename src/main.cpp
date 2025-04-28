#include <iostream>
#include "process_table.h"
#include "fcfs.h"
#include "sjf.h"
#include "psch.h"
#include "scheduler.h"
using namespace std ; 


int main(){
    Process_Table pt ;
    pt.add_process(0, 10, 1) ;
    pt.add_process(1, 0, 2) ;
    pt.add_process(2, 8, 3) ;
    pt.add_process(3, 6, 0) ;
    pt.add_process(4, 7, 5) ;
    Scheduler scheduler= Scheduler() ;

    Algorithm* algo = new FCFS() ; 
    
    scheduler.setAlgorithm(algo);
    scheduler.setProcessTable(pt);
    vector<int> order = scheduler.run();
    
    cout << "\nExecution order (FCFS):\n";
    for (int pid : order) {
        cout << "P" << pid << " ";
    }
    cout << "\n";
    algo = new SJF() ;
    scheduler.setAlgorithm(algo);
    order = scheduler.run();    
    cout << "\nExecution order (SJF):\n";
    for (int pid : order) {
        cout << "P" << pid << " ";
    }
    cout << "\n";
    algo = new Psch() ;
    scheduler.setAlgorithm(algo);
    order = scheduler.run();
    cout << "\nExecution order (Priority):\n";
    for (int pid : order) {
        cout << "P" << pid << " ";
    }

    cout << "\n";
    return 0 ;
}