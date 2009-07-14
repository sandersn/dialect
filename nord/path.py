from util import dct
from util.lst import window, mapn, concat
from util.fnc import elem
from util.cl import findif
def iterable(genfunc):
    def wrapper(*args, **kwargs):
        class _iterable(object):
            def __iter__(self):
                return genfunc(*args, **kwargs)
        return _iterable()
    return wrapper
def it(genthunk):
    return iterable(genthunk)()
@iterable
def mapi(f, *ls):
    for xs in zip(*ls):
        yield f(*xs)
## util ##
class Eq:
    """Interns things, making them test by eq?, not equal? (is, not ==)

    Useful in Python, where equal? testing is the default but sometimes you
    need eq? testing. Since it reduces == calls to a pointer compare it might
    also improve efficiency in some cases"""
    def __init__(self, x):
        self.x = x
    def get(self):
        return self.x
    def __str__(self):
        return "'%s" % (self.x,)
    def __repr__(self):
        return "Eq(%r)" % (self.x,)
## code ##
def leaves(tree):
    (head,children) = tree
    if children:
        return mapn(leaves, children)
    else:
        return [head]
def trigrams(tree):
    return mapi('-'.join, window(leaves(tree), 3))
# NOTE: type path = str, but is [str] internally
#typecheck((str, [object]), [str])
def paths(tree):
    return mapi('-'.join, bracketpaths(makepaths(tree, [])))
#typecheck((str,[object]), [Eq], [[Eq]])
def makepaths(tree, path):
    (head, children) = tree
    path = path + [Eq(head)]
    if children:
        return mapn(lambda child: makepaths(child, path), children)
    else:
        return [path]
#typecheck([[Eq]], [[str]])
def bracketpaths(paths):
    "add brackets to disambiguate paths (and remove Eq wrapper)"
    spans = set(node for (node,n) in dct.count(concat(paths)).items() if n>1)
    firsts = dict((node,findif(elem(node),paths)[-1]) for node in spans)
    lasts = dict((node,findif(elem(node),reversed(paths))[-1]) for node in spans)
    #typecheck([Eq], [str])
    def bracket(path):
        (first1,first2) = map(list, edge(path, firsts))
        (last1,last2) = map(list, edge(path, lasts))
        if first2:
            return mapi(Eq.get, first1+[first2[0], Eq("[")]+first2[1:])
        elif last2:
            return mapi(Eq.get, last1+[Eq("]")]+last2)
        else:
            return mapi(Eq.get, path)
    return mapi(bracket, paths)
#typecheck([Eq], {Eq:Eq}, set)
def edge(path, edges):
    def edgemost(node):
        return edges.get(node,None)==path[-1]
    return backspan(edgemost, path)
def backspan(f, l):
    lowest = len(l)
    for i,x in reversed(list(enumerate(l))):
        if f(x):
            lowest = i
    return (l[:lowest], l[lowest:])
