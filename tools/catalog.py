"""Společné funkce pro český jazykový balíček Orcy.

Pravidla kontroly kopírují zdroják Orcy (src/shared/plugins/languages/*,
src/shared/plugins/artifacts/plugin-language-pack-artifact.ts):
- chráněné klíče (bezpečnostní texty) se nepřekládají,
- délka překladu <= max(64, 4 x délka angličtiny), nejvýš 8192 znaků,
- žádný nový řádek, pokud ho nemá angličtina,
- žádné řídicí ani bidi znaky,
- klíče bez teček a bez __proto__/prototype/constructor.
Navíc hlídáme shodu proměnných {{x}}, {x}, HTML/React značek <x>, </x>, <x/> a entit.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PLURAL_RE = re.compile(r"_(zero|one|two|few|many|other)$")
CS_PLURALS = ("one", "few", "many", "other")
PH_RE = re.compile(r"\{\{[^{}]*\}\}|\{[A-Za-z0-9_]+\}|</?[A-Za-z][\w.-]*\s*/?>|<\d+\s*/?>|</\d+>|&[a-z]+;|\$t\([^)]*\)")
BIDI_RE = re.compile("[؜‎‏‪-‮⁦-⁩]")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def flatten(obj, prefix="", out=None):
    out = {} if out is None else out
    for k, v in obj.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            flatten(v, p, out)
        else:
            out[p] = v
    return out


def unflatten(flat):
    root = {}
    for path in sorted(flat):
        node = root
        parts = path.split(".")
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = flat[path]
    return root


_protected = None


def _load_protected():
    global _protected
    if _protected is None:
        data = load_json(os.path.join(HERE, "protected-copy-keys.json"))
        with open(os.path.join(HERE, "translatable-chrome.txt"), encoding="utf-8") as f:
            chrome = {l.strip() for l in f if l.strip()}
        _protected = (set(data["keys"]), list(data["prefixes"]), chrome)
    return _protected


def is_protected(path):
    keys, prefixes, chrome = _load_protected()
    if any(path.startswith(p) for p in prefixes):
        return True
    cand = path
    while cand:
        if cand in keys or PLURAL_RE.sub("", cand) in keys:
            return True
        cand = cand.rpartition(".")[0]
    root = "auto.components.settings."
    if path.startswith(root) and path not in chrome:
        if re.match(r"plugin", path[len(root):], re.I):
            return True
    return False


def placeholders(s):
    return sorted(PH_RE.findall(s))


def string_problems(path, value, en):
    """Vrátí seznam problémů jednoho překladu (prázdný = v pořádku)."""
    probs = []
    if not isinstance(value, str):
        return [f"{path}: hodnota není text"]
    if not value.strip():
        probs.append(f"{path}: prázdný překlad")
    for ch in value:
        c = ord(ch)
        if (c <= 0x1F and c != 0x0A) or 0x7F <= c <= 0x9F or c in (0x2028, 0x2029, 0xFEFF):
            probs.append(f"{path}: zakázaný řídicí znak U+{c:04X}")
            break
    if BIDI_RE.search(value):
        probs.append(f"{path}: bidi znak")
    if en is not None:
        if "\n" in value and "\n" not in en:
            probs.append(f"{path}: přidaný nový řádek")
        limit = min(8192, max(64, 4 * len(en)))
        if len(value) > limit:
            probs.append(f"{path}: příliš dlouhé ({len(value)} > {limit})")
        a, b = placeholders(en), placeholders(value)
        if a != b:
            probs.append(f"{path}: nesedí proměnné/značky EN={a} CS={b}")
    elif len(value) > 8192:
        probs.append(f"{path}: příliš dlouhé")
    return probs
