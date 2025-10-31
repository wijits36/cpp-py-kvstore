#include "server.h"
#include <iostream>
#include <sstream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

Server::Server(int port) : port_(port), server_socket_(-1) {
    // Constructor - just stores the port
    // Socket creation happens in start()
}

Server::~Server() {
    // Destructor - close socket if it's open
    if (server_socket_ != -1) {
        close(server_socket_);
        std::cout << "Server socket closed" << std::endl;
    }
}

void Server::start() {
    // Step 1: Create socket
    server_socket_ = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket_ < 0) {
        std::cerr << "ERROR: Failed to create socket" << std::endl;
        return;
    }
    std::cout << "Socket created" << std::endl;
    
    // Step 2: Allow reusing the address (useful for quick restarts)
    int opt = 1;
    setsockopt(server_socket_, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    
    // Step 3: Setup server address structure
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));  // Zero out the structure
    server_addr.sin_family = AF_INET;              // IPv4
    server_addr.sin_addr.s_addr = INADDR_ANY;      // Accept from any IP
    server_addr.sin_port = htons(port_);           // Port (converted to network byte order)
    
    // Step 4: Bind socket to address
    if (bind(server_socket_, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "ERROR: Failed to bind to port " << port_ << std::endl;
        close(server_socket_);
        return;
    }
    std::cout << "Bound to port " << port_ << std::endl;
    
    // Step 5: Start listening for connections
    if (listen(server_socket_, 5) < 0) {
        std::cerr << "ERROR: Failed to listen on socket" << std::endl;
        close(server_socket_);
        return;
    }
    std::cout << "Listening for connections..." << std::endl;
    
    // Step 6: Accept connections in a loop
    while (true) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        
        // Accept blocks until a client connects
        int client_socket = accept(server_socket_, (struct sockaddr*)&client_addr, &client_len);
        if (client_socket < 0) {
            std::cerr << "ERROR: Failed to accept connection" << std::endl;
            continue;  // Try again
        }
        
        std::cout << "Client connected!" << std::endl;
        
        // Handle this client
        handleClient(client_socket);
        
        // Close connection
        close(client_socket);
        std::cout << "Client disconnected" << std::endl;
    }
}

void Server::handleClient(int client_socket) {
    char buffer[4096];  // Buffer for reading data
    
    while (true) {
        // Clear buffer
        memset(buffer, 0, sizeof(buffer));
        
        // Read data from client
        ssize_t bytes_read = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
        
        if (bytes_read <= 0) {
            // Connection closed or error
            break;
        }
        
        // Convert to string
        std::string data(buffer, bytes_read);
        
        // Process each line (commands end with \n)
        std::istringstream stream(data);
        std::string line;
        
        while (std::getline(stream, line)) {
            // Remove any trailing \r (Windows line endings)
            if (!line.empty() && line.back() == '\r') {
                line.pop_back();
            }
            
            // Skip empty lines
            if (line.empty()) {
                continue;
            }
            
            std::cout << "Received: " << line << std::endl;
            
            // Process command and get response
            std::string response = processCommand(line);
            
            std::cout << "Sending: " << response;
            
            // Send response back to client
            send(client_socket, response.c_str(), response.length(), 0);
        }
    }
}

std::string Server::processCommand(const std::string& command) {
    // Split command into parts
    std::istringstream iss(command);
    std::string cmd, key, value;
    
    iss >> cmd >> key;
    
    // Handle each command type
    if (cmd == "SET") {
        // For SET, read the rest of the line as the value
        std::getline(iss, value);
        // Remove leading space
        if (!value.empty() && value[0] == ' ') {
            value = value.substr(1);
        }
        
        if (key.empty() || value.empty()) {
            return "ERROR MISSING_ARGUMENTS\n";
        }
        
        store_.set(key, value);
        return "OK\n";
    }
    else if (cmd == "GET") {
        if (key.empty()) {
            return "ERROR MISSING_ARGUMENTS\n";
        }
        
        auto result = store_.get(key);
        if (result.has_value()) {
            return "OK " + result.value() + "\n";
        } else {
            return "ERROR KEY_NOT_FOUND\n";
        }
    }
    else if (cmd == "DELETE") {
        if (key.empty()) {
            return "ERROR MISSING_ARGUMENTS\n";
        }
        
        bool removed = store_.remove(key);
        if (removed) {
            return "OK\n";
        } else {
            return "ERROR KEY_NOT_FOUND\n";
        }
    }
    else if (cmd == "EXISTS") {
        if (key.empty()) {
            return "ERROR MISSING_ARGUMENTS\n";
        }
        
        bool exists = store_.exists(key);
        return exists ? "OK 1\n" : "OK 0\n";
    }
    else {
        return "ERROR INVALID_COMMAND\n";
    }
}
