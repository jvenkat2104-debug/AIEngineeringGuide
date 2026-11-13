"""Project the maintained Markdown into a generated Zensical input directory."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tmp" / "web-docs"
REPO = "https://github.com/jvenkat2104-debug/jvenkat2104-debug.github.io/blob/main/"

def destination(source):
    if source.is_relative_to(ROOT / "content"):
        relative = source.relative_to(ROOT / "content")
    elif source.is_relative_to(ROOT / "downloads"):
        relative = source.relative_to(ROOT)
    else:
        return None
    if relative.name == "README.md":
        relative = relative.with_name("index.md")
    relative = Path(relative.as_posix().replace("/05-technical-grinding/", "/tools/").replace("/06-industry-tours/", "/industry-visits/"))
    return OUT / relative

def rewrite(source, text):
    def replace(match):
        label, link = match.groups()
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
            return match.group(0)
        path, sep, anchor = link.partition("#")
        resolved = (source.parent / path).resolve()
        if not resolved.exists():
            raise ValueError(f"Missing source link: {source.relative_to(ROOT)} -> {link}")
        target = destination(resolved)
        if target is None:
            relative = resolved.relative_to(ROOT).as_posix()
            new = REPO + relative
        else:
            import os
            new = Path(os.path.relpath(target, destination(source).parent)).as_posix()
        return f"[{label}]({new}{sep}{anchor})"
    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", replace, text)

def main():
    # Only clear the generated tree, and confirm it is within this workspace.
    assert OUT.resolve().is_relative_to((ROOT / "tmp").resolve())
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    sources = sorted((ROOT / "content").rglob("*.md")) + sorted((ROOT / "downloads").glob("*.md"))
    for source in sources:
        target = destination(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        text = rewrite(source, source.read_text(encoding="utf-8"))
        target.write_text(text, encoding="utf-8")
    historical = {"Engineering_Branch_Selection_Guide.pdf", "Campus_to_Corporate_Blueprint.pdf"}
    for source in (ROOT / "downloads").glob("*.pdf"):
        if source.name in historical:
            continue  # Preserve source editions in GitHub, outside the published site.
        shutil.copy2(source, OUT / "downloads" / source.name)
    shutil.copy2(ROOT / "downloads" / "canteen-starter.zip", OUT / "downloads" / "canteen-starter.zip")
    shutil.copytree(ROOT / "site" / "assets", OUT / "assets", dirs_exist_ok=True)
    print(f"Prepared {len(sources)} Markdown pages and PDF downloads in {OUT}")

if __name__ == "__main__":
    main()
