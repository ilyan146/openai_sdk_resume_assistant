# List of params
playwright_params = {"command": "npx", "args": ["@playwright/mcp@latest"]}

# file_storage_path = os.path.abspath(os.path.join(os.getcwd(), "file_storage"))
# files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", file_storage_path]}

# send_email_params = {"command": "uv", "args": ["run", "agent_tools.py"]}

memory_params = {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": "file:./memory/ed.db"}}
