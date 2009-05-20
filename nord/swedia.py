from util.lst import splitby, each
from util.txt import between
from util.fnc import negate
from util.cl import findif
from itertools import dropwhile
import os
def fromkeys(l, cons):
    d = {}
    for x in l:
        d[x] = cons()
    return d
## code ##
def newline(line):
    return line.startswith("*")
def read(filename):
    sents = splitby(newline,
                    dropwhile(negate(newline), open(filename, encoding='utf-8')),
                    first=True)
    sents = (' '.join(sent) for sent in sents if not sent[0].startswith("*INT:"))
    return [between(sent, ":", "%").split() for sent in sents]
def extractTnt(path, regions):
    corpora = fromkeys(regions, list)
    for corpus in os.listdir(path):
        r = findif(corpus.startswith, regions)
        if r:
            corpora[r].append(corpus)
        elif corpus.startswith('.'):
            pass
        else:
            print('corpus', corpus, 'not found')
    for region,files in corpora.items():
        t = '\n'.join(chain(chain(*map(read, files))))
        open(region + '.t', 'w', encoding='utf-8').write(t)
# To get a list stop words, maybe try:
# set(readall(chain(regions.values())) - set(open('talbanken.tt'))
# this is not ideal of course, but it should definitely tell us if umlauts
# are represented differently
if __name__=="__main__":
    each(print, read('TestOM_1sp.cha'))
