cmake_minimum_required(VERSION 3.10)

project(scheduler VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

add_executable(scheduler 
    src/main.cpp
    src/process.cpp
    src/process_table.cpp
    src/fcfs.cpp
    src/scheduler.cpp
    )

target_include_directories(scheduler PRIVATE include)