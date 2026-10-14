from ortools.sat.python import cp_model

# Creates the model.
model = cp_model.CpModel()

# Data.
rood = model.NewIntVar(1, 5, "rood")
groen = model.NewIntVar(1, 5, "groen")
wit = model.NewIntVar(1, 5, "wit")
blauw = model.NewIntVar(1, 5, "blauw")
geel = model.NewIntVar(1, 5, "geel")
kleuren = [rood, groen, wit, blauw, geel]

Brit = model.NewIntVar(1, 5, "Brit")
Zweed = model.NewIntVar(1, 5, "Zweed")
Deen = model.NewIntVar(1, 5, "Deen")
Noor = model.NewIntVar(1, 5, "Noor")
Duitser = model.NewIntVar(1, 5, "Duitser")
nationaliteiten = [Brit, Zweed, Deen, Noor, Duitser]

thee = model.NewIntVar(1, 5, "thee")
koffie = model.NewIntVar(1, 5, "koffie")
melk = model.NewIntVar(1, 5, "melk")
bier = model.NewIntVar(1, 5, "bier")
water = model.NewIntVar(1, 5, "water")
dranken = [thee, koffie, melk, bier, water]

PallMall = model.NewIntVar(1, 5, "PallMall")
Dunhill = model.NewIntVar(1, 5, "Dunhill")
Blends = model.NewIntVar(1, 5, "Blends")
BlueMaster = model.NewIntVar(1, 5, "BlueMaster")
Prince = model.NewIntVar(1, 5, "Prince")
sigaren = [PallMall, Dunhill, Blends, BlueMaster, Prince]

honden = model.NewIntVar(1, 5, "honden")
vogels = model.NewIntVar(1, 5, "vogels")
katten = model.NewIntVar(1, 5, "katten")
paarden = model.NewIntVar(1, 5, "paarden")
goudvis = model.NewIntVar(1, 5, "goudvis")
huisdieren = [honden, vogels, katten, paarden, goudvis]

# er zijn 5 huizen in verschillende kleuren
model.AddAllDifferent(rood, groen, wit, blauw, geel)

# in elk huis woont iemand met een andere nationaliteit
model.AddAllDifferent(Brit, Zweed, Deen, Noor, Duitser)

# niemand heeft hetzelfde dier, rookt dezelfde sigaar of drinkt dezelfde drank
model.AddAllDifferent(thee, koffie, melk, bier, water)
model.AddAllDifferent(PallMall, Dunhill, Blends, BlueMaster, Prince)
model.AddAllDifferent(honden, vogels, katten, paarden, goudvis)

model.Add(Brit == rood) # de Brit leeft in het rode huis
model.Add(Zweed == honden) # de Zweed heeft honden
model.Add(Deen == thee) # de Deen drinkt thee
model.Add(groen + 1 == wit) # het groene huis staat links van het witte huis
model.Add(groen == koffie) # de bewoner van het groene huis drinkt koffie
model.Add(PallMall == vogels) # diegene die Pall Mall rookt, houdt vogels
model.Add(geel == Dunhill) # de bewoner van het gele huis rookt Dunhill
model.Add(melk == 3) # de man in het middelste huis drinkt melk
model.Add(Noor == 1) # de Noor leeft in het eerste huis

# de man die Blends rookt, leeft naast diegene die katten heeft
diff_Blends_katten = model.NewIntVar(-4, 4, 'diff_Blends_katten')
model.Add(diff_Blends_katten == Blends - katten)
model.AddAbsEquality(1, diff_Blends_katten)

# de man met de paarden leeft naast de Dunhill-roker
diff_paarden_Dunhill = model.NewIntVar(-4, 4, 'diff_paarden_Dunhill')
model.Add(diff_paarden_Dunhill == paarden - Dunhill)
model.AddAbsEquality(1, diff_paarden_Dunhill)

model.Add(BlueMaster == bier) # diegene die BlueMaster rookt, drinkt ook bier
model.Add(Duitser == Prince) # de Duitser rookt Prince

# de Noor woont naast het blauwe huis
diff_Noor_blauw = model.NewIntVar(-4, 4, 'diff_Noor_blauw')
model.Add(diff_Noor_blauw == Noor - blauw)
model.AddAbsEquality(1, diff_Noor_blauw)

# de man die Blends rookt, heeft een buur die water drinkt
diff_Blends_water = model.NewIntVar(-4, 4, 'diff_Blends_water')
model.Add(diff_Blends_water == Blends - water)
model.AddAbsEquality(1, diff_Blends_water)

# Creates the solver and solve.
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Statistics.
print('\nStatistics')
print('  - conflicts      : %i' % solver.NumConflicts())
print('  - branches       : %i' % solver.NumBranches())
print('  - wall time      : %f s' % solver.WallTime())

if status != cp_model.INFEASIBLE:
        goudvis_owner = [
            n for n in nationaliteiten if solver.Value(n) == solver.Value(goudvis)
        ][0]
        print('De', goudvis_owner.Name(), 'bezit de goudvis')
else:
        print('Geen oplossing voor het Einstein-raadsel')
