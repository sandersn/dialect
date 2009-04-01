#!/bin/python2.5
# to run: nohup python2.5 build.py >build.out &
import os
import sys
import shutil
from util.lst import cross
import hielo
import extract
import cat
## util ##
def each(f, l):
    for x in l:
        f(x)
## code ##
def blade(args):
    """run cross comparisons"""
    (iterations, samples, r, suffix, division) = args
    outputname = 'res-11-%s-%s-%s-%s-%s.txt' % tuple(args)
    print 'Starting', outputname, '...'
    open('ice-%s.sh' % suffix,'w').write(hielo.gensh(outputname,
                                                     suffix,
                                                     division))
    try:
        os.remove(outputname)
    except OSError:
        pass # who cares if the output file didn't already exist?
    params = open('params.h','w')
    params.write('#define ITERATIONS %s\n' % iterations)
    params.write('#define SAMPLES %s\n' % samples)
    params.write('#define R_MEASURE %s\n' % r)
    params.close()
    os.system('g++ -o ctrl.out params.h icectrl.cpp')
    
    nohup = open('nohup.out','w')
    nohup.write('Running %s' % (suffix,))
    nohup.close()
    os.system('nice -n 6 nohup bash ice-%s.sh >>nohup.out' % suffix)

    graphname = 'graph-11-%s-%s-%s-%s-%s.txt' % tuple(args)
    f = open(graphname, 'w')
    for src,dsts in hielo.process(outputname, int(iterations)).items():
        f.write(src)
        for dst in dsts:
            f.write('  ' + dst) # This is a stupid way to do this ok
        f.write('\n')
    f.close()
def distance():
    outputname = 'dist-11-100-1000-r-path-gor.txt'
    print 'Starting', outputname, '...'
    open ('ice-distance.sh','w').write(hielo.gensh(outputname, 'path', 'gor'))
    try: # delete previous run (since ice-distance.sh appends to the file)
        os.remove(outputname)
    except OSError:
        pass # don't complain for the first run when there is no output file
    params = open('params.h','w')
    params.write('#define ITERATIONS 1000\n')
    params.write('#define SAMPLES 1000\n')
    params.write('#define R_MEASURE r')
    params.close()

    os.system('g++ -o ctrl.out params.h icectrl.cpp')
    os.system('nice -n 6 nohup bash ice-distance.sh >>nohup.out')
def divide():
    """Most of the work that this did has been taken over by generating
    sspeaker-*.csv and then running extract.generate"""
    cat.generate('ns')
    cat.generate('nsrandom')

target = "all"
# run the (possibly correct?) distance measure
if target=='distance':
    distance()
# if needed, regenerate compressed files
elif target=='regen':
    extract.generate('sspeaker-londonscotlandshuffle.csv')
    extract.generate('sspeaker-region.csv')
    # Note: filtering speakers by birthplace/education is still done ooband
    # by using sspeaker-*.csv
    # though see extract.shufflelondonscotland for an example
elif target=='all':
    params = cross(['1000'],
                   ['500','1000'],
                   ['r','r_sq'],
                   ['path','trigram'],
                   ['ns', 'nsrandom', 'gor'])
    each(blade, params)
    # hielo.count('res-11-%s-%s-%s-%s.txt', params)
