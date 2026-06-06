# light-obsidian-mcp

**Language / Язык:** [English](#english) | [Русский](#русский)

---

## English

MCP server for working with your Obsidian vault via Claude Desktop and other MCP-compatible clients.

### Tools

| Tool | Description |
|---|---|
| `read_note` | Read a note by relative path |
| `write_note` | Create or overwrite a note |
| `list_notes` | List `.md` files in a folder |
| `search_notes` | Full-text search across notes |

### Installation

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/)

Add to your Claude Desktop config:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["light-obsidian-mcp"],
      "env": {
        "OBSIDIAN_VAULT": "C:\\path\\to\\your\\obsidian\\vault"
      }
    }
  }
}
```

Replace `OBSIDIAN_VAULT` with the path to your vault and restart Claude Desktop.

---

## Русский

MCP-сервер для работы с Obsidian vault через Claude Desktop и другие MCP-совместимые клиенты.

### Инструменты

| Инструмент | Описание |
|---|---|
| `read_note` | Читает заметку по относительному пути |
| `write_note` | Создаёт или перезаписывает заметку |
| `list_notes` | Список `.md` файлов в папке |
| `search_notes` | Полнотекстовый поиск по содержимому |

### Установка

Требования: [uv](https://docs.astral.sh/uv/getting-started/installation/)

Добавьте в конфиг Claude Desktop:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["light-obsidian-mcp"],
      "env": {
        "OBSIDIAN_VAULT": "C:\\path\\to\\your\\obsidian\\vault"
      }
    }
  }
}
```

Замените `OBSIDIAN_VAULT` на путь к вашему vault и перезапустите Claude Desktop.
