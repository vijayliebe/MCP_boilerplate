#!/usr/bin/env python3
"""
Minimal MCP Server - Basic boilerplate for testing connection
This is a minimal implementation to verify MCP client-server communication.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List

class MinimalMCPServer:
    def __init__(self):
        self.name = "minimal-mcp-server"
        self.version = "1.0.0"
    
    def get_tools(self) -> List[Dict]:
        """Return available tools."""
        return [
            {
                "name": "test_mcp_call",
                "description": "A simple hello tool to test MCP connection",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name to greet"
                        }
                    },
                    "required": ["name"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict:
        """Handle tool calls."""
        if name == "test_mcp_call":
            greeting = f"Hello, {arguments.get('name', 'World')}! MCP connection is working! 🎉"
            return {
                "type": "text",
                "text": greeting
            }
        else:
            return {
                "type": "text",
                "text": f"Unknown tool: {name}"
            }
    
    async def handle_request(self, request: Dict) -> Dict:
        """Handle MCP JSON-RPC requests."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        # Build base response
        def build_response(result=None, error=None):
            response = {"jsonrpc": "2.0"}
            if request_id is not None:
                response["id"] = request_id
            if result is not None:
                response["result"] = result
            if error is not None:
                response["error"] = error
            return response
        
        try:
            if method == "initialize":
                return build_response(result={
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version
                    }
                })
            
            elif method == "tools/list":
                return build_response(result={
                    "tools": self.get_tools()
                })
            
            elif method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                result = await self.call_tool(name, arguments)
                
                return build_response(result={
                    "content": [result]
                })
            
            else:
                return build_response(error={
                    "code": -32601,
                    "message": f"Method not found: {method}"
                })
                
        except Exception as e:
            return build_response(error={
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            })
    
    async def run_stdio(self):
        """Run the server using stdio transport."""
        while True:
            request = None
            request_id = None
            try:
                # Read JSON-RPC request from stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                request = json.loads(line.strip())
                request_id = request.get("id")
                response = await self.handle_request(request)
                
                # Write JSON-RPC response to stdout
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                # For parse errors, id must be null per JSON-RPC 2.0 spec
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                # If request was parsed, use its id; otherwise omit id field
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                # Only include id if request had an id (don't set to null)
                if request_id is not None:
                    error_response["id"] = request_id
                print(json.dumps(error_response), flush=True)

async def main():
    """Main entry point."""
    server = MinimalMCPServer()
    await server.run_stdio()

if __name__ == "__main__":
    asyncio.run(main())

