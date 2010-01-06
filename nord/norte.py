from __future__ import division
from util.lst import group, cross, concat
from util import dct
from util.txt import chomp
from consts import swediaSites
import os
from codecs import open
### util ###
def typecheck(*args):
    def wrapper(f):
        return f
    return wrapper
def pairwise(l):
    return [(x,y) for i,x in enumerate(l) for y in l[i+1:]]
### runner ###
def multirun(feature):
    params = open('params.h','w')
    params.write('#define ITERATIONS 100\n')
    params.write('#define SAMPLES 1000\n')
    params.write('#define R_MEASURE r')
    params.close()

    os.system('g++ -O2 -o ctrl.out params.h icesig.cpp')
    suffix = '-' + feature + '.dat'
    ctrl = "nice -n 6 ./ctrl.out".split()
    pairs = pairwise(swediaSites)
    tasks = [ctrl + [sq(fro+suffix), sq(to+suffix)] for (fro,to) in pairs]
    files = ['dist-%s-%s-tmp.txt' % (fro,to) for (fro, to) in pairs]
    return (tasks,files)
def sq(s):
    return "'" + s + "'"
def combine(feature):
    "Combine the disparate output files into one"
    out = 'dist-100-1000-r-%s-interview.txt' % (feature,)
    pairs = pairwise(swediaSites)
    files = ['dist-%s-%s-tmp.txt' % (fro,to) for (fro,to) in pairs]
    outf = open(out, 'w')
    for file in files:
        outf.write(open(file).read())
    outf.close()
def run(feature):
    out = 'dist-100-1000-r-%s-interview.txt' % (feature,)
    print('Starting', out, '...')
    open ('swedia-distance.sh','w',encoding='utf-8').write(gensh(out, feature))
    try: # delete previous run (since swedia-distance.sh appends to the file)
        os.remove(out)
    except OSError:
        pass # don't complain for the first run when there is no output file
    params = open('params.h','w')
    params.write('#define ITERATIONS 100\n')
    params.write('#define SAMPLES 1000\n')
    params.write('#define R_MEASURE r')
    params.close()

    os.system('g++ -O2 -o ctrl.out params.h icesig.cpp')
    os.system('nice -n 6 nohup bash swedia-distance.sh >>nohup.out')
def gensh(outname, suffix):
    sh = '#!/bin/bash\n'
    suffix = '-' + suffix + '.dat'
    return sh + '\n\n'.join("""echo Starting %(n1)s %(n2)s ...
nice -n 6 ./ctrl.out '%(n1)s%(suf)s' '%(n2)s%(suf)s' >>'%(out)s'"""
                              % dict(n1=name1,n2=name2,suf=suffix,out=outname)
                            for name1,name2 in pairwise(swediaSites))
def norm(s):
    if s.endswith("_tiny\n"):
        return chomp(s)[:-5]
    else:
        return chomp(s)
### analysis ###
@typecheck(str, [(str,str,str)])
def clean(outname):
    return [(norm(src),norm(dst),sig)
            for (src,dst,dots,sig) in group(list(open(outname)), 4)]
            #for (src,dst,d_avg,dots,sig) in group(list(open(outname)), 5)]
@typecheck([(str,str,str)], int, [(str,str)])
def significants(edges, iterations):
    return [(src,dst) for (src,dst,sig) in edges
                      if float(sig) / iterations <= 0.05]
@typecheck([(str,str,str)], int, {str:[str]})
def graph(edges, iterations):
    return dct.collapse_pairs(significants(edges, iterations))
def directed(graph):
    return dct.collapse_pairs(concat([[(k,v),(v,k)]
                                      for k in graph for v in graph[k]]))
@typecheck(str, int, {str:[str]})
def process(outname, iterations):
    return graph(clean(outname), iterations)
@typecheck(str, [[str]], {(str,str):int})
def count(filepattern, params):
    return dct.count([(src,dst) for param in params
                                for (src,dst) in
                      significants(clean(filepattern % tuple(param)), 1000)])
## pat = 'res-11-%s-%s-%s-%s.dat'
## params = [['1000', '1000', 'r', 'tiny'], ['1000', '1000', 'r', 'trigram'], ['1000', '1000', 'r_sq', 'tiny'], ['1000', '1000', 'r_sq', 'trigram'], ['1000', '500', 'r', 'tiny'], ['1000', '500', 'r', 'trigram'], ['1000', '500', 'r_sq', 'tiny'], ['1000', '500', 'r_sq', 'trigram']]
## d = count(pat, params)
# TODO: Fold this code in somehow
## >>> f = dct.filter_values(lambda v : v > 2, d)
## >>> f
## {('Middle_England', 'SE_England'): 5, ('London', 'Scotland'): 5, ('London', 'Wales'): 3, ('London', 'Northumbria'): 3, ('Heart_of_England', 'Wales'): 3, ('NW_England', 'SE_England'): 3, ('London', 'NW_England'): 4, ('London', 'Middle_England'): 4, ('NW_England', 'Scotland'): 3, ('London', 'SE_England'): 6, ('SE_England', 'Scotland'): 4}
## >>> from pprint import pprint
## >>> pprint(f)
## {('Heart_of_England', 'Wales'): 3,
##  ('London', 'Middle_England'): 4,
##  ('London', 'NW_England'): 4,
##  ('London', 'Northumbria'): 3,
##  ('London', 'SE_England'): 6,
##  ('London', 'Scotland'): 5,
##  ('London', 'Wales'): 3,
##  ('Middle_England', 'SE_England'): 5,
##  ('NW_England', 'SE_England'): 3,
##  ('NW_England', 'Scotland'): 3,
##  ('SE_England', 'Scotland'): 4}
## total = set(dct.filter_values(lambda v : v > 2, d).keys())
## sigs = map(set, [significants(clean(pat % tuple(param)), int(param[0])) for param in params])
## print [total & sig for sig in sigs]
# or maybe sig - total? 
