"""Složí přeložené dávky do locales/cs.json a zkontroluje výsledek.

Použití: python3 -I tools/assemble.py [--merge]
--merge: přidá dávky k existujícímu locales/cs.json (po aktualizaci Orcy)
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import CS_PLURALS, flatten, is_protected, load_json, string_problems, unflatten  # noqa: E402
from check_batch import load_out  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
en = flatten(load_json(os.path.join(ROOT, "tools", "en.json")))

cs = {}
if "--merge" in sys.argv:
    cs = flatten(load_json(os.path.join(ROOT, "locales", "cs.json")))
missing_items = 0
for bpath in sorted(glob.glob(os.path.join(ROOT, "work", "batch-*.json"))):
    nn = re.search(r"batch-(\d+)", bpath).group(1)
    out = load_out(nn)
    for it in load_json(bpath):
        v = out.get(it["id"])
        if v is None:
            missing_items += 1
            continue
        if it["type"] == "text":
            keys = [k for k, val in en.items() if val == it["en"] and not is_protected(k)] if it.get("keys_total") else it["keys"]
            for k in keys:
                if isinstance(v, str):
                    cs[k] = v
                else:
                    cs[k] = v.get(k, v["*"])
        else:
            for form in CS_PLURALS:
                cs[f"{it['key']}_{form}"] = v[form]

# Ruční opravy (sjednocení terminologie)
overrides_path = os.path.join(ROOT, "tools", "overrides.json")
if os.path.exists(overrides_path):
    for k, v in load_json(overrides_path).items():
        if k.startswith("_"):
            continue
        if k not in en and re.sub(r"_(one|few|many|other)$", "_other", k) not in en:
            print(f"VAROVÁNÍ: override pro neexistující klíč {k}")
        if v is None:
            cs.pop(k, None)
        else:
            cs[k] = v

# Kontrola proti angličtině (pravidla Orcy)
problems = []
for k, v in cs.items():
    src = en.get(k)
    if src is None:
        base = re.sub(r"_(zero|one|two|few|many|other)$", "", k)
        src = en.get(f"{base}_other", en.get(base))
        if k.endswith("_one") and f"{base}_one" in en:
            src = en[f"{base}_one"]
    if is_protected(k):
        problems.append(f"{k}: chráněný klíč")
    problems += string_problems(k, v, src)

catalog = unflatten(cs)
os.makedirs(os.path.join(ROOT, "locales"), exist_ok=True)
with open(os.path.join(ROOT, "locales", "cs.json"), "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)
    f.write("\n")

translatable = [k for k in en if not is_protected(k)]
covered = sum(1 for k in translatable if k in cs or re.sub(r"_(one|other)$", "_other", k) in cs)
size = os.path.getsize(os.path.join(ROOT, "locales", "cs.json"))
print(f"záznamů v cs.json: {len(cs)}, velikost {size / 1024 / 1024:.2f} MB (limit 5 MB)")
print(f"pokrytí přeložitelných anglických klíčů: {covered}/{len(translatable)} = {100 * covered // len(translatable)} %")
print(f"nepřeložené položky dávek: {missing_items}")
print(f"problémů: {len(problems)}")
for p in problems[:50]:
    print("  -", p)
sys.exit(0 if not problems and size <= 5 * 1024 * 1024 else 1)
