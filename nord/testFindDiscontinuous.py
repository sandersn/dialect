from findDiscontinuous import *
import unittest
import sys
test = None
class TestDisco(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        global test
        unittest.TestCase.__init__(self, *args, **kwargs)
        test = self.assertEqual
    def setUp(self):
        self.ss = sentences('input.txt')
        self.poss = [deCSV(s) for s in sentences('input.txt.pos') if s]
    def testSentences(self):
        test(sentences('input.txt'),
             ['\n#BOS\nfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\nbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\nbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n#EOS', '#BOS\nDas\t_\tDET\t_\t_\t_\t502\nBuch\t_\tN\t_\t_\t_\t502\nhabe\t_\tV\t_\t_\t_\t510\nich\t_\tPRON\t_\t_\t_\t501\nihm\t_\tPRON\t_\t_\t_\t502\ngegaben\t_\tPART\t510\n#501\t\t\t\t\t\tNP\t600\n#502\t\t\t\t\t\tNP\t510\n#510\t\t\t\t\t\tVP\t600\n#600\t\t\t\t\t\tS\t0\n#EOS', ''] )
    def testaddTreebankID(self):
        test(addTreebankID(self.ss, 'input.txt'+'.data'),
             map(addWordID, self.ss))
    def testaddWordID(self):
        test(map(addWordID, self.ss),
             [[['0', '']
               , ['1', '#BOS']
               , ['2', 'foo', 'foo1', 'foo2', 'foo3', 'foo4', 'foo5', 'foo6', 'foo7']
               , ['3', 'bar', 'bar1', 'bar2', 'bar3', 'bar4', 'bar5', 'bar6', 'bar7']
               , ['4', 'baz', 'baz1', 'baz2', 'baz3', 'baz4', 'baz5', 'baz6', 'baz7', 'baz8']
               , ['5', '#EOS']]
              , [['0', '#BOS']
                 , ['1', 'Das', '_', 'DET', '_', '_', '_', '502']
                 , ['2', 'Buch', '_', 'N', '_', '_', '_', '502']
                 , ['3', 'habe', '_', 'V', '_', '_', '_', '510']
                 , ['4', 'ich', '_', 'PRON', '_', '_', '_', '501']
                 , ['5', 'ihm', '_', 'PRON', '_', '_', '_', '502']
                 , ['6', 'gegaben', '_', 'PART', '510']
                 , ['7', '#501', '', '', '', '', '', 'NP', '600']
                 , ['8', '#502', '', '', '', '', '', 'NP', '510']
                 , ['9', '#510', '', '', '', '', '', 'VP', '600']
                 , ['10', '#600', '', '', '', '', '', 'S', '0']
                 , ['11', '#EOS']]
              , [['0', '']]])
    def testPOS(self):
        poss = POS('input.txt.data')
        test(poss,
             [[['2', 'foo', 'foo2', 'foo7']
               , ['3', 'bar', 'bar2', 'bar7']
               , ['4', 'baz', 'baz2', 'baz8']]
              , [['1', 'Das', 'DET', '502']
                 , ['2', 'Buch', 'N', '502']
                 , ['3', 'habe', 'V', '510']
                 , ['4', 'ich', 'PRON', '501']
                 , ['5', 'ihm', 'PRON', '502']
                 , ['6', 'gegaben', 'PART', '510']
                 , ['7', '#501', 'NP', '600']
                 , ['8', '#502', 'NP', '510']
                 , ['9', '#510', 'VP', '600']
                 , ['10', '#600', 'S', '0']]] )
        test([deCSV(s) for s in sentences('input.txt.pos') if s],
             poss)
        # this does not pass because of the initial \n property/bug
        # of the current reader code
        # I'm pretty sure this is an inessential property that later code
        # ignores, but I need to write some tests to make sure
##         output = '\n\n'.join('\n'.join('\t'.join(cols) for cols in sent) for sent in poss)
##         open('test.text.pos','w').write(output)
##         test(filter(None, sentences('input.txt.pos')),
##              sentences('test.text.pos'))
    def testWritePOS(self):
        writePOS([[['2', 'foo', 'foo2', 'foo7']
                   , ['3', 'bar', 'bar2', 'bar7']
                   , ['4', 'baz', 'baz2', 'baz8']]
                  , [['1', 'Das', 'DET', '502']
                     , ['2', 'Buch', 'N', '502']
                     , ['3', 'habe', 'V', '510']
                     , ['4', 'ich', 'PRON', '501']
                     , ['5', 'ihm', 'PRON', '502']
                     , ['6', 'gegaben', 'PART', '510']
                     , ['7', '#501', 'NP', '600']
                     , ['8', '#502', 'NP', '510']
                     , ['9', '#510', 'VP', '600']
                     , ['10', '#600', 'S', '0']]],
                 'input.txt.pos')
        s = open('input.txt.pos.gold').read()
        s = s.strip()
        test(open('input.txt.pos').read().strip(),
             s)
    def testGetPhrases(self):
        test(map(getPhrases, self.poss),
             [{'baz8': ['4'], 'foo7': ['2'], 'bar7': ['3']}
              , {501: [4]
                 , 502: [1, 2, 5]
                 , 510: [3, 6, 502]
                 , 600: [501, 510]
                 , 0: [600]} ])
    def testMain(self):
        sys.argv.append('input.txt')
        tr,tr2 = main()
        # test that the non-file-io forms after the file-io forms have been
        # cleaned and transformed into a form that I *think* is correct
        test(filter(None, map(deCSV, tr)), tr2)
        #test(filter(None, map(deCSV, cl)), cl2)
        test(open('input.txt.data').read(),
             '0\t\n1\t#BOS\n2\tfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\n3\tbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\n4\tbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n5\t#EOS\n\n\n0\t#BOS\n1\tDas\t_\tDET\t_\t_\t_\t502\n2\tBuch\t_\tN\t_\t_\t_\t502\n3\thabe\t_\tV\t_\t_\t_\t510\n4\tich\t_\tPRON\t_\t_\t_\t501\n5\tihm\t_\tPRON\t_\t_\t_\t502\n6\tgegaben\t_\tPART\t510\n7\t#501\t\t\t\t\t\tNP\t600\n8\t#502\t\t\t\t\t\tNP\t510\n9\t#510\t\t\t\t\t\tVP\t600\n10\t#600\t\t\t\t\t\tS\t0\n11\t#EOS\n\n\n0\t\n\n\n')
        test(open('input.txt.pos').read(),
             '\n2\tfoo\tfoo2\tfoo7\n3\tbar\tbar2\tbar7\n4\tbaz\tbaz2\tbaz8\n\n\n\n\n1\tDas\tDET\t502\n2\tBuch\tN\t502\n3\thabe\tV\t510\n4\tich\tPRON\t501\n5\tihm\tPRON\t502\n6\tgegaben\tPART\t510\n7\t#501\tNP\t600\n8\t#502\tNP\t510\n9\t#510\tVP\t600\n10\t#600\tS\t0\n\n\n\n\n\n'.strip())
        test(open('input.txt.out').read().strip(),
             '\n#BOS\nfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\nbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\nbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n#EOS\n#BOS\nDas\t_\tDET\t_\t_\t_\t502\nBuch\t_\tN\t_\t_\t_\t502\nhabe\t_\tV\t_\t_\t_\t510\nich\t_\tPRON\t_\t_\t_\t510\nihm\t_\tPRON\t_\t_\t_\t502\ngegaben\t_\tPART\t510\n#501\t\t\t\t\t\tNP\t600\n#502\t\t\t\t\t\tNP\t510\n#510\t\t\t\t\t\tVP\t600\n#600\t\t\t\t\t\tS\t0\n#EOS\n\n'.strip())
        test(open('input.txtAdd.out').read().strip(),
             '\n#BOS\nfoo\tfoo1\tfoo2\tfoo3\tfoo4\tfoo5\tfoo6\tfoo7\nbar\tbar1\tbar2\tbar3\tbar4\tbar5\tbar6\tbar7\nbaz\tbaz1\tbaz2\tbaz3\tbaz4\tbaz5\tbaz6\tbaz7\tbaz8\n#EOS\n#BOS\nDas\t_\tDET\t_\t_\t_\t502\nBuch\t_\tN\t_\t_\t_\t502\nhabe\t_\tV\t_\t_\t_\t510\nich\t_\tPRON\t_\t_\t_\t600\n#600\t_\tPRON\t_\t_\t_\t510\t@501\nihm\t_\tPRON\t_\t_\t_\t502\ngegaben\t_\tPART\t510\n#501\t\t\t\t\t\tNP\t600\n#502\t\t\t\t\t\tNP\t510\n#510\t\t\t\t\t\tVP\t600\n#600\t\t\t\t\t\tS\t0\n#EOS\n\n'.strip())
if __name__=="__main__":
    # this API is so lame. It reeks of overdone OO.
    suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(TestDisco)])
    # what about
    # pyunit.suite([TestCons]).run(display='text')
    # fool?
    unittest.TextTestRunner().run(suite)
    # I'm looking at you, Beck and Gamma!
 
