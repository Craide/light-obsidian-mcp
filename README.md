# light-obsidian-mcp

[![PyPI version](https://img.shields.io/pypi/v/light-obsidian-mcp)](https://pypi.org/project/light-obsidian-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/light-obsidian-mcp)](https://pypi.org/project/light-obsidian-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Actions](https://github.com/Craide/light-obsidian-mcp/actions/workflows/publish.yml/badge.svg)](https://github.com/Craide/light-obsidian-mcp/actions)

MCP server for working with your Obsidian vault via Claude Desktop and other MCP-compatible clients.

### Why light-obsidian-mcp?

Unlike other Obsidian integrations, this server works **directly with the vault folder** on your file system:

- **No Obsidian plugins required** — nothing to install or configure inside Obsidian itself
- **Obsidian doesn't need to be running** — read and write notes at any time, even when the app is closed

### Tools

| Tool | Description |
|---|---|
| `read_note` | Read a note by relative path |
| `write_note` | Create or overwrite a note |
| `list_notes` | List `.md` files in a folder |
| `search_notes` | Full-text search across notes |
| `get_all_notes_content` | Return full content of all notes for analysis |
| `write_vault_index` | Generate and save vault description + tags table |
| `read_vault_index` | Read the saved vault description and tags |

### Installation

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/)

The example below shows setup for **Claude Desktop**, but the server works with any MCP-compatible client: Cursor, Windsurf, Zed, Continue, and others — the config format is the same.

Add to your Claude Desktop config:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["--python", "3.13", "light-obsidian-mcp"],
      "env": {
        "OBSIDIAN_VAULT": "C:\\path\\to\\your\\obsidian\\vault"
      }
    }
  }
}
```

Replace `OBSIDIAN_VAULT` with the path to your vault and restart your client.

---