#!/usr/bin/env python3
"""Confirm Cursor can resolve the team-marketplace catalog to the native plugin.

Schema validation does not require owner.name, does not join metadata.pluginRoot
with each plugin source, and does not check that the resolved native manifest
exists or that its name matches the catalog entry. Cursor cannot load a catalog
that misses those even when check-jsonschema passes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = Path(".cursor-plugin") / "marketplace.json"
NATIVE_PLUGIN = Path("plugins") / "valcraft" / ".cursor-plugin" / "plugin.json"


def source_starts_with_root(source: str, plugin_root: str) -> bool:
    source_parts = Path(source).parts
    root_parts = Path(plugin_root).parts
    return (
        len(source_parts) >= len(root_parts)
        and source_parts[: len(root_parts)] == root_parts
    )


def resolve_plugin_dir(plugin_root: str, source: str) -> Path:
    if source_starts_with_root(source, plugin_root):
        return Path(source)
    return Path(plugin_root) / source


def missing_text(value: object) -> bool:
    return not isinstance(value, str) or value == ""


def check(root: Path) -> list[str]:
    errors: list[str] = []
    marketplace_path = root / MARKETPLACE
    expected_plugin = (root / NATIVE_PLUGIN).resolve()
    try:
        catalog = json.loads(marketplace_path.read_text())
    except FileNotFoundError:
        return [f"{MARKETPLACE.as_posix()} does not exist"]
    except json.JSONDecodeError as error:
        return [f"{MARKETPLACE.as_posix()} is not valid JSON: {error}"]
    if not isinstance(catalog, dict):
        return [f"{MARKETPLACE.as_posix()} must be a JSON object"]

    owner = catalog.get("owner")
    owner_name = owner.get("name") if isinstance(owner, dict) else None
    if missing_text(owner_name):
        errors.append(f"{MARKETPLACE.as_posix()}: owner.name is missing")

    metadata = catalog.get("metadata")
    plugin_root = metadata.get("pluginRoot") if isinstance(metadata, dict) else None
    if missing_text(plugin_root):
        errors.append(f"{MARKETPLACE.as_posix()}: metadata.pluginRoot is missing")
        plugin_root = None

    if not expected_plugin.is_file():
        errors.append(f"{NATIVE_PLUGIN.as_posix()} does not exist")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{MARKETPLACE.as_posix()}: plugins is missing or empty")
        return errors
    if plugin_root is None:
        return errors

    for index, entry in enumerate(plugins):
        prefix = f"{MARKETPLACE.as_posix()} plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} is not an object")
            continue
        source = entry.get("source")
        name = entry.get("name")
        if missing_text(source):
            errors.append(f"{prefix}: source is missing")
            continue
        plugin_dir = resolve_plugin_dir(plugin_root, source)
        resolved = (root / plugin_dir / ".cursor-plugin" / "plugin.json").resolve()
        relative = (plugin_dir / ".cursor-plugin" / "plugin.json").as_posix()
        if not resolved.is_file():
            errors.append(f"{prefix}: {relative} does not exist")
            continue
        if resolved != expected_plugin:
            errors.append(f"{prefix}: {relative} is not {NATIVE_PLUGIN.as_posix()}")
            continue
        try:
            plugin = json.loads(resolved.read_text())
        except json.JSONDecodeError as error:
            errors.append(f"{NATIVE_PLUGIN.as_posix()} is not valid JSON: {error}")
            continue
        plugin_name = plugin.get("name") if isinstance(plugin, dict) else None
        if missing_text(name):
            errors.append(f"{prefix}: name is missing")
            continue
        if plugin_name != name:
            errors.append(
                f"{prefix}: name {name!r} does not match "
                f"{NATIVE_PLUGIN.as_posix()} name {plugin_name!r}"
            )
    return errors


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print("usage: check-cursor-marketplace.py [repository-root]", file=sys.stderr)
        return 2
    root = Path(argv[0]).resolve() if argv else DEFAULT_ROOT
    errors = check(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Cursor marketplace catalog resolves to " f"{NATIVE_PLUGIN.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
