import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

vault_path = os.environ.get("OBSIDIAN_VAULT")
if not vault_path:
    raise RuntimeError("OBSIDIAN_VAULT environment variable is not set. Specify the vault path in your Claude Desktop config.")
VAULT = Path(vault_path)

mcp = FastMCP("vault")


# ---------------------------------------------------------------------------
# Basic note operations
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Vault index  (core/description.md + core/tags.md)
# ---------------------------------------------------------------------------

@mcp.tool()
def get_all_notes_content() -> str:
    """Return the full content of every note in the vault.
    Use this before calling write_vault_index to analyse the vault."""
    parts = []
    for p in sorted(VAULT.rglob("*.md")):
        rel = str(p.relative_to(VAULT))
        text = p.read_text(encoding="utf-8", errors="ignore")
        parts.append(f"### {rel}\n{text}")
    return "\n\n---\n\n".join(parts) if parts else "No notes found"


@mcp.tool()
def write_vault_index(description: str, tags: str) -> str:
    """Save the vault index: description and tags table.
    Always call get_all_notes_content first, analyse the notes, then pass:
      - description: a brief summary of what this vault is about
      - tags: a markdown table of all tags found across notes with short descriptions

    Saves to:
      core/description.md
      core/tags.md
    """
    core = VAULT / "core"
    core.mkdir(parents=True, exist_ok=True)

    (core / "description.md").write_text(description, encoding="utf-8")
    (core / "tags.md").write_text(tags, encoding="utf-8")

    return "Saved: core/description.md and core/tags.md"


@mcp.tool()
def read_vault_index() -> str:
    """Read the vault index: description and tags table from core/."""
    desc_path = VAULT / "Core" / "Description.md"
    tags_path = VAULT / "Core" / "Tags.md"

    if not desc_path.exists() and not tags_path.exists():
        return "Vault index not found. Generate it first with write_vault_index."

    parts = []
    if desc_path.exists():
        parts.append(f"## Description\n\n{desc_path.read_text(encoding='utf-8')}")
    if tags_path.exists():
        parts.append(f"## Tags\n\n{tags_path.read_text(encoding='utf-8')}")

    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
