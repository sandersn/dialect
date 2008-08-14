"""To use:
iceread.read('sspeakers.csv', 12)
Note: contains a hard-coded corpus path. read and corpus will only work on jones
Note: Convert sspeakers to comma delimited. The default is tab-delimited.
"""
from util import dct
from util.fnc import car, cdr, cur, pipe, iseq, elem
from util.lst import takewhile, mapn
from util.reflect import traced
from typecheck import typecheck
import re
import csv
## util ##
def splitby(f, l, first=False):
    """a->bool*[a]*bool->[[a]]--Why isn't this in the util.lst library?

    Because itertools.groupby provides an iterator version of it. I thought
    that it sufficed at the time, but as an iterator it is too destructive."""
    outer = []
    it = iter(l)
    if first:
        acc = [it.next()]
    else:
        acc = []
    for x in it:
        if not f(x):
            acc.append(x)
        else:
            outer.append(acc)
            acc = [x]
    outer.append(acc)
    return outer
def carcdr(l):
    return l[0],l[1:]
## code ##
def clean(line):
    return takewhile(lambda c:c!='(' and c!='{', line.strip())
def indent(line):
    return len(takewhile(iseq(' '), line))
def useful(line):
    return 'ignore' not in line and line[0] != "["
def speaker_code(line): # warning! I think this is borken
    match = re.search("<#X?[0-9]{1,4}:[0-9]:([A-Z?])>", line)
    return match.group(1) if match else ''
@typecheck(object, {str:[(str, [object])]})
def sentences(lines):
    @typecheck([str], [(str, [object])], n=int)
    def parseloop(lines, n=0):
        return [(clean(lines[0]),
                 parseloop(lines[1:], n=n+1) if lines[1:] else [])
                for lines in splitby(lambda line:n==indent(line), lines, True)]
    return dct.collapse(splitby(elem('<sent>'), lines, first=True),
                        pipe(car, speaker_code),
                        pipe(cdr, cur(filter, useful), parseloop, car))
@typecheck(str, int, {str:[(str,str)]})
def groupby(speakerfile, index):
    "12 is birthplace, 14 is education level; 1 is filename, 3 is speaker code"
    return dct.collapse_pairs([(x[index],(x[1],x[3])) for x in
                               csv.reader(open(speakerfile))][1:])
    ## note:should filter by amount of data not number of speakers
@typecheck({str:[(str,str)]}, {str:[(str, [object])]})
def corpus(speakers):
    "Warning! This contains a hard-coded path specific to jones"
    @typecheck((str,str), [(str, [object])])
    def per_speaker((fname,speaker)):
         return sentences(open('/Volumes/Data/Corpora/en/ice-gb/ice-gb-2/data/'+
                               fname.lower()+'.cor'))[speaker]
    return dct.map(lambda files: mapn(per_speaker, files), speakers)
def read(speakerfile, index):
    return corpus(groupby(speakerfile, index))

