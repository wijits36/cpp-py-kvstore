#include "kvstore.h"

void KVStore::set(const std::string& key, const std::string& value) {
    // The [] operator on unordered_map will:
    // - Create the key if it doesn't exist
    // - Update the value if it does exist
    data_[key] = value;
}

std::optional<std::string> KVStore::get(const std::string& key) const {
    // Try to find the key in the map
    auto it = data_.find(key);
    
    // If not found, return empty optional (nullopt)
    if (it == data_.end()) {
        return std::nullopt;
    }
    
    // If found, return the value wrapped in optional
    // it->second is the value (it->first would be the key)
    return it->second;
}

bool KVStore::remove(const std::string& key) {
    // erase() returns the number of elements removed
    // For unordered_map, this is either 0 or 1
    return data_.erase(key) > 0;
}

bool KVStore::exists(const std::string& key) const {
    // count() returns 1 if key exists, 0 if not
    // For unordered_map, it's faster than find() for just checking existence
    return data_.count(key) > 0;
}

size_t KVStore::size() const {
    // Simply return the number of elements in the map
    return data_.size();
}

void KVStore::clear() {
    // Remove all elements from the map
    data_.clear();
}
