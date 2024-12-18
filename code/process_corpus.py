
corpus = []
with open("../data/oracc_etcsri.vrt", "r", encoding="utf-8") as file:
    for line in file:
        if line.startswith("<text"):
            parts = line.strip().split()
            corpus.append([parts[1], parts[3]]) #append cdli number and period
            continue
        if line.startswith("<") or line.strip() == "":
            continue
        parts = line.strip().split("\t")
        corpus.append([parts[1], parts[4], parts[6]]) #append lemma, transcription and pos subcategory

#categorize texts for different periods
LagasII = {}
UrIII = {}
OldAkkadian = {}
EarlyDynastic = {}


period = None

for i in range(len(corpus)):
    if len(corpus[i]) == 2: # identifies a part containing the cdli-number and period.
        cdli = corpus[i][0]
        if corpus[i][1] == 'period="UrIII"':
            UrIII[cdli] = [[], []]
            period = "UrIII"
        elif corpus[i][1] == 'period="EarlyDynastic"':
            EarlyDynastic[cdli] = [[], []]
            period = "EarlyDynastic"
        elif corpus[i][1] == 'period="OldAkkadian"':
            OldAkkadian[cdli] = [[], []]
            period = "OldAkkadian"
        elif corpus[i][1] == 'period="OldBabylonian"': # The Old Babylonian period is ignored
            period = None
        elif corpus[i][1] == 'period="LagašII"':
            LagasII[cdli] = [[], []]
            period = "LagasII"
        else:
            period = None
    else:
        if period is None: #if the period is unknown, the inscription will be ignored
            continue
        if (corpus[i][2] == 'RN Royal Name' or corpus[i][0] == 'Utuheŋal') and corpus[i-1][0] not in ["dumu", "dumu.KA", "pabilga", "egia", "šeš", "dam"]: #check that the royal name is not a relative or a spouse that is mentioned.
            if i>2:
                if corpus[i-3][0] == "šeš" and corpus[i-2][0] == "ki" and corpus[i-1] == "aŋ": # Filter out names that appear in the structure "The beloved brother of X", where X is a royal name
                    continue
            if period == "UrIII":
                UrIII[cdli][0].append(corpus[i][0])
            elif period == "LagasII":
                LagasII[cdli][0].append(corpus[i][0])
            elif period == "OldAkkadian":
                OldAkkadian[cdli][0].append(corpus[i][0])
            elif period == "EarlyDynastic":
                EarlyDynastic[cdli][0].append(corpus[i][0])

        elif corpus[i][2] == 'DN Divine Name' and corpus[i][0] not in ['_', 'X']: # Some of the divine names are _ or X in the corpus, and they are discarded.
            if period == "UrIII":
                UrIII[cdli][1].append(corpus[i][0])
            elif period == "LagasII":
                LagasII[cdli][1].append(corpus[i][0])
            elif period == "OldAkkadian":
                OldAkkadian[cdli][1].append(corpus[i][0])
            elif period == "EarlyDynastic":
                EarlyDynastic[cdli][1].append(corpus[i][0])


def ED_kings():
    kings = {}
    for text, names in EarlyDynastic.items():
        if names[0] and names[1]:
            if not names[0][0] in kings:
                kings[names[0][0]] = []
            for deity in set(names[1]):
                if deity not in kings[names[0][0]]:
                    kings[names[0][0]].append(deity)
    return kings

def UrIII_kings():
    kings = {}
    for text, names in UrIII.items():
        if names[0] and names[1]:
            if not names[0][0] in kings:
                kings[names[0][0]] = []
            for deity in set(names[1]):
                if deity not in kings[names[0][0]]:
                    kings[names[0][0]].append(deity)
    return kings

def OA_kings():
    kings = {}
    for text, names in OldAkkadian.items():
        if names[0] and names[1]:
            if not names[0][0] in kings:
                kings[names[0][0]] = []
            for deity in set(names[1]):
                if deity not in kings[names[0][0]]:
                    kings[names[0][0]].append(deity)
    return kings

def LagasII_kings():
    kings = {}
    for text, names in LagasII.items():
        if names[0] and names[1]:
            if not names[0][0] in kings:
                kings[names[0][0]] = []
            for deity in set(names[1]):
                if deity not in kings[names[0][0]]:
                    kings[names[0][0]].append(deity)
    return kings
