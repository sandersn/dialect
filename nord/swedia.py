from util.lst import splitby, each, concat
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
        # TODO : Filter line-ending ^U ('\x15')
        t = '\n'.join(filter(isne('\x15'),
                             concat(concat(map(read(path), files)))))
        open(region + '.t', 'w', encoding='utf-8').write(t)
# To get a list stop words, maybe try:
# set(readall(concat(regions.values())) - set(open('talbanken.tt'))
# this is not ideal of course, but it should definitely tell us if umlauts
# are represented differently
if __name__=="__main__":
    each(print, read('TestOM_1sp.cha'))
