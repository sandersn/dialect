# -*- coding: utf-8 -*-
"""
0. Manually make a list of which files go with which regions.
   All steps below operate over regions.
1. Extract POS tags from Talbanken
2. Train with TnT
3. Extract SweDiaSyn words into TNT formats
 - are blanks allowed? it will make it easier to emit CoNLL files for Maltparser
4. Tag SweDiaSyn
5. Post-process tagged SweDiaSyn to CoNLL format (or other)
6. Dependency parse SweDiaSyn
7. Post-process tagged SweDiaSyn to ?? format for Berkeley parser.
 - this requires uncrossing! probably!
8. Constituency parse with Berkeley parser
9. Run icectrl.out with various parameter settings. Steal this from ice/build.py

SCons, in Python, replaces make and allows extensibility in Python.
Of course there's rake too

ghc --make only rebuilds as needed, so that at least is pretty fast
TODO:Write test code to make sure SweDiaSyn files can be opened.
     I don't trust these funny Swedish characters!
TODO: Mail those Listserv guys AGAIN. Geez! C'mon!
TODO: Insert the correct utf-8 combining characters.
"""
import os
regions = [['', '', ''],
           ['', '', '', '', ''],
           ['', '']]
tbpath = '/Volumes/Data/Corpora/sv/Talbanken05/FPS/'
swpath = '/Volumes/Data/Corpora/sv/SweDiaSyn/Korrekturläst/'
talbanken = [tbpath + 'SD.tiger.xml',
             tbpath + "P.tiger.xml",
             tbpath + "IB.tiger.xml",
             tbpath + "G.tiger.xml"]
swediaRegions = [
  'Ankarsrum',
  'Anundsjo',
  'Arjeplog',
  'Arsunda',
  'Asby',
  'Bara',
  'Bengtsfors',
  'Boda',
  'Bredsatra',
  'Faro',
  'Floby',
  'Fole',
  'Frillesas',
  'Indal',
  'Jamshog',
  'Köla',
  'Leksand',
  'Loderup',
  'Nederlulea',
  'Norra Rorum',
  'Orust',
  'Ossjo',
  'Overkalix',
  'Segerstad',
  'Skinnskatteberg',
  'Sorunda',
  'Sproge',
  'StAnna',
  'Torsås',
  'Torso',
  'Torsö',
  'Vaxtorp',
  'Viby',
  'Villberga',
]
swediaRegionsEjkorrekturlast = [
  'Löderup',
  'Pite',
  'anu',
  'ara',
  'arjeplog',
  'ars',
  'aspås',
  'bara',
  'broby',
  'burtråsk',
  'delsbo',
  'gråsö',
  'ind',
  'lod',
  'nederkalix',
  'nysåtra',
  'oka',
  'ors',
  'pit',
  'sar',
  'sårna',
  'sorsele',
  'toh',
  'vindeln',
]


def each(f, l):
    for x in l: f(x)
def sys(cmd):
    result = os.system(cmd)
    if result: raise Error("Something went wrong")
def blade(files):
    # 1. Extract POS tags from Talbanken
    os.system('ghc --make TrainPosTalbanken')
    # TODO: TrainPosTalbanken should insert sentence delimiters
    os.system('./TrainPosTalbanken %s >talbanken.tt' % (' '.join(talbanken),))
    # TODO: Not tested below here
    # 2. Train with TnT
    os.system('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    return
    # TODO: Not done
    # 4. Tag SweDiaSyn
    for region in regions:
        os.system('tnt talbanken %s.t >%s.tag' % (region,region))
#blade(None) # each(blade, regions.values())
# TEST:
def fromkeys(l, cons):
    d = {}
    for x in l:
        d[x] = cons()
    return d
def find(f, l):
    for x in l:
        if f(x):
            return x
    else:
        return None
print(len(swediaRegions))
corpora = fromkeys(swediaRegions, list)
for corpus in os.listdir(swpath):
    r = find(corpus.startswith, swediaRegions)
    if r:
        corpora[r].append(corpus)
    elif corpus.startswith('.'):
        pass
    else:
        print('corpus', corpus, 'not found')
for region,files in corpora.items():
    print(region.encode('utf8'))
    for f in files:
        print('\t', f.encode('utf8'))
