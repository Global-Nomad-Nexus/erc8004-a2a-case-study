"""Check the public SVG gallery, provenance, links, and manuscript boundary.

Only the Python standard library is required. This verifies that figure values
have not drifted from their tracked source tables, rather than mirroring the
SVG drawing implementation with a second set of magic numbers.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "{http://www.w3.org/2000/svg}"
MD_FILES = [ROOT / name for name in ("README.md", "REPRODUCING.md", "RESULTS.md", "WORKFLOW.md", "figures/README.md")]
FORBIDDEN_EXTENSIONS = {".tex", ".bib", ".docx", ".pdf", ".rtf"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_figures() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/visualise/build_release_figures.py"), "--check"],
                   cwd=ROOT, check=True)
    manifest = json.loads((ROOT / "figures/manifest.json").read_text(encoding="utf-8"))
    entries = manifest["figures"]
    require(len(entries) == 4 and len({e["file"] for e in entries}) == 4,
            "expected four distinct SVG assets")
    for entry in entries:
        path = ROOT / "figures" / entry["file"]
        require(path.is_file() and path.suffix == ".svg", "missing vector asset")
        require(digest(path) == entry["svg_sha256"], f"SVG digest mismatch: {path.name}")
        tree = ET.parse(path)
        root = tree.getroot()
        require(root.tag == SVG_NS + "svg", f"invalid SVG root: {path.name}")
        require(root.find(SVG_NS + "title") is not None and root.find(SVG_NS + "desc") is not None,
                f"missing accessible title or description: {path.name}")
        require(len(root.findall(".//" + SVG_NS + "text")) >= 10,
                f"text should remain editable in the SVG: {path.name}")
        for forbidden in ("image", "foreignObject", "script", "iframe"):
            require(root.find(".//" + SVG_NS + forbidden) is None,
                    f"forbidden embedded or active asset in {path.name}")
        for element in root.iter():
            require(not any(key.endswith("}href") or key == "href" for key in element.attrib),
                    f"external reference in {path.name}")
        require(entry["alt_text"] and entry["interpretation_boundary"],
                f"missing figure description or boundary: {path.name}")
        for source in entry["inputs"]:
            relative = Path(source["path"])
            require(not relative.is_absolute() and ".." not in relative.parts,
                    "manifest input must stay within repository")
            require(digest(ROOT / relative) == source["sha256"],
                    f"source table drift: {relative}")


def verify_links() -> None:
    for doc in MD_FILES:
        text = doc.read_text(encoding="utf-8")
        for target in re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            require((doc.parent / target).exists(), f"broken relative link in {doc.relative_to(ROOT)}: {target}")


def verify_boundary() -> None:
    names = subprocess.run(["git", "ls-files", "--cached"], cwd=ROOT, check=True,
                           capture_output=True, text=True).stdout.splitlines()
    offending = [p for p in names if Path(p).suffix.lower() in FORBIDDEN_EXTENSIONS]
    require(not offending, f"manuscript/RTF files tracked: {offending}")


def main() -> int:
    verify_figures()
    verify_links()
    verify_boundary()
    print("PASS: SVG sources, digests, accessibility text, links, and manuscript boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
