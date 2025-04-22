#include <iostream>
#include "process_table.h"
using namespace std ; 


int main(){
    Process_Table pt ;
    pt.add_process(0, 10, 1) ;
    pt.add_process(1, 5, 2) ;
    pt.add_process(2, 8, 3) ;
    pt.add_process(3, 6, 4) ;
    pt.add_process(4, 7, 5) ;
    pt.add_process(5, 4, 6) ;
    pt.add_process(6, 3, 7) ;
    pt.add_process(7, 2, 8) ;
    pt.add_process(8, 1, 9) ;
    pt.print_process_table() ;
    cout << "Size of process table: " << pt.get_size() << endl ;
    pt.remove_process(2) ;
    cout << "After removing process 2: " << pt.get_size() << endl ;
    const Process * p = pt.get_process(3) ;
    if (p != nullptr) {
        p->print_process() ;
    } else {
        cout << "Process 3 not found" << endl ;
    }
    return 0 ;
}