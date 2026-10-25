#!/usr/bin/env python3
"""Validate the Grok Build plugin before it is pinned into the xAI catalog.

Checks the things that are cheap here and expensive to find in review:
manifest shape, MCP transport, skill frontmatter, the zenrows-* namespace
rule, and that every skill a skill points at actually exists.

Run: python3 scripts/validate-plugin.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".grok-plugin" / "plugin.json"
MCP = ROOT / ".mcp.json"
SKILLS = ROOT / "skills"

REQUIRED_MANIFEST_KEYS = [
    "name", "version", "description", "author",
    "repository", "homepage", "license", "keywords",
]
# xAI pushes generic keywords back: they drive the plugin CTA and mis-fire it.
GENERIC_KEYWORDS = {
    "web-scraping", "scraping", "web scraping", "data-extraction", "crawl",
    "browser-automation", "mcp", "api", "cli", "proxy", "deploy", "database",
}
REQUIRED_FILES = ["README.md", "CHANGELOG.md", "LICENSE", "assets/logo.png"]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
BACKTICKED = re.compile(r"`(zenrows(?:-[a-z-]+)?)`")
# Names from the Claude/Copilot plugins that must not survive the port.
LEGACY_NAMES = [
    "scrape-webpage", "extract-structured-data", "browser-automation",
    "capture-api-calls", "using-zenrows", "getting-started",
]


def frontmatter_field(text: str, field: str) -> str | None:
    m = FRONTMATTER.match(text)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if line.startswith(f"{field}:"):
            return line.split(":", 1)[1].strip().strip("'\"")
    return None


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    # --- manifest -----------------------------------------------------
    try:
        manifest = json.loads(MANIFEST.read_text())
    except Exception as e:
        print(f"FAIL: {MANIFEST.name}: {e}", file=sys.stderr)
        return 1

    for key in REQUIRED_MANIFEST_KEYS:
        if not manifest.get(key):
            errors.append(f"plugin.json: missing or empty `{key}`")
    if manifest.get("name") != "zenrows":
        errors.append(f"plugin.json: name must be 'zenrows', got {manifest.get('name')!r}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        errors.append(f"plugin.json: version {manifest.get('version')!r} is not x.y.z")
    hit = GENERIC_KEYWORDS.intersection(k.lower() for k in manifest.get("keywords", []))
    if hit:
        errors.append(
            f"plugin.json: keywords must be brand-scoped; generic terms found: {sorted(hit)}"
        )

    # --- mcp ----------------------------------------------------------
    try:
        mcp = json.loads(MCP.read_text())
    except Exception as e:
        print(f"FAIL: {MCP.name}: {e}", file=sys.stderr)
        return 1

    servers = mcp.get("mcpServers", {})
    if list(servers) != ["zenrows"]:
        errors.append(f".mcp.json: expected exactly one server 'zenrows', got {list(servers)}")
    else:
        srv = servers["zenrows"]
        if srv.get("type") != "http":
            errors.append(f".mcp.json: transport must be 'http', got {srv.get('type')!r}")
        if not str(srv.get("url", "")).startswith("https://"):
            errors.append(f".mcp.json: url must be https, got {srv.get('url')!r}")
        for forbidden in ("command", "args", "env"):
            if forbidden in srv:
                errors.append(f".mcp.json: hosted server must not declare `{forbidden}`")

    # --- skills -------------------------------------------------------
    dirs = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    names: set[str] = set()
    for d in dirs:
        md = SKILLS / d / "SKILL.md"
        if not md.is_file():
            errors.append(f"skills/{d}: no SKILL.md")
            continue
        text = md.read_text()
        name = frontmatter_field(text, "name")
        desc = frontmatter_field(text, "description")
        if not name:
            errors.append(f"skills/{d}: frontmatter has no `name`")
            continue
        names.add(name)
        if name != d:
            errors.append(f"skills/{d}: frontmatter name {name!r} does not match directory")
        if not (name == "zenrows" or name.startswith("zenrows-")):
            errors.append(f"skills/{d}: name {name!r} is outside the zenrows-* namespace")
        if not desc:
            errors.append(f"skills/{d}: frontmatter has no `description`")
        for legacy in LEGACY_NAMES:
            if re.search(rf"(?<![-a-z]){re.escape(legacy)}(?![-a-z])", text):
                errors.append(f"skills/{d}: leftover pre-port skill name {legacy!r}")

    for d in dirs:
        md = SKILLS / d / "SKILL.md"
        if not md.is_file():
            continue
        for ref in set(BACKTICKED.findall(md.read_text())):
            if ref not in names:
                errors.append(f"skills/{d}: references `{ref}`, which is not a skill here")

    if errors:
        print("Plugin validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"Plugin OK: {len(dirs)} skills, 1 mcpServer (http), version {manifest['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
