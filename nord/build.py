# -*- coding: utf-8 -*-
"""
0. Manually make a list of which files go with which regions.
(Regions are based on filename right now)

Notes:
SCons, in Python, replaces make and allows extensibility in Python.
"""
import os
import sys
import consts
import norte
import cgitb
from util.lst import partition
import subprocess
# cgitb.enable(format='text') # hurting more than it's helping right now

def multirun(n, tasks, files):
    processes = [subprocess.Popen(tasks[i], stdout=open(files[i],'w'))
                 for i in range(n)]
    i = n
    while processes != []:
        subprocess.Popen(['sleep', '0.25']).wait()
        processes, dones = partition(lambda p:p.poll() is None, processes)
        for _ in dones:
            if i < len(tasks):
                print("Starting", ' '.join(tasks[i]))
                processes.append(subprocess.Popen(tasks[i],
                                                  stdout=open(files[i], 'w')))
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
def tagDep(inext='tag', outext='dep'):
    run('ghc -O2 --make ConvertTagsToConll -main-is ConvertTagsToConll.main')
    for region in consts.swediaSites:
        # 5. Post-process tagged SweDiaSyn to CoNLL format
        run("./ConvertTagsToConll '%s.%s' >'%s.conll'" % (region,inext,region))
        # 6. Dependency parse SweDiaSyn
        # TODO: This must eventually depend on a config file, not command line
        # options
        os.chdir('malt-1.2')
        run("java -Xmx512m -jar malt.jar -c swemalt -i '../%s.conll' -o '../%s.%s.conll' -m parse" % (region,region,outext))
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
        # run("./ConvertTagsToTxt '%s.tag' >'%s.txt'" % (region,region))
        run("./ConvertTagsToTxt '%s.t' >'%s.txt'" % (region,region))
        # 8. Constituency parse with Berkeley parser
        run("java -Xmx1G -jar berkeleyParser.jar -gr talbanken.gr <'%s.txt' >'%s.mrg'" % (region,region))
def retagDep():
    # 101.0 based on parts of speech by Berkeley parser,
    run('ghc -O2 --make ConvertPTBToTags')
    for region in consts.swediaSites:
        # 101.1 extract just the parts of speech, dump them to .retag
        run("./ConvertPTBToTags '%s.mrg' >'%s.retag'" % (region,region))
    # 101.2 call tagDep with different parameters
    tagDep(inext='retag', outext='redep')
    # etc etc ... that is, just rerun everything else on the new 'redep' files
def genFeatures():
    # so I guess this is 10.0: generate features from annotations
    run('ghc -O2 --make Path -main-is Path.main')
    run('ghc -O2 --make DepPath -main-is DepPath.main')
    for region in consts.swediaSites:
        run("./Path '%s.mrg' trigram >'%s-trigram.dat'" % (region,region))
        run("./Path '%s.mrg' path >'%s-path.dat'" % (region,region))
        run("./DepPath '%s.dep.conll' node >'%s-dep.dat'" % (region,region))
        run("./DepPath '%s.redep.conll' node >'%s-redep.dat'" % (region,region))
        run("./DepPath '%s.dep.conll' arc >'%s-deparc.dat'" % (region,region))
        all = open('%s-all.dat' % region, 'w')
        all.write(region + '\n')
        for feature in ['path', 'trigram', 'dep']:
            # TODO:Make sure that \n***\n doesn't write 1 too many newlines
            all.writelines(open('%s-%s.dat' % (region,feature)).readlines()[1:])
            all.write('\n***\n')
        all.close()
def variants():
    return ((measure,feature)
            for measure in ['r', 'r_sq', 'kl', 'js']
            for feature in ['path', 'trigram', 'dep', 'redep', 'deparc', 'all'])
def syntaxDist():
    # 9. Run ctrl.out with various parameter settings.
    for measure, feature in variants():
        multirun(6, *norte.icetasks(consts.swediaSites,
                                    feature, 'icedist.cpp',
                                    measure=measure, iterations=10))
        norte.combine(feature, 'dist', measure=measure, iterations=10)
def syntaxSig():
    # 11. Run ctrl.out with various parameter settings.
    for measure, feature in variants():
        multirun(6, *norte.icetasks(consts.swediaSites,
                                    feature, 'icesig.cpp', measure))
        norte.combine(feature, 'sig', measure)
def syntaxFeatures():
    run('ghc -O2 --make RankFeatures')
    # 12. Dump a list of all features between each pair of site clusters.
    for measure, feature in variants():
        # 12.1 Make cluster files first
        norte.combineFeatures(consts.agreeClusters, feature)
        multirun(6, *norte.icetasks(list(consts.agreeClusters.keys()),
                                    feature, 'icefeat.cpp', measure))
        # 12.2 Then analyse it
        tmps = ' '.join([
            "%s-%s-tmp.txt" % pair
            for pair in norte.pairwise(list(consts.agreeClusters.keys()))])
        run('./RankFeatures %s >feat-5-1000-%s-%s-interview.txt'
            % (tmps,measure,feature))
def genAnalysis():
    run('ghc -O2 --make FormatDistance')
    run('ghc -O2 --make CalculateGeoDistance')
    run('./CalculateGeoDistance >dist-10-1000-geo-interview.txt')
    run('./FormatDistance dist-10-1000-geo-interview.txt pairwise > dist-10-1000-geo-interview.csv')
    # 13.2 Next a 2-D table (full/redundant-matrix) for R
    run('./FormatDistance dist-10-1000-geo-interview.txt square > dist-10-1000-geo-interview-R.txt')
    # 13. Generate some analysis of the output
    for measure, feature in variants():
        # 13.1 First a 2-D table (half-matrix) for Excel
        run('./FormatDistance dist-10-1000-%s-%s-interview.txt pairwise > dist-10-1000-%s-%s-interview.csv' % (measure, feature, measure, feature))
        # 13.2 Next a 2-D table (full/redundant-matrix) for R
        run('./FormatDistance dist-10-1000-%s-%s-interview.txt square > dist-10-1000-%s-%s-interview-R.txt' % (measure, feature, measure, feature))
    # 10.3 Here is the resulting R code. Cmd-S the resulting window after
    # sizing it to a nice size.
    # maybe there is an automated way to do this.
    # > dep <- read.table("/Users/zackman/Documents/dialect/nord/dist-10-1000-r-dep-interview-R.txt", header=TRUE)
    ## > path <- read.table("/Users/zackman/Documents/dialect/nord/dist-10-1000-r-path-interview-R.txt", header=TRUE)
    ## > trigram <- read.table("/Users/zackman/Documents/dialect/nord/dist-10-1000-r-trigram-interview-R.txt", header=TRUE)
    ## > geo <- read.table("/Users/zackman/Documents/dialect/nord/dist-10-1000-geo-R.txt", header=TRUE)
    ## > plclust(hclust(as.dist(trigram), method="ward"), hang=-1, sub="", xlab="", ylab="Trigram")
    ## > plclust(hclust(as.dist(path), method="ward"), hang=-1, sub="", xlab="", ylab="Leaf-Ancestor Path")
    ## > plclust(hclust(as.dist(dep), method="ward"), hang=-1, sub="", xlab="", ylab="Dependency")
    ## > plclust(hclust(as.dist(geo), method="ward"), hang=-1, sub="", xlab="", ylab="Geographical Distance")
    ## source("/Users/zackman/Documents/dialect/montecarlo Mantel example.R")
    ## cor(vectorise(geo), vectorise(dep)) (cross [geo,trigram,path,dep])
    ## mantel(geo, dep, 33) (cross [geo,trigram,path,dep]
def genMaps():
    run('ghc -O2 --make ConvertDistToL04')
    for measure, feature in variants():
        run('./ConvertDistToL04 dist-10-1000-%s-%s-interview.txt >dist-10-1000-%s-%s-interview.dif' % (measure, feature, measure, feature))
        run('RuG-L04/bin/mds -o mds-10-1000-%s-%s-interview.vec 3 dist-10-1000-%s-%s-interview.dif' % (measure, feature, measure, feature))
        try:
            run('rm out.trn') # mapsetup won't overwrite out.trn
        except:
            pass
        run('RuG-L04/bin/mapsetup -l interview.coo -p')
        cfg = open('Sverigekarta.cfg', 'w')
        cfg.write('transform: out.trn\n')
        cfg.write('labels: interview.labels\n')
        cfg.write('coordinates: interview.coo\n')
        cfg.write('clipping: sverige.clp\n')
        #TODO: cfg.write(province borders???)
        cfg.close()
        run('RuG-L04/bin/maprgb -o Sverigekarta-mds-%s-%s.eps Sverigekarta.cfg mds-10-1000-%s-%s-interview.vec' % (measure, feature, measure, feature))
        # run('Something to convert eps to pdf')
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
