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

def elapsed(startTime):
    """return the amount of time
    which as elapsed since startTime"""
    return time.time()-startTime

def sentences(fileName):
    """return a list of sentences"""

    outFile = open('temp.txt', 'w')
    text = open (fileName, 'r')
    
    for line in text:
        line = line.rstrip('\r\n')
        if re.match(r'#BOS', line):
            outFile.write("\n")
            outFile.write(line)
            outFile.write("\n")
        elif re.match(r'#EOS',line):
            outFile.write(line)
            outFile.write("\n\n")
        else:
            outFile.write (line)
            outFile.write("\n")
         #   outFile.write('\n')

    outFile.close()
    outText = open('temp.txt', 'r').read()

    sentences = re.split('\n{2,}', outText)
    
    return(sentences)


def addWordID(sentence):
    """ return a list of data of each sentence
        in treebank file with wordID added  """

    i=0
    lineList = list()
    lines = sentence.split('\n')
    for line in lines:
        columns = line.split('\t')
        #print columns
        columns.insert(0, i)
        lineList.append(columns)
        i+=1
        if re.search (r'#EOS', line):
            i=0 ### to ensure wordIDs in the range of the length of sentence,
                ### so that such ID numbers will not be confused
                ### with phrasesIDs that are in the range of 500~

    return(lineList)


def POS(fileName, outFileName):        
    """read in a file of tree structrue and returns a file
    with a list of wordID, word, POS and motherID"""
    
    inFile = open(fileName, 'r') 
    outPOS = open (outFileName, 'w')
    
    for line in inFile:
        if line == '\n':
            outPOS.write(line)
        else:
            
            line = line.rstrip('\r\n')
            columns = line.split('\t')
            #print columns
            #print len(columns)
            
            try: ### check which column the POS tag is in
                     ### it occurrence in relation to the 2nd / 7th columns is more regular
                     ### the rest is to account for special cases
                if re.match(r'#[EB]OS', line):
                     outPOS.write("\n")
                elif len(columns[2])>0:
                    outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[3], columns[-1]))
                    #print columns[0], columns[1]
                elif len(columns[7])>0:
                    if re.search(r'([a-z]|--)', columns[7]):
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[6], columns[-1]))
                        #print columns[0], columns[1]
                    elif re.search(r'(OA|HD|CJ|MO|NK|DA|PM|RC|OC|SB|MNR|PG|AG)', columns[7]):
                    ### to avoid tags of grammatical function that are not POS tags
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[5], columns[-1]))
                        #print columns[0], columns[1]
                    else:
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[7], columns[-1]))
                        #print columns[0], columns[1]
                elif len(columns[6]) > 0:              
                    if re.search(r'[a-z]', columns[6]):
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[5], columns[-1]))
                        #print columns[0], columns[1]
                    elif re.match(r'--', columns[6]):
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[5], columns[-1]))
                        #print columns[0], columns[1]
                    else:
                        outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[6], columns[-1]))
                        #print columns[0], columns[1]
                elif len(columns[5]) > 0:
                    outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[5], columns[-1]))
                    #print columns[0], columns[1]
                else:
                    outPOS.write('%s\t%s\t%s\t%s\n' % (columns[0], columns[1], columns[7], columns[-1]))
                    #print columns[0], columns[1]


            except IndexError:
                pass
    inFile.close()
    outPOS.close()
    

def getPhrases (sentence):
    """extract phrases from treebank data"""
    
    ### make lists of words and phrases
    wordList=list()
    phraseList = list()
    
    #print "\n"
    
    lines = sentence.split("\n") ### to get information of one word per line
    #print lines
    for line in lines:
        if len(line)>1:
            if re.match(r'#[BE]OS', line):
                continue
            else:
            ### each line has 1) word or phraseID, 2) POS and 3)mother node ID
                try:
                    columns = line.split("\t")
                    #print columns
                    num = columns[0] ### itemID
                    item = columns[1] ### word or phrase
                    motherID = columns[-1]
                    POS = columns[2]
                                       
                    #print word
                    #print ID

                    ### create a word list in the format:
                    ### [wordID, word, POS, motherID]
                    if re.match(r'[^#]', item):
                        wordList.append([])
                        wordList[-1].append(num) ### wordID
                        wordList[-1].append(item) ### word
                        wordList[-1].append(POS)
                        wordList[-1].append(motherID)
                        
                    ### create a phrase list in the format:
                    ### [phrase, POS, motherID]
                    elif re.match(r'#', item):
                        phraseList.append([])
                        #phraseList[-1].append(num)
                        item = item.strip('#')
                        phraseList[-1].append(item) ### phrase
                        phraseList[-1].append(POS)
                        phraseList[-1].append(motherID)
                            
                except IndexError:
                    pass
                
                if line == "\n":
                    continue

   
    #print wordList
    #print '\n'
    #print phraseList
            

    ### Based on the wordList and the phraseList,
    ### group elemnts of the same mother node together
    ### mother node as the key, and daughters as the value
    phrases=dict() 
    
    for word in wordList: 
        motherID = word[-1]
        #print motherID
        #phrases[word[-1]]=list()
        phrases[motherID]=list()

        for item in wordList:
            if item[-1] ==motherID:
                phrases[motherID].append(item[0])
                
    #print phrases
    #print phraseList

    ### check if certain phrases are daughters of another phrase
    for phrase in phraseList:
        motherID = phrase[-1]
        if phrases.has_key(motherID):
            phrases[motherID].append(phrase[0])
        else:
            phrases[motherID] = list()
            phrases[motherID].append(phrase[0])


    ### change string format to number for further process
    tree = dict()    
    for key, value in phrases.items():
        if value == []:
            print "ERROR! Cannot handle empty tree."
            return ['ERROR']
        else:
            try:                
                k = int(key)
                tree.has_key(k)
                leaves = map(int, phrases[key])
                tree[k]= leaves
            except ValueError:
                tree.has_key(key)
                tree[key]= phrases[key]         

            
    return(tree)


def flatten(tree):
    """ take a tree structure and return its leaves into a list"""

    mothers = tree.keys()
    daughters = tree.values()
    #pprint.pprint(tree)
    
    ### under each grandmom node, change each mother node with its daughters
    i = 0
    for node, leaves in tree.items():
        for leaf in leaves:
            if leaf >=500:
                for i in range(len(leaves)):
                    for mother in mothers:
                        if mother == leaves[i]:
                            tree[node].extend(tree[mother])
                            leafIndex = tree[node].index(leaves[i])
                            del tree[node][leafIndex]
                    
                i+=1
    return(tree)

        
def discontinuous(flapTree):
    """take a dictionary of tree structure and report discontinue nodes"""

    span = flapTree
    disList = list()
    i=0
    for key, leaves in span.items():
        leaves.sort()
        
        if len(leaves) ==1:
            #print key, 'single daughter', span[key]
            continue
        
        elif len(leaves) > 1:
            for i in range(len(leaves)):### make sure it loops over every pair in the list
                try:
                    if leaves[i+1]-leaves[i]<1:
                       # print key, 'continue', leaves[i], leaves[i+1], span[key]
                        i+=1
                    elif leaves[i+1]-leaves[i]==1:
                       # print key, 'continue', leaves[i], leaves[i+1], span[key]
                        i+=1
                    
                    elif leaves[i+1]-leaves[i]>1:
                       # print key, 'DISCONTINUE', leaves[i], leaves[i+1], span[key]
                        disList.append((leaves[i],leaves[i]+1) ) ### the discontinuos point and the next word
                        
                        i+=1
                except IndexError:
                    pass
    return disList 
    


########################
def main():
    startTime=time.time()
    inputData = None
    try:
        inputData = sys.argv[1]
    except IndexError:
        inputData = raw_input("Please give the name of input file:  " )
    
    
    IDFile = open (inputData+'.data', 'w') ### create a temp file with wordID added
    
    sents = sentences(inputData) ### original treebank data
    for sentence in sents:
        words = addWordID(sentence) ### a list of words in each sentence

        for word in words:
            IDFile.write('\t'.join(map(str, word[:-1])) + '\t')
##             for col in word[:-1]:
##                 # NCS: No-op; if len(word) < 2, the word[:-1] loop never executes
##                 if len(word)<2:
##                     IDFile.write(word[-1])
##                     IDFile.write('\n')
##                 else:
##                     IDFile.write('%s\t' % col)
            IDFile.write(word[-1])
            IDFile.write('\n')
        IDFile.write('\n\n')

    IDFile.close()

    ##################################################
    ### get relevant data from the treebank data
    POS(inputData+'.data', inputData+'.pos') 

    ##################################################
    ### find DISCONTINUOUS nodes in each tree and output modified structures
    clauses = sentences(inputData+'.pos')
    treeData = sentences(inputData+'.data') ### to be changed and printed later
    #print treeData[0]
    
    modFile = open(inputData+'.out', 'w') ### if discontinuous nodes are found in certain trees,
                                      ### their modified tree structure will be printed into a seperate file 

    modAddFile = open(inputData+'Add.out', 'w')### add extra nodes while modify the structure



    ### check structures sentence by sentence
    correction = 0 ### count how many sentences in the file involve discontinuity 
    for i in range(len(clauses)):
        phrases = getPhrases(clauses[i])
        tree = flatten(phrases)
        span = discontinuous(tree)
        if len(span)>0: ### if there are discontinuous elements in the structure
            correction +=1
            try:                
                for j in range(len(span)):
                    k = 0
                    discon = str(span[j][0]) ### the discontinous word
                    nextWord = str(span[j][1])

                lines = treeData[i].split('\n')
                for line in lines:
                    columns = line.split('\t')
                    
                    #print columns
                    if columns[0]==discon:
                        oldMother = columns[-1]
                        #print type(oldMother)
                    if columns[0]==nextWord:
                        newMother = columns[-1]
                        #print type(newMother)
                
                addNode = ('60%s' % k) ### to be used later as added node
                                       ### add nodes in each sentence starts from 600
                #print addNode
                k+=1
                
                for l in lines:
                    columns = l.split('\t')
                    
                    ### node raising 
                    if newMother != '0' and newMother > oldMother:
                        if oldMother == 0:
                            for col in columns[1:-1]:
                                modFile.write('%s\t' % col) 
                                modAddFile.write('%s\t' % col)
                            modFile.write(columns[-1])
                            modFile.write('\n')
                            modAddFile.write(columns[-1])
                            modAddFile.write('\n')
                            
                        elif re.search(oldMother, columns[1]):
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
                            for col in columns[1:-1]:
                                modFile.write('%s\t' % col)
                                modAddFile.write('%s\t' % col)
                            modFile.write(columns[-1])
                            modFile.write('\n')
                            modAddFile.write(columns[-1])
                            modAddFile.write('\n')
                            
                    elif newMother == '0':
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
                            for col in columns[1:-1]:
                                modFile.write('%s\t' % col)
                                modAddFile.write('%s\t' % col)
                            modFile.write(columns[-1])
                            modFile.write('\n')
                            modAddFile.write(columns[-1])
                            modAddFile.write('\n')

                    ### raise the node of the next word
                    elif newMother != '0' and newMother < oldMother:
                        if nextWord == columns[0]:
                            for col in columns[1:-1]:
                                modFile.write('%s\t' % col)
                                modAddFile.write('%s\t' % col)
                            modFile.write(oldMother)
                            modFile.write('\n')
                            modAddFile.write(addNode)
                            modAddFile.write('\n')
                            
                            ### a new entry for added node
                            modAddFile.write('#%s\t' % addNode)
                            for col in columns[2:-1]:
                                modAddFile.write('%s\t' % col)
                            modAddFile.write('%s\t@%s' % (oldMother, newMother))
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
                            
                    
            except TypeError:
                pass
            
        else: ### for sentences that do not have any discontinuous elements
            lines = treeData[i].split('\n')
            for line in lines:
                columns = line.split('\t')
                for col in columns[1:-1]:
                    modFile.write('%s\t' % col)
                    modAddFile.write('%s\t' % col)
                modFile.write(columns[-1])
                modFile.write('\n')
                modAddFile.write(columns[-1])
                modAddFile.write('\n')

    percentage = correction/i*100  
    print "There are",i,"sentences in this file."
    print correction,"sentences involve discontinuous structures. (",percentage,"%)"
    elapsedTime=elapsed(startTime)
    print "elapsed time = ", elapsedTime
    modFile.write('elapsed time = %s ' % elapsedTime)
    modAddFile.write('elapsed time = %s ' % elapsedTime)
    
    sys.exit(0)        
    
if __name__ == "__main__":
    main()
