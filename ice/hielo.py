from __future__ import division
from util.lst import group, cross, concat
from util import dct
from util.text import chomp
from typecheck import typecheck
regions = {'gor':('East', 'WestMidlands', 'EastMidlands', "London",
               "Southeast", "Southwest", "Northeast", "Northwest",
               "Scotland", "Wales", "Yorkshire"),
           'ns': ('London', 'Scotland'),
           'nsrandom':('Ldonon', 'Stolcnad')}
def pairwise(l):
    return [(x,y) for i,x in enumerate(l) for y in l[i+1:]]
def gensh(outname, suffix, division):
    sh = '#!/bin/bash\n'
    suffix = '-' + suffix + '.dat'
    return sh + '\n\n'.join('''echo Starting %(n1)s %(n2)s ...
nice -n 6 ./ctrl.out %(n1)s%(suf)s %(n2)s%(suf)s >>%(out)s'''
                              % dict(n1=name1,n2=name2,suf=suffix,out=outname)
                            for name1,name2 in pairwise(regions[division]))
def norm(s):
    if s.endswith("_tiny\n"):
        return chomp(s)[:-5]
    else:
        return chomp(s)
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
