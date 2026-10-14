# Kakuro - CSP
Vul alle cellen in met cijfers tussen 1 en 9. 
Rijen en kolommen mogen geen herhalend nummers bevatten.
De sommen zowel verticaal als horizontaal moeten kloppen met de ingevulde cijfers.
Als er al deels ingevulde getallen staan moet je deze laten staan.
## Mappen en bestanden

- `examples/`: drie voorbeelden per formaat, met 2 x 2, 3 x 3 en 4 x 4 speelvakjes.
- `solutions/`: dezelfde negen voorbeelden, ingevuld en met dezelfde bestandsnamen.
- `practice/`: twee extra oefeningen per formaat, zonder meegeleverde oplossing.
- `app/`: interactieve puzzels
- `solver.py`: het enige bestand waarin je jouw CSP-code moet schrijven.
- `solve.py`: leest een puzzel, voert jouw code uit, controleert en bewaart het antwoord.
- `checker.py`: controleert een ingevulde CSV tegen de oorspronkelijke puzzel.
- `csv_io.py`: de meegeleverde lees- en schrijffuncties.

De 2 x 2- en 3 x 3-puzzels hebben geen startcijfers. De 4 x 4-puzzels hebben enkele
vaste startcijfers om ze geschikt te maken voor deze introductie. Alle meegeleverde
puzzels hebben precies één oplossing. Formaat betekent het aantal **speelvakjes**;
de rand met somaanwijzingen komt daar nog bij.

## Zelf oplossen

Open een terminal in deze map en start:

```powershell
python app/run.py
```

Kies een puzzel in het menu. Rood duidt een gebroken regel aan. Groen betekent dat
een volledige rij of kolom voldoet aan de som en geen herhaalde cijfers bevat.
Rood krijgt voorrang als de andere reeks door hetzelfde vakje een regel schendt.
Grijze vakjes bevatten vaste startcijfers.

Gebruik Tab of de pijltjestoetsen om te bewegen. Wis een cijfer met Backspace of Delete.
Met **CSV opslaan** bewaar je jouw huidige invulling; met **CSV laden** laad je een
invulling voor de geselecteerde puzzel. Een onvolledige export bevat nog `?` en wordt
door de automatische checker niet als een volledige oplossing aanvaard.

De app heeft geen extra Python-pakketten nodig. Je kunt `app/index.html` ook rechtstreeks
in een browser openen. Stop de server met Ctrl+C. Gebruik `python app/run.py --port 0`
als poort 8000 al bezet is.

## Het CSV-formaat

Komma's scheiden de velden. Links bovenaan staat `#`. De bovenste rij bevat de
kolomsommen. De eerste kolom bevat de rijsommen. Een `?` is een leeg speelvakje;
een cijfer in de oorspronkelijke puzzel is een vast startcijfer.

Voorbeeld, `examples/2x2_01.csv`:

```csv
#,4,6
3,?,?
7,?,?
```

Een ingevulde CSV behoudt de rand en vervangt de vraagtekens door cijfers:

```csv
#,4,6
3,1,2
7,3,4
```

Bijvoorbeeld `answers/mijn_antwoord.csv`. Gebruik komma's, geen puntkomma's.
De helperfuncties ondersteunen UTF-8, een optionele BOM, CRLF en spaties rond velden.

## Jouw CSP implementeren

Installeer OR-Tools eenmalig in de Python-omgeving waarin je werkt:

```powershell
python -m pip install -r requirements.txt
```

Open `solver.py`. Alleen het model en een klein testvoorbeeld zijn voorzien.
Vul de functie `solve_kakuro` zelf aan.

De functie krijgt `row_sums`, `column_sums` en `givens`. In `givens` staan tuples
`(rij, kolom, cijfer)` met indices vanaf 0. Geef een lijst van lijsten met gehele
cijfers terug. Geef `None` terug als OR-Tools bewijst dat het model geen oplossing heeft.

Je kunt `solver.py` rechtstreeks uitvoeren, ook via de Run-knop van je editor:

```powershell
python solver.py
```

Onderaan staat hetzelfde kleine 2 x 2-voorbeeld als in `examples/2x2_01.csv`.

Voor een ander klein testvoorbeeld kun je de sommen en startcijfers onderaan aanpassen.

Wil je een puzzel uit een CSV laden, automatisch controleren en het antwoord bewaren?
Gebruik dan:

```powershell
python solve.py examples/2x2_01.csv
```

Je antwoord wordt automatisch gecontroleerd en, als het correct is, opgeslagen in
`answers/examples_2x2_01.csv`. Probeer vervolgens andere voorbeelden en oefeningen:

```powershell
python solve.py examples/3x3_01.csv
python solve.py practice/4x4_01.csv --output answers/mijn_antwoord.csv
```

## Een CSV afzonderlijk controleren

Dit werkt zowel voor antwoorden uit jouw programma als voor een CSV uit de app:

```powershell
python checker.py examples/2x2_01.csv answers/examples_2x2_01.csv
```

De checker leest geen oplossingsbestand. Hij controleert de afmetingen, de oorspronkelijke
somaanwijzingen, cijfers 1-9, startcijfers, alle sommen en de afwezigheid van herhalingen.
Een geldig alternatief wordt ook aanvaard als je later een puzzel met meerdere oplossingen maakt.

Exitcode 0 betekent correct; 1 betekent een geschonden regel; 2 betekent een onvolledige,
verkeerd gevormde of onleesbare CSV. De foutmelding vermeldt wat je moet aanpassen.

## OR-Tools-referentie

Het gebruik van `CpModel`, `CpSolver` en de oplossingsstatus volgt het
[officiële CP-SAT-voorbeeld](https://developers.google.com/optimization/cp/cp_solver).
De voorbeeldcode uit de les kan je gebruiken voor de syntaxis van somconstraints en `AddAllDifferent`.
