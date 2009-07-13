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
    #typecheck((str,[object]), [Eq], [[Eq]])
    def makepaths(tree, path):
        (head, children) = tree
        path = path + [Eq(head)]
        if children:
            return mapn(lambda child: makepaths(child, path), children)
        else:
            return [path]
    return mapi('-'.join, bracketpaths(makepaths(tree, [])))
#typecheck([[Eq]], [[str]])
def bracketpaths(paths):
    "add brackets to disambiguate paths (and remove Eq wrapper)"
    spans = dct.count(concat(paths))
    hapax = set(node for (node,n) in spans.items() if n==1)
    #spans = set(node for (node,n) in dct.count(concat(paths)).items() if n>1)
    firsts = dict((node,findif(elem(node),paths)[-1]) for node in spans)
    lasts = dict((node,findif(elem(node),reversed(paths))[-1]) for node in spans)
    #typecheck([Eq], [str])
    def bracket(path):
        first = edge(path, firsts, hapax)
        last = edge(path, lasts, hapax)
        if first != -1:
            return mapi(Eq.get,path[:first+1])+["["]+mapi(Eq.get,path[first+1:])
        elif last != -1:
            return mapi(Eq.get,path[:last])+["]"]+mapi(Eq.get,path[last:])
        else:
            return mapi(Eq.get, path)
    def bracket2(path):
        (first1,first2) = edge2(path, firsts)
        (last1,last2) = edge2(path, lasts)
        if first1: # maybe first2
            return mapi(Eq.get, first1+first2[0]+["["]+first2[1:])
        elif last2: # maybe last1
            return mapi(Eq.get, last1+["["]+last2)
        else:
            return mapi(Eq.get, path)
    return mapi(bracket, paths)
#typecheck([Eq], {Eq:Eq}, set, int)
def edge(path, edges, hapax):
    "find the index of the highest node that receives a bracket, -1 if none"
    highest = -1
    for i,node in reversed(list(enumerate(path))):
        #if edges.get(node,Eq(None))==path[-1]:
        if edges[node]==path[-1] and node not in hapax:
            highest = i
    return highest
def edge2(path, edges):
    def edgemost(x):
        return edges.get(node,None)==path[-1]
    return span(edgemost, reversed(path))
def span(f, l):
    for i,x in enumerate(l):
        if not f(x):
            return (l[:i],l[i:])
    else:
        return (l, [])
