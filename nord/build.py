# -*- coding: utf-8 -*-
"""
0. Manually make a list of which files go with which regions.

Notes:
SCons, in Python, replaces make and allows extensibility in Python.
Of course there's rake too
"""
import os
import sys
from util.lst import each
import swedia
import paths

def run(cmd):
    result = os.system(cmd)
    if result: raise Exception("Error: '%s' returned code %d" % (cmd, result))
def extractTalbanken():
    # 1. Train on POS tags from Talbanken
    # the explicit linker paths are needed to avoid MacPort's borken iconv
    # which is apparently just a giant series of macros?
    run('ghc --make -L/usr/lib -L/opt/local/lib TrainPosTalbanken')
    run('ghc --make -L/usr/lib -L/opt/local/lib --make RepairTalbanken')
    run('./TrainPosTalbanken %s >talbanken.tt' % (' '.join(paths.talbanken),))
    run('./RepairTalbanken %s >talbanken.mrg' % (' '.join(paths.talbanken),))
def tagPos():
    # 2. Train TnT on Talbanken POS tags
    run('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    swedia.extractTnt(paths.swpath, paths.swediaRegions)
    # 4. Tag SweDiaSyn
    for region in paths.swediaRegions:
        run("tnt talbanken '%s.t' >'%s.tag'" % (region,region))
def tagDep():
    run('ghc --make ConvertTagsToConll')
    for region in paths.swediaRegions:
        # 5. Post-process tagged SweDiaSyn to CoNLL format
        run("./ConvertTagsToConll '%s.tag' >'%s.conll'" % (region,region))
        # 6. Dependency parse SweDiaSyn
        # TODO: This must eventually depend on a config file, not command line
        # options
        os.chdir('malt-1.2')
        run("java -Xmx512M -jar malt.jar -c swemalt -i '../%s.conll' -o '../%s.dep.conll' -m parse" % (region, region))
        os.chdir('..')
def trainCfg():
    # n. Convert Talbanken to PTB (single-line?) for training (with uncrossing?!)
    # Several are supported, guess I'll have to read the GrammarTrainer code
    # n+1. Train using GrammarTrainer
    # TODO: There are more options:  -SMcycles 5 (6 cycles overfits)
    run('java -Xmx512M -cp berkeleyParser.jar edu.berkeley.nlp.PCFGLA.GrammarTrainer -path talbanken.mrg -out talbanken.gr -treebank SINGLEFILE')
def tagCfg():
    # 7. Post-process tagged SweDiaSyn to ?? format for Berkeley parser.
    # - this requires uncrossing! probably!
    # PTB tokenised, one per line (PTB is s-exps basically) (extension .mrg?)
    # may be able to use nltk for this
    # 8. Constituency parse with Berkeley parser
    for region in swediaRegions:
        run('jar -Xms512M -jar berkeleyParser.jar -gr talbanken.gr <%s.mrg >%s.cfg')
def syntaxDist():
    # 9. Run icectrl.out with various parameter settings.
    # Steal this from ice/build.py
    return
def blade(runner, targets):
    for target in targets:
        print("Running target", target)
        getattr(runner, target)()
if __name__=="__main__":
    import build
    blade(build,
          sys.argv[1:] if sys.argv[1:] else 'extractTalbanken tagPos'.split())
# TODO: Remove (or normalise to Talbanken) pauses in swedia.extractTxt
# They look like - <first second> - also there's some funny [/] and [/-]

