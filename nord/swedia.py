from util.lst import splitby, each, concat, fst, snd
from util.txt import between
from util.fnc import negate, cur, curry, isne, pipe
from util.cl import findif
from util import dct
from itertools import dropwhile, chain
import os
# Types are invading this code. It's stupid but I can't help it.
# I don't want to port this code to Haskell so it's going into the comments.
# type sites = [str]
# type regions = {str:[str]}

def newline(line):
    return line.startswith("*")
def visible(path):
    return path[0] != '.'
@curry
def read(path, filename):
    sents = splitby(newline,
                    dropwhile(negate(newline),
                              open(path + filename, encoding='utf-8')),
                    first=True)
    sents = (' '.join(sent) for sent in sents if not sent[0].startswith("*INT:"))
    return [between(sent, ":", "%").split() for sent in sents]
def groupedSites(path, sites):
    "path*[site] -> {site:[path]}"
    corpora = dct.collapse(filter(visible, os.listdir(path)),
                           keymap=lambda f: findif(f.startswith, sites))
    if None in corpora:
        print ("Missing:", corpora[None])
        del corpora[None]
    return corpora
def groupedRegions(path, regions):
    "path*{region:[site]} -> {region:[path]}"
    return dct.map(pipe(cur(groupedSites)(path), dict.values, concat),
                   regions)
def extractTnt(path, sites):
    for region,files in groupedSites(path, sites).items():
        t = '\n'.join(filter(isne('\x15'),
                             concat(concat(map(read(path), files)))))
        open(region + '.t', 'w', encoding='utf-8').write(t)
## exploratory ##
def sharedtopwords(talbanken, regions):
    talwords = [fst(line.split()) for line in s.splitlines() if line[0] != ' ']
    talvocab = set(talwords)
    talcount = dct.count(talwords)
    swewords = [w for r in regions for w in r.splitlines()]
    swevocab = set(swewords)
    swecount = dct.count(swewords)
    unsharedTokensTal = sum(talcount[w] for w in sharedVocab)
    unsharedTokensSwe = sum(swecount[w] for w in sharedVocab)
    print(len(talvocab))
    print(len(swevocab))
    print(len(swevocab & talvocab))
    print(len(swevocab - talvocab))
    print(len(talvocab - swevocab)
          + len(swevocab - talvocab)
          + len(swevocab & talvocab))
    print(unsharedTokensTal)
    print(unsharedTokensSwe)
    print(len(talwords) + len(swewords) - unsharedTokensTal - unsharedTokensSwe)
lap = pipe(map, list) # Python 3 sucks
# (iterators as imperative laziness are at fault here)
def corpusSize(path, regions, grouper):
    numbers = dct.map(lambda files:lap(pipe(read(path), len), files),
                      grouper(path, regions))
    ssums = sorted(dct.map(sum, numbers).items(), key=snd)
    for region, total in ssums:
        print(region, ":\t", total, '\t', numbers[region])
if __name__=="__main__":
    each(print, read('TestOM_1sp.cha'))
