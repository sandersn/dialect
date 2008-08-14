from util import dct
from util.lst import window, mapn, concat
from util.fnc import elem
from util.cl import findif
from typecheck import typecheck
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
def leaves((head,children)):
    if children:
        return mapn(leaves, children)
    else:
        return [head]
def trigrams(tree):
    return map('-'.join, window(leaves(tree) ,3))
# NOTE: type path = str, but is [str] internally
@typecheck((str, [object]), [str])
def paths(tree):
    paths = []
    @typecheck((str,[object]), [Eq], [[Eq]])
    def makepaths((head, children), path):
        path = path + [Eq(head)]
        if children:
            return mapn(lambda child: makepaths(child, path), children)
        else:
            return [path]
    return map('-'.join, bracketpaths(makepaths(tree, [])))
@typecheck([[Eq]], [[str]])
def bracketpaths(paths):
    "add brackets to disambiguate paths (and remove Eq wrapper)"
    spans = dct.count(concat(paths))
    hapax = set(node for (node,n) in spans.items() if n==1)
    firsts = dict((node,findif(elem(node),paths)[-1]) for node in spans)
    lasts = dict((node,findif(elem(node),reversed(paths))[-1]) for node in spans)
    @typecheck([Eq], [str])
    def bracket(path):
        first = edge(path, firsts, hapax)
        last = edge(path, lasts, hapax)
        if first != -1:
            return map(Eq.get,path[:first+1])+["["]+map(Eq.get,path[first+1:])
        elif last != -1:
            return map(Eq.get,path[:last])+["]"]+map(Eq.get,path[last:])
        else:
            return map(Eq.get, path)
    return map(bracket, paths)
@typecheck([Eq], {Eq:Eq}, set, int)
def edge(path, edges, hapax):
    "find the index of the highest node that receives a bracket, -1 if none"
    highest = -1
    for i,node in reversed(list(enumerate(path))):
        if edges[node]==path[-1] and node not in hapax:
            highest = i
    return highest
