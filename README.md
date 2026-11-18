# Čeština pro Orcu

Komunitní jazykový balíček, který přeloží rozhraní [Orcy](https://onorca.dev) do češtiny. Balíček obsahuje jen data (`"execution": "data"`), nespouští žádný kód.

## Instalace (lokálně, ze složky)

1. Stáhni nebo naklonuj tuto složku na disk, např. `~/Projekty/orca-czech`.
2. V Orce otevři **Settings → Plugins → Development** (Vývoj).
3. Klikni na **Add path** a zadej cestu ke složce `orca-czech` (tu, ve které je `orca-plugin.json`).
4. Potvrď kontrolu pluginu a zapni ho.
5. V nastavení jazyka Orcy vyber **Čeština**.

Klíče, které v balíčku chybí, Orca zobrazí anglicky. Bezpečnostní dialogy (instalace pluginů, potvrzení mazání apod.) Orca záměrně vždy zobrazuje v originále. Tyto texty balíček obsahovat nesmí, takže zůstanou anglicky.

## Obsah

| Soubor | Popis |
|---|---|
| `orca-plugin.json` | Manifest pluginu |
| `locales/cs.json` | Český katalog (stejná struktura jako anglický katalog Orcy) |
| `STYLE.md` | Styl překladu a slovník pojmů – závazné pro další úpravy |
| `tools/` | Skripty pro přípravu, kontrolu a aktualizaci překladu |

## Kontrola

```bash
python3 -I tools/assemble.py
```

Skript složí přeložené dávky z `work/`, zapíše `locales/cs.json` a zkontroluje pravidla Orcy: zachování proměnných `{{…}}` a značek `<…>`, délkový limit (max(64, 4× angličtina)), žádné přidané řádky, žádné řídicí znaky ani chráněné klíče, velikost do 5 MB.

## Aktualizace po nové verzi Orcy

1. Stáhni nový anglický katalog ze zdrojáků Orcy (`src/renderer/src/i18n/locales/en.json` v repozitáři stablyai/orca).
2. `python3 -I tools/update.py /cesta/k/en.json`: odstraní zastaralé překlady a uloží nový zdroj.
3. `python3 -I tools/prep.py 1 --missing-only`: vytvoří dávku jen s novými a změněnými texty.
4. Přelož `work/batch-00.json` do `work/out-00-01.json` (formát popisuje `tools/check_batch.py`), zkontroluj přes `python3 -I tools/check_batch.py 00`.
5. `python3 -I tools/assemble.py --merge` a zvyš `version` v `orca-plugin.json`.

## Zdroj překladu

Výchozí anglický katalog: stablyai/orca, commit `cd83a24` (18. 11. 2026). Překlad vznikl strojově s pomocí Claude podle `STYLE.md` a prochází lidskou revizí.

## Licence

MIT
