#!/usr/bin/env python3
"""
Test client for MCP server - Manual JSON-RPC testing
Run this to verify your server is working correctly.
"""

import json
import subprocess
import sys
import os

def test_mcp_server():
    """Test MCP server with manual JSON-RPC calls."""
    
    server_path = os.path.join(os.path.dirname(__file__), "server.py")
    
    # Start server process
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("=" * 60)
    print("Testing MCP Server")
    print("=" * 60)
    
    try:
        # Test 1: Initialize
        print("\n1. Testing initialize...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        init_result = json.loads(response)
        print(f"✓ Initialize successful")
        print(f"  Server: {init_result.get('result', {}).get('serverInfo', {}).get('name')}")
        
        # Test 2: List tools
        print("\n2. Testing tools/list...")
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(list_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        list_result = json.loads(response)
        tools = list_result.get('result', {}).get('tools', [])
        print(f"✓ Found {len(tools)} tool(s):")
        for tool in tools:
            print(f"  - {tool.get('name')}: {tool.get('description')}")
        
        # Test 3: Call hello tool
        print("\n3. Testing tools/call (hello)...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "hello",
                "arguments": {
                    "name": "Developer"
                }
            }
        }
        
        process.stdin.write(json.dumps(call_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        call_result = json.loads(response)
        content = call_result.get('result', {}).get('content', [])
        if content:
            print(f"✓ Tool call successful:")
            print(f"  {content[0].get('text', '')}")
        
        print("\n" + "=" * 60)
        print("All tests passed! 🎉")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"Server stderr: {stderr_output}")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_mcp_server()

