"""Produce and read/write tiny format text files. Call extract.generate.
Only works on jones. This code is specific to my syntax distance project.
iceread.read sort of is, but actually {str:[tree]} is generally useful since
you can choose which column is the key"""
from __future__ import division
#from typed import check
from util.lst import fst,snd,concat,mapn
from util.fnc import cur
from util import dct
from path import mapi, trigrams, paths
#check(str, [[str]], str, None)
def write(name, region, fname):
    open(fname,'w').write(name + "\n" +
                          "\n***\n".join("\n".join(sent) for sent in region))
#check([(str, [object])], None)
def generate(sentences):
    write(region, mapi(trigrams, sentences), region+'-trigram.dat')
    write(region, mapi(paths, sentences), region+'-path.dat')
def gen2iterable(genfunc):
    def wrapper(*args, **kwargs):
        class _iterable(object):
            def __iter__(self):
                return genfunc(*args, **kwargs)
        return _iterable()
    return wrapper
