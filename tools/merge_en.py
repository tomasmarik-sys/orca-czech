"""Sloučí anglický katalog vydané Orcy s katalogem z větve main.

Použití: python3 -I tools/merge_en.py VYDANI.json MAIN.json VYSTUP.json

Balíček má sedět na Orcu, kterou lidé opravdu používají (vydání), ale hodí se mít
přeložené i klíče z main, které teprve vyjdou. Proto:
- základem jsou všechny klíče z main,
- klíče z vydání mají přednost (jejich angličtina se zobrazuje teď),
- klíče, které jsou jen ve vydání, se přidají.
Výstup pak předej tools/update.py.

Stažení obou katalogů (gh CLI):
  gh api "repos/stablyai/orca/contents/src/renderer/src/i18n/locales/en.json?ref=v1.4.263" \\
    -H "Accept: application/vnd.github.raw" > en-release.json
  gh api "repos/stablyai/orca/contents/src/renderer/src/i18n/locales/en.json?ref=main" \\
    -H "Accept: application/vnd.github.raw" > en-main.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import flatten, load_json  # noqa: E402

if len(sys.argv) != 4:
    sys.exit(__doc__)
release_path, main_path, out_path = sys.argv[1:]
release_tree = load_json(release_path)
merged = load_json(main_path)
release = flatten(release_tree)
main = flatten(merged)

for path, value in release.items():
    node = merged
    parts = path.split(".")
    for part in parts[:-1]:
        nxt = node.get(part)
        if not isinstance(nxt, dict):
            nxt = node[part] = {}
        node = nxt
    node[parts[-1]] = value

only_release = [k for k in release if k not in main]
differs = [k for k in release if k in main and release[k] != main[k]]
only_main = [k for k in main if k not in release]
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"klíčů celkem {len(flatten(merged))}: jen ve vydání {len(only_release)}, "
      f"jinak ve vydání (použito vydání) {len(differs)}, jen v main {len(only_main)}")
