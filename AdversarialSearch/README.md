# Boter-kaas-en-eieren - Search

Deze opdracht heeft vier stappen. Begin met zelf spelen en implementeer daarna minimax.
Alpha-beta en expectimax zijn verdere uitbreidingen.

## Start de app

Open een terminal in deze map:

```powershell
python run.py
```

De app opent op http://127.0.0.1:8001/. Houd de terminal open en stop met Ctrl+C.
Als de poort bezet is, gebruik `python run.py --port 0`.
Stap 1 werkt ook door `index.html` rechtstreeks te openen. Voor stappen 2-4 moet de
Python-server draaien, omdat de app dan jouw Python-functies gebruikt.

## Stap 1: zelf spelen

Kies **1 - Speel zelf X en O**. Speel beide kanten om te beurt door vakjes aan te klikken.
X begint. Drie gelijke tekens op een rij, kolom of diagonaal winnen. Na een winst of
gelijkspel is het spel afgelopen; je kunt een nieuw spel starten.

De score wordt altijd bekeken vanuit X:

- X wint: +1.
- O wint: -1.
- Gelijkspel: 0.

## Het bord en de meegeleverde functies

Een bord is een tuple van negen tekens: `X`, `O` of `.` voor leeg. De indices zijn:

```text
0 1 2
3 4 5
6 7 8
```

Bijvoorbeeld:

```python
board = ('X', 'X', '.',
         'O', 'O', '.',
         '.', '.', '.')
```

In `game.py` staan helpers die je niet hoeft te schrijven:

- `utility(board)`: +1, -1 of 0 als het spel afgelopen is, anders `None`.
- `legal_moves(board)`: de indices van de toegestane zetten.
- `play_move(board, move, player)`: een nieuw bord na de zet; het oude bord blijft intact.
- `other_player(player)`: wisselt X en O.

Let op: **0 is ook een eindscore**. Gebruik `result is not None` om een eindtoestand
te herkennen. De waarde blijft altijd vanuit X bekeken, ook als O aan zet is.

## Stap 2: minimax

Vul alleen `minimax(board, player)` in `student_minimax.py` in.
X maximaliseert; O minimaliseert.
Je kunt dit kleine bestand rechtstreeks uitvoeren:

```powershell
python student_minimax.py
python checker.py minimax
```

Kies daarna **2 - Minimax** in de app. **Laat X spelen** gebruikt jouw code; jij speelt O
door te klikken. Het kiezen van een zet op basis van de kindwaarden is al voorzien.
Bij meerdere even goede zetten wordt de eerste gekozen; elke optimale zet is geldig.

## Stap 3: alpha-beta pruning

Vul `alphabeta(board, player, alpha, beta)` in `student_alphabeta.py` in.

```powershell
python student_alphabeta.py
python checker.py alphabeta
```

Kies **3 - Alpha-beta pruning**. Vergelijk dezelfde toestand met minimax: de waarde
moet gelijk zijn, terwijl minder posities kunnen worden onderzocht. De teller telt
aanroepen inclusief eindtoestanden; dezelfde toestand via twee paden telt twee keer.
Waarden uit een gesnoeide tak kunnen grenzen zijn: de checker vergelijkt de waarde
bij de volledige begin-grenzen, niet willekeurige interne terugkeerwaarden.

## Stap 4: expectimax

Vul `expectimax(board, player)` in `student_expectimax.py` in.
X maximaliseert nog steeds, maar **O kiest nu uniform willekeurig** uit de toegestane
zetten. O is dus een kansnode: neem het gemiddelde van de kindwaarden.

```powershell
python student_expectimax.py
python checker.py expectimax
```

Kies **4 - Expectimax**. Met **Volgende zet** kiest jouw code voor X, of kiest de app
een willekeurige toegestane zet voor O. Zo kun je beide spelers stap voor stap volgen.
De verwachte score ligt tussen -1 en +1 en hoeft geen geheel getal te zijn.
Vergelijk de waarde en keuzes met minimax.

Een klein voorbeeld met O aan zet:

```text
X X .
O O .
X O X
```

O kan op vakje 5 meteen winnen (-1 voor X), of op vakje 2 spelen waarna het gelijkspel
wordt (0). Minimax geeft deze toestand waarde -1. Expectimax geeft waarde
`(-1 + 0) / 2 = -0.5`, omdat beide O-zetten even waarschijnlijk zijn.

## Controleren en debuggen

De checker gebruikt alle bereikbare toestanden om onafhankelijk correcte waarden
te berekenen en controleert standaard een selectie met beide spelers, winst, verlies,
gelijkspel en kansnodes:

```powershell
python checker.py minimax --all
python checker.py alphabeta --all
python checker.py expectimax --all
```

Exitcode 0: correct; 1: een waarde is fout; 2: onvolledige code of een uitvoeringfout.
Opgeslagen wijzigingen aan de studentfunctie worden bij de volgende AI-zet ingelezen.
