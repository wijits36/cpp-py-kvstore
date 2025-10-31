#ifndef SERVER_H
#define SERVER_H

#include "kvstore.h"
#include <string>

/**
 * Server - TCP server for key-value store
 * 
 * Listens on a port, accepts connections, and processes
 * commands according to the protocol specification.
 */
class Server {
public:
    /**
     * Constructor
     * @param port The port to listen on (default: 8080)
     */
    Server(int port = 8080);
    
    /**
     * Destructor - closes socket if open
     */
    ~Server();
    
    /**
     * Start the server
     * This will block and run until interrupted
     */
    void start();

private:
    /**
     * Handle a single client connection
     * @param client_socket The connected client's socket
     */
    void handleClient(int client_socket);
    
    /**
     * Process a single command line
     * @param command The command string to process
     * @return The response string to send back
     */
    std::string processCommand(const std::string& command);
    
    int port_;              // Port to listen on
    int server_socket_;     // Server's listening socket
    KVStore store_;         // The key-value store
};

#endif // SERVER_H
