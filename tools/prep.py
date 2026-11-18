"""Rozdělí anglický katalog na dávky k překladu.

Použití: python3 -I tools/prep.py [počet_dávek] [--missing-only]
--missing-only: jen klíče, které v locales/cs.json chybí (po aktualizaci Orcy)
Výstup: work/batch-XX.json  (seznam položek)
Položka:
  {"id": "s00042", "type": "text",   "en": "...", "keys": ["a.b.c", ...]}
  {"id": "p00007", "type": "plural", "en_one": "...", "en_other": "...", "key": "a.b.count"}
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import PLURAL_RE, flatten, is_protected, load_json  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
missing_only = "--missing-only" in sys.argv
n_batches = int(args[0]) if args else 14

en = flatten(load_json(os.path.join(ROOT, "tools", "en.json")))
keys = [k for k in en if not is_protected(k) and isinstance(en[k], str)]
if missing_only:
    have = set(flatten(load_json(os.path.join(ROOT, "locales", "cs.json"))))
    keys = [k for k in keys if k not in have and PLURAL_RE.sub("_one", k) not in have]
    print("chybějících klíčů k překladu:", len(keys))
print("klíčů celkem", len(en), "chráněných", len(en) - len(keys))

plural_bases = {}
texts = {}
for k in keys:
    m = PLURAL_RE.search(k)
    if m:
        plural_bases.setdefault(PLURAL_RE.sub("", k), {})[m.group(1)] = en[k]
    else:
        texts.setdefault(en[k], []).append(k)

items = []
for i, (val, ks) in enumerate(texts.items()):
    items.append({"id": f"s{i:05d}", "type": "text", "en": val, "keys": ks, "_sort": min(ks)})
for i, (base, forms) in enumerate(plural_bases.items()):
    items.append({
        "id": f"p{i:05d}", "type": "plural", "key": base,
        "en_one": forms.get("one", forms.get("other")), "en_other": forms.get("other", forms.get("one")),
        "_sort": base,
    })
items.sort(key=lambda it: it["_sort"])


def size(it):
    return len(it.get("en", "")) + len(it.get("en_one", "")) + len(it.get("en_other", "")) + 40


total = sum(size(it) for it in items)
target = total / n_batches
os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
batch, acc, idx = [], 0, 0


def flush():
    global batch, acc, idx
    for it in batch:
        it.pop("_sort", None)
        if it["type"] == "text" and len(it["keys"]) > 6:
            it["keys_total"] = len(it["keys"])
            it["keys"] = it["keys"][:6]
    with open(os.path.join(ROOT, "work", f"batch-{idx:02d}.json"), "w", encoding="utf-8") as f:
        json.dump(batch, f, ensure_ascii=False, indent=1)
    print(f"batch-{idx:02d}: {len(batch)} položek, {acc} znaků")
    batch, acc, idx = [], 0, idx + 1


for it in items:
    batch.append(it)
    acc += size(it)
    if acc >= target and idx < n_batches - 1:
        flush()
if batch:
    flush()
print("položek", len(items), "textů", len(texts), "plurálů", len(plural_bases))
