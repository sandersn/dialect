"""Produce and read/write tiny format text files. Call extract.generate.
Only works on jones. This code is specific to my syntax distance project.
iceread.read sort of is, but actually {str:[tree]} is generally useful since
you can choose which column is the key"""
from __future__ import division
from typecheck import typecheck
from util.lst import fst,snd,concat,mapn
from util.fnc import cur
from util import dct
import path
import iceread
@typecheck(str, (str,[[str]]))
def read(fname):
    acc = []
    region = []
    f = open(fname)
    name = chomp(f.next())
    for line in imap(chomp,f):
        if line=="***":
            region.append(acc)
            acc = []
        else:
            acc.append(line)
    region.append(acc)
    f.close()
    return name,region
@typecheck(str, [[str]], str, None)
def write(name, region, fname):
    open(fname,'w').write(name + "\n" +
                          "\n***\n".join("\n".join(sent) for sent in region))
def chars():
    i = 0
    while True:
        s = ''
        j = i
        while j+32 > 255:
            s += chr(j % 223 + 32)
            j //= 223
        yield s + chr(j % 223 + 32)
        i += 1
def encode(l):
    return dict(zip(l, chars()))
@typecheck({str:[[(str, [object])]]}, {str:[[(str, [object])]]})
def tinify(regions):
    items = sorted(dct.count(mapn(concat, regions.values())).items(), key=snd)
    code = encode(map(fst, items))
    return dct.map(cur(map, cur(map, code.__getitem__)), regions)
def readcorpus(extractor, speakers):
    return dct.map(cur(map, extractor), iceread.read(speakers, 12))
def generate(speakers):
    for region, data in tinify(readcorpus(path.trigrams,speakers)).items():
        write(region, data, region+'-trigram.dat')
    for region, data in tinify(readcorpus(path.paths,speakers)).items():
        write(region, data, region+'-path.dat')
import csv
import random
def shufflelondonscotland():
    speakers = list(csv.reader(open('sspeaker-londonscotland.csv')))
    londoners = len([s for s in speakers if s[12]=='London'])
    random.shuffle(speakers)
    for i,s in enumerate(speakers):
        s[12] = 'Ldonon' if i < londoners else 'Stolcnad'
    csv.writer(open('sspeaker-londonscotlandshuffle.csv', 'w')).writerows(speakers)
