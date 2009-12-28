# -*- coding: utf-8 -*-
"""
0. Manually make a list of which files go with which regions.
(Regions are based on filename right now)

Notes:
SCons, in Python, replaces make and allows extensibility in Python.
"""
import os
import sys
import swedia
import consts
import norte
import cgitb
from util.lst import partition
import subprocess
cgitb.enable(format='text')

def multirun(n,tasks,files):
    processes = [subprocess.Popen([tasks[i]], stdout=file(files[i],'w'))
                 for i in range(n)]
    i = n
    while i < len(tasks):
        subprocess.Popen(['sleep', '1']).wait()
        processes, dones = partition(lambda p:p.poll() is None, processes)
        for done in dones:
            processes.append(subprocess.Popen([tasks[i]],
                                              stdout=file(files[i], 'w')))
            i += 1
def run(cmd):
    result = os.system(cmd)
    if result: raise Exception("Error: '%s' returned code %d" % (cmd, result))
def extractTalbanken():
    # 1. Train on POS tags from Talbanken
    # 1.1 Also Convert Talbanken to PTB for training
    # (TODO:with uncrossing?!)
    alltalbanken = ' '.join(consts.talbanken)
    run('ghc -O2 --make ConvertTalbankenToTags -main-is ConvertTalbankenToTags.main')
    run('ghc -O2 --make ConvertTalbankenToPTB -main-is ConvertTalbankenToPTB.main')
    run('./ConvertTalbankenToTags %s >talbanken.tt' % (alltalbanken,))
    run('./ConvertTalbankenToPTB %s >talbanken.mrg' % (alltalbanken,))
def tagPos():
    # rm Swedia.o is needed because -main-is switch makes the linker dumber
    run('rm Swedia.o')
    run('ghc -O2 --make Swedia -main-is Swedia.main')
    # 2. Train TnT on Talbanken POS tags
    run('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    run('./Swedia')
    # 4. Tag SweDiaSyn
    for region in consts.swediaSites:
        run("tnt talbanken '%s.t' >'%s.tag'" % (region,region))
def tagDep():
    run('ghc -O2 --make ConvertTagsToConll')
    for region in consts.swediaSites:
        # 5. Post-process tagged SweDiaSyn to CoNLL format
        run("./ConvertTagsToConll '%s.tag' >'%s.conll'" % (region,region))
        # 6. Dependency parse SweDiaSyn
        # TODO: This must eventually depend on a config file, not command line
        # options
        os.chdir('malt-1.2')
        run("java -Xmx512m -jar malt.jar -c swemalt -i '../%s.conll' -o '../%s.dep.conll' -m parse" % (region, region))
        os.chdir('..')
def trainCfg():
    # 7. Train CFG using GrammarTrainer
    # TODO: There are more options:  -SMcycles 5 (6 cycles overfits)
    run('java -Xmx1024m -cp berkeleyParser.jar '
        'edu.berkeley.nlp.PCFGLA.GrammarTrainer -path talbanken.mrg '
        '-out talbanken.gr -treebank SINGLEFILE')
def tagCfg():
    run('ghc -O2 --make ConvertTagsToTxt -main-is ConvertTagsToTxt.main')
    for region in consts.swediaSites:
        # 8.0 Post-process tagged SweDiaSyn to sentence-per-line format
        run("./ConvertTagsToTxt '%s.tag' >'%s.txt'" % (region,region))
        # 8. Constituency parse with Berkeley parser
        run("java -Xmx1G -jar berkeleyParser.jar -gr talbanken.gr <'%s.txt' >'%s.mrg'" % (region,region))
def genFeatures():
    run('ghc -O2 --make Path')
    run('ghc -O2 --make DepPath')
    for region in consts.swediaSites:
        run("./Path '%s.mrg' t >'%s-trigram.dat'" % (region,region))
        run("./Path '%s.mrg' p >'%s-path.dat'" % (region,region))
        run("./DepPath '%s.dep.conll' >'%s-dep.dat'" % (region,region))
def syntaxDist():
    # 9. Run icectrl.out with various parameter settings.
    # TODO: Only does paths right now, no trigrams or dependency-paths
    norte.run('path')
    norte.run('trigram')
    norte.run('dep')
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
# TODO: Cut off last couple of characters from each word for POS tagging?
