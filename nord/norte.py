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
def icetasks(regions, feature, cpp, iterations=100):
    params = open('params.h','w')
    params.write('#define ITERATIONS %s\n' % (iterations,))
    params.write('#define SAMPLES 1000\n')
    params.write('#define R_MEASURE r')
    params.close()

    os.system('g++ -O2 -o ctrl.out params.h ' + cpp)
    suffix = '-' + feature + '.dat'
    cmd = "nice -n 6 ./ctrl.out".split()
    pairs = pairwise(regions)
    tasks = [cmd + [fro+suffix, to+suffix] for (fro,to) in pairs]
    files = ['%s-%s-tmp.txt' % (fro,to) for (fro, to) in pairs]
    return (tasks,files)
def combine(feature, type, iterations=100):
    "Combine the disparate output files into one"
    out = '%s-%s-1000-r-%s-interview.txt' % (type,iterations,feature,)
    pairs = pairwise(swediaSites)
    files = ['%s-%s-tmp.txt' % (fro,to) for (fro,to) in pairs]
    outf = open(out, 'w')
    for file in files:
        outf.write(open(file).read())
    outf.close()
def combineFeatures(clusters, feature):
    for name,cluster in clusters.items():
        outf = open('%s-%s.dat' % (name, feature), 'w')
        outf.write(out + '-' + '-'.join(group) + '\n')
        for inf in cluster:
            outf.writelines(list(open(inf))[1:])
        outf.close()
