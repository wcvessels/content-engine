#!/usr/bin/env python3
"""Pin the versioned manifest seam: a manifest validates against the pinned
schema whose `schema_version` const matches the manifest's own value. The
accepted set is {1.0, 1.1}; any other version fails loud.

This is the proof for that seam, not the gate itself (the gate is described in
each lane's stages/01-ingest/CONTEXT.md). Assert-based, no framework.

    python test_manifest_versions.py        # needs `jsonschema`
"""
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve().parent              # _standards/schema/
SAMPLES = HERE.parent.parent / "samples"            # repo-root/samples/

# The accepted set: schema_version -> the pinned schema that owns that version.
SCHEMAS = {
    "1.0": HERE / "manifest-1.0.schema.json",
    "1.1": HERE / "manifest-1.1.schema.json",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validator_for(version):
    """The seam rule: pick the pinned schema whose const matches the manifest's
    own schema_version. A version outside the accepted set fails loud."""
    if version not in SCHEMAS:
        raise ValueError(
            f"unsupported schema_version {version!r}; accepted: {sorted(SCHEMAS)}"
        )
    return Draft202012Validator(load(SCHEMAS[version]))


def is_valid(manifest, version):
    try:
        validator_for(version).validate(manifest)
        return True
    except ValidationError:
        return False


# Each pinned schema's const matches the key it is filed under (no mislabel).
for ver, path in SCHEMAS.items():
    assert load(path)["properties"]["schema_version"]["const"] == ver, (
        f"{path.name}: const != {ver}"
    )

# Check 1: every committed sample passes the pinned schema its own
# schema_version names. The committed set is a mix (3x 1.0, 1x 1.1), so this
# also proves both pinned schemas accept real engine output.
samples = sorted(SAMPLES.glob("*_manifest.json"))
assert samples, "no sample manifests found under samples/"
seen = set()
for s in samples:
    m = load(s)
    ver = m["schema_version"]
    assert ver in SCHEMAS, f"{s.name}: schema_version {ver!r} not in accepted set {sorted(SCHEMAS)}"
    assert is_valid(m, ver), f"{s.name}: failed its own pinned schema {ver}"
    seen.add(ver)
assert seen == {"1.0", "1.1"}, f"committed samples cover {sorted(seen)}, expected both 1.0 and 1.1"

# Check 2: synthesize a 1.1 manifest from a real 1.0 sample (bump the version,
# drop contactsheet_jpg) and confirm it PASSES 1.1 and FAILS 1.0. Proves
# per-version pinning, not a blanket pass. The reverse also holds: the real 1.0
# sample FAILS the 1.1 schema.
base10 = next(load(s) for s in samples if load(s)["schema_version"] == "1.0")
m11 = copy.deepcopy(base10)
m11["schema_version"] = "1.1"
del m11["artifacts"]["contactsheet_jpg"]
assert is_valid(m11, "1.1"), "1.1 fixture must pass manifest-1.1"
assert not is_valid(m11, "1.0"), "1.1 fixture must FAIL manifest-1.0"
assert not is_valid(base10, "1.1"), "a real 1.0 manifest must FAIL manifest-1.1"

# Check 3: a version outside the accepted set fails loud.
try:
    validator_for("9.9")
    raise AssertionError("bogus schema_version 9.9 must fail loud")
except ValueError:
    pass

print(
    f"OK: {len(samples)} sample(s) valid against their pinned schema; "
    f"1.1 accepted, 1.1-vs-1.0 and 1.0-vs-1.1 rejected, bogus 9.9 rejected."
)
