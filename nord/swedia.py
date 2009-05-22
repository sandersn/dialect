from util.lst import splitby, each, concat, fst, snd
from util.txt import between
from util.fnc import negate, curry, isne
from util.cl import findif
from util import dct
from itertools import dropwhile, chain
import os

def newline(line):
    return line.startswith("*")
@curry
def read(path, filename):
    sents = splitby(newline,
                    dropwhile(negate(newline),
                              open(path + filename, encoding='utf-8')),
                    first=True)
    sents = (' '.join(sent) for sent in sents if not sent[0].startswith("*INT:"))
    return [between(sent, ":", "%").split() for sent in sents]
def groupCorpora(path, regions):
    visible = lambda path: path[0] != '.'
    corpora = dct.collapse(filter(visible, os.listdir(path)),
                           keymap=lambda f: findif(f.startswith, regions))
    if None in corpora:
        print ("Missing:", corpora[None])
        del corpora[None]
    return corpora
def extractTnt(path, regions):
    for region,files in groupCorpora(path, regions).items():
        t = '\n'.join(filter(isne('\x15'),
                             concat(concat(map(read(path), files)))))
        open(region + '.t', 'w', encoding='latin1').write(t)
def sharedtopwords(talbanken, regions):
    "NB talbanken.tt uses latin1, *.t also now uses latin1"
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
if __name__=="__main__":
    each(print, read('TestOM_1sp.cha'))
