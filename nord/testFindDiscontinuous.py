from findDiscontinuous import *
import unittest
import sys
test = None
class TestDisco(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        global test
        unittest.TestCase.__init__(self, *args, **kwargs)
        test = self.assertEqual
    def testSentences(self):
        test(sentences('input.txt'),
             ['\n#BOS\nfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\nbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\nbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n#EOS', '#BOS\nfunk\tfunk1\tfunk2\tfunkshun\tfunk4\tfunk5\tfunk6\tfunk7\tfunk8\nadelic\tadelic1\tadelic2\tfunkadelic\tadelic4\tadelic5\tadelic6\tadelic7\tadelic8\n#EOS', ''])
    def testaddWordID(self):
        ss = sentences('input.txt')
        test(map(addWordID, ss),
             [[[0, ''], [1, '#BOS'], [2, 'foo', 'foo1', 'foo2', 'foo3', 'foo4', 'foo5', 'foo6', 'foo7'], [3, 'bar', 'bar1', 'bar2', 'bar3', 'bar4', 'bar5', 'bar6', 'bar7'], [4, 'baz', 'baz1', 'baz2', 'baz3', 'baz4', 'baz5', 'baz6', 'baz7', 'baz8'], [5, '#EOS']], [[0, '#BOS'], [1, 'funk', 'funk1', 'funk2', 'funkshun', 'funk4', 'funk5', 'funk6', 'funk7', 'funk8'], [2, 'adelic', 'adelic1', 'adelic2', 'funkadelic', 'adelic4', 'adelic5', 'adelic6', 'adelic7', 'adelic8'], [3, '#EOS']], [[0, '']]])
    def testMain(self):
        sys.argv.append('/Users/zackman/Documents/dialect/nord/input.txt')
        sents = main()
        test(open('input.txt.data').read(),
             '0\t\n1\t#BOS\n2\tfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\n3\tbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\n4\tbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n5\t#EOS\n\n\n0\t#BOS\n1\tfunk\tfunk1\tfunk2\tfunkshun\tfunk4\tfunk5\tfunk6\tfunk7\tfunk8\n2\tadelic\tadelic1\tadelic2\tfunkadelic\tadelic4\tadelic5\tadelic6\tadelic7\tadelic8\n3\t#EOS\n\n\n0\t\n\n\n')
        test(open('input.txt.pos').read(),
             '2\tfoo\tfoo2\tfoo7\n3\tbar\tbar2\tbar7\n4\tbaz\tbaz2\tbaz8\n\n\n1\tfunk\tfunk2\tfunk8\n2\tadelic\tadelic2\tadelic8\n\n\n\n\n')
        test(sents, map(addWordID, sentences('input.txt')))
if __name__=="__main__":
    # this API is so lame. It reeks of overdone OO.
    suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(TestDisco)])
    # what about
    # pyunit.suite([TestCons]).run(display='text')
    # fool?
    unittest.TextTestRunner().run(suite)
    # I'm looking at you, Beck and Gamma!
 
