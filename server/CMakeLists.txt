# Minimum CMake version required
cmake_minimum_required(VERSION 3.10)

# Project name and version
project(kvstore_server VERSION 1.0)

# Use C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add compiler warnings (helps catch bugs!)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")

# Source files - we'll add more as we build
set(SOURCES
    src/main.cpp
)

# Create the executable
add_executable(server ${SOURCES})

# Link against pthread (we'll need this for networking later)
target_link_libraries(server pthread)
