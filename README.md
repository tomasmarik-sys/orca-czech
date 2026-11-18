# Čeština pro Orcu

Komunitní jazykový balíček, který přeloží rozhraní [Orcy](https://onorca.dev) do češtiny. Balíček obsahuje jen data (`"execution": "data"`), nespouští žádný kód.

## Instalace z GitHubu

```bash
orca plugin install tomasmarik-sys/orca-czech
```

Nebo v Orce: **Settings → Plugins → Add plugin**, zvol instalaci z Gitu a zadej `tomasmarik-sys/orca-czech`. Orca nainstaluje nejnovější označenou verzi (tag `vX.Y.Z`). Balíček obsahuje jen překlady, takže se zapne bez schvalování. Pak v **Settings → Appearance → Language** vyber **čeština**.

## Instalace pro vývoj (ze složky)

1. Naklonuj repozitář na disk: `git clone https://github.com/tomasmarik-sys/orca-czech.git`.
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

Prověřená varování, která jsou v pořádku, jsou v `tools/lint-allow.json` a lint je už nehlásí. Po aktualizaci Orcy se tak ukážou jen nová. Když nová varování projdeš a jsou v pořádku, ulož je přes `python3 -I tools/lint.py --write-allow`.

### Git hook

Před každým commitem se spustí lint a `orca plugin validate`. Po naklonování ho zapni jednou příkazem:

```bash
git config core.hooksPath tools/hooks
```

### Ruční kontrola v Orce

Automaticky nejde poznat, jestli je text tlačítko, nebo stav („Otevřít“ × „Otevřený“), ani jestli se vejde. Po každé aktualizaci proto balíček načti (`orca plugin dev load .`), přepni Orcu do češtiny a projdi aspoň: hlavní okno a postranní panel, Úlohy (filtry), detail PR a issue, Automatizace, nastavení (Vzhled, Obecné, Agenti, Integrace), menu nové karty, prohlížeč a jeho menu, menu „…“ v průzkumníku a nativní menu aplikace. Hledej useknuté texty, slovesa na místě stavů a zbylou angličtinu mimo chráněné texty.

## Aktualizace po nové verzi Orcy

1. Stáhni anglický katalog vydané verze (tag, např. `v1.4.263`) i větve main ze zdrojáků Orcy (`src/renderer/src/i18n/locales/en.json` v repozitáři stablyai/orca, příkazy jsou v `tools/merge_en.py`) a slouč je: `python3 -I tools/merge_en.py en-release.json en-main.json en-merged.json`.
2. `python3 -I tools/update.py en-merged.json`: odstraní zastaralé překlady a uloží nový zdroj. Do `tools/protected-copy-keys.json` doplň chráněné klíče vydané Orcy (`/Applications/Orca.app/Contents/Resources/app.asar.unpacked/out/shared/plugins/languages/protected-copy-keys.json`) a překlady klíčů, které se tím staly chráněnými, z `locales/cs.json` odeber.
3. `python3 -I tools/prep.py 1 --missing-only`: vytvoří dávku jen s novými a změněnými texty.
4. Přelož `work/batch-00.json` do `work/out-00-01.json` (formát popisuje `tools/check_batch.py`), zkontroluj přes `python3 -I tools/check_batch.py 00`.
5. `python3 -I tools/assemble.py --merge` a zvyš `version` v `orca-plugin.json`.
6. `python3 -I tools/lint.py` a ruční kontrola v Orce (viz výše).

## Zdroj překladu

Anglický katalog (`tools/en.json`) je sloučení vydané Orcy `v1.4.263` a větve main (commit `d161ce3`, 18. 11. 2026) přes `tools/merge_en.py`. Texty z vydání mají přednost, klíče z main, které zatím nevyšly, jsou přeložené dopředu. Stejně tak `tools/protected-copy-keys.json` je sjednocení seznamu z main a z vydané Orcy. Překlad vznikl strojově s pomocí Claude podle `STYLE.md` a prochází lidskou revizí.

## Licence

MIT
