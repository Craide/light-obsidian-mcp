import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

vault_path = os.environ.get("OBSIDIAN_VAULT")
if not vault_path:
    raise RuntimeError("OBSIDIAN_VAULT environment variable is not set. Specify the vault path in your Claude Desktop config.")
VAULT = Path(vault_path)

mcp = FastMCP("vault")

@mcp.tool()
def read_note(path: str) -> str:
    """Read a note from the vault. path — relative path, e.g. concepts/zettelkasten.md"""
    full = VAULT / path
    if not full.exists():
        return f"File not found: {path}"
    return full.read_text(encoding="utf-8")

@mcp.tool()
def write_note(path: str, content: str) -> str:
    """Create or overwrite a note in the vault."""
    full = VAULT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    return f"Saved: {path}"

@mcp.tool()
def list_notes(folder: str = "") -> str:
    """List .md files in a vault folder. folder — relative path, empty = root."""
    target = VAULT / folder
    if not target.exists():
        return f"Folder not found: {folder}"
    files = [str(p.relative_to(VAULT)) for p in target.rglob("*.md")]
    return "\n".join(files) if files else "No files found"

@mcp.tool()
def search_notes(query: str) -> str:
    """Search notes by content."""
    results = []
    for p in VAULT.rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if query.lower() in text.lower():
            results.append(str(p.relative_to(VAULT)))
    return "\n".join(results) if results else "Nothing found"

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
