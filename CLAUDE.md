# Blutti Frutti – projekt-átadó (Claude Code-nak)

Ez a repo a **Blutti Frutti** iPhone-os költségfigyelő PWA, amit fadeApu (a gazda) a feleségének, **Annának** készíttet. A fejlesztés eddig a Claude appban (Cowork) folyt; innentől itt, Claude Code-ban folytatódik. Ez a fájl mindent tartalmaz, ami a folytatáshoz kell. **Magyarul kommunikálj fadeApuval, egyszerűen – kezdő, nem fejlesztő.** Káromkodik, ne vedd magadra.

## 1. Mi ez és hol fut

- Egyfájlos, offline, telepíthető webapp (PWA). **Minden adat a telefonon van** (`localStorage`, kulcs: `blutti-frutti-v1`) – nincs szerver, nincs backend, nincs szinkron.
- Élesben: **GitHub Pages**, ebből a repóból (`leszedemahalyadat/blutti-frutti`, `main` ág gyökere). Cím: `https://leszedemahalyadat.github.io/blutti-frutti/` – Anna ezt rakta a főképernyőre.
- **Kiadás = push a `main`-re.** A Pages workflow magától lefut (1–3 perc). Nincs más teendő, semmit nem kell sehova feltölteni.
- Testvérappok (külön repók, külön tároló, ugyanaz a motor): Szojkodó Helyzetó (Zoli, `szojkodo-helyzeto`), zsuKe$$ (Zsuzsus, anyós, `zsukess`), Ákos Kasszája (`akos-kassza`), Lácsó Lóvé (fadeApu sajátja, még nincs repója). **Ezekhez innen ne nyúlj**, csak ha fadeApu kéri.

## 2. Fájlok

| Fájl | Mi ez |
|---|---|
| `src/blutti-frutti.html` | **A forrás.** Ezt szerkeszd. Egy fájl: CSS + HTML + JS (IIFE-ben) + beágyazott Three.js r152 UMD (~630 KB, ne nyúlj hozzá). |
| `build.py` | Forrás → `index.html`. Hozzárakja a `<head>`-et (manifest, ikonok, iOS meta, indítóképek), a „rakd a főképernyőre” sávot és a service worker regisztrációt. Futtatás: `python3 build.py` |
| `index.html` | **Generált kiadott fájl.** Soha ne kézzel szerkeszd – mindig `build.py`-jal. |
| `sw.js` | Service worker. **Minden kiadásnál a `C` cache-nevet eggyel feljebb kell vinni** (`blutti-v16` → `blutti-v17`), különben a telefon a régit mutatja. |
| `manifest.webmanifest`, `icon-*.png`, `splash-*.png`, `.nojekyll` | PWA körítés, kész, nem változik. |
| `tools/test.js` | Teljes regressziós teszt Playwrighttal (betöltés, beírás, napzárás, játékok, Gépház, reset, túlcsordulás-ellenőrzés). `node tools/test.js` – csak a hibákat írja ki. `FULL=1` → két képernyőméret. |
| `tools/quest-shot.js` | A 3D játék füstteszte WebGL-lel (swiftshader) + 4 képernyőkép a `tools/.tmp/`-be. |

Teszthez kell: `npm i playwright && npx playwright install chromium`.

### Kiadás lépésről lépésre
1. Szerkeszd `src/blutti-frutti.html`-t.
2. `node -e` helyett gyors szintaxis-ellenőrzés: szedd ki az utolsó `<script>` tartalmát és `node --check` (vagy futtasd a tesztet).
3. `node tools/test.js` → csak `DUP IDS: wTip,vh,vOk` jelenhet meg (ismert, ártalmatlan: egy SVG-gradiens és a modal gombjai).
4. `python3 build.py`
5. `sw.js`: `const C="blutti-vNN"` → NN+1
6. Commit (magyar üzenet, mit lát a felhasználó), push `main`-re. Ellenőrzés: `gh api repos/leszedemahalyadat/blutti-frutti/actions/runs --jq '.workflow_runs[0] | "\(.status) \(.conclusion)"'`
7. **Csak akkor adj ki, ha fadeApu kimondta** („mehet ki”, „rakd ki”). Alapból előnézetet kér, megnézi, aztán enged. Előnézet itt: build egy ideiglenes fájlba és mutasd meg / írd le, mi változott.

## 3. Hol tart most (2026-11-08)

**Élesben:** `sw.js` = `blutti-v17` (2026-11-08, Anna kérései + minitérkép-javítás). A v17 újdonságai:
- **Fizunap** (`S.settings.payday`, Gépház): ha meg van adva, a napi plafon gördülő: (az időszak bevételei − `fixedSum()` − dugipénz − az időszakban eddig, a mai nap előttig elköltött) ÷ hátralévő napok a következő fizuig, 100-ra lefelé kerekítve (`rollLimit`). Időszak: `periodOf(d)` → `{s,e}` (fizunaptól a következő fizunapig, `e` kizárt); fizunap nélkül naptári hónap. A fizunap előtt 1–4 nappal beírt `fizu` már a következő időszaké (`incPeriodStart`). Csak `S.settings.paydayFrom`-tól él (`rollOn`), a régi napok értékelése nem változik. Gördülő módban nincs `bigShare` és nincs `carry` (a carry-kapcsoló rejtve). Ha az időszakban még nincs bevétel → régi 30 napos számolás + figyelmeztetés.
- **Hol tartok kártya** a Ma fülön (`renderHt`, `#htCard`): maradt = bevétel − fix − dugipénz − elszórva (`periodSum`). Fix lehúzások lenyitva „✓ kiment” pipával (`S.fixPaid[időszak-kezdet][fixId]={a:számla,v:összeg}`) – kipipáláskor a költős számláról levonja, visszavéve visszaadja.
- **Tervezett kiadás:** beíráskor „⏳ Még nem ment ki” (`e.plan`), kipipálva `e.paid=dátum`. Amíg `isPlan(e)`, `applyAcct` nem mozgatja a számlát. A tervezett tétel nem a napi szórásba (`dayData().plan`) megy, hanem gördülő módban a következő napoktól az időszaki keretbe.
- **Költős számla** (`S.wealth.main`, ★ a Vagyonban, `mainAcct()`): kiadásnál alapból kijelölve.
- „Mi változott?” útmutató: `WN_VER="4"`.

Korábbi (v16-ig) tartalom:
- Ma fül: napi plafon, költés/bevétel beírás, Bevétel kártya (havi összeg, mai, előző hónap, forrás szerinti bontás), 7 napos kihívás kártya, napzárás („Nap lezárása” – akkor is számít, ha nem költött).
- **Jövedelem-modell (v3, Bluttinál ÉLES, a többi appban még nem):** a Gépházban nincs „várható havi jövedelem”, hanem **Jövedelem = az utolsó 30 nap beírt bevételei** (`income30(d)`). Napi plafon = (jövedelem − fix lehúzások − dugipénz) / 30,4, 500-ra lefelé kerekítve (`suggestedLimitAt`). Amíg a 30 napban nincs beírt bevétel, a régi `settings.incomeExpected` él fallbackként (`incomeFallback()`), és figyelmeztető sor jelenik meg.
- **Bevétel beírásakor kötelező két koppintás:** „Hogyan jött?” (`VIAS`: Készpénz / Bankkártya-utalás / Revolut / Más → `e.via`, utolsó megjegyezve `S.lastVia`) és kategória (`IN_CATS`: Fizu, Kapott zsé, Mellékes, Más lé). A via-koppintás **nem** ment, a kategória-koppintás ment (ha van összeg). A Napló sor és a Bevétel kártya mutatja a módot.
- Vagyon fül (saját számlák, Anna maga veszi fel; tartozások „neked tartoznak”), bővíthető havi fix lehúzások, dugipénz/célok.
- Játék fül: **Tündér Quest** (3D nyílt világú akció-RPG, zseton nélkül játszható) + Memória, Tologatós (8-puzzle), Színkód (mastermind) zsetonért. Zseton = 7 lezárt nap a kihívásban.
- Liquid glass téma Anna színeivel (világos, pasztell), animációk, egyszeri „Mi változott?” útmutató (`WN_VER="3"`, `S.settings.wn`).
- Service worker frissítés-javítás: install `fetch(..., {cache:"reload"})`, lekérés `no-cache`, új verziónál a lap egyszer újratölt (`controllerchange`), előtérbe hozáskor `reg.update()`.

**Forrásban kész, de még nincs kint:** semmi – a `src/` és az élő egyezik.

**Gép-beállítás (fadeApu Macje):** Node.js a `~/.local/node/bin`-ben van (nincs a PATH-ban, nincs Homebrew, nincs `gh`) → `export PATH="$HOME/.local/node/bin:$PATH"` a tesztek előtt. A kiadás ellenőrzése `gh` helyett: `curl -s https://leszedemahalyadat.github.io/blutti-frutti/sw.js | head -c 60`.

## 4. Hogyan épül fel a kód (a nagy fájlon belül)

Minden az egyetlen `<script>` IIFE-jében van. Fontosabb részek, keresd a nevet:
- **Állapot:** `S` objektum (`S.entries[]` {id,date "YYYY-MM-DD",type "in"|"out",cat,amount,note,via?,acct?}, `S.closed{}`, `S.ack{}`, `S.settings{incomeExpected, manualLimit, savingsGoal, fixed[], wn, ...}`, `S.wealth`, `S.goals`, `S.challenge`, `S.rpg`, `S.lastVia`). `save()` ír localStorage-ba, `resetCache()` törli a `cache{}` memoizálót. `today()` a mai dátum.
- **Keret-számolás:** `fixedSum()`, `income30()`, `incomeBase()`, `suggestedLimitAt(d)`, `baseLimitAt(d)`, `bigShare(d)` (nagy kiadás szétosztása), `dayLimitBase(d)`, `limitFor(d)` (napi plafon az adott napra, memoizálva `cache["l"+d]`), `score()`.
- **Beírás:** `openEntry(t, presetCat)`, `renderCats()`, `renderVias(t)`, `renderEntryAccts(t)`, `submitEntry()` (`$("addBtn")`), kategória-koppintás automentés.
- **Render:** `renderAll()` → `renderToday()`, `renderIncome()`, `renderLog()`, `renderVagyon()`, `renderGames()`, `renderSettings()`, `refreshSettingsLive()`, `refreshIncomeNow()`.
- **Kihívás / zseton:** `chDayOk(d)` (= `!!S.closed[d]`), `chStreak()`, `chState()`; zseton = `floor(streak/7) − played`.
- **Játékok:** `GAMES[]` (id, name, need, free, canvas, start, score…), `openGame()`, `gBegin()`, `gFinish()`, `closeGame()`; közös overlay `#game`, `#pgCanvas`, `#pgGL` (WebGL vászon, csak a questnél látszik), `#pgStage`, `#pgStart`/`#pgEnd`.
- **Tündér Quest:** `/* ===== Fade Quest UI ===== */` CSS-blokk és a `/* ================= FADE QUEST ... */` JS-blokk (átskinelve: Tündéranyó, Butikos, Nagyi Rózsi; ellenségek pletykafelhő / kapzsi egér / bádogbaba / trollmacska / shoppingsárkány; különleges: 💫 Tündérpor-robbanás). 64×64 generált világ (`rpgRng`), `rpgStart/rpgStop`, `rpgUpdate` (valós idejű mob-AI), `rpgAttack`, `rpgKill`, `rpgDialog`, 3 kazamata (`rpgEnterDung`: tologatós lapok / karok sorrendje / 3 kulcs). Renderelés: WebGL (`glInit`, `glBuildMap`, `glFrame`, `glHuman`, `glCreature`), ha nincs WebGL → 2.5D canvas (`rpgDraw`). Irányítás: pointer events hosszan nyomva mozog (150 ms), `#rpgAtk`. **`rpgSave()` szándékosan nem menti az átmeneti mezőket** (`atkT, inv, hitT, comboT, swing, face, combo`) – egyszer emiatt nem lehetett ütni újranyitás után.
- **Útmutató:** `WN_VER`, `WN_STEPS[]`, `whatsNew()`; friss (üres) felhasználónak nem ugrik fel.

## 5. Szabályok, amiket fadeApu elvár

- **Előnézet először, kiadás csak szóra.** „Ne rakd ki” = tényleg ne.
- Zsuzsus (anyós) adatai, Altegio-adatok soha ne kerüljenek ebbe az appba.
- Nyelvezet az appban: könnyed szleng (lé, zsé, della, „spanom”), Anna színeivel; a meglévő fülek elrendezését ne forgasd fel (egy UX-átszervezést korábban elutasított).
- Minden kiadásnál: SW cache bump + teszt. Ha valami elromlik élesben, az előző verzió a git históriában van (`git revert`).
- Frissítés a telefonon: az app bezár–újranyit kétszer; ha sokáig nem jön, Safariban megnyitva frissül. (Az új SW-logika óta ez már többnyire magától megy.)
- iPhone 13 / 13 Pro / 16 Pro a célkészülékek; a 3D játék teljesítményét valódi telefonon még nem mérték – ha nehéz, kisebb árnyéktérkép / rajzolási táv.

## 6. Ismert dolgok, buktatók

- `DUP IDS: wTip,vh,vOk` a tesztben = ismert, ártalmatlan (statikus ellenőrzés, ugyanaz az id egy SVG-ben és egy sablonban).
- `#pgGL` vászonból **pontosan egy** legyen; a GL vászon csak a quest alatt látszik (`rpgStart` kapcsolja), különben eltakarja a többi játékot.
- Az iOS-en a `fill()`/blur + `innerHTML` csere egyszer kivételt dobott a Vagyon szerkesztésnél → `setTimeout(renderVagyon,0)` maradjon.
- Tesztben a gyűjtőkártya-modal (`#ckModal`) a Lácsó Lóvéban van, itt nincs – a harness ettől függetlenül kezeli.
- A `build.py` a forráson három kis cserét csinál (import-összefésülés, „nincs plafon” sáv, egy szöveg) – ha ezek a horgonyszövegek változnak a forrásban, a build `assert`-tel elszáll: igazítsd a `build.py`-t.

## 7. Ötletek, amik felmerültek (nem kért, nem sürgős)

Napszak-váltás és eső a questben, több biom/küldetés/szörny, lövedékes mobok, kitérés gomb; gyűjtőkártyák (Pokémon-szerű, a Lácsó Lóvéban már megvannak) Blutti-ba is; a jövedelem-modell finomhangolása Anna visszajelzése alapján.
