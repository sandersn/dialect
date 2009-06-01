# -*- coding: utf-8 -*-
"""
0. Manually make a list of which files go with which regions.
   All steps below operate over regions.

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
def extractPos():
    # 1. Extract POS tags from Talbanken
    run('ghc --make TrainPosTalbanken')
    run('TrainPosTalbanken %s >talbanken.tt' % (' '.join(paths.talbanken),))
def tagPos():
    # 2. Train TnT on Talbanken
    run('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    # - are blanks allowed?
    # (it will make it easier to emit CoNLL files for Maltparser)
    swedia.extractTnt(paths.swpath, paths.swediaRegions)
    # 4. Tag SweDiaSyn
    for region in paths.swediaRegions:
        run("tnt talbanken '%s.t' >'%s.tag'" % (region,region))
def tagDep():
    for region in swediaRegions:
        # 5. Post-process tagged SweDiaSyn to CoNLL format
        run('ghc --make ConvertTagsToConll')
        run("ConvertTagsToConll '%s.tag' >'%s.conll'" % (region,region))
        # 6. Dependency parse SweDiaSyn
        # TODO: This must eventually depend on a config file, not command line
        # options
        run("java -Xmx256M -jar malt-1.2/malt.jar -c swemalt -i '%s.conll' -o '%s.dep.conll' -m parse" % (region, region))
def tagCfg():
    # 7. Post-process tagged SweDiaSyn to ?? format for Berkeley parser.
    # - this requires uncrossing! probably!
    # 8. Constituency parse with Berkeley parser
    return
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
          sys.argv[1:] if sys.argv[1:] else 'extractPos tagPos'.split())
# TODO: Remove (or normalise to Talbanken) pauses in swedia.extractTxt
# They look like - <first second> - also there's some funny [/] and [/-]

