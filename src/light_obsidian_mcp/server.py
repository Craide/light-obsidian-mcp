import os
import shutil
import yaml
from pathlib import Path
from mcp.server.fastmcp import FastMCP

vault_path = os.environ.get("OBSIDIAN_VAULT")
if not vault_path:
    raise RuntimeError("OBSIDIAN_VAULT environment variable is not set. Specify the vault path in your Claude Desktop config.")
VAULT = Path(vault_path)

mcp = FastMCP("vault")


def _safe_path(path: str) -> Path | None:
    """Resolve path and verify it stays within the vault. Returns None if outside."""
    full = (VAULT / path).resolve()
    if not full.is_relative_to(VAULT.resolve()):
        return None
    return full


@mcp.tool()
def read_note(path: str) -> str:
    """Read a note from the vault. path — relative path, e.g. concepts/zettelkasten.md"""
    full = _safe_path(path)
    if full is None:
        return "Access denied: path is outside the vault"
    if not full.exists():
        return f"File not found: {path}"
    return full.read_text(encoding="utf-8")


@mcp.tool()
def write_note(path: str, content: str) -> str:
    """Create or overwrite a note in the vault."""
    full = _safe_path(path)
    if full is None:
        return "Access denied: path is outside the vault"
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    return f"Saved: {path}"


@mcp.tool()
def move_note(src: str, dst: str) -> str:
    """Move or rename a note within the vault.
    src — current relative path, dst — new relative path.
    e.g. move_note('inbox/idea.md', 'concepts/idea.md')"""
    src_path = _safe_path(src)
    dst_path = _safe_path(dst)
    if src_path is None or dst_path is None:
        return "Access denied: path is outside the vault"
    if not src_path.exists():
        return f"File not found: {src}"
    if not src_path.is_file():
        return f"Not a file: {src}"
    if dst_path.exists():
        return f"Already exists: {dst}"
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_path), str(dst_path))
    return f"Moved: {src} → {dst}"


@mcp.tool()
def list_notes(folder: str = "") -> str:
    """List .md files in a vault folder. folder — relative path, empty = root."""
    target = _safe_path(folder) if folder else VAULT.resolve()
    if target is None:
        return "Access denied: path is outside the vault"
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


@mcp.tool()
def delete_note(path: str) -> str:
    """Delete a note from the vault. path — relative path, e.g. concepts/zettelkasten.md"""
    full = _safe_path(path)
    if full is None:
        return "Access denied: path is outside the vault"
    if not full.exists():
        return f"File not found: {path}"
    if not full.is_file():
        return f"Not a file: {path}"
    full.unlink()
    return f"Deleted: {path}"


@mcp.tool()
def get_frontmatter(path: str) -> str:
    """Read YAML frontmatter from a note. Returns metadata fields like tags, date, author, etc.
    Returns empty if the note has no frontmatter."""
    full = _safe_path(path)
    if full is None:
        return "Access denied: path is outside the vault"
    if not full.exists():
        return f"File not found: {path}"
    text = full.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return "No frontmatter found"
    try:
        end = text.index("---", 3)
        raw = text[3:end].strip()
        data = yaml.safe_load(raw)
        return yaml.dump(data, allow_unicode=True, sort_keys=False)
    except Exception as e:
        return f"Failed to parse frontmatter: {e}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
