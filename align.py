from __future__ import division # Corporate math still sucks
from util import dct
from util.fnc import cur,compose,pipe,negate,iseq,named
from util.reflect import postmortem
from util.lst import concat, avg, fst, snd, car, cdr
from itertools import imap
import lev
from unifeat import unify
from operator import sub, or_, and_
fs = ['../phonology/dialect/utp02datanew.txt',
      '../phonology/dialect/see26datanew.txt',
      '../phonology/dialect/sgb20datanew.txt',
      '../phonology/dialect/sgj20datanew.txt',
      '../phonology/dialect/sgl20datanew.txt',
      '../phonology/dialect/sif20datanew.txt',
      '../phonology/dialect/siw20datanew.txt',
      '../phonology/dialect/siz20datanew.txt',
      '../phonology/dialect/siy20datanew.txt',
      '../phonology/dialect/smd20datanew.txt',]
def read_unicode(f):
    "filename->[[utf-8-char]]"
    return map(lambda u: map(lambda s:s.encode('utf8'), u),
               file(f).read().decode('utf16').split(u'\n'))
def self_sub(change):
    "lev.Rule -> bool -- Is this a boring self-substitution?"
    return change.type==lev.SUB and change.src==change.dst
class Hash():
    "Box with proxied __eq__ and __hash__ to allow custom hashing (dict & set)"
    def __init__(self, eq, hash, x):
        lev.init_attrs(self, locals())
    def __str__(self):
        return 'Hash(%s, eq=%s, hash=%s)' % (self.x, self.eq, self.hash)
    def __repr__(self):
        return 'Hash(eq=%r, hash=%r, x=%r)' % (self.eq, self.hash, self.x)
    def __hash__(self):
        return self.hash(self.x)
    def __eq__(self, other):
        return self.eq(self.x, other.x)
    def get(self):
        return self.x
def cmpset(l, eq, hash):
    return set(hx.get() for hx in set(Hash(eq, hash, x) for x in l))
def collapse_envs(rules):
    "[lev.Rule] -> set<lev.Rule>"
    return cmpset(rules, lev.Rule.eq_env, lev.Rule.hash_env)
def classify(row):
    "[[lev.Rule]] -> {utf-8-char:set<lev.Rule>}"
    return dct.map(set, #collapse_envs,
                   dct.collapse(filter(negate(self_sub), concat(row)),
                                keymap=lambda rule:rule.src))
def compare(l1, l2):
    "str*str -> [[lev.Rule]]"
    lang1 = read_unicode(l1)
    lang2 = read_unicode(l2)
    dist = lev.totalavgdistance(map(unify, lang1), map(unify, lang2))
    return map(lambda s1,s2:(lev.enviro(s2,s1,dist) if s2 else []),
               lang1, lang2)
def run_compare_to_base(fs):
    "[str] -> [{utf-8-char:set<lev.Rule>}]"
    return map(pipe(cur(compare, fs[0]), classify), fs)
def run_compare_all_to_sgbsiy(fs):
    """[str] -> {utf-8-char:set<lev.Rule>}
    (siy<=>sgb) - (map (base<=>) rest)"""
    sgb = fs[2]
    siy = fs[8]
    base = fs[0]
    del fs[8]; del fs[2]; del fs[0] # dangerous but who cares
    diff = classify(compare(sgb, siy))
    others = map(compose(classify, cur(compare, base)), fs)
    # return dct_mapall(lambda v,*rest: reduce(sub, rest, v), diff, *others)
    kws = {'default':set()}
    return dct.zipwith((lambda v,*rest: reduce(sub, rest, v)), diff, *others, **kws)
def run_compare_sgbsiy_to_base(fs):
    """[str] -> {utf-8-char:set<lev.Rule>}
    ((sgb <=> base) | (sgb <=> base)) - (map (<=> base) rest)"""
    sgb = fs[2]
    siy = fs[8]
    base = fs[0]
    del fs[8]; del fs[2]; del fs[0] # dangerous but who cares
    outsiders = dct.zipwith(or_,
                            classify(compare(base, sgb)),
                            classify(compare(base, siy)),
                            default=set())
    others = map(compose(classify, cur(compare, base)), fs)
    kws = {'default':set()}
    return dct.zipwith((lambda v,*rest: reduce(sub, rest, v)), outsiders, *others, **kws)
def run_compare_sgb_and_siy_to_base(fs):
    """[str] -> {utf-8-char:set<lev.Rule>}
    ((sgb <=> base) & (sgb <=> base)) - (map (<=> base) rest)"""
    sgb = fs[2]
    siy = fs[8]
    base = fs[0]
    del fs[8]; del fs[2]; del fs[0] # dangerous but who cares
    outsiders = dct.zipwith(and_,
                            classify(compare(base, sgb)),
                            classify(compare(base, siy)),
                            default=set())
    others = map(compose(classify, cur(compare, base)), fs)
    kws = {'default':set()}
    return dct.zipwith((lambda v,*rest: reduce(sub, rest, v)), outsiders, *others, **kws)
def run_compare_shared_sgbsiy(fs):
    """this really needs a lenient definition of eq?
    (sgb <=> base) & (siy <=> base)"""
    sgb = fs[2]
    siy = fs[8]
    base = fs[0]
    del fs[8]; del fs[2]; del fs[0] # dangerous but who cares
    return dct.zipwith(and_,
                       classify(compare(base, sgb)),
                       classify(compare(base, siy)),
                       default=set())
getsrc = named('src', lambda rule: rule.src)
getdst = named('dst', lambda rule: rule.dst)
getpair = named('rule', lambda rule: (rule.dst, rule.src))
def run_collapse_differences(fs, get=getdst):
    base = fs[0]
    del fs[0]
    subs = [[get(rule) for rule in concat(compare(base,f))
             if rule.type==lev.SUB and rule.dst!=rule.src]
            for f in fs]
    return dct.zip(dct.count(concat(subs)), default=0, *map(dct.count, subs))
def lst_except(l, *ns):
    """Totally inefficient! You have been warned, dude!
    (requiring ns to be ordered could help a lot if I actually cared)"""
    acc = []
    for i,x in enumerate(l):
        if i not in ns:
            acc.append(x)
    return acc
def find_collapsed(f, collapsed):
    "{char:[int]} -> [(char,int)] (sorted)"
    return sorted(dct.map(f, collapsed).items(), key=snd, reverse=True)
diff = lambda freqs:avg([freqs[2],freqs[8]]) - avg(lst_except(freqs,0,2,8))
def variance(freqs):
    average = avg(cdr(freqs))
    return sum((average - c)**2 for c in cdr(freqs)) / average
find_difference = cur(find_collapsed, diff)
find_variance = cur(find_collapsed, variance)
def to_html_group_differences(f, name, differences):
    print >>f, "<h1>%s</h1>" % name
    print >>f, "<table border=1 cellspacing=0 bordercolor='black'><tr><td></td><th>Char</th><th>Variance</th>",
    for i, (sub,variance) in enumerate(differences):
        if isinstance(sub, tuple):
            s = "<tr><td>%s</td><td>%s &rarr; %s</td><td>%s</td></tr>"
            row = i, sub[1], sub[0], variance
        else:
            s = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
            row = i, sub, variance
        print >>f, s % row
    print >>f, "</table>"
def to_html_variances(f, name, variances):
    print >>f, "<h1>%s</h1>" % name
    print >>f, "<table border=1 cellspacing=0 bordercolor='black'><tr><th>Char</th><th>Variance</th>",
    for pair in variances:
        print >>f, "<tr><td>%s</td><td>%s</td></tr>" % pair
    print >>f, "</table>"
def to_html_differences(f, name, combined):
    "file*str*{char:[int]} "
    print >>f, '''<h1>%s</h1>''' % name
    print >>f, "<table border=1 cellspacing=0 bordercolor='black'><tr><th>Char</th><th>All</th>",
    print >>f, ''.join('<th>%s</th>' % f[21:24] for f in fs[1:]), "<th>Avg</th></tr>"
    for char,counts in combined.items():
        print >>f, "<tr><td>%s</td>" % char,
        print >>f, ''.join("<td>%s</td>" % c for c in counts),
        print >>f, "<td>%.2f</td></tr>" % avg(counts[1:])
    print >>f, "</table>"
def to_html(f,name,row):
    print >>f, '''<h1>%s</h1>''' % name
    for char,changes in row.items():
        print >>f, '<h2>%s</h2><p>' % char
        for change in changes:
            print >>f, '%s<br/>' % change.to_html()
        print >>f, '</p>'

if __name__=="__main__":
    setup = ((run_compare_sgb_and_siy_to_base,
              'rule/smartenv',
              '((sgb <=> base) & (siy <=> base)) - (map (<=> base) rest), eq?-rule/smartenv',
              'sgb_and_siy_to_base'),
             (run_compare_sgb_and_siy_to_base,
              'rule',
              '((sgb <=> base) & (siy <=> base)) - (map (<=> base) rest), eq?-rule',
              'sgb_and_siy_to_base-simple'),
             (run_compare_sgbsiy_to_base,
              'rule',
              '((sgb <=> base) | (siy <=> base)) - (map (<=> base) rest), eq?-rule',
              'sgbsiy_to_base-simple'),
             (run_compare_shared_sgbsiy,
              'all',
              '(sgb <=> base) & (siy <=> base), eq?-all',
              'shared_sgbsiy-full'),
             (run_compare_shared_sgbsiy,
              'rule',
              '(sgb <=> base) & (siy <=> base), eq?-rule',
              'shared_sgbsiy-simple'),
             (run_compare_shared_sgbsiy,
              'rule/smartenv',
              '(sgb <=> base) & (siy <=> base), eq?-rule/smartenv',
              'shared_sgbsiy')
             )
    setup = ((run_collapse_differences,
              'xxx',
              'Counting differences',
              'count_differences'),)
    for run,rule,title,fname in setup:
        #f = open('align_'+fname+'-revised.html', 'w')
        f = open(fname+'.html', 'w')
        print >>f, '''<html><head>
    <meta http-equiv="content-type" content="text-html; charset=utf-8">
    <title>Observed changes from baseline English</title></head><body>'''
        lev.setRuleCompare(rule)
        #to_html(f, title, run(list(fs)))
        for attr in (getsrc,getdst,getpair):
            to_html_group_differences(f,
                              "%s &ndash; %s" % (title,attr.func_name),
                              find_difference(run(list(fs), attr)))
##             to_html_differences(f,
##                                 "%s &ndash; %s" % (title,attr.func_name),
##                                 run(list(fs), attr))

##     map(to_html,
##         ('utp02', 'see26', 'sgb20', 'sgj20', 'sgl20', 'sif20','siw20','siz20'),
##          run(fs))
        print >>f, '</body></html>'
        f.close()
# number of things that got thrown out because they were shared
{'': 18,
 '\xc9\x99': 3,
 '\xc9\x9b': 1,
 'b': 7,
 'e': 1,
 'd': 2,
 '\xc9\x91': 6,
 'k': 8,
 'j': 1,
 '\xca\xb0': 6,
 '\xc9\x94': 3,
 'o': 3,
 'n': 2,
 'p': 1,
 's': 3,
 '\xc9\xaa': 4,
 't': 7,
 '\xca\x8a': 7,
 'v': 0,
 'w': 2,
 '\xca\x83': 0}
{'': 31,
 '\xc9\x99': 4,
 '\xc9\x9b': 2,
 'b': 8,
 'e': 1,
 'd': 2,
 '\xc9\x91': 7,
 'k': 8,
 'j': 2,
 '\xca\xb0': 8,
 '\xc9\x94': 4,
 'o': 4,
 'n': 3,
 'p': 5,
 's': 6,
 '\xc9\xaa': 10,
 't': 9,
 '\xca\x8a': 7,
 'v': 1,
 'w': 2,
 '\xca\x83': 1}
# changes that weren't even shared by at least one of the others
# (so actually these should be calculated also at some point)
set(['\xc9\x9c', '\xc9\x92', '\xc9\xbe', '\xc3\xa7', '\xc3\xa6', '\xc9\xa8', '\xc9\xab', '\xc9\xac', '\xc9\xaf', '\xc3\xb0', '\xca\x94', '\xce\xb8', '\xca\x8f', '\xca\x89', '\xca\x82', 'a', '\xca\x8c', 'g', 'f', 'i', 'h', 'm', 'l', 'r', 'z'])
# segments with [dorsal] cause a violation (in the OT paper) (this def is a
# little weak)
# try lining up everything logically for the HTML dump
# clustering is really clustering pathologies and then I would like to extract
# the details so that treatment can be prescribed once particular patterns of
# deafness are identified and categorised
# worked on Tuesday 1.5 h looking for this paper.
# Wednesday 2 h + 8.25-22
# Thursday: 8:30 - 11:45
# Friday: 9:15 - 9:45
# try to find 'guidelines for constraints' paper again
# I uh, can't find this, but here some cool papers on the ROA (abstract only)
# 909: Boersma and Hamann show that the 'prototype effect' can be derived
# by OT simulations who optimise their grammars.
# 484: Jonas Kuhn's thesis on computational OT syntax (OT-LFG)
# 895: An alternative to iterative footing (might be relevant, the abstract
# seems a little confused)
# 888: Proves that the computational complexity of stochastic OT learning
# algorithms is k-1
# 883: Tessier's BCD dissertation
# 878 (823) (844.8): McCarthy's OT-CC 'Slouching toward optimality'
# 873: Antilla's T-orders
# 872: Pater et al: Harmonic Grammars translate into linear systems. I think
# these grammars are supersets of OT grammars. They have code available.
# 863/864: Andries Coetzee: I think this is the weird non-OT talk he gave at
# Phonology Fest weekend. (His dissertation is at 687)
# 858: Hayes and Wilson's Maximum Entropy Learning
# 851: Oostendorp argues against Port's incomplete neutralisation
# 835: On-line learning of underlying forms. 10 pages! But it's magic!
# 818: Use a freakin' machine to do OT! Also, Finnish is hard.
# 811: Learn underlying forms by restricting search to a lexical subspace. (short too)
# 798: Prince turns OT back into Harmony Theory via 'utility functions'??
# 844.12: Tesar talks about learning paradigms
# 794: Hey! It's those FRed people! But with a paper instead of bad Ruby.
# 780: Pater shows how to handle variation with an RCD-family algorithm
# 746: Apouussidou and Boersma compare GLA and EDCD for learning stress.
# GLA is better. Surprise!
# 739: Pater modifies BCD to learn Stratal OT (?) grammars.
# 695: Tesar creates Constrast Analysis for learning (see 811)
# 688: Generating 'contenders' from an infinite list of candidates. FSTs+RCD
# 683: McCarthy shows how to learn faithful /B/->[B] mappings after having
# learnt the harder /A/->[B] one.
# 672..675: Keller and Asudeh: GLA sucks! (although RCD does too)
# 638: Boersma reviews Tesar & Smolensky 2000 and says that learnability means
# that not all factorial typologies are possible??!
# 625: Jaeger: compares Stochastic OT with Boersma's MaxEnt model and shows
# that you can get GLA to work with Maximum Entropy too and you get
# guaranteed convergence
# 620: Tesar and Prince use phonotactics (?) to learn phono. alternations
# 618/619: " " et al add inconsistency detection to BCD, speeding it up
# 610: A U Mass thesis on syncope
# 600: Some constraints generate violations quadratic in the length of the word
# like Align(Foot, Word), so you can prove that OT phonology is not regular.
# 592: Catalan may have similar syllabification to Mongolian in its clitics
# 562: Prince explains comparative tableaux (I think have this already)
# 544: Jaeger: Proposes Bidirectional GLA (sets up a speaker/hearer loop?)
# 537: Prince and Smolensky's original OT manuscript, revised slightly
# 536: Prince explores alternative architectures more similar to Harmny Theory
# from the 80s. And sees what happens.
# 500: Entailed Rankings Arguments: Prince formalises what a machine needs to
# know to do OT. (I think I have this already)
# 463: Somebody wrote a contraint runner in 2001. As usual, works on stress.
# 459: More candidates than atoms in the universe: somebody bad at math debunks
# OT again. (n m) not n!m! maybe...
# 446: Broselow writes about Stress-epenthesis interactions.
# (I may have this already)
# 426: (Tesar introduces inconsistency detection)
# 418: Lombardi explains why L2 English speakers use either [s] or [t] based on L1
# 400: Minimal constraint demotion in (human) acquisition of German
# 392: Argument that pure Lexicon Optimisation is too restrictive
# 390: Michael Hammond does some more logic<=>OT isomorphisms
#
