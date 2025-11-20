# Minimum CMake version required
cmake_minimum_required(VERSION 3.10)

# Project name and version
project(kvstore_server VERSION 1.0)

# Use C++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add compiler warnings (helps catch bugs!)
if(MSVC)
    # MSVC (Windows Visual Studio)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
else()
    # GCC/Clang (Linux/macOS)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
endif()

# Coverage support (optional, enable with -DCOVERAGE=ON)
option(COVERAGE "Enable coverage reporting" OFF)
if(COVERAGE)
    message(STATUS "Building with coverage support")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
endif()

# Source files for the server
set(SERVER_SOURCES
    src/main.cpp
    src/kvstore.cpp
    src/server.cpp
)

# Source files for the test program
set(TEST_SOURCES
    src/test_kvstore.cpp
    src/kvstore.cpp
)

# Create the server executable
add_executable(server ${SERVER_SOURCES})

# Create the test executable
add_executable(test_kvstore ${TEST_SOURCES})

# Link against pthread
target_link_libraries(server pthread)
target_link_libraries(test_kvstore pthread)
