"""Připraví překlad po aktualizaci Orcy.

Použití: python3 -I tools/update.py /cesta/k/novemu/en.json
Nový en.json je ve zdrojácích Orcy: src/renderer/src/i18n/locales/en.json

Co dělá:
1. porovná nový anglický katalog s tools/en.json,
2. z locales/cs.json odstraní překlady klíčů, které zmizely nebo jejichž angličtina se změnila,
3. uloží nový tools/en.json.
Pak spusť:  python3 -I tools/prep.py 1 --missing-only   (dávky jen s novými texty)
            ... přelož work/batch-*.json ...
            python3 -I tools/assemble.py --merge
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import flatten, load_json, unflatten  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PL = re.compile(r"_(zero|one|two|few|many|other)$")

old = flatten(load_json(os.path.join(ROOT, "tools", "en.json")))
new = flatten(load_json(sys.argv[1]))
cs_path = os.path.join(ROOT, "locales", "cs.json")
cs = flatten(load_json(cs_path))


def source(flat, k):
    if k in flat:
        return flat[k]
    base = PL.sub("", k)
    return flat.get(f"{base}_other", flat.get(base))


added = [k for k in new if k not in old]
changed = [k for k in new if k in old and new[k] != old[k]]
removed = [k for k in old if k not in new]
stale = [k for k in cs if source(new, k) is None or source(new, k) != source(old, k)
         or (k.endswith("_one") and new.get(k) != old.get(k))]
for k in stale:
    del cs[k]
with open(cs_path, "w", encoding="utf-8") as f:
    json.dump(unflatten(cs), f, ensure_ascii=False, indent=2)
    f.write("\n")
shutil.copyfile(sys.argv[1], os.path.join(ROOT, "tools", "en.json"))
print(f"nové klíče {len(added)}, změněné {len(changed)}, odstraněné {len(removed)}")
print(f"z cs.json odebráno zastaralých překladů: {len(stale)}")
print("Další krok: python3 -I tools/prep.py 1 --missing-only")
