from __future__ import division
from util.lst import group, cross, concat
from util import dct
from util.txt import chomp
import consts
from consts import swediaSites
import os
import csv
from codecs import open
### util ###
def pairwise(l):
    return [(x,y) for i,x in enumerate(l) for y in l[i+1:]]
def tail(it): # iterators suck
    return list(it)[1:]
### runner ###
def icetasks(regions, feature, cpp, measure, sample, norm, iterations=100):
    writeparams(iterations, sample, measure, norm)

    os.system('g++ -O2 -o ctrl.out params.h ' + cpp)
    suffix = '-' + feature + '.dat'
    cmd = "nice -n 6 ./ctrl.out".split()
    pairs = pairwise(regions)
    tasks = [cmd + [fro+suffix, to+suffix] for (fro,to) in pairs]
    files = ['%s-%s-tmp.txt' % (fro,to) for (fro, to) in pairs]
    return (tasks,files)
def writeparams(iterations=100, sample=1000, measure='r', norm='ratio'):
    params = open('params.h','w')
    params.write('#define ITERATIONS %s\n' % (iterations,))
    if sample=='full':
        params.write('#define FULLCORPUS\n')
        params.write('#define SAMPLES 0\n')
    else:
        params.write('#define SAMPLES %s\n' % (sample,))
    if norm=='ratio':
        print('#define ratio normalisation')
        params.write('#define RATIO_NORM\n')
    elif norm=='over':
        print('#define overuse normalisation')
        params.write('#define OVERUSE_NORM\n')
    else:
        print('#define only frequency normalisation')
    params.write('#define R_MEASURE %s\n' % (measure,))
    params.close()
def combine(feature, type, measure, sample, norm, iterations=100):
    "Combine the disparate output files into one"
    out = ('%s-%s-%s-%s-%s-%s.txt' %
           (type,iterations,sample,measure,feature,norm,))
    pairs = pairwise(swediaSites)
    files = ['%s-%s-tmp.txt' % (fro,to) for (fro,to) in pairs]
    outf = open(out, 'w')
    for file in files:
        outf.write(open(file).read())
    outf.close()
def combineFeatures(clusters, feature):
    suffix = '-' + feature + '.dat'
    for name,cluster in clusters.items():
        outf = open('%s-%s.dat' % (name, feature), 'w', encoding='utf-8')
        outf.write(name + '-' + '-'.join(cluster) + '\n')
        for inf in cluster:
            outf.writelines(list(open(inf + suffix, encoding='utf-8'))[1:])
        outf.close()
def findSigs(num, sample, norm):
    f = csv.reader(open("sig-%s-%s-%s.csv" % (num,sample,norm), encoding='ascii'),
                   delimiter=',')
    sigs = zip(consts.features,
               [[m for (m,n) in zip(consts.measures, tail(line)) if n=="0"]
                for line in tail(f)])
    return set((f,m) for f,row in sigs for m in row)
