# Minimal MCP Server Boilerplate

A minimal Model Context Protocol (MCP) server implementation in Python for testing client-server communication.

## What This Does

This boilerplate provides the absolute minimum code needed to:
- ✅ Connect with MCP clients (Cursor, Claude Desktop, etc.)
- ✅ Respond to initialization requests
- ✅ List available tools
- ✅ Execute a simple "hello" tool

## Quick Start

### 1. Prerequisites

- Python 3.9 or higher
- No external dependencies required!

### 2. Test Locally

```bash
# Make server executable
chmod +x server.py

# Run the test client
python test_client.py
```

You should see:
```
============================================================
Testing MCP Server
============================================================

1. Testing initialize...
✓ Initialize successful
  Server: minimal-mcp-server

2. Testing tools/list...
✓ Found 1 tool(s):
  - hello: A simple hello tool to test MCP connection

3. Testing tools/call (hello)...
✓ Tool call successful:
  Hello, Developer! MCP connection is working! 🎉

============================================================
All tests passed! 🎉
============================================================
```

## Connecting to MCP Clients

### Cursor IDE

1. **Find your Cursor MCP config file:**
   - macOS: `~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
   - Windows: `%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
   - Linux: `~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

2. **Add this configuration** (update paths to match your system):
   ```json
   {
     "mcpServers": {
       "minimal-mcp-server": {
         "command": "python3",
         "args": ["/absolute/path/to/mcp-boilerplate/server.py"],
         "cwd": "/absolute/path/to/mcp-boilerplate"
       }
     }
   }
   ```

3. **Restart Cursor** and verify connection in settings

4. **Test:** Ask Cursor to "Call the hello tool with name 'YourName'"

### Claude Desktop

1. **Find Claude's config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the same configuration** as above

3. **Restart Claude Desktop**

4. **Test:** Ask Claude to use the hello tool

## Project Structure

```
mcp-boilerplate/
├── server.py          # Main MCP server implementation
├── test_client.py     # Local testing script
├── requirements.txt   # Dependencies (empty - uses stdlib)
├── mcp-config.json    # Example client configuration
└── README.md          # This file
```

## How It Works

### MCP Protocol Flow

1. **Initialize**: Client sends initialization request
   ```json
   {"method": "initialize", "params": {...}}
   ```

2. **List Tools**: Client requests available tools
   ```json
   {"method": "tools/list"}
   ```

3. **Call Tool**: Client executes a tool
   ```json
   {"method": "tools/call", "params": {"name": "hello", "arguments": {...}}}
   ```

### Key Components

- **`MinimalMCPServer`**: Main server class
- **`get_tools()`**: Returns tool definitions
- **`call_tool()`**: Executes tool logic
- **`handle_request()`**: Routes JSON-RPC requests
- **`run_stdio()`**: Main loop reading from stdin, writing to stdout

## Extending the Boilerplate

### Adding a New Tool

1. **Add tool definition** in `get_tools()`:
   ```python
   {
       "name": "my_tool",
       "description": "Does something useful",
       "inputSchema": {
           "type": "object",
           "properties": {
               "param": {"type": "string", "description": "..."}
           },
           "required": ["param"]
       }
   }
   ```

2. **Add handler** in `call_tool()`:
   ```python
   if name == "my_tool":
       result = do_something(arguments.get("param"))
       return {"type": "text", "text": result}
   ```

### Adding Dependencies

If you need external libraries:

1. Add to `requirements.txt`:
   ```
   requests>=2.31.0
   ```

2. Install:
   ```bash
   pip install -r requirements.txt
   ```

## Troubleshooting

**Server not connecting?**
- Verify Python path is correct in config
- Use absolute paths (not relative)
- Check file permissions (`chmod +x server.py`)

**"Method not found" errors?**
- Ensure method names match exactly (case-sensitive)
- Check JSON-RPC format is correct

**Server crashes?**
- Verify Python 3.9+ is installed
- Check for syntax errors: `python -m py_compile server.py`

## Next Steps

Once connection is verified:
- Add your custom tools
- Integrate with databases, APIs, or services
- Add error handling and logging
- Implement MCP resources and prompts

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Example Servers](https://github.com/modelcontextprotocol/servers)

## License

MIT License - feel free to use this boilerplate for your projects!

