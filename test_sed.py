## from unittest import TestCase, TestSuite, TestLoader, TextTestRunner
import tester
from util.lst import *
from sed import *
def checktype(f):
    args,res = typ(f).split("->")
    return res.strip()==typ(f(*map(mak,args.strip().split("*"))))
### data ###
def testRegions(self):
    # 1. all of the values are in the range 315
    test(set(concat(regions.values())) - set(range(1,315)), set())
    # 2. the only skipped rows are Isle of Man and region 23
    # (which is now in Wales), plus row 1 which holds the word titles
    test(set(range(1,315)) ^ set(concat(regions.values())),
         set([1, 75, 76, 191, 192]))
    #TODO: Check that each region has the correct number of sites.
    # London has apparently only two regions here.
    # Also check correlation between similarity and number of sites.
    # This needs to be normalised for
    test(dct.map(len, regions),
         dict(zip(['em', 'ld', 'ee', 'wm', 'sw', 'yk', 'ne', 'se', 'nw'],
                  [  58,    2,   40,   31,   58,   34,   15,   41,   30])))
### read CSV ###
    # extract, curried, takewhile, dropwhile, split_by ought all to be
    # added to util. Since str is not [char] in Python, there need to be
    # two versions of takewhile and dropwhile. This is necessary in Scheme
    # for the same reason.
    # extract also needs two versions for most languages
def testLstExtract(self):
    test(lst_extract([], []), [])
    test(lst_extract(range(10), []), [])
    # this version allows multiple identical values
    test(lst_extract(range(10), [0,0,0]), [0,0,0])
    test(lst_extract(range(10), [0,1,2]), [0,1,2])
    # and out-of-order values
    test(lst_extract(range(10), [2,0,1]), [2,0,1])
    test(lst_extract(range(10), range(10)), range(10))
    test(lst_extract(range(10), reversed(range(10))),
         list(reversed(range(10))))
    # but this ability may be superfluous in a portable, efficient version
def testCurried(self):
    # trivial
    f = lambda: 12
    test(f(), 12)
    test(curried(f)(), 12)
    add1 = lambda n:n+1
    test(add1(2), 3)
    test(curried(add1)(3), 4)
    add = lambda n,m:n+m
    test(add(2,3), 5)
    test(curried(add)(2)(3), 5)
    curried(add)(2)
    self.assertRaises(TypeError, curried(add)(2), 3, 4)
    self.assertRaises(TypeError, curried(add), 2, 3)
def testTakewhile(self):
    test(takewhile(lambda _:True)("foo"), "foo")
    test(takewhile(lambda _:False)("foo"), "")
    test(takewhile(lambda c:c=='c')("foo"), "")
    test(takewhile(lambda c:c!='c')("foo"), "foo")
    test(takewhile(lambda c:c=='f')("foo"), "f")
    test(map(takewhile(lambda c:c!='-'), ["foo-bar", "barbaz", "---"]),
         ['foo', 'barbaz', ''])
def testDropwhile(self):
    test(dropwhile(lambda _:True)("foo"), "")
    test(dropwhile(lambda _:False)("foo"), "foo")
    test(dropwhile(lambda c:c=='c')("foo"), "foo")
    test(dropwhile(lambda c:c!='c')("foo"), "")
    test(dropwhile(lambda c:c=='f')("foo"), "oo")
    test(map(dropwhile(lambda c:c!='-'), ["foo-bar", "barbaz", "---"]),
         ['-bar', '', '---'])
def testMapc(self):
    test(mapc(lambda _:True)(range(3)), [True, True, True])
    test(mapc(lambda n:n+1)(range(3)), range(1,4))
    test(map(mapc(lambda n:n+1), [range(3), range(4,6), range(3,9)]),
         [range(1,4), range(5,7), range(4,10)])
### read CSV ###
# this is rickety ad-hoc code, so the purpose of these tests is NOT to stress
# the code; it's essentially throw-away, conformed to the shape of the data
# anyway. These tests are meant to make sure the output of group_regions
# is exactly the data structure I expect. This is tested using fake data.
fake = map(list, transpose(['hey aV1L redC1C redV1L carV1H carV1L'.split(),
                            map(str, range(1,7)),
                            map(str, range(11,17)),
                            map(str, range(111,117))]))
fake_regions = {'e':[2,3], 'f':[4]}
grouped_sed = group_sed_in_gor()
# answer = analyse(grouped_sed) # this makes the test run VERY slowly
# because the real analysis takes about a minute or so.
def testGroupWords(self):
    answer = group_words(fake)
    test(len(fake), 6)
    test(typ(fake), '[[str]]')
    test(typ(answer), "{str:{str:{str:[float]}}}")
    test(set(answer.keys()), set('a red car'.split()))
    test(set(answer['red'].keys()), set(["C1", "V1"]))
    test(answer["red"]["C1"].keys(), ["C"])
    test(answer["red"]["C1"]["C"], [3.0, 13.0, 113.0])
def testGroupRegions(self):
    answer = group_regions(fake_regions, group_words(fake))
    test(typ(fake_regions), "{str:[int]}")
    test(typ(answer), "{str:{str:{str:{str:[float]}}}}")
    test(set(answer.keys()), set('ef'))
    test(answer,
         {'e':{'a': {"V1":{"L":[2,12]}},
               'red': {"C1":{"C":[3,13]}, "V1":{"L":[4,14]}},
               'car': {"V1":{"H":[5,15], "L":[6,16]}}},
          'f':{'a': {"V1":{"L":[112]}},
               'red': {"C1":{"C":[113]}, "V1":{"L":[114]}},
               'car': {"V1":{"H":[115], "L":[116]}}}})
def testGroupSedInGor(self):
    # is't the right type?
    test(typ(grouped_sed), "{str:{str:{str:{str:[float]}}}}")
    # did it work
    test('ee' in grouped_sed, True)
    test('wmen' in grouped_sed['ee'], True)
    test('V1' in grouped_sed['ee']['wmen'], True)
    test(grouped_sed["ee"]["wmen"]["V1"].keys(), ["H"])
def testFlatten(self):
    flat = flatten(grouped_sed)
    fake = {'a':{'a':{'a':{'a':[1.0,2.0,3.0]},
                      'b':{'b':[0.0,12.0,1.1]},
                      'c':{'0':[0.0]}}}}
    test(typ(flat), "[[[{str:[float]}]]]")
    test(flat[0][51][0], grouped_sed["ee"]["wmen"]["V1"])
    test(flatten(fake), [[[{'a':[1.0,2.0,3.0]},
                           {'b':[0.0,12.0,1.1]},
                           {'0':[0.0]}]]])
def testFeatureSub(self):
    # no-op
    test(feature_sub({},{}), 0.0)
    test(feature_sub({'a':[1.0]},{}), 1.0)
    test(feature_sub({},{'a':[1.0]}), 1.0)
    test(feature_sub({'a':[]}, {'a':[1.0]}), 0.0)
    # unshared features
    test(feature_sub({'a':[1.0]},{'b':[1.0]}), 2.0)
    # shared features
    test(feature_sub({'a':[1.0]},{'a':[1.0]}), 0.0)
    test(feature_sub({'a':[1.0]},{'a':[0.0]}), 1.0)
    test(feature_sub({'a':[1.0]},{'a':[0.5]}), 0.5)
    # -cross
    test(feature_sub({'a':[1.0]},{'a':[0.5,1.0]}), 0.25)
    test(feature_sub({'a':[1.0]},{'a':[0.5,0.0]}), 0.75)
    test(feature_sub({'a':[1.0,0.5]},{'a':[0.5,0.0]}), 0.5)
    test(feature_sub({'a':[1.0,2.0]},{'a':[0.5,0.0]}), 1.25)
    # -avg
    test(feature_sub({'a':[1.0],'b':[0.0,1.0]},
                     {'a':[0.5,0.0],'b':[0.5]}), 1.25)
    # whole fish execution!
    test(feature_sub({'a':[1.0],'b':[0.0,1.0],'c':[0.0]},
                     {'a':[0.5,0.0],'b':[0.5],'d':[]}), 3.25)
    test(feature_sub({'a':[1.0],'b':[0.0,3.0],'c':[0.0]},
                     {'a':[0.5,0.0],'b':[5.0],'d':[]}), 6.25)
    # imbalanced number of informants
    test((feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                      {'a':[0.5],    'b':[0.5]    }) ==
          feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                      {'a':[0.5,0.0],'b':[0.5,1.0]}) ==
          feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                      {'a':[0.5,1.0,0.0],'b':[0.5,0.0,1.0]})),
         True)
    test(feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                     {'a':[0.5],    'b':[0.5]    }),
         1.0)
    test(feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                     {'a':[0.5,0.0],'b':[0.5,1.0]}),
         1.0)
    test(feature_sub({'a':[1.0,0.0],'b':[0.0,1.0]},
                     {'a':[0.5,1.0,0.0],'b':[0.5,0.0,1.0]}),
         1.0)
    # = 0 unshared features + avg(sum(|0.5-1.0| + |0.5-0.1| + .. + |
    #NOTE: I don't think this is quite right. The missing features have way too
    # much weight, so when C/V are compared (which happens often) they will
    # quickly outweigh the other data. What is a good weight?
    #total_feature_count = len(fs1+fs2)
    # then maybe ??
    #unshared_weight = (1/total_feature_count) * len(set(fs1) ^ set(fs2))
    # ne and ld are the smallest
def testSedAvg(self):
    test(checktype(sed_avg), True)
    test(sed_avg([{"a":[0.0,1.0],"b":[0.3,3.0]}], []), 0.0)
    test(sed_avg([], [{"a":[0.0,1.0],"b":[0.3,3.0]}]), 0.0)
    test(sed_avg([{"a":[0.0,1.0],"b":[0.3,3.0]}], [{'a':[0.0,1.0]}]), 1.5)
    # is the cross >>= avg really working?
    # that is, can we duplicate existing data with no change to the average?
    test(sed_avg([{"a":[0.0,1.0],"b":[0.3,3.0]}],
                 [{'a':[0.0,1.0]},{'a':[1.0,2.0]},
                  {'a':[0.0,1.0]},{'a':[1.0,2.0]}]),
         sed_avg([{"a":[0.0,1.0],"b":[0.3,3.0]}],
                 [{'a':[0.0,1.0]},{'a':[1.0,2.0]}]))
    # OK, so uhhh .. is that enough? I don't know.
def testSedAvgTotal(self):
    test(checktype(sed_avg_total), True)
    test(sed_avg_total(([[]], [{"a":[0.0,1.0],"b":[0.3,3.0]}])), 0.0)
    test(sed_avg_total(([[{"a":[0.0,1.0],"b":[0.3,3.0]}]],
                        [[{'a':[0.0,1.0]}]])),
         0.75)
    # average of multiple items remains the same
    test(sed_avg_total(([[{"a":[0.0,1.0],"b":[0.3,3.0]}],
                         [{"a":[0.0,1.0],"b":[0.3,3.0]}]],
                        [[{'a':[0.0,1.0]}],[{'a':[0.0,1.0]}]])),
         0.75)
    # the number of words in each region must be the same
    self.assertRaises(TypeError,
                      sed_avg_total,
                      ([[{"a":[0.0,1.0],"b":[0.3,3.0]}],
                         [{"a":[0.0,1.0],"b":[0.3,3.0]}]],
                        [[{'a':[0.0,1.0]}],[{'a':[0.0,1.0]}],[{'b':[3.0]}]]))
def testSedLevenshtein(self):
    # same number of characters but some different features
    test(sed_levenshtein(([{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                          [{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}]),
                         5.0),
         3.5)
    test(lev._levenshtein([{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                          [{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}],
                          5.0,
                          (lambda _:5.0,lambda _:5.0,feature_sub)),
         [[0.0,5.0,10.0],
          [5.0,1.5,6.5],
          [10.0,6.25,3.5]])
    # identical features but different values
    test(sed_levenshtein(([{'a':[0.0,1.0]}, {'b':[1.0,1.5]}],
                          [{'a':[1.0,1.0]}, {'b':[1.0,1.2]}]),
                         5.0),
         0.75)
    test(lev._levenshtein([{'a':[0.0,1.0]}, {'b':[1.0,1.5]}],
                          [{'a':[1.0,1.0]}, {'b':[1.0,1.2]}],
                          5.0,
                          (lambda _:5.0,lambda _:5.0,feature_sub)),
         [[0.0,5.0,10.0],
          [5.0,0.5,5.5],
          [10.0,5.5,0.75]])
def testSedDistance(self):
    # same as sed_levenshtein with only one region
    test(sed_distance(([[{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                        [{'a':[0.0,0.0]}, {'a':[0.0,0.5]}]],
                       [[{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}]]),
                      5.0),
         3.5)
    # zip ignores unmatched extras
    test(sed_distance(([[{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                        [{'a':[0.0,0.0]}, {'a':[0.0,0.5]}]],
                       [[{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}]]),
                      5.0),
         3.5)
    # sum of two identical things is twice the original
    test(sed_distance(([[{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                        [{'a':[0.0,1.0]}, {'a':[1.0,1.5]}]],
                       [[{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}],
                        [{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}]]),
                      5.0),
         7.0)
    # sum works otherwise (3.5 + 0.75 from sed_levenshtein)
    test(sed_distance(([[{'a':[0.0,1.0]}, {'a':[1.0,1.5]}],
                        [{'a':[0.0,1.0]}, {'b':[1.0,1.5]}]],
                       [[{'a':[1.0,1.0], 'b':[0.0,1.5]}, {'b':[1.0,1.2]}],
                        [{'a':[1.0,1.0]}, {'b':[1.0,1.2]}]]),
                      5.0),
         4.25)
def testAnalyse(self):
    # is it correct to use different averages for each pair?
    # it doesn't make any difference for the actual results so I guess
    # it doesn't matter.
    # averages = map(sed_avg_total, lst.all_pairs(flatten(grouped_sed))),
    # test(stdev(averages) < 1.0, True)
    pass
def testMak(self):
    test(mak('bool'), False)
    test(mak('int'), 0)
    test(mak('float'), 0.0)
    test(mak('str'), '')
    test(mak('[int]'), [0])
    test(mak('[bool]'), [False])
    test(mak('{str:int}'), {'':0})
    test(mak('(int,int,str)'), (0,0,''))
    self.assertRaises(ValueError, mak, '[int}')
    self.assertRaises(ValueError, mak, '{int}') # ironically, of course, this
    # is valid Python 3.0 syntax. (this is the real reason Guido wanted to
    # get rid of lambda)
    self.assertRaises(ValueError, mak, '[]')
    self.assertRaises(ValueError, mak, '{}')
    self.assertRaises(ValueError, mak, '{:}')
    self.assertRaises(ValueError, mak, '()')

tester.runTest(__import__(__name__), locals())
