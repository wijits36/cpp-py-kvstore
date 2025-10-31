#include "kvstore.h"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "Testing KVStore class..." << std::endl;
    
    KVStore store;
    
    // Test 1: Store and retrieve
    std::cout << "Test 1: SET and GET" << std::endl;
    store.set("name", "Alice");
    auto value = store.get("name");
    assert(value.has_value());  // Should have a value
    assert(value.value() == "Alice");  // Should be "Alice"
    std::cout << "  ✓ SET name=Alice, GET name=" << value.value() << std::endl;
    
    // Test 2: Get non-existent key
    std::cout << "Test 2: GET non-existent key" << std::endl;
    auto missing = store.get("notfound");
    assert(!missing.has_value());  // Should NOT have a value
    std::cout << "  ✓ GET notfound returned empty" << std::endl;
    
    // Test 3: Update existing key
    std::cout << "Test 3: Update existing key" << std::endl;
    store.set("name", "Bob");
    value = store.get("name");
    assert(value.value() == "Bob");
    std::cout << "  ✓ Updated name to Bob" << std::endl;
    
    // Test 4: EXISTS
    std::cout << "Test 4: EXISTS" << std::endl;
    assert(store.exists("name") == true);
    assert(store.exists("notfound") == false);
    std::cout << "  ✓ EXISTS works correctly" << std::endl;
    
    // Test 5: DELETE
    std::cout << "Test 5: DELETE" << std::endl;
    bool removed = store.remove("name");
    assert(removed == true);
    assert(store.exists("name") == false);
    std::cout << "  ✓ DELETE removed the key" << std::endl;
    
    // Test 6: Delete non-existent
    std::cout << "Test 6: DELETE non-existent" << std::endl;
    removed = store.remove("notfound");
    assert(removed == false);
    std::cout << "  ✓ DELETE on missing key returned false" << std::endl;
    
    // Test 7: SIZE
    std::cout << "Test 7: SIZE" << std::endl;
    store.set("key1", "value1");
    store.set("key2", "value2");
    assert(store.size() == 2);
    std::cout << "  ✓ Size is correct: " << store.size() << std::endl;
    
    // Test 8: CLEAR
    std::cout << "Test 8: CLEAR" << std::endl;
    store.clear();
    assert(store.size() == 0);
    assert(store.exists("key1") == false);
    std::cout << "  ✓ CLEAR removed all keys" << std::endl;
    
    std::cout << "\n✅ All tests passed!" << std::endl;
    
    return 0;
}
