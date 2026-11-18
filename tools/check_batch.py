"""Kontrola přeložené dávky.

Použití: python3 -I tools/check_batch.py XX
Čte work/batch-XX.json a všechny work/out-XX-*.json (části se slučují).
Formát výstupu (JSON objekt id -> hodnota):
  text:   "překlad"  nebo  {"*": "výchozí překlad", "plný.klíč": "jiný překlad pro tento klíč"}
  plural: {"one": "...", "few": "...", "many": "...", "other": "..."}
Vypíše chybějící položky a problémy; návratový kód 0 = vše v pořádku.
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import CS_PLURALS, string_problems  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_out(nn):
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "work", f"out-{nn}-*.json"))):
        with open(path, encoding="utf-8") as f:
            try:
                merged.update(json.load(f))
            except json.JSONDecodeError as e:
                print(f"CHYBA JSON v {os.path.basename(path)}: {e}")
                sys.exit(2)
    return merged


def check(nn, quiet=False):
    with open(os.path.join(ROOT, "work", f"batch-{nn}.json"), encoding="utf-8") as f:
        batch = json.load(f)
    out = load_out(nn)
    ids = {it["id"] for it in batch}
    probs, missing = [], []
    for it in batch:
        v = out.get(it["id"])
        if v is None:
            missing.append(it["id"])
            continue
        if it["type"] == "text":
            if isinstance(v, str):
                probs += string_problems(it["id"], v, it["en"])
            elif isinstance(v, dict) and "*" in v:
                for k, s in v.items():
                    probs += string_problems(f"{it['id']}[{k}]", s, it["en"])
            else:
                probs.append(f"{it['id']}: text musí být řetězec nebo objekt s klíčem '*'")
        else:
            if not isinstance(v, dict) or set(v) != set(CS_PLURALS):
                probs.append(f"{it['id']}: plurál musí mít přesně klíče {CS_PLURALS}")
                continue
            for form in CS_PLURALS:
                src = it["en_one"] if form == "one" else it["en_other"]
                p = string_problems(f"{it['id']}.{form}", v[form], src)
                # {{count}} smí v 'one' chybět (anglické _one ho někdy nemá)
                probs += p
    extra = [k for k in out if k not in ids]
    if extra:
        probs.append(f"neznámá id: {extra[:10]}")
    if not quiet:
        print(f"dávka {nn}: {len(batch)} položek, přeloženo {len(batch) - len(missing)}, chybí {len(missing)}")
        if missing:
            print("chybí (prvních 30):", missing[:30])
        for p in probs[:80]:
            print("  -", p)
        if len(probs) > 80:
            print(f"  ... a dalších {len(probs) - 80}")
    return len(missing), len(probs)


if __name__ == "__main__":
    m, p = check(sys.argv[1])
    sys.exit(0 if m == 0 and p == 0 else 1)
