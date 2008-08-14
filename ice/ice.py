"""This code unrepentantly requires Python 2.5.
Please do not use #!/usr/bin/python since Jones' python is only 2.3
instead do
$ python2.5 ice.py

See also translations to Caml and C++. C++ (ice.cpp) is the version currently
in use."""
from __future__ import division # Python sucks at math
import sys
import re
import random
from itertools import imap
from operator import le
from util import dct
from util.fnc import car, cdr, compose, cur, iseq
from util.fs import slurp, dump
from util.lst import fst, snd, concat, mapn, cross, unzip, window
from util.reflect import traced
from util.cl import findif, countif
from util.text import chomp
from iceread import groupby, read
from path import paths
def debug(e): # I think I defined this somewhere in util
    print e
    return e
## Nerbonne's counting and comparison ##
def permutation(dialect):
    return concat([random.choice(dialect) for _ in xrange(1000)])
def countpaths(a,b):
    "[Path]*[Path]->{Path:(float,float)}"
    #TODO:I should change default=0 to some smoothed value
    return dct_zip(dct.count(a), dct.count(b), default=0)
def normalise(a,b):
    """[Path]*[Path]->{Path:(float,float)} where type Path = [str]"""
    ab = countpaths(a,b)
    N = len(a) + len(b)
    n = len(ab)
## Original code: (7 lines to 8)
##    def norm((a_i,b_i)):
##        fa = a_i/len(a)
##        fb = b_i/len(b)
##        f = fa+fb
##        ci=a_i+b_i
##        return (ci*fa*2*n)/(f*N), (ci*fb*2*n)/(f*N)
##    return dct.map(norm, ab)
    for k, [a_i,b_i] in ab.iteritems():
        fa = a_i/len(a)
        fb = b_i/len(b)
        f = fa+fb
        ci = a_i+b_i
        ab[k][0] = (ci*fa*2*n)/(f*N)
        ab[k][1] = (ci*fb*2*n)/(f*N)
    return ab
def ara_avg(l, key):
    total = 0
    for x in l:
        total += key(x)
    return total / len(l)
def dct_zip(*ds,**kws):
    """Just like dct.zip except it returns lists instead of tuples,
    which is the Wrong Thing usually, but I need to make destructive updates
    """
    e={}
    if 'default' in kws:
        default = kws['default']
        for k in reduce(set.__or__, map(set,ds)):
            e[k] = [d.get(k,default) for d in ds]
    else:
        for k in ds[0]:
            try:
                e[k] = [d[k] for d in ds]
            except KeyError: pass
    return e
def normaliseall(a,b):
    "[[Path]]*[[Path]]->{Path:[(float,float)]}--Organise Paths by sentence."
##    return dct.map(norm, dct.zip(default=(0,0),
##                   *[normalise(permutation(a),
##                               permutation(b)) for _ in xrange(1000)])
    # main body: 3 lines to 11
    # norm: 6 lines to 14
    tmp = {}
    for sentence in a:
        for path in sentence:
            if path not in tmp: tmp[path] = [None] * 1000
    for sentence in b:
        for path in sentence:
            if path not in tmp: tmp[path] = [None] * 1000
##     for path in set(concat(a)) | set(concat(b)):
##         tmp[path] = [[0,0]] * 1000
    ab = a
    ab.extend(b)
    del a; del b
    for i in xrange(1000):
        normtmp = normalise(permutation(ab), permutation(ab))
	for k,v in tmp.iteritems():
            try:
                v[i] = normtmp[k]
            except KeyError:
                v[i] = [0,0]
        del normtmp
        sys.stdout.write('.'); sys.stdout.flush()
    del ab
    print
    for abs in tmp.itervalues(): # this used to be the norm function
        all_as = ara_avg(abs, fst)
        all_bs = ara_avg(abs, snd)
        if all_as==0.0 and all_bs==0.0:
            pass
        elif all_as==0.0:
            for i,[a,b] in enumerate(abs):
                abs[i][1] = b/all_bs
        elif all_bs==0.0:
            for i,[a,b] in enumerate(abs):
                abs[i][0] = a/all_as
        else:
            for i,[a,b] in enumerate(abs):
                abs[i][0] = a/all_as
                abs[i][1] = b/all_bs
    return tmp
def r(c):
    total = 0 # I am not convinced this is a useful optimisation for Python
    for a,b in c: # unless its GC is messed up by nested functions, which
        avg = (a+b)/2 # I suspect.
        total += abs(a-avg) + abs(b-avg)
    return total
#    def tmp((a,b)):
#        avg = (a+b)/2
#        return abs(a-avg) + abs(b-avg)
#    return sum(imap(tmp,c))
def compare(a,b):
    r_total = debug(r(normalise(concat(a),concat(b)).itervalues()))
    # Original code: (1 line to 10)
    # return countif(cur(le,r_total), map(r,unzip(normaliseall(a,b).values())))
    count = 0
    totals = [0] * 1000
    normeds = normaliseall(a,b)
    for ab in normeds.itervalues():
        for i in xrange(1000):
            a,b = ab[i]
            avg_ab = (a + b) / 2
            totals[i] += abs(a - avg_ab) + abs(b - avg_ab)
    return countif(cur(le,r_total), totals)
if __name__=="__main__":
    l1name,l1 = extract.read(sys.argv[1])
    l2name,l2 = extract.read(sys.argv[2])
    #(l1name,l1),(l2name,l2) = slurp(sys.argv[1])
    print l1name, l2name,
    print compare(l1,l2)
    
##  x = iceread.groupby(sys.argv[1], 12) # x :: {str:[Node]}
                                    # where Node :: str | (str, [Node])
##  dump('trees.dat', x)
##  x = dct.map(lambda speaker: map(paths, speaker), x) # x :: 
##  dump('paths.dat', x)
##   import gc
##   ##x = slurp('paths.dat') #resume after doing above steps
##   #results = [] # had got up to 8:12
##   for (l1name,l1),(l2name,l2) in cross(x.iteritems(), x.iteritems())[:4]:
##     print l1name, l2name,
##     total_r = compare(l1,l2)
##     print total_r
##     gc.collect()
    #results.append(total_r)
  #results = [compare(l1,l2) for l1,l2 in cross(x.values(), x.values())]
"""Notes on memory consumption:
slurp('paths.dat') takes about 50 MB. So the gimped compare (that is
(r . normalise)) was only taking about a meg or two for each call"""
{(']', 'PU,CL', 'OD,NP', 'NPHD,N'): (0.0, 1.75),
 ('PU,CL', 'OD,CL', '[', 'SU,NP', 'NPHD,PRON'): (1.75, 0.0),
 ('PU,CL', '[', 'INTOP,AUX'): (0.0, 1.75),
 ('PU,CL', '[', 'SU,NP', 'NPHD,PRON'): (1.75, 0.0),
 ('PU,CL', 'VB,VP', 'MVB,V'): (1.75, 1.75),
 (']', 'PU,CL', 'OD,CL', 'VB,VP', 'MVB,V'): (1.75, 0.0), ('PU,CL', 'SU,NP', 'NPHD,N'): (0.0, 1.75)}
## ps = dct.count(paths(read_ice(list(open('/Volumes/Data/Corpora/en/ICE-GB/ice-gb-2/data/s1a-012.cor')))))
## for path,count in ps.items():
##     print '%s\t%s' % (count, path)
# nohup python ice.py 
