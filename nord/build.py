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
# import cgitb
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
def tryrm(file):
    try:
        run('rm ' + file)
    except:
        pass
def stage1(): # jones
    # run all the first taggers/extracters
    extractTalbanken()
    tagPos()
    tagDep()
def stage2(): # banks
    # train berkeleyParser on banks
    # first copy talbanken.mrg to banks
    run('scp ncsander@jones.ling.indiana.edu:Documents/dialect/nord/talbanken.mrg ./')
    trainCfg()
def stage3():
    # generate features on jones
    run('scp ncsander@cl.indiana.edu:Documents/dialect/nord/talbanken.gr ./')
    tagCfg()
    genFeatures()
def stage4():
    # syntax distance/sig on banks
    run('scp ncsander@jones.ling.indiana.edu:Documents/dialect/nord/*.dat ./')
    syntaxDist()
    syntaxSig()
def stage5():
    # extract most important features on jones
    run('scp ncsander@cl.indiana.edu:Documents/dialect/nord/dist*.txt ./')
    run('scp ncsander@cl.indiana.edu:Documents/dialect/nord/sig*.txt ./')
    syntaxFeatures()
def stage6():
    # generate analysis and maps on flenser
    run('scp ncsander@cl.indiana.edu:Documents/dialect/nord/dist*.txt ./')
    run('scp ncsander@cl.indiana.edu:Documents/dialect/nord/sig*.txt ./')
    run('scp ncsander@jones.ling.indiana.edu:Documents/dialect/nord/feat*.txt ./')
    genMaps()
    genAnalysis()
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
    run('ghc -O2 --make Swedia -main-is Swedia.main')
    # 2. Train TnT on Talbanken POS tags
    run('tnt-para talbanken.tt')
    # 3. Extract SweDiaSyn words into TnT format
    run('./Swedia')
    # 4. Tag SweDiaSyn
    for region in consts.swediaSites:
        run("tnt -m talbanken '%s.t' >'%s.tag'" % (region,region))
def tagDep(inext='tag', outext='dep'):
    run('ghc -O2 --make ConvertTagsToConll -main-is ConvertTagsToConll.main')
    for region in consts.swediaSites:
        # 5. Post-process tagged SweDiaSyn to CoNLL format
        run("./ConvertTagsToConll '%s.%s' malt >'%s.conll'" % (region,inext,region))
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
    run('ghc -O2 --make ConvertTagsToConll -main-is ConvertTagsToConll.main')
    for region in consts.swediaSites:
        # 8.0 Post-process tagged SweDiaSyn to sentence-per-line format
        run("./ConvertTagsToConll '%s.tag' berkeley >'%s.txt'" % (region,region))
        # 8. Constituency parse with Berkeley parser
        run("java -Xmx1G -jar berkeleyParser.jar -useGoldPOS -gr talbanken.gr <'%s.txt' >'%s.mrg'" % (region,region))
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
    run('ghc -O2 --make ConvertBerkeleyToFeature -main-is ConvertBerkeleyToFeature.main')
    run('ghc -O2 --make ConvertMaltToFeature -main-is ConvertMaltToFeature.main')
    run('ghc -O2 --make ConvertTagsToFeature')
    run('ghc -O2 --make CombineFeatures')
    for region in consts.swediaSites:
        run("./ConvertBerkeleyToFeature '%s.mrg' trigram >'%s-retrigram.dat'" % (region,region))
        run("./ConvertBerkeleyToFeature '%s.mrg' path >'%s-path.dat'" % (region,region))
        run("./ConvertBerkeleyToFeature '%s.mrg' psg >'%s-psg.dat'" % (region,region))
        run("./ConvertBerkeleyToFeature '%s.mrg' grand >'%s-grand.dat'" % (region,region))
        run("./ConvertMaltToFeature '%s.dep.conll' node >'%s-dep.dat'" % (region,region))
        run("./ConvertMaltToFeature '%s.redep.conll' node >'%s-redep.dat'" % (region,region))
        run("./ConvertMaltToFeature '%s.dep.conll' arc >'%s-deparc.dat'" % (region,region))
        run("./ConvertTagsToFeature '%s.tag' unigram >'%s-unigram.dat'" % (region,region))
        run("./ConvertTagsToFeature '%s.tag' trigram >'%s-trigram.dat'" % (region,region))
        run("./CombineFeatures '%s-path.dat' '%s-dep.dat' '%s-trigram.dat' >'%s-all.dat'" % ((region,) * 4))

variants = [(num,sample,measure,feature,norm) for sample in consts.samples
                                              for measure in consts.measures
                                              for feature in consts.features
                                              for norm in consts.norms
                                              for num in consts.numnorms ]
def syntaxDist():
    # 9. Run ctrl.out with various parameter settings.
    for sample, measure, feature, norm in variants:
        multirun(6, *norte.icetasks(consts.swediaSites,
                                    feature, 'icedist.cpp',
                                    measure, sample, norm, 10))
        norte.combine(feature, 'dist', measure, sample, norm, 10)
def syntaxSig():
    # 11. Run ctrl.out with various parameter settings.
    for sample, measure, feature, norm in variants:
        multirun(6,
                 *norte.icetasks(consts.swediaSites,
                                 feature, 'icesig.cpp', measure, sample, norm))
        norte.combine(feature, 'sig', measure, sample, norm)
def syntaxFeatures():
    run('ghc -O2 --make RankFeatures')
    clusters = sorted(consts.agreeClusters.keys(), reverse=True)
    # 12. Dump a list of all features between each pair of site clusters.
    for sample in consts.samples:
        for feature in consts.features:
            for norm2 in ['over', 'ratio']:
                # 12.1 Make cluster files first
                norte.combineFeatures(consts.agreeClusters, feature)
                multirun(6,
                         *norte.icetasks(clusters, feature,
                                         'icefeat.cpp', 'r', sample, norm2))
                # 12.2 Then analyse it
                tmps = ' '.join(["%s-%s-tmp.txt" % pair
                                 for pair in norte.pairwise(clusters)])
                run('./RankFeatures %s >feat-5-%s-%s-%s.txt'
                    % (tmps,sample,feature,norm2))
def syntaxFeaturesSimple():
    for sample, measure, feature, norm in variants:
        norte.writeparams(1000, sample, measure, norm)
        run('g++ -O2 -o ctrl.out params.h icefeat.cpp')

        for site in set(consts.swediaSites) - set(["Jamshog"]):
            run("./ctrl.out Jamshog-%s.dat '%s-%s.dat' > 'tmp-Jamshog-%s.txt'"
                % (feature, site, feature, site))
        tmps = ' '.join("'tmp-Jamshog-%s.txt'" % (site,)
                        for site in set(consts.swediaSites) - set(["Jamshog"]))
        run('./RankFeatures %s >feat-5-%s-%s-%s-%s-jamshog.txt'
            % (tmps,sample,measure,feature,norm))
def syntaxFeaturesDiagram():
    "This runs on flenser so it properly should have a 'gen' prefix I guess"
    run('ghc -O2 --make FormatFeatures')
    for sample in consts.samples:
        for feature in consts.features:
            for norm2 in ['over', 'ratio']:
                v = (sample,feature,norm2)
                run('./FormatFeatures feat-5-%s-%s-%s.txt' % v)
                for (fro,to) in norte.pairwise(sorted(consts.agreeClusters.keys(), reverse=True)):
                    fname = ('%s-%s-feat-5-%s-%s-%s' % ((to,fro) + v),)
                    run('latex %s.txt' % fname)
                    run('dvips -Ppdf %s.dvi' % fname)
                    run('ps2pdf %s.ps' % fname)
    run('mv *pdf ../')
def genAnalysis():
    run('ghc -O2 --make FormatDistance')
    run('ghc -O2 --make CalculateGeoDistance')
    run('ghc -O2 --make CalculateSizeDifference')
    run('./CalculateGeoDistance >dist-geo.txt')
    run('./FormatDistance dist-geo.txt pairwise > dist-geo.csv')
    run('./FormatDistance dist-travel.txt pairwise > dist-travel.csv')
    # 13.2 Next a 2-D table (full/redundant-matrix) for R
    run('./FormatDistance dist-geo.txt square > dist-geo-R.txt')
    run('./FormatDistance dist-travel.txt square > dist-travel-R.txt')
    run('./CalculateSizeDifference > size-R.txt')
    # 13. Generate some analysis of the output
    for variant in variants:
        # 13.1 First a 2-D table (half-matrix) for Excel
        run('./FormatDistance dist-%s-%s-%s-%s-%s.txt pairwise > dist-%s-%s-%s-%s-%s.csv' % (variant * 2))
        # 13.2 Next a 2-D table (full/redundant-matrix) for R
        run('./FormatDistance dist-%s-%s-%s-%s-%s.txt square > dist-%s-%s-%s-%s-%s-R.txt' % (variant * 2))
    # 13.3 make a CSV of significances
    for norm in consts.norms:
        for sample in consts.samples:
            for num in consts.numnorms:
                run('grep -c 0 sig*.txt >sigtmp.txt')
                sigs = dict(line.strip().split(':') for line in open('sigtmp.txt'))
                outf = open('sig-%s-%s-%s.csv' % (num,sample,norm), 'w')
                outf.write(',' + ','.join(consts.measures) + '\n')
                for feature in consts.features:
                    outf.write(feature + ',')
                    outf.write(','.join(
                        sigs['sig-%s-%s-%s-%s-%s.txt' %
                             (num, sample, measure, feature, norm)]
                        for measure in consts.measures))
                    outf.write('\n')
                outf.close()
    # 13.4 Run correlations AND hierarchical cluster figures
    # TODO: Still have to rotate to portrait after generation
    # TODO: Should generate pairwise comparisons between all feature types
    #   for each measure. But it doesn't yet.
    run('R CMD BATCH genAnalysis.R')
def genMaps():
    run('ghc -O2 --make ConvertDistToL04')
    for variant in variants:
        run('./ConvertDistToL04 dist-%s-%s-%s-%s-%s.txt >dist-%s-%s-%s-%s-%s.dif' % (variant * 2))
        run('RuG-L04/bin/mds -K -o mds-%s-%s-%s-%s-%s.vec 3 dist-%s-%s-%s-%s-%s.dif' % (variant * 2))
        tryrm('out.trn')
        tryrm('out.map')
        tryrm('out.clp')
        run('RuG-L04/bin/mapsetup -b 105 -p -c 30orter.clp -m 30orter.map')
        run('RuG-L04/bin/maprgb -o Sverigekarta-mds-%s-%s-%s-%s-%s.eps 30orter.cfg mds-%s-%s-%s-%s-%s.vec' % (variant * 2))
        # does ps2pdf work on eps? I don't need this now anyway...
        # run('ps2pdf Sverigekarta-mds-%s-%s-%s-%s-%s.eps' % variant)
        ## Clustering with cophenetic mapping to a map ##
        ## Note: 2-30 clusters are possible. but 2-8 gives better maps. ##
        run('RuG-L04/bin/cluster -wm -b -m 2-8 -o cluster-%s-%s-%s-%s-%s.dif dist-%s-%s-%s-%s-%s.dif' % (variant * 2))
        ## , then sum multiple clusters (this has to be outside the loop)##
        ## this can be very fancy, like weighting all the significant ones for
        ## a single distance measure the same over feature differences,
        ## re-allocating the insignificant ones' weight to them. ##
    run('RuG-L04/bin/difsum -o Sverigekarta-cluster.dif '
        + ' '.join('cluster-%s-%s-%s-%s-%s.dif' % v for v in variants))
    for num in consts.numnorms:
        for sample in consts.samples:
            # for numnorm=1, sample=ratio might actually be useful
            sigs = norte.findSigs(num, sample, 'ratio')
            if not sigs:
                print('nothing to see here')
                continue
            run('RuG-L04/bin/difsum -o Sverigekarta-cluster-%s-%s.dif ' % (num,sample)
                + ' '.join('cluster-%s-%s-%s-%s-ratio.dif' % (num,sample,measure,feature)
                            for feature in consts.features
                            for measure in consts.measures
                            if (feature,measure) in sigs))
            run('RuG-L04/bin/mapdiff -c 2.5 -o Sverigekarta-cluster-%s-%s.eps 30orter.cfg Sverigekarta-cluster-%s-%s.dif' % (num,sample,num,sample))
    run('mv *eps ..')
def genMoreAnalysis():
    "Yeah, this is a stupid name. But it does what it says what it does."
    run('ghc -O2 --make Analysis')
    run('ghc -O2 --make Consensus')
    tryrm('correlations.tex')
    tryrm('consensusses.tex')
    run('RuG-L04/bin/maprgb -r -o Sverigekarta-Landskap-consensus-1-1000.eps 30orter.cfg consensus-1-1000.vec')
    run('RuG-L04/bin/maprgb -r -o Sverigekarta-Landskap-consensus-1-full.eps 30orter.cfg consensus-1-full.vec')
    run('RuG-L04/bin/maprgb -r -o Sverigekarta-Landskap-consensus-5-1000.eps 30orter.cfg consensus-5-1000.vec')
    # running either of this is unsafe because they require hand-tweaking of the
    # code. They both now take *some* parameters, but not everything
    # or travel-sig-inclusion or cos-exclusion or row/col-inclusion in Consensus
    # (or unigram-exclusion, another good idea)
    for num in consts.numnorms:
        for sample in consts.samples:
            for norm in consts.norms:
                run('echo %s-%s-%s >>consensusses.tex' % (num,sample,norm))
                run('./Consensus %s %s %s correlations-R.txt >>consensusses.tex'
                    % (num,sample,norm))
                for key in ['geo', 'travel', 'size']:
                    run('echo %s-%s-%s-%s >>correlations.tex' % (num,sample,norm,key))
                    run('./Analysis %s %s %s %s >>correlations.tex' % (num,sample,norm,key))
    # TODO: FormatFeatures goes in here somewhere with
    # latex clusterA-clusterD-feat-5-1000-r-trigram-ratio.txt && dvips -Ppdf clusterA-clusterD-feat-5-1000-r-trigram-ratio.dvi && ps2pdf clusterA-clusterD-feat-5-1000-r-trigram-ratio.ps && open clusterA-clusterD-feat-5-1000-r-trigram-ratio.pdf
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
