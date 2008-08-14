import csv
from util.lst import group, transpose
from util import dct
short = {'East\n':'ee',
         'EastMidlands\n':'em',
         'London\n':'ld',
         'Northeast\n':'ne',
         'Northwest\n':'nw',
         'Southeast\n':'se',
         'Southwest\n':'sw',
         'WestMidlands\n':'wm',
         'Yorkshire\n':'yk'}
def sed2r():
    lists = csv.reader(open('sed_distances.txt'), delimiter='\t')
    titles = lists.next()[1:]
    d = {}
    for i,row in enumerate(lists):
        for j,n in enumerate(row[1:]):
            if n and float(n):
                d[titles[i],titles[j]] = float(n)
    return d
def ice2r():
    return dict(((short[r1],short[r2]),float(value))
                for r1,r2,value in group(list(open('dist-11-100-1000-r-path-gor.txt')), 3)
                if not any(r in ['Scotland\n', 'Wales\n'] for r in [r1,r2]))
def stringify(zipped):
    print zipped
    return '\n'.join('c(%s)' % ','.join(map(str,ns))
                     for ns in transpose(zipped.values()))
def combine(sed, ice):
    setify = lambda d: dct.map_keys(frozenset, d)
    d = dct.zip(setify(sed), setify(ice))
    del d[frozenset(['ld', 'se'])]
    del d[frozenset(['sw', 'se'])]
    del d[frozenset(['nw', 'se'])]
    del d[frozenset(['ld', 'nw'])]
    del d[frozenset(['ld', 'em'])]
    del d[frozenset(['yk', 'em'])]
    return d
print stringify(combine(sed2r(), ice2r()))
