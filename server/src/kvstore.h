#ifndef KVSTORE_H
#define KVSTORE_H

#include <string>
#include <unordered_map>
#include <optional>

/**
 * KVStore - In-memory key-value storage
 * 
 * This class provides a simple interface for storing and retrieving
 * string key-value pairs. All operations are performed in-memory.
 */
class KVStore {
public:
    /**
     * Store a key-value pair
     * If the key already exists, its value is updated
     */
    void set(const std::string& key, const std::string& value);
    
    /**
     * Retrieve a value by key
     * Returns std::nullopt if the key doesn't exist
     */
    std::optional<std::string> get(const std::string& key) const;
    
    /**
     * Remove a key-value pair
     * Returns true if the key existed and was removed
     * Returns false if the key didn't exist
     */
    bool remove(const std::string& key);
    
    /**
     * Check if a key exists
     * Returns true if the key exists, false otherwise
     */
    bool exists(const std::string& key) const;
    
    /**
     * Get the number of stored key-value pairs
     */
    size_t size() const;
    
    /**
     * Remove all key-value pairs
     */
    void clear();

private:
    // The actual storage: maps strings to strings
    std::unordered_map<std::string, std::string> data_;
};

#endif // KVSTORE_H
