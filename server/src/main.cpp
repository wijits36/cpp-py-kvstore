#include <iostream>
#include "server.h"

int main() {
    std::cout << "Key-Value Store Server v1.0" << std::endl;
    std::cout << "Starting server on port 8080..." << std::endl;
    
    // Create and start the server
    Server server(8080);
    server.start();
    
    return 0;
}
