#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "life-os-schema.yaml"
DIST = ROOT / "dist"
SITE = ROOT / "site"

TYPE_MAP = {
    "string": {"type": "string"},
    "date": {"type": "string", "format": "date"},
    "number": {"type": "number"},
    "boolean": {"type": "boolean"},
    "array": {"type": "array"},
    "string_or_array": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
    "string_or_number": {"oneOf": [{"type": "string"}, {"type": "number"}]},
    "number_or_false": {"oneOf": [{"type": "number"}, {"const": False}]},
}


def load_schema():
    return yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))


def json_schema_for_contract(schema: dict) -> dict:
    props = {}
    required = []
    enums = schema.get("enums", {})
    for group in ("core_fields", "context_fields"):
        for name, spec in (schema.get(group) or {}).items():
            typ = spec.get("type", "string") if isinstance(spec, dict) else "string"
            prop = dict(TYPE_MAP.get(typ, {"type": "string"}))
            if isinstance(spec, dict):
                if spec.get("items"):
                    prop.setdefault("type", "array")
                    prop["items"] = {"type": spec["items"]}
                if spec.get("enum") and spec["enum"] in enums:
                    values = enums[spec["enum"]]
                    prop["enum"] = [v.get("value") if isinstance(v, dict) else v for v in values]
                if spec.get("description"):
                    prop["description"] = spec["description"]
                if spec.get("required") or spec.get("required_new"):
                    required.append(name)
            props[name] = prop
    props["type"] = {"type": "string", "enum": sorted(schema.get("types", {}).keys())}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://viggomeesters.github.io/vault-schema/vault-schema.schema.json",
        "title": "Vault Schema Note Frontmatter",
        "description": "JSON Schema export generated from life-os-schema.yaml for public-safe note frontmatter validation.",
        "type": "object",
        "required": sorted(set(required)),
        "properties": props,
        "additionalProperties": True,
    }


def markdown_tables(schema: dict) -> str:
    lines = [
        "# Generated Schema Reference",
        "",
        "Generated from `life-os-schema.yaml`. Do not edit by hand; run `make generate`.",
        "",
        f"Schema version: `{schema.get('version')}`  ",
        f"Updated: `{schema.get('updated')}`",
        "",
        "## Folders",
        "",
        "| Folder | Structure | Purpose |",
        "| --- | --- | --- |",
    ]
    for folder, spec in (schema.get("folders") or {}).items():
        lines.append(f"| `{folder}` | `{spec.get('structure', '')}` | {spec.get('purpose', '')} |")
    lines += ["", "## Types", "", "| Type | Location | Filename | Categories |", "| --- | --- | --- | --- |"]
    for name, spec in (schema.get("types") or {}).items():
        cats = ", ".join((spec.get("categories") or {}).keys())
        lines.append(f"| `{name}` | `{spec.get('location')}` | `{spec.get('filename')}` | {cats} |")
    lines += ["", "## Context fields", "", "| Field | Type | Required new | Description |", "| --- | --- | --- | --- |"]
    for name, spec in (schema.get("context_fields") or {}).items():
        lines.append(f"| `{name}` | `{spec.get('type')}` | `{bool(spec.get('required_new'))}` | {spec.get('description','')} |")
    return "\n".join(lines) + "\n"


def site_index(schema: dict) -> str:
    types = schema.get("types", {})
    rows = "\n".join(
        f"<tr><td><code>{name}</code></td><td><code>{spec.get('location')}</code></td><td>{len(spec.get('categories') or {})}</td></tr>"
        for name, spec in types.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vault Schema v{schema.get('version')}</title>
  <meta name="description" content="Machine-readable vault schema contract for structured Obsidian vaults.">
  <style>
    body {{ font-family: Inter, ui-sans-serif, system-ui, sans-serif; margin: 0; background: #0b1020; color: #e5edf8; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 48px 24px 80px; }}
    .hero {{ border: 1px solid #24324d; border-radius: 28px; padding: 34px; background: linear-gradient(135deg,#111a2e,#0b1020); }}
    h1 {{ font-size: clamp(2.4rem, 8vw, 5rem); margin: 0 0 12px; }}
    p {{ color: #a7b3c8; line-height: 1.6; }}
    a {{ color: #5eead4; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 28px; background: #111a2e; border-radius: 18px; overflow: hidden; }}
    th,td {{ padding: 14px 16px; border-bottom: 1px solid #24324d; text-align: left; }}
    th {{ color: #93c5fd; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap: 14px; margin: 26px 0; }}
    .card {{ padding: 18px; border: 1px solid #24324d; border-radius: 18px; background:#111a2e; }}
    .big {{ font-size: 2rem; font-weight: 800; color:#f8fafc; }}
  </style>
</head>
<body><main>
  <section class="hero">
    <h1>Vault Schema</h1>
    <p>Machine-readable vault contract for structured Obsidian vaults. YAML source, generated JSON Schema, templates, synthetic examples, and public-safe validation gates.</p>
    <p><a href="https://github.com/viggomeesters/vault-schema">GitHub</a> · <a href="vault-schema.schema.json">JSON Schema</a> · <a href="generated-schema-reference.md">Generated reference</a></p>
  </section>
  <section class="cards">
    <div class="card"><div class="big">v{schema.get('version')}</div><p>Schema version</p></div>
    <div class="card"><div class="big">{len(types)}</div><p>Note types</p></div>
    <div class="card"><div class="big">{len(schema.get('folders') or {})}</div><p>Top folders</p></div>
  </section>
  <table><thead><tr><th>Type</th><th>Location</th><th>Categories</th></tr></thead><tbody>{rows}</tbody></table>
</main></body></html>"""


def main() -> None:
    schema = load_schema()
    DIST.mkdir(exist_ok=True)
    SITE.mkdir(exist_ok=True)
    json_schema = json_schema_for_contract(schema)
    (DIST / "vault-schema.schema.json").write_text(json.dumps(json_schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "docs" / "generated-schema-reference.md").write_text(markdown_tables(schema), encoding="utf-8")
    (SITE / "index.html").write_text(site_index(schema), encoding="utf-8")
    (SITE / "vault-schema.schema.json").write_text(json.dumps(json_schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (SITE / "generated-schema-reference.md").write_text((ROOT / "docs" / "generated-schema-reference.md").read_text(encoding="utf-8"), encoding="utf-8")
    print(f"generated artifacts for schema v{schema.get('version')}")


if __name__ == "__main__":
    main()
