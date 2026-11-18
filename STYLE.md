# Čeština pro Orcu – styl a slovník pojmů

Platí pro `locales/cs.json`. Chybějící klíče Orca zobrazí anglicky. Bezpečnostní texty (chráněné klíče) překládat nelze, Orca je vždy ukáže v originále.

## Hlas a oslovení

- Kde to jde, uživatele neoslovuj. Použij neutrální formulaci: `Vybrat větev`, `Žádné worktree nenalezeny`, `Soubor se nepodařilo uložit.`
- Pokud věta oslovení potřebuje, **tykej** důsledně: `Připoj se k hostiteli a zkus to znovu.`, `tvůj účet`, `Chceš pokračovat?` Nikdy nevykej.
- Tlačítka, položky menu a příkazy jsou v **infinitivu**: `Otevřít`, `Uložit`, `Smazat`, `Odebrat`, `Zkusit znovu`, `Zrušit`, `Kopírovat`.
- Chybové hlášky ve větě: `… se nepodařilo načíst.`, v krátkém štítku `Načtení selhalo`.
- Potvrzovací dotazy jsou neosobní otázky: `Zavřít okno?`, `Smazat worktree?`
- Stavové štítky jako přídavné jméno nebo příčestí ve správném rodě: `Připojeno`, `Nepřipojeno`, `Probíhá…`, `Hotovo`.
- „Loading…“ → `Načítání…`, „Saving…“ → `Ukládání…`, „Searching…“ → `Hledání…`.

## Typografie

- Čeština nemá title case. Velké písmeno jen na začátku a u vlastních jmen: „Open Recent Projects“ → `Otevřít nedávné projekty`.
- Štítky, tlačítka a nadpisy bez tečky na konci. Celé věty s tečkou, pokud ji má angličtina.
- Trojtečka `…` (jeden znak), ne `...`, pokud angličtina používá `…`. Pokud angličtina má `...`, zachovej `...`.
- Uvozovky v souvislém textu `„…“`. Obsah v backtickách `` ` `` a kód ponech beze změny.
- Mezi číslem a jednotkou mezera (`5 MB`), procenta `50 %` jen pokud to proměnná dovolí: `{{percent}}%` ponech beze změny (formátování dělá kód).
- Spojovník mezi anglickým termínem a českým slovem nepiš, česky se skloňuje: `název worktree`, `název větve`, `SSH připojení`, `titulek PR`.
- Nezvyšuj délku zbytečně. Čeština je o 10–30 % delší, pro tlačítka a záložky volíme kratší přirozenou variantu, ale bez ztráty významu. Tvrdý limit: max(64 znaků, 4× délka angličtiny).

## Co se nepřekládá

- Proměnné `{{name}}`, `{name}`, značky `<0>…</0>`, `<label>…</label>`, `<br/>`, entity `&amp;` – musí zůstat **přesně** stejné a ve stejném počtu. Text uvnitř párové značky přelož. Pořadí proměnných se změnit smí.
- Názvy produktů a značek: Orca, Claude, Claude Code, Codex, GitHub, GitLab, Slack, Linear, Jira, Google, VS Code, Cursor, Docker, SSH, Git, npm, Composio atd.
- Příkazy, cesty, přepínače, kód, názvy kláves (`Enter`, `Esc`, `Tab`, `Cmd`, `Shift`), hodnoty nastavení, URL.
- Popisky převzaté z UI jiného produktu.
- Pokud je text čistě technický (název souboru, příkaz, jen proměnná), ponech ho beze změny.

## Plurály

Angličtina má `_one` a `_other`. Čeština potřebuje čtyři tvary (pravidla CLDR):

| tvar    | čísla           | příklad                   |
|---------|-----------------|---------------------------|
| `one`   | 1               | `{{count}} soubor`        |
| `few`   | 2–4             | `{{count}} soubory`       |
| `many`  | desetinná čísla | `{{count}} souboru`       |
| `other` | 0, 5+           | `{{count}} souborů`       |

Pokud anglický tvar `_one` neobsahuje `{{count}}`, český `one` ho také nemá (`Jeden soubor`). Ostatní tvary vycházejí z anglického `_other` a mají stejné proměnné. Shoduj i sloveso a přídavné jméno: `Smazán {{count}} soubor` / `Smazány {{count}} soubory` / `Smazáno {{count}} souborů`.

## Slovník pojmů

| English | Česky | Poznámka |
|---|---|---|
| worktree | worktree (ten worktree, mn. č. worktree) | Nesklonné ve všech pádech: `v worktree`, `3 worktree`. Odlišné od workspace. |
| workspace | pracovní prostor | |
| repository / repo | repozitář / repo | |
| branch / base branch | větev / základní větev | |
| commit | commit; sloveso `commitnout`, `commitovat` | |
| pull request / PR | pull request / PR | GitLab `merge request` ponech. |
| merge, rebase, diff, stash | merge, rebase, diff, stash | Slovesa: `sloučit` (merge), `rebasovat`, `stashnout`. Podstatná jména anglicky. |
| checkout | checkout; sloveso `přepnout na`, `checkoutnout` | Podle kontextu: „Checkout branch“ → `Přepnout na větev`. |
| push / pull / fetch | push / pull / fetch | Slovesa `pushnout`, `pullnout`, `fetchnout`, ale „Push“ na tlačítku → `Push`. |
| remote (Git) / remote host | remote / vzdálený hostitel | Přídavné jméno: `vzdálený`. |
| issue | issue (to issue, mn. č. issues) | |
| review / code review | review / code review; sloveso `zkontrolovat` | |
| check (CI) | kontrola (CI) | `Kontroly CI prošly` |
| label | štítek | |
| approve / comment | schválit / komentář | |
| source control | správa verzí | |
| agent | agent, agenti, agentů | |
| chat / prompt | chat / prompt | |
| skill / plugin / hook | skill / plugin / hook | |
| session | relace | „Terminal session“ → `relace terminálu`. U agentů lze `sezení` jen pokud angličtina myslí konverzaci; jinak `relace`. |
| terminal / shell | terminál / shell | |
| tab | karta | Klávesa zůstává `Tab`. |
| pane / panel | podokno / panel | Split pane: `Rozdělit podokno`. Oba pojmy odlišuj. |
| sidebar / status bar | postranní panel / stavový řádek | |
| editor / browser | editor / prohlížeč | |
| command palette / quick open | paleta příkazů / rychlé otevření | |
| file / folder / directory | soubor / složka / adresář | |
| project | projekt | |
| host / server / SSH host | hostitel / server / SSH hostitel | |
| automation / task | automatizace / úloha | |
| dashboard | přehled | |
| settings / preferences | nastavení / předvolby | |
| shortcut / keybinding | klávesová zkratka / přiřazení kláves | |
| sign in / sign out / log in | přihlásit se / odhlásit se | |
| account / provider / model | účet / poskytovatel / model | |
| token | token | |
| usage / quota / rate limit | využití / kvóta / limit požadavků | |
| credits / balance | kredity / zůstatek | |
| notification | oznámení | |
| delete / remove | smazat / odebrat | Pojmy důsledně odlišuj. |
| enable / disable / default | zapnout / vypnout / výchozí | `Enabled` → `Zapnuto`. |
| pin / unpin / unread / archive | připnout / odepnout / nepřečtené / archivovat | |
| environment / sandbox | prostředí / sandbox | |
| dictation | diktování; sloveso `diktovat` | |
| clipboard | schránka | |
| port forwarding | přesměrování portů | |
| bot | bot | |
| webhook | webhook | |
| marketplace | tržiště | |
| theme | motiv | |
| workspace options | možnosti pracovního prostoru | |
| card | karta (u UI prvků „karta“), u stylů zobrazení `kartička` nevolit | |
| run / runs | spustit / běh, běhy | |
| retry / try again | zkusit znovu | |
| learn more | další informace | |
| copy / paste / cut | kopírovat / vložit / vyjmout | |
| open / close | otevřít / zavřít | Stav PR „Open“ → `Otevřený`. |
| search | hledat / hledání | |
| filter | filtr; sloveso `filtrovat` | |
| upload / download | nahrát / stáhnout | |
| sync | synchronizace; sloveso `synchronizovat` | |
| update | aktualizace; sloveso `aktualizovat` | |
| install / uninstall | nainstalovat / odinstalovat | |
| connect / disconnect | připojit / odpojit | |
| runtime / remote runtime | běhové prostředí / vzdálené běhové prostředí | Ve vyhledávacích klíčových slovech zůstává `runtime`. |
| worker (orchestrace, boti) | worker (workera, workeři) | Coordinator → `koordinátor`. |
| Space (správce místa) | Space | Název funkce, nepřekládá se. |
| Chat UI | chatové rozhraní | Sekce nastavení `Chatové rozhraní`. |
| Computer Use | Computer Use | Název funkce. |
| artifact | artefakt | |
| stage / unstage / staged | připravit / zrušit přípravu / připravené | Podle VS Code. |
| fork | fork; sloveso `forknout` | |
| turn (agenta) | tah | |
| draft (PR) | koncept | |
| assignee / reviewer | řešitel / recenzent | |
| daemon | démon | |
| recipe | recept | |
| ticket | tiket | |
| passphrase | heslová fráze | |
| Orca | Orca (Orcy, Orce, Orcu) | Ženský rod. |
| Počty bez plurálu | `Štítek: {{count}}` | Kde angličtina nemá `_one/_other`, volíme tvar, který se neskloňuje. |

## Kontext

Každá položka má seznam klíčů (`keys`), kde se text používá. Klíč napoví, co je text zač: `.title` nadpis, `.description` popis, `.placeholder` zástupný text v poli, `.button`/`.action` tlačítko, `.tooltip` bublinová nápověda, `.error`/`.failed` chyba, `.label` štítek. Pokud stejná angličtina potřebuje v různých klíčích jiný český tvar (typicky „Open“ jako tlačítko vs. stav), použij objekt `{"*": "výchozí", "plný.klíč": "varianta"}`.
