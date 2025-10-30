# Key-Value Store Protocol Specification

## Overview
This document describes the text-based protocol for communication between the Python client and C++ server.

## Transport
- **Protocol**: TCP/IP
- **Default Port**: 8080
- **Encoding**: UTF-8
- **Message Delimiter**: Newline (`\n`)

## Message Format

### Client Requests
All client requests follow this format:
```
COMMAND key [value]\n
```

- `COMMAND`: Uppercase command name
- `key`: The key to operate on (no spaces allowed)
- `value`: Optional value (only for SET command)
- Each message must end with a newline character

### Server Responses
All server responses are single lines:
```
STATUS [data]\n
```

- `STATUS`: Either `OK` or `ERROR`
- `data`: Optional data depending on the command

## Commands

### SET
Stores a key-value pair.

**Request:**
```
SET key value\n
```

**Success Response:**
```
OK\n
```

**Example:**
```
Client: SET username Alice\n
Server: OK\n
```

### GET
Retrieves the value for a given key.

**Request:**
```
GET key\n
```

**Success Response:**
```
OK value\n
```

**Error Response:**
```
ERROR KEY_NOT_FOUND\n
```

**Example:**
```
Client: GET username\n
Server: OK Alice\n
```

### DELETE
Removes a key-value pair.

**Request:**
```
DELETE key\n
```

**Success Response:**
```
OK\n
```

**Error Response:**
```
ERROR KEY_NOT_FOUND\n
```

**Example:**
```
Client: DELETE username\n
Server: OK\n
```

### EXISTS
Checks if a key exists in the store.

**Request:**
```
EXISTS key\n
```

**Success Response:**
```
OK 1\n  (key exists)
OK 0\n  (key does not exist)
```

**Example:**
```
Client: EXISTS username\n
Server: OK 1\n
```

## Error Codes

| Error Code | Description |
|------------|-------------|
| `KEY_NOT_FOUND` | The requested key does not exist |
| `INVALID_COMMAND` | Unknown or malformed command |
| `MISSING_ARGUMENTS` | Required arguments not provided |

## Protocol Limitations

This is a simple protocol with known limitations:

1. **Keys and values cannot contain spaces** - Space is used as a delimiter
2. **Keys and values cannot contain newlines** - Newline marks end of message
3. **No binary data support** - Text only
4. **No authentication** - Anyone who can connect has full access
5. **No encryption** - All data transmitted in plain text
6. **Single-threaded** - Server handles one request at a time (initially)

## Future Enhancements

Possible improvements for later:
- Length-prefixed messages to support spaces and newlines
- Authentication tokens
- TLS/SSL encryption
- Batch operations
- TTL (time-to-live) for keys
- Pub/sub capabilities

## Testing with Command Line

You can test the server manually using `netcat`:
```bash
nc localhost 8080
SET test hello
OK
GET test
OK hello
```
