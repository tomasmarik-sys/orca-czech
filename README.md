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

Ruční opravy jednotlivých klíčů patří do `tools/overrides.json` (hodnota `null` klíč vynechá). Po úpravě spusť `python3 -I tools/assemble.py --merge`.

```bash
python3 -I tools/lint.py            # --verbose vypíše všechna varování
```

Lint kontroluje hotový `locales/cs.json`. **Chyby** (blokují commit): pravidla Orcy, chráněné klíče, vykání, trojtečka jinak než v angličtině, neúplný plurál, záměna Remove/Delete („Odebrat“/„Smazat“), override neprojevený v `cs.json`. **Varování** (k ruční kontrole): klíče chráněné v nainstalované Orce, stejný překlad pro různé texty v jedné komponentě, předložka před názvem aplikace nebo služby („v {{app}}“), víceslovný text shodný s angličtinou.

### Git hook

Před každým commitem se spustí lint a `orca plugin validate`. Po naklonování ho zapni jednou příkazem:

```bash
git config core.hooksPath tools/hooks
```

### Ruční kontrola v Orce

Automaticky nejde poznat, jestli je text tlačítko, nebo stav („Otevřít“ × „Otevřený“), ani jestli se vejde. Po každé aktualizaci proto balíček načti (`orca plugin dev load .`), přepni Orcu do češtiny a projdi aspoň: hlavní okno a postranní panel, Úlohy (filtry), detail PR a issue, Automatizace, nastavení (Vzhled, Obecné, Agenti, Integrace), menu nové karty, prohlížeč a jeho menu, menu „…“ v průzkumníku a nativní menu aplikace. Hledej useknuté texty, slovesa na místě stavů a zbylou angličtinu mimo chráněné texty.

## Aktualizace po nové verzi Orcy

1. Stáhni nový anglický katalog ze zdrojáků Orcy (`src/renderer/src/i18n/locales/en.json` v repozitáři stablyai/orca).
2. `python3 -I tools/update.py /cesta/k/en.json`: odstraní zastaralé překlady a uloží nový zdroj.
3. `python3 -I tools/prep.py 1 --missing-only`: vytvoří dávku jen s novými a změněnými texty.
4. Přelož `work/batch-00.json` do `work/out-00-01.json` (formát popisuje `tools/check_batch.py`), zkontroluj přes `python3 -I tools/check_batch.py 00`.
5. `python3 -I tools/assemble.py --merge` a zvyš `version` v `orca-plugin.json`.
6. `python3 -I tools/lint.py` a ruční kontrola v Orce (viz výše).

## Zdroj překladu

Výchozí anglický katalog: stablyai/orca, commit `cd83a24` (18. 11. 2026). Překlad vznikl strojově s pomocí Claude podle `STYLE.md` a prochází lidskou revizí.

## Licence

MIT
