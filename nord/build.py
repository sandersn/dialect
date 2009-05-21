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

Notes:
SCons, in Python, replaces make and allows extensibility in Python.
Of course there's rake too

ghc --make only rebuilds as needed, so that at least is pretty fast
"""
import os
from util.lst import each
import swedia
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


def sys(cmd):
    result = os.system(cmd)
    if result: raise Error("Something went wrong")
def blade(files):
    # 1. Extract POS tags from Talbanken
    sys('ghc --make TrainPosTalbanken')
    sys('./TrainPosTalbanken %s >talbanken.tt' % (' '.join(talbanken),))
    # 2. Train with TnT
    sys('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    # TODO: Test this next
    swedia.extractTnt(swpath, swediaRegions)
    return
    # TODO: Not done
    # 4. Tag SweDiaSyn
    for region in regions:
        sys('tnt talbanken %s.t >%s.tag' % (region,region))
if __name__=="__main__":
    blade(None) # each(blade, regions.values())
# TODO: Add stop words in swedia.read, things like pauses, etc
# TODO: Add execfile to python3.0 startup sequence, at least in emacs
