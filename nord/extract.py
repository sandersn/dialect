"""Produce and write star-separated feature files. Call extract.generate.
This code is specific to my syntax distance project. """
from __future__ import division
from util.lst import fst,snd,concat,mapn
from util.fnc import cur
from util import dct
from path import mapi, trigrams, paths
def write(name, region, fname):
    open(fname,'w', encoding='utf-8').write(name + "\n" +
                          "\n***\n".join("\n".join(sent) for sent in region))
# str * [tree] -> None
def generate(region, sentences):
    sentences = [s for s in sentences if s]
    write(region, mapi(trigrams, sentences), region+'-trigram.dat')
    write(region, mapi(paths, sentences), region+'-path.dat')
