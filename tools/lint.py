"""Kontrola hotového locales/cs.json: technická pravidla Orcy + styl podle STYLE.md.

Použití: python3 -I tools/lint.py [--verbose] [--orca /Applications/Orca.app] [--write-allow]
Návratový kód: 0 = bez chyb (varování nevadí), 1 = chyby.

CHYBY (blokují commit):
  - technická pravidla Orcy (proměnné, délka, nové řádky, řídicí znaky)
  - chráněné klíče (seznam balíčku i seznam nainstalované Orcy, pokud je k dispozici)
  - vykání
  - trojtečka „…“ / „...“ jinak než v angličtině
  - neúplný plurál (chybí některý z tvarů one/few/many/other)
  - Remove → „Smazat…“, Delete → „Odebrat…“
  - override z tools/overrides.json není v cs.json (zapomenuté assemble.py --merge)
VAROVÁNÍ (k ruční kontrole):
  - různé anglické texty ve stejné komponentě se stejným překladem
  - předložka před proměnnou s názvem aplikace/služby („v {{app}}“)
  - víceslovný text shodný s angličtinou
Prověřená varování jsou v tools/lint-allow.json a nehlásí se; --write-allow je tam zapíše všechna aktuální.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalog import CS_PLURALS, PLURAL_RE, flatten, is_protected, load_json, string_problems  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBOSE = "--verbose" in sys.argv
ORCA_APP = "/Applications/Orca.app"
if "--orca" in sys.argv:
    ORCA_APP = sys.argv[sys.argv.index("--orca") + 1]
LIVE_PROTECTED = os.path.join(
    ORCA_APP, "Contents/Resources/app.asar.unpacked/out/shared/plugins/languages/protected-copy-keys.json"
)

en = flatten(load_json(os.path.join(ROOT, "tools", "en.json")))
cs = flatten(load_json(os.path.join(ROOT, "locales", "cs.json")))
overrides = {k: v for k, v in load_json(os.path.join(ROOT, "tools", "overrides.json")).items() if not k.startswith("_")}

errors = collections.defaultdict(list)
warnings = collections.defaultdict(list)


def source_for(k):
    if k in en:
        return en[k]
    base = PLURAL_RE.sub("", k)
    if k.endswith("_one") and f"{base}_one" in en:
        return en[f"{base}_one"]
    return en.get(f"{base}_other", en.get(base))


def is_plural(k):
    return bool(PLURAL_RE.search(k))


# --- technická pravidla a chráněné klíče -------------------------------------
live = None
if os.path.exists(LIVE_PROTECTED):
    data = load_json(LIVE_PROTECTED)
    live = (set(data["keys"]), list(data.get("prefixes", [])))


def live_protected(k):
    keys, prefixes = live
    if any(k.startswith(p) for p in prefixes):
        return True
    c = k
    while c:
        if c in keys or PLURAL_RE.sub("", c) in keys:
            return True
        c = c.rpartition(".")[0]
    return False


for k, v in cs.items():
    src = source_for(k)
    if src is None:
        errors["klíč, který v anglickém katalogu neexistuje"].append(k)
        continue
    for p in string_problems(k, v, src):
        errors["pravidla Orcy"].append(p)
    if is_protected(k):
        errors["chráněný klíč (seznam balíčku)"].append(k)
    elif live and live_protected(k):
        warnings["chráněný v nainstalované Orce (zobrazí se anglicky)"].append((k, k))

# --- vykání ------------------------------------------------------------------
VY_RE = re.compile(r"\b(Vy|vy|vás|vám|vámi|váš|vaše|vaši|vašeho|vašem|vašich)\b|\b[a-zá-ž]{3,}(ete|ěte|íte|ujte)\b", re.I)
VY_OK = {"komplete", "athlete", "delete", "complete", "obsolete", "concrete", "paste"}
for k, v in cs.items():
    for m in VY_RE.finditer(re.sub(r"\{\{[^}]*\}\}|`[^`]*`", "", v)):
        if m.group(0).lower() not in VY_OK:
            errors["vykání (STYLE.md: vždy tykat)"].append(f"{k}: „{m.group(0)}“ v „{v[:70]}“")
            break

# --- trojtečka -----------------------------------------------------------------
for k, v in cs.items():
    src = source_for(k) or ""
    if ("…" in src) != ("…" in v) or ("..." in src) != ("..." in v):
        errors["trojtečka jinak než v angličtině"].append(f"{k}: „{src[:40]}“ → „{v[:40]}“")

# --- plurály -----------------------------------------------------------------
bases = {PLURAL_RE.sub("", k) for k in cs if is_plural(k)}
for b in sorted(bases):
    missing = [f for f in CS_PLURALS if f"{b}_{f}" not in cs]
    if missing:
        errors["neúplný plurál"].append(f"{b}: chybí {', '.join(missing)}")

# --- Odebrat / Smazat ----------------------------------------------------------
for k, v in cs.items():
    src = source_for(k) or ""
    if re.match(r"(?i)remove\b", src) and re.match(r"(?i)smaz", v):
        errors["Remove přeloženo jako Smazat"].append(f"{k}: „{src[:40]}“ → „{v[:40]}“")
    if re.match(r"(?i)delete\b", src) and re.match(r"(?i)odebr", v):
        errors["Delete přeloženo jako Odebrat"].append(f"{k}: „{src[:40]}“ → „{v[:40]}“")

# --- overrides musí být v cs.json -----------------------------------------------
for k, v in overrides.items():
    if v is None and k in cs:
        errors["override null, ale klíč v cs.json je (spusť assemble.py --merge)"].append(k)
    elif v is not None and cs.get(k) != v:
        errors["override se liší od cs.json (spusť assemble.py --merge)"].append(k)

# --- varování: stejný překlad pro různé texty v jedné komponentě ---------------


def norm(s):
    s = re.sub(r"\{\{[^}]*\}\}", "", s.lower()).strip().rstrip(".…?!:")
    return " ".join(w[:-1] if w.endswith("s") and len(w) > 3 else w for w in s.split())


groups = collections.defaultdict(lambda: collections.defaultdict(set))
for k, v in cs.items():
    if k in en and not is_plural(k) and len(en[k]) <= 40:
        groups[k.rpartition(".")[0]][v].add(norm(en[k]))
for parent, by_cs in groups.items():
    for v, ens in by_cs.items():
        if len(ens) > 1:
            warnings["stejný překlad pro různé texty v jedné komponentě"].append((f"{parent} = {v}", f"{parent}: „{v}“ ← {sorted(ens)}"))

# --- varování: předložka před názvem aplikace ------------------------------------
APP_VAR = r"\{\{(app|appName|editor|ide|browser|source|tool|provider|service|integration)\}\}"
PREP_RE = re.compile(r"(?<![\w{])(v|ve|s|se|z|ze|k|ke|do|na|pro) " + APP_VAR)
for k, v in cs.items():
    if PREP_RE.search(v):
        warnings["předložka před názvem aplikace/služby (skloňování, „v VS Code“)"].append((k, f"{k}: „{v[:70]}“"))

# --- varování: text shodný s angličtinou -----------------------------------------
CODEISH = re.compile(r"[`$@{}<>=/\\;|]|^\s*(git|gh|npm|pnpm|yarn|orca|claude|codex|cd|ls)\b|--\w")
for k, v in cs.items():
    if k in en and v == en[k] and re.search(r"[A-Za-z]{3,} [a-z]{3,}", v) and not CODEISH.search(v):
        warnings["víceslovný text shodný s angličtinou"].append((k, f"{k}: „{v[:60]}“"))

# --- výstup --------------------------------------------------------------------


def report(title, bucket, limit):
    for cat, items in bucket.items():
        print(f"{title} {cat}: {len(items)}")
        for it in items[: (None if VERBOSE else limit)]:
            print(f"    {it}")
        if not VERBOSE and len(items) > limit:
            print(f"    … a dalších {len(items) - limit} (--verbose)")


# --- prověřená varování (tools/lint-allow.json) -----------------------------------
ALLOW_PATH = os.path.join(ROOT, "tools", "lint-allow.json")
if "--write-allow" in sys.argv:
    allow_out = {cat: sorted(i for i, _ in items) for cat, items in warnings.items()}
    with open(ALLOW_PATH, "w", encoding="utf-8") as f:
        json.dump({"_poznamka": "Prověřená varování lintu, která jsou v pořádku. Nová varování se hlásí dál. "
                   "Přegenerování: python3 -I tools/lint.py --write-allow (jen po ruční kontrole!)", **allow_out},
                  f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"zapsáno {sum(len(v) for v in allow_out.values())} prověřených varování do tools/lint-allow.json")
allowed = {}
if os.path.exists(ALLOW_PATH):
    allowed = {k: set(v) for k, v in load_json(ALLOW_PATH).items() if not k.startswith("_")}
n_allowed = 0
for cat in list(warnings):
    keep = [(i, m) for i, m in warnings[cat] if i not in allowed.get(cat, set())]
    n_allowed += len(warnings[cat]) - len(keep)
    warnings[cat] = [m for _, m in keep]
    if not warnings[cat]:
        del warnings[cat]
stale = sum(len(v) for v in allowed.values()) - n_allowed

print(f"lint cs.json: {len(cs)} záznamů" + ("" if live else f" (Orca v {ORCA_APP} nenalezena, kontrola proti ní vynechána)"))
report("CHYBA", errors, 20)
report("varování", warnings, 5)
n_err = sum(len(v) for v in errors.values())
print(f"prověřená varování (tools/lint-allow.json): {n_allowed}" + (f", zastaralých položek: {stale}" if stale else ""))
print("výsledek:", "OK" if not n_err else f"{n_err} chyb")
sys.exit(1 if n_err else 0)
