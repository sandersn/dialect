#!/usr/bin/env python
#############################################################
###                                                       ###
### Written by: Yu-Yin Hsu                                ###
### December 2008                                         ###
### (L555 Fall08 )                                        ###
###                                                       ###
### This script takes treebank data,                      ###
### processes each tree structure in the data,            ###
### report discontinuous structures in each sentence,     ###
### and return a file with modified tree structures.      ###
#############################################################

from __future__ import division
import os, sys, string, re, pprint, time
from util.lst import partition, findif

def elapsed(startTime):
    """return the amount of time
    which as elapsed since startTime"""
    return time.time()-startTime
def deCSV(sentence):
    "[str] -> [[[str]]]"
    rez = [line.split('\t') for line in sentence.split('\n') if line!='']
    return filter(None, rez)
def reCSV(sentence):
    "[[[str]]] -> [str]"
    return '\n'.join('\t'.join(map(str, word)) for word in sentence)
def sentences(fileName):
    """str -> [sentence] -- return a list of sentences
    where sentence = str (though implicitly [str] separated by \n)"""
##     sentences = []
##     acc = []
##     for line in open(fileName):
##         line = line.rstrip('\r\n')
##         if re.match(r"#BOS", line):
##             sentences.append(''.join("\n" + line for line in acc))
##             acc = [line]
##         else:
##             acc.append(line)
##     sentences.append(''.join("\n" + line for line in acc))
##     sentences.pop(0)
##     sentences.append('')
##     return sentences
    outFile = open('temp.txt', 'w')
    text = open (fileName, 'r')
    
    for line in text:
        line = line.rstrip('\r\n')
        if re.match(r'#BOS', line):
            outFile.write("\n")
            outFile.write(line + "\n")
        elif re.match(r'#EOS',line):
            outFile.write(line)
            outFile.write("\n\n")
        else:
            outFile.write (line + "\n")
         #   outFile.write('\n')

    outFile.close()
    outText = open('temp.txt', 'r').read()

    sentences = re.split('\n{2,}', outText)
    
    return(sentences)
def writeTreebank(sentences, fileName):
    f = open(fileName, 'w')
    for s in sentences:
        for word in s:
            f.write('\t'.join(map(str, word)) + '\n')
        f.write('\n\n')
    f.close()

def addTreebankID(sents):
    "original treebank data * IDed treebank output filename"
    return map(addWordID, sents)
def addWordID(sentence):
    """str -> [[int,str...]] -- return a list of data of each sentence
        in treebank file with wordID added  """
    #return [[i]+word for i,word in enumerate(deCSV(sentence))]
    return [[str(i)]+line.split('\t') for i,line in enumerate(sentence.split('\n'))]

def writePOS(poss, outFileName):
    outPOS = open(outFileName, 'w')
    outPOS.write('\n\n\n\n\n'.join(map(reCSV, poss)))
    outPOS.close()
def POS(treebank):
    """[[[str]]]->[[[str]]] -- remove all fields from the treebank but
    wordID, word, POS and motherID"""
    poss = []
    pos = []
    def collect(columns, *ns):
        pos.append([columns[n] for n in ns])
    for sentence in treebank:
        pos = []
        for columns in sentence:
            if len(columns) < 3: # empty and #BOS/#EOS
                pass
            elif len(columns[2])>0:
                collect(columns, 0, 1, 3, -1)
            elif len(columns[7])>0:
                if re.search(r'([a-z]|--)', columns[7]):
                    collect(columns, 0, 1, 6, -1)
                elif re.search(r'(OA|HD|CJ|MO|NK|DA|PM|RC|OC|SB|MNR|PG|AG)', columns[7]):
                ### to avoid tags of grammatical function that are not POS tags
                    collect(columns, 0, 1, 5, -1)
                else:
                    collect(columns, 0, 1, 7, -1)
            elif len(columns[6]) > 0:
                if re.search(r'[a-z]', columns[6]):
                    collect(columns, 0, 1, 5, -1)
                elif re.match(r'--', columns[6]):
                    collect(columns, 0, 1, 5, -1)
                else:
                    collect(columns, 0, 1, 6, -1)
            elif len(columns[5]) > 0:
                collect(columns, 0, 1, 5, -1)
            else:
                collect(columns, 0, 1, 7, -1)
        if pos: poss.append(pos)
    return poss

def isWord(item):
    return re.match(r'[^#]', item)
def isPhrase(item):
    return re.match(r'#', item)
def createWordPhraseList(lines):
    ### each line has 1) word or phraseID, 2) POS and 3)mother node ID
    ### itemID, word or phrase, POS, motherID
    def isLinePhrase((num, item, POS, motherID)):
        return isPhrase(item)
    ### make lists of words and phrases
    phrases, wordList = partition(isLinePhrase, lines)
    phraseList = [[item.strip("#"), POS, motherID]
                  for [num, item, POS, motherID] in phrases]
    return wordList, phraseList

def groupNodeElements(wordList, phraseList):
    """ Based on the wordList and the phraseList,
     group elemnts of the same mother node together mother node as the key,
     and daughters as the value"""
    phrases=dict()
    
    for (_,_,_,motherID) in wordList:
        phrases[motherID] = [id for id,_,_,itemMotherID in wordList
                             if itemMotherID==motherID]

    ### check if certain phrases are daughters of another phrase
    for (id,_,motherID) in phraseList:
        phrases.setdefault(motherID, []).append(id)

    return phrases
def getPhrases (sentence):
    """extract phrases from treebank data"""
    wordList,phraseList = createWordPhraseList(sentence)
    phrases = groupNodeElements(wordList, phraseList)
    ### change string format to number for further process
    tree = dict()
    for key, value in phrases.items():
        if value == []:
            print "ERROR! Cannot handle empty tree."
            return ['ERROR']
        else:
            try:
                tree[int(key)]= map(int, value)
            except ValueError:
                tree[key] = value
    return tree


def flatten(tree):
    """ take a tree structure and return its leaves into a list"""

    mothers = tree.keys()
    ### under each grandmom node, change each mother node with its daughters
    for node, daughters in tree.items():
        for i,daughter in enumerate(daughters):
            for mother in mothers:
                if mother == daughters[i]:
                    tree[node].extend(tree[mother])
                    leafIndex = tree[node].index(daughters[i])
                    del tree[node][leafIndex]
    return(tree)
def unions(sets):
    return reduce(set.union, sets)
def flatten2(tree):
    flat = {}
    def flattenNode(mother):
        if mother==0 or mother >= 500:
            flat[mother] = unions(map(flattenNode, tree[mother]))
            return flat[mother]
        else:
            return set([mother])
    if 0 in tree:
        flattenNode(0)
    return flat
def pairs(l):
    return [(l[i],l[i+1]) for i in range(len(l)-1)]
def discontinuous(span):
    """take a dictionary of tree structure and report discontinue nodes"""
    disList = []
    for leaves in span.values():
        ### make sure it loops over every pair in the list
        for start,next in pairs(sorted(leaves)):
            if next - start > 1:
                ### the discontinuos point and the next word
                disList.append((start, start+1))
    return disList

def writeSentence(sentence, file, addFile):
    for columns in sentence:
        writeWord(columns[1:], file)
        writeWord(columns[1:], addFile)
def writeWord(word, file):
    file.write('\t'.join(map(str, word)) + '\n')

########################
def main():
    startTime=time.time()
    inputData = None
    try:
        inputData = sys.argv[1]
    except IndexError:
        inputData = raw_input("Please give the name of input file:  " )
    
    sents = sentences(inputData) ### original treebank data
    treeData = addTreebankID(sents)
    writeTreebank(treeData, inputData+'.data')

    ##################################################
    ### get relevant data from the treebank data
    clauses = POS(treeData)
    writePOS(clauses, inputData+'.pos')
    ##################################################
    ### find DISCONTINUOUS nodes in each tree and output modified structures
    ### to be changed and printed later
    ### if discontinuous nodes are found in certain trees,
    modFile = open(inputData+'.out', 'w') 
    ### their modified tree structure will be printed into a seperate file 
    ### add extra nodes while modify the structure
    modAddFile = open(inputData+'Add.out', 'w')



    ### check structures sentence by sentence
    correction = 0 ### count how many sentences in the file involve discontinuity 
    for clause,tree in zip(clauses, treeData):
        span = discontinuous(flatten(getPhrases(clause)))
        if len(span) < 1:
            ### for sentences that do not have any discontinuous elements
            writeSentence(tree, modFile, modAddFile)
            continue
        ### if there are discontinuous elements in the structure
        correction +=1
        for s in span:
            k = 0
            discon = str(s[0]) ### the discontinous word
            nextWord = str(s[1]) ### and its successor
        oldMother = int(findif(lambda c: discon==c[0], tree)[-1])
        newMother = int(findif(lambda c: nextWord==c[0], tree)[-1])

        addNode = ('60%s' % k) ### to be used later as added node
                               ### add nodes in each sentence starts from 600
        #print addNode
        k+=1

        for columns in tree:

            ### node raising 
            if newMother != 0 and newMother > oldMother:
                # WARNING: This case is not unit tested
                # I guess I never raise all the way to the root?
                print 'untested branch 1 : nonroot newMother > oldMother'
                if oldMother == 0:
                    for col in columns[1:-1]:
                        modFile.write('%s\t' % col) 
                        modAddFile.write('%s\t' % col)
                    modFile.write(columns[-1])
                    modFile.write('\n')
                    modAddFile.write(columns[-1])
                    modAddFile.write('\n')

                elif re.search(str(oldMother), columns[1]):
                    for col in columns[1:-1]:
                        modFile.write('%s\t' % col)
                        modAddFile.write('%s\t' % col)
                    modFile.write(str(newMother))
                    modFile.write('\n')
                    modAddFile.write(str(addNode))
                    modAddFile.write('\n')

                    ### a new entry for added node
                    modAddFile.write('#%s\t' % addNode)
                    for col in columns[2:-1]:
                        modAddFile.write('%s\t' % col)
                    modAddFile.write('%s\t@%s' % (newMother, columns[-1]))
                    ### old information on node preserved
                    modAddFile.write('\n')                            

                else:
                    for col in columns[1:-1]:
                        modFile.write('%s\t' % col)
                        modAddFile.write('%s\t' % col)
                    modFile.write(columns[-1])
                    modFile.write('\n')
                    modAddFile.write(columns[-1])
                    modAddFile.write('\n')

            elif newMother == 0:
                # WARNING: This case is not unit tested
                # I guess I never raise all the way to the root?
                # maybe it's because I'm using ints now? (no)
                print 'nontested branch 2: root'
                modAddFile.write('ddddd')
                if discon == columns[0]:
                    for col in columns[1:-1]:
                        modFile.write('%s\t' % col)
                        modAddFile.write('%s\t' % col)
                    modFile.write(newMother)
                    modFile.write('\n')
                    modAddFile.write(addNode)
                    modAddFile.write('\n')

                    ### a new entry for added node
                    modAddFile.write('#%s\t' % addNode)
                    for col in columns[2:-1]:
                        modAddFile.write('%s\t' % col)
                    modAddFile.write('%s\t@%s' % (newMother, columns[-1]))
                    ### old information on node preserved
                    modAddFile.write('\n')

                else:
                    # WARNING: This case is not unit tested
                    for col in columns[1:-1]:
                        modFile.write('%s\t' % col)
                        modAddFile.write('%s\t' % col)
                    modFile.write(columns[-1])
                    modFile.write('\n')
                    modAddFile.write(columns[-1])
                    modAddFile.write('\n')

            ### raise the node of the next word
            elif newMother != 0 and newMother < oldMother:
                if nextWord == columns[0]:
                    writeWord(columns[1:-1] + [oldMother], modFile)
                    writeWord(columns[1:-1] + [addNode], modAddFile)
                    ### a new entry for added node
                    writeWord(["#" + addNode] +
                               columns[2:-1] +
                               [oldMother, "@%s" % newMother],
                              modAddFile)

                else:
                    writeWord(columns[1:], modFile)
                    writeWord(columns[1:], modAddFile)
            

    percentage = correction/len(clauses)*100
    print "There are",len(clauses),"sentences in this file."
    print correction,"sentences involve discontinuous structures. (",percentage,"%)"
    elapsedTime=elapsed(startTime)
    print "elapsed time = ", elapsedTime
##     modFile.write('elapsed time = %s ' % elapsedTime)
##     modAddFile.write('elapsed time = %s ' % elapsedTime)
    
    return
    
if __name__ == "__main__":
    main()
