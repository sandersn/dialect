"Extract data from CSV of SED data, courtesy of Bob Shackleton."
"For great justice!"
from util.fnc import cur, compose#, pipe
from util.lst import fst,snd,car,cdr
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
def mapc(f,l):
    return map(f,l)
## read CSV ##
def group_words(csv):
    "[[str]]-> {str:{str:{str:[float]}}} ie {Word:{Segment:{Feature:[Value]}}}"
    segment_name = lambda s: s[:re.search('[0-9]', s).end()]
    segment = fnc.pipe(car, dropwhile(str.islower), segment_name)
    feature = lambda s: s[re.search('[0-9]', s).end():]

    words = dct.collapse(cdr(csv),
                         fnc.pipe(car, takewhile(str.islower)),
                         fnc.ident)
    features = lambda l:(feature(car(l)),map(float,cdr(l)))
    phones = lambda l: dct.map(dict, dct.collapse(l, segment, features))
    return dct.map(phones, words)
def group_regions(regions, words):
    """{str:[int]}*{str:{str:[(str,[float])]}} ->
         {str:{str:{str:[(str,[float])]}}}
    that is, {Region:{Word:{Segment:[Feature]}}}"""
    sub2 = lambda n: n-2
    dctmapper = curried(dct.map)
    def outermost(range):
        inner = dctmapper(dctmapper(lst_extract(map(sub2, range))))
        return dct.map(inner, words)
    return dct.map(outermost, regions)
def group_sed_in_gor():
    reader = list(csv.reader(open('sed.csv')))
    return group_regions(regions, group_words(lst.transpose(reader)))
def flatten(regions):
    '{str:{str:{str:{str:[float]}}}} -> [[[{str:[float]}]]]'
    def flatten1(d):
        return map(snd, sorted(d.items()))
    return map(mapc(flatten1), map(flatten1, flatten1(regions)))
### analysis ###
def analyse(regions, avgs=None):
    keys = lst.all_pairs(sorted(regions.keys()))
    regions = lst.all_pairs(flatten(regions))
    avgregions = lst.avg(map(sed_avg_total, regions))
    return dict(zip(keys, map(sed_distance(avgregions), regions)))
def feature_sub((cons1,fs1), (cons2,fs2)):
    "{str:[float]}*{str:[float]} -> float"
#             sum(map(uncurry(lst.cross) | map(sub | abs) | lst.avg,
#                     dct.zip(fs1,fs2.values())))
    return (len(set(fs1) ^ set(fs2))
            + sum(lst.avg(abs(inf1-inf2) for inf1,inf2 in lst.cross(f1,f2))
                  for f1,f2 in dct.zip(fs1,fs2).values()))
#TODO: This looks badly wrong. Why is there a cross in there? Shouldn't it be:
    if cons1 != cons2:
        return len(fs1) + len(fs2)
    else:
        return sum(abs(f1-f2) for f1,f2 in dct.zip(fs1, fs2).values())
def makesegment(d):
    features = dict(C=dict(GL=0.0, V=0.0, H=0.0,), #['C','PV','H','IR','HW','VO','L','W','V','GL','PL'],
                    # got rid of
                    V=dict(B=1.0, H=1.0, L=1.0, R=1.0), #Got rid of '' and "RH"
                    R=dict(MN=1.5, PL=1.0))
    type,keys = cl.findif(lambda (t,fs): any(k in fs for k in d), features.items())
    keys.update(d)
    return (type, keys)
cons = fst
@curried
def sed_distance(avg, (region1, region2)):
    return sum(map(sed_levenshtein(avg),zip(region1,region2)))
@curried
def sed_levenshtein(avg,(ws1,ws2)):
    return lev._levenshtein(ws1, ws2, avg,
                           (lambda _:avg,lambda _:avg,feature_sub))[-1][-1]
def sed_avg(ws1, ws2):
    "[{str:[float]}]*[{str:[float]}] -> float"
    return lst.avg(map(fnc.uncurry(feature_sub), lst.cross(ws1, ws2)))
def sed_avg_total((region1, region2)):
    "([[{str:[float]}]],[[{str:[float]}]]) -> float"
    return lst.avg(map(sed_avg, region1, region2)) / 2
### type reification ###
import types
def typ(x):
    def docstring_type(f):
        s = car(f.__doc__.splitlines())
        if '->' in s and '--' in s:
            return text.before(s, '--').strip()
        else:
            return s
    if isinstance(x, bool):
        return 'bool'
    elif isinstance(x, int):
        return 'int'
    elif isinstance(x, float):
        return 'float'
    elif isinstance(x, str):
        return 'str'
    elif isinstance(x, tuple):
        return '(' + ','.join(map(typ, x)) + ')'
    elif isinstance(x, list):
        if len(x) > 0:
            return '[' + typ(x[0]) + ']'
        else:
            return "[]"
    elif isinstance(x, dict):
        try:
            k = x.iterkeys().next()
            return "{" + typ(k) + ":" + typ(x[k]) + "}"
        except StopIteration:
            return "{}"
    elif isinstance(x, types.FunctionType):
        return docstring_type(x)
    else:
        return str(type(x))
## type instantiation
def mak(s):
    def check(type, expected, i):
        if s[i]!=expected:
            raise ValueError("""Bad %s syntax at character %i:
    Expected: %s; Found; %s""" % (type, i, expected, s[i]))
    def make(i):
        if s[i:i+4]=='bool': return i+4,bool()
        elif s[i:i+3]=='int': return i+3,int()
        elif s[i:i+5]=='float': return i+5,float()
        elif s[i:i+3]=='str': return i+3,str()
        elif s[i]=='[': # cof*monad*cof
            i,x = make(i+1)
            check("list", "]", i)
            return i+1,[x]
        elif s[i]=="{":
            i,k = make(i+1)
            check("dictionary", ":", i)
            i,v = make(i+1)
            check("dictionary", "}", i)
            return i+1,{k:v}
        elif s[i]=='(':
            xs = []
            i,x = make(i+1)
            xs.append(x)
            check("tuple", ",", i)
            while s[i]==',':
                i,x = make(i+1)
                xs.append(x)
            check("tuple", ")", i)
            return i+1,tuple(xs)
        else:
            raise ValueError("Bad syntax at character %i" % i)
        # turns out I need a Real Parser to allow use of functions.
        # oh well.
##             i,types = make(i) # this may have infinite recursion
##             # it's not right anyway since it doesn't allow multiple arguments
##             if s[i:i+2]=="->": i+=2
##             i,v = make(i)
##             def f(*args):
##                 for arg,type in zip(args,types):
##                     assert typ(arg)==type, "Type mismatch"
##                 return v
##             return f
    return make(0)[1]
### Maybe monad ###
#     ret might also be called mlist
#     ret :: a -> Maybe a
#     ret = Just
#     >>= should really be named seq ( or mplus )
#     >>= :: Maybe a -> (a -> Maybe b) -> Maybe b
#     >>= Nothing f = Nothing
#     >>= (Just a) f = f a
#     >> should really be named ignore ( or mcdr )
#     >> :: Maybe a -> Maybe b -> Maybe b
#     >> Nothing _ = Nothing
#     >> (Just a) m = m
### List monad ###
#     ret :: a -> [a]
#     ret = list
#     >>= :: [a] -> (a -> [b]) -> [b]
#     >>= [] f = [] -- this is unnecessary since this is the 
#     >>= l f = mapn f l
#     >> [] _ = []
#     >> _ l = l
