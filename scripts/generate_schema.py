#!/usr/bin/env python3
"""
Generate `src/datamaker/generated/schema.py` from `spec/openapi.json`.

WHY THIS EXISTS: every route method in this package used to be annotated
`-> Dict`, which tells a type checker nothing and an IDE less. The API's own
OpenAPI document already describes 209 of its 240 operations precisely, so the
shapes are generated from it rather than hand-copied - the same arrangement
`datamaker-js` uses. Hand-copied types are how an SDK drifts behind its API.

Two flags matter for the drift check to mean anything:

  --disable-timestamp   the default header stamps the generation time, so two
                        runs of the same input would differ and `--check` would
                        fail every time.
  a pinned generator    output is only reproducible for a fixed version, so CI
                        installs the same one this file names.

Usage:
    python scripts/generate_schema.py            # write the file
    python scripts/generate_schema.py --check    # fail if it is stale
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.json"
OUT = ROOT / "src" / "datamaker" / "generated" / "schema.py"
ALIASES = ROOT / "src" / "datamaker" / "types.py"

# Pinned: the generator's output is only byte-stable for a fixed version, and
# an unpinned bump would surface as a mysterious CI failure on an unrelated PR.
GENERATOR = "datamodel-code-generator==0.71.0"

# `typing.TypedDict` rather than pydantic on purpose. The client returns
# `response.json()` - plain dicts - so these annotate what is already there
# instead of changing what callers receive at runtime. Existing code that does
# `project["name"]` keeps working; it just gets checked now.
ARGS = [
    "--input-file-type",
    "openapi",
    "--output-model-type",
    "typing.TypedDict",
    "--target-python-version",
    "3.11",
    "--disable-timestamp",
    "--use-standard-collections",
    "--use-union-operator",
]


def generate(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "uvx",
            "--from",
            GENERATOR,
            "datamodel-codegen",
            "--input",
            str(SPEC),
            "--output",
            str(destination),
            *ARGS,
        ],
        check=True,
    )


# Names that cannot be recovered, with the reason. `allOf` composition (zod's
# `.extend()`) is merged away by the generator rather than emitted as a class,
# and a schema used only inside a union never gets one either. Listed here so
# the gap is explicit; the audit fails if this list grows.
KNOWN_UNRECOVERABLE = {
    "SetDetail": "allOf composition (Set + createdByName) is merged away",
    "PackInstallListItem": "allOf composition (PackInstall + installedByName)",
    "SchemaGraphNavigation": "only referenced inside a union; no standalone class",
}


def write_aliases(schema_path: Path, aliases_path: Path) -> list[str]:
    """Map each spec schema name to the generated class that really matches it.

    The generator gives inline path/property schemas priority for a bare name,
    so `components.schemas.Plan` can land as `Plan1` while an unrelated nested
    object takes `Plan`. Silently importing the wrong one is precisely the
    "wrong type that type-checks" failure this package exists to avoid, so the
    mapping is derived by comparing KEY SETS against the spec on every run and
    the numbering never reaches hand-written code.
    """
    spec = json.loads(SPEC.read_text())
    comps = spec["components"]["schemas"]
    src = schema_path.read_text()
    blocks = dict(re.findall(r"^class (\w+)\(TypedDict\):\n((?:    .*\n)+)", src, re.M))
    keys = {n: set(re.findall(r"^    (\w+):", b, re.M)) for n, b in blocks.items()}
    plain = set(re.findall(r"^(\w+): TypeAlias", src, re.M))

    lines, missing = [], []
    for name in sorted(comps):
        want = set((comps[name].get("properties") or {}).keys())
        if not want:
            if name in blocks or name in plain:
                lines.append(f"{name} = _s.{name}")
            else:
                missing.append(name)
            continue
        exact = [c for c, k in keys.items() if k == want]
        if len(exact) == 1:
            lines.append(f"{name} = _s.{exact[0]}")
        elif name in exact:
            lines.append(f"{name} = _s.{name}")
        else:
            missing.append(name)

    unexpected = sorted(set(missing) - set(KNOWN_UNRECOVERABLE))
    if unexpected:
        print(
            "\nThese spec schemas no longer map to a uniquely-matching generated "
            "class:\n  " + "\n  ".join(unexpected) +
            "\n\nEither the spec changed shape or the generator's naming did. Do NOT "
            "\npaper over it by picking a numbered class by hand - confirm which class "
            "\nreally matches, then update KNOWN_UNRECOVERABLE or fix the spec.\n",
            file=sys.stderr,
        )
        raise SystemExit(1)

    body = [
        '"""Spec schema names, resolved to the classes the generator produced.',
        "",
        "Generated by scripts/generate_schema.py - do not edit by hand.",
        "",
        "Import types from HERE, not from `generated.schema`: the generator lets an",
        "inline schema take a bare name like `Plan` and renames the real component to",
        "`Plan1`, so the numbering is not stable across spec changes. This module is",
        "re-derived by matching key sets against the spec on every generation.",
        '"""',
        "",
        "from .generated import schema as _s",
        "",
    ]
    for name, why in sorted(KNOWN_UNRECOVERABLE.items()):
        body.append(f"# {name}: {why}")
    body.append("")
    body.extend(lines)
    body.append("")
    aliases_path.write_text("\n".join(body))
    return missing


def main() -> int:
    if not SPEC.exists():
        print(f"missing {SPEC.relative_to(ROOT)}", file=sys.stderr)
        return 1

    check = "--check" in sys.argv

    if not check:
        generate(OUT)
        missing = write_aliases(OUT, ALIASES)
        classes = OUT.read_text().count("(TypedDict):")
        exported = ALIASES.read_text().count(" = _s.")
        print(
            f"wrote {OUT.relative_to(ROOT)} ({classes} TypedDicts) and "
            f"{ALIASES.relative_to(ROOT)} ({exported} names, {len(missing)} unrecoverable)"
        )
        return 0

    if not OUT.exists():
        print(
            "src/datamaker/generated/schema.py is missing.\n"
            "Run `python scripts/generate_schema.py` and commit it.",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        fresh_path = Path(tmp) / "schema.py"
        generate(fresh_path)
        fresh_aliases = Path(tmp) / "types.py"
        write_aliases(fresh_path, fresh_aliases)
        if (
            fresh_path.read_text() != OUT.read_text()
            or fresh_aliases.read_text() != ALIASES.read_text()
        ):
            print(
                "\nsrc/datamaker/generated/schema.py is stale or hand-edited.\n"
                "Run `python scripts/generate_schema.py` and commit the result.\n"
                "These types are generated from spec/openapi.json - editing them\n"
                "by hand puts the SDK back to describing an API that has moved on.\n",
                file=sys.stderr,
            )
            return 1

    print("generated types match the spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
