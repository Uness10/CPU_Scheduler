# CPU Scheduler Project

This project implements a CPU scheduling simulation. Follow the steps below to build and run the project.

## Prerequisites

1. **CMake**: Ensure CMake is installed on your system. You can download it from [CMake's official website](https://cmake.org/).

2. **MinGW**: Install MinGW for compiling C++ code. Ensure the `gcc` and `g++` compilers are available in your PATH.
3. **Git** (optional): If you cloned this repository, ensure Git is installed.

## Steps to Build and Run

### 1. Clone the Repository (Optional)
If you haven't already, clone the repository:
```bash
git clone https://github.com/Uness10/CPU_Scheduler.git
cd CPU_Scheduler
```

### 2. Build the Project
Use CMake to configure and build the project:
```bash
mkdir build
cd build
cmake ..
cmake --build .
```

### 3. Run the Project
After building, execute the generated binary:
```bash
./CPU_Scheduler
```
Replace `CPU_Scheduler` with the actual name of the generated binary if it differs.