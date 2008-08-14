import tester
import iceread
import path
import extract
from util import dct
from util.lst import concat
from util.fnc import cur
tree = iceread.sentences('''[<sent> <#X9987:1:A>]
root
 A
  1
  2
  3
 B
  i
  ii
   x
   y
 C
  1
  2
   in
   out
[<sent> <#X9987:1:?>]
A
 1
  i
  ii
 2
  x
  y
[<sent> totally missing!??]
root
 A
  arf
  quad
  quam
  quim
 B
  neighbourhood'''.split('\n'))
acltree = iceread.sentences('''[<sent> <#1:1:A>]
A
 B
  p
  q
 B
  r
  s
[<sent> <#2:1:A>]
A
 B
  p
  q
  r
  s'''.split('\n'))
palmtree = iceread.sentences('''[<sent> <#1:1:A>]
S
 Ns
  the
  closest
  thing
  P
   to
   Ns
    a
    home
 Vsb
  was
 N
  a
  string
  hammock
  S+
   and
   +,
   Fa
    Rq
     when
    Ni
     it
    Vd
     rained
   +,
   Np
    some
    palm
    fronds
   Vd
    draped
   P
    over
    sticks'''.split('\n'))
def testPaths(self):
    acls = map(path.paths, acltree["A"])
    test(acls,
         [["A-[-B-p", "A-]-B-q", "A-B-[-r", "]-A-B-s"],
          ["A-[-B-p", "A-B-q", "A-B-r", "]-A-B-s"]])
    ps = map(path.paths, palmtree["A"])
    test(ps, [['S-[-Ns-the',
               'S-Ns-closest',
               'S-Ns-thing',
               'S-Ns-P-[-to',
               'S-Ns-P-Ns-[-a',
               'S-]-Ns-P-Ns-home',
               'S-Vsb-was',
               'S-N-[-a',
               'S-N-string',
               'S-N-hammock',
               'S-N-S+-[-and',
               'S-N-S+-+,',
               'S-N-S+-Fa-[-Rq-when',
               'S-N-S+-Fa-Ni-it',
               'S-N-S+-]-Fa-Vd-rained',
               'S-N-S+-+,',
               'S-N-S+-Np-[-some',
               'S-N-S+-Np-palm',
               'S-N-S+-]-Np-fronds',
               'S-N-S+-Vd-draped',
               'S-N-S+-P-[-over',
               ']-S-N-S+-P-sticks']])
    test({'hi-[-child-grandchild0':1,
          ']-hi-child3': 1,
          'hi-child2':1,
          'hi-]-child-grandchild1':1},
         dct.count(path.paths(iceread.sentences('''[<sent> <#1:1:A>]
hi
 child
  grandchild0
  grandchild1
 child2
 child3'''.split('\n'))['A'][0])))
def testRead(self):
    test(["A"], palmtree.keys())
    test(set(["A", "?", '']), set(tree.keys()))
    test({'': [('root',
                [('A', [('arf', []), ('quad', []), ('quam', []), ('quim', [])]),
                 ('B', [('neighbourhood', [])])])],
          '?': [('A', [('1', [('i', []), ('ii', [])]),
                       ('2', [('x', []), ('y', [])])])],
          'A': [('root',
                 [('A', [('1', []), ('2', []), ('3', [])]),
                  ('B', [('i', []), ('ii', [('x', []), ('y', [])])]),
                  ('C', [('1', []), ('2', [('in', []), ('out', [])])])])]},
         tree)
def testFiltered(self):
    test(194, len(list(open('sspeaker-filter.csv'))))
def testBirthplace(self):
    ss = iceread.groupby('sspeaker-filter.csv', 12)
    test(set(["Wales", "Scotland", "Southeast","West Midlands",
              "Northeast","Southwest", "East Midlands", "East", "London",
              "Yorkshire", "Northwest", "India", "China", "Spain"]), set(ss))
    #test({}, ss)
def testTinify(self):
    regions = {'The Moon!':map(path.paths, concat(acltree.values())),
               "Bikini Gulch":map(path.paths, concat(tree.values()))}
    test([2,3], map(len, regions.values()))
    test([['root-[-A-1',
           'root-A-2',
           'root-]-A-3',
           'root-B-[-i',
           'root-B-ii-[-x',
           'root-]-B-ii-y',
           'root-C-[-1',
           'root-C-2-[-in',
           ']-root-C-2-out'],
          ['root-[-A-arf',
           'root-A-quad',
           'root-A-quam',
           'root-]-A-quim',
           ']-root-B-neighbourhood'],
          ['A-[-1-i',
           'A-]-1-ii',
           'A-2-[-x',
           ']-A-2-y']],
         regions["Bikini Gulch"])
    neoregions = extract.tinify(regions)
    test(2, len(neoregions))
    test({'The Moon!': [['7', '5', "'", '6'], ['7', '0', '.', '6']],
          'Bikini Gulch': [['"', ',', '+', '!', '*', '4', '-', '3', ')'],
                           ['1', '%', '(', '&', '$'],
                           ['/', ' ', '#', '2']]},
         neoregions)
def DONOTtestCorpus(self):
    # this only works on jones since it actually slurps in the corpus files
    pass
tester.runTest(__import__(__name__), locals())
