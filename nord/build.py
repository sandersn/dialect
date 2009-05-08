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
TODO:Install cabal and thence Text.XML.HaXml on jones
TODO:Figure out how to cons on sentence dividers in TrainPosTalbanken
"""
import os
regions = [['', '', ''],
           ['', '', '', '', ''],
           ['', '']]
tbpath = '/Volumes/Corpora/Data/sv/Talbanken05/FPS/'
talbanken = [tbpath + 'SD.tiger.xml',
             tbpath + "P.tiger.xml",
             tbpath + "IB.tiger.xml",
             tbpath + "G.tiger.xml"]

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
blade(None) # each(blade, regions.values())
