"Extract data from CSV of SED data, courtesy of Bob Shackleton."
"For great justice!"
from util.fnc import cur, compose#, pipe
from util.lst import fst,snd,car,cdr,concat
from util.reflect import traced,postmortem
from util import fnc, lst, dct, text
import inspect
import csv
import re
import lev
## data ##
regions = dict(ne=(1,3), # plus site 3 of 6 (Yorkshire)
               nw=(2,4,5,7),
               yk=(6,), # plus sites 1,2,3 of 10 (Lincolnshire)
               wm=(11,12,15,16,17,),
               em=(8,9,10,13,14,18,),
               ee=(19,20,21,22,27,28,29,),
               se=(25,26,33,34,35,39,40,),
               sw=(24,31,32,36,37,38,),
               ld=(30,)) # plus 23 is now part of Wales.
# NOTE:The changed regions are not included
regions = dict(ne=range(2,11)+range(17,23),
               nw=range(11,17)+range(23,41)+range(77,83),
               yk=range(41,75), #+range(75,77) (Isle of Man isn't on GOR map)
               wm=range(112,126)+range(140,157),
               em=range(83,112)+range(126,140)+range(157,172),
               ee=range(172,191)+range(217,238),
               se=range(206,217)+range(262,279)+range(302,315),
               sw=range(193,206)+range(240,262)+range(279,302),
               ld=range(238,240))
## util ##
def curried(f):
    def curhelp(n, args):
        if n==0:
            return f(*args)
        else:
            return lambda arg: curhelp(n-1, args+[arg])
    arity = len(inspect.getargspec(f)[0])
    if arity==0: # a no-op because the function shouldn't be curried at all
        return f
    else:
        return curhelp(arity, [])
def carcdr(f):
    return lambda l, *args, **kwargs: f(l[0], l[1:], *args, **kwargs)
@curried
def lst_extract(n, l):
    return [l[i] for i in n]
@curried
def takewhile(f, s):
    for i,c in enumerate(s):
        if not f(c):
            return s[:i]
    else:
        return s
@curried
def dropwhile(f, s):
    for i,c in enumerate(s):
        if not f(c):
            return s[i:]
    else:
        return ''
@curried
def cmap(f,l):
    return map(f,l)
chop = lambda s: s[:-1]
## read CSV ##
def group_words(csv):
    "[[str]]-> {str:{str:(str,{str:[float]})}} ie {Word:{Segment:{Feature:[Value]}}}"
    segment_name = lambda s: s[:re.search('[0-9]', s).end()]
    segment = fnc.pipe(car, dropwhile(str.islower), segment_name)
    feature = lambda s: s[re.search('[0-9]', s).end():]
    fillsegments = curried(dct.map_items)(makesegment)
    features = carcdr(lambda title, data:(feature(title), map(float, data)))
    phones = lambda l: dct.map(dict, dct.collapse(l, segment, features))

    words = dct.collapse(cdr(csv),
                         fnc.pipe(car, takewhile(str.islower)),
                         fnc.ident)
    return dct.map(fnc.pipe(phones, fillsegments), words)
def group_regions(regions, words):
    """{str:[int]}*{str:{str:(str,{str:[float]})}} ->
         {str:{str:{str:(str,{str:[float]})}}}
    that is, {Region:{Word:{Segment:(Type,{Feature:[Value]})}}}"""
    sub2 = lambda n: n-2
    dctmapper = curried(dct.map)
    def outermost(range):
        inner = dctmapper(dctmapper(lst_extract(map(sub2, range))))
        return dct.map(inner, words)
    return dct.map(outermost, regions)
def group_sed_in_gor():
    reader = list(csv.reader(open('sed.csv')))
    return group_regions(regions, group_words(lst.transpose(reader)))
#@check(str,{str:[float]},(str,{str:[float]}))
def makesegment(type,d):
    # C's numbers:
    # GL=PV: {0,.5,1}, H/HW/W: {0,1}, V=C=PL=IR=VO={0,1}, L={0,1,2}
    # I think H/HW/W should be collapsed at read time. L(6), PV(5) and C(4) not
    # also not IR,VO,PL(2) but I wish we had more of them.
    size = len(d.itervalues().next())
    features = dict(C=dict(GL=0.0, V=0.0, H=0.0, PV=0.0, L=0.0),#H=HW=W total(6)
                    V=dict(B=1.0, H=1.0, L=1.0, R=1.0), #Got rid of '' and "RH"
                    R=dict(MN=1.5, PL=1.0),
                    # mult's range is 0.0 - 2.0 but its meaning varies?
                    MULT=dict(MULT=1.0),
                    VC=dict()) # VC is erroneous data eh.
    #TODO:Collapse H/HW/W
    #TODO:Decide if V's L and C's L are different and if so make them different
    keys = dct.map(lambda default:[default]*size, features[chop(type)])
    keys.update(d)
    return keys
def flatten(regions):
    '{str:{str:{str:{str:[float]}}}} -> [[[{str:[float]}]]]'
    def flatten1(d):
        return map(snd, sorted(d.items()))
    return map(cmap(flatten1), map(flatten1, flatten1(regions)))
### analysis ###
def analyse(regions, avgs=None):
    keys = lst.all_pairs(sorted(regions.keys()))
    regions = lst.all_pairs(flatten(regions))
    avgregions = lst.avg(map(sed_avg_total, regions))
    return dict(zip(keys, map(sed_distance(avgregions), regions)))
def feature_sub(seg1, seg2):
    "({str:float}*{str:float}) -> float"
    return (len(set(seg1) ^ set(seg2))
            + sum(abs(f1-f2) for f1,f2 in dct.zip(seg1,seg2).values()))
@curried
def sed_distance(avg, (region1, region2)):
    "float*([[{str:[float]}]],[[{str:[float]}]])->float"
    return sum(map(sed_levenshtein(avg), zip(region1, region2)))
def transpose_word(word):
    "[{str:[float]}] -> [[{str:float}]]"
    def transpose_segment(seg):
        return [dict(zip(seg.keys(), ns)) for ns in lst.transpose(seg.values())]
    return lst.transpose(map(transpose_segment, word))
@curried
def sed_levenshtein(avg,(ws1,ws2)):
    "float*([{str:[float]}],[{str:[float]}])->float"
    def levenshtein((w1, w2)):
        return lev._levenshtein(w1, w2, avg,
                                (lambda _:avg,lambda _:avg,feature_sub))[-1][-1]
    return lst.avg(map(levenshtein,
                       lst.cross(transpose_word(ws1), transpose_word(ws2))))
def sed_avg(ws1, ws2):
    "[{str:[float]}]*[{str:[float]}] -> float"
    segs1,segs2 = (concat(transpose_word(ws1)), concat(transpose_word(ws1)))
    return lst.avg(map(fnc.uncurry(feature_sub), lst.cross(segs1, segs2)))
def sed_avg_total((region1, region2)):
    "([[{str:[float]}]],[[{str:[float]}]]) -> float"
    return lst.avg(map(sed_avg, region1, region2)) / 2
