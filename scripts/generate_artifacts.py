#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "vault-schema.json"
LEGACY_YAML_PATH = ROOT / "life-os-schema.yaml"
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


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def dump_legacy_yaml(schema: dict) -> None:
    LEGACY_YAML_PATH.write_text(
        yaml.safe_dump(schema, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )



def update_versions(schema: dict) -> None:
    path = ROOT / "versions.json"
    versions = json.loads(path.read_text(encoding="utf-8"))
    versions.update({
        "schema": f"v{schema.get('version')}",
        "version": str(schema.get("version")),
        "updated": str(schema.get("updated")),
        "types": len(schema.get("types") or {}),
        "templates": len([p for p in (ROOT / "templates").rglob("*") if p.is_file()]),
        "source": "vault-schema.json",
        "legacy_yaml": "life-os-schema.yaml",
        "schema_sha256": hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(),
        "legacy_yaml_sha256": hashlib.sha256(LEGACY_YAML_PATH.read_bytes()).hexdigest(),
    })
    path.write_text(json.dumps(versions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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
    type_names = sorted(schema.get("types", {}).keys())
    props["type"] = {"type": "string", "enum": type_names}
    conditionals = []
    for note_type, spec in sorted((schema.get("types") or {}).items()):
        categories = sorted((spec.get("categories") or {}).keys())
        then_schema = {"properties": {"category": {"type": "string", "enum": categories}}}
        category_conditionals = []
        for category in categories:
            allowed_areas = (((schema.get("type_category_area") or {}).get(note_type) or {}).get(category) or {}).get("allowed_areas") or []
            if allowed_areas:
                category_conditionals.append({
                    "if": {"properties": {"category": {"const": category}}, "required": ["category"]},
                    "then": {"properties": {"area": {"type": "string", "enum": sorted(allowed_areas)}}},
                })
        if category_conditionals:
            then_schema["allOf"] = category_conditionals
        conditionals.append({
            "if": {"properties": {"type": {"const": note_type}}, "required": ["type"]},
            "then": then_schema,
        })
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://viggomeesters.github.io/vault-schema/vault-schema.schema.json",
        "title": "Vault Schema Note Frontmatter",
        "description": "JSON Schema export generated from canonical vault-schema.json for public-safe note frontmatter validation.",
        "type": "object",
        "required": sorted(set(required)),
        "properties": props,
        "allOf": conditionals,
        "additionalProperties": True,
    }


def markdown_tables(schema: dict) -> str:
    lines = [
        "# Generated Schema Reference",
        "",
        "Generated from canonical `vault-schema.json`. Do not edit by hand; run `make generate`.",
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
  <meta name="description" content="Machine-readable JSON vault schema contract for structured agent-readable vaults.">
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
    <p>Machine-readable JSON vault contract for structured agent-readable vaults. JSON canonical source, generated JSON Schema, legacy YAML export, templates, synthetic examples, and public-safe validation gates.</p>
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
    docs_dir = ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)
    dump_legacy_yaml(schema)
    update_versions(schema)
    json_schema = json_schema_for_contract(schema)
    json_schema_text = json.dumps(json_schema, indent=2, ensure_ascii=False) + "\n"
    generated_reference = markdown_tables(schema)
    site_html = site_index(schema)

    (DIST / "vault-schema.schema.json").write_text(json_schema_text, encoding="utf-8")
    (docs_dir / "generated-schema-reference.md").write_text(generated_reference, encoding="utf-8")

    (SITE / "index.html").write_text(site_html, encoding="utf-8")
    (SITE / "vault-schema.schema.json").write_text(json_schema_text, encoding="utf-8")
    (SITE / "generated-schema-reference.md").write_text(generated_reference, encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")

    (docs_dir / "index.html").write_text(site_html, encoding="utf-8")
    (docs_dir / "vault-schema.schema.json").write_text(json_schema_text, encoding="utf-8")
    (docs_dir / ".nojekyll").write_text("", encoding="utf-8")
    print(f"generated artifacts for schema v{schema.get('version')}")


if __name__ == "__main__":
    main()
