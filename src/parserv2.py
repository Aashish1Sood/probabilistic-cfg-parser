from pcfgCreatorv2 import pcfgCreator
from pcfgCreatorv2 import PCFG
import fileinput
from copy import deepcopy
from tree import Node,Tree
import math

class Table:
    def __init__(self,num):
        self.table = [[{} for i in range(num+1)]for j in range(num+1)]
    def printTable(self):
        for i in range(len(self.table[0])):
            print self.table[i]
NoParse =0
#f = open("output1.txt", "w")
outFile = open("dev.parsesh2","w")
class parserCreator:
    def __init__(self,pcfg):
        self.pcfg = pcfg
        self.nRules={}

    def checkWordsinTermList(self,wordList):
        allWordsPresent = True
        wordsAbsent = []
        for word in wordList:
            if word not in self.pcfg.terms:
                allWordsPresent = False
                wordsAbsent.append(word)
        return allWordsPresent,wordsAbsent

    def logProb(self):
        for key in self.pcfg.rProbDict:
            self.pcfg.rProbDict[key] = math.log10(self.pcfg.rProbDict[key])

    def fillUnknowns(self,wordsAbsent,wordList):
        for i,item in enumerate(wordList):
            if item in wordsAbsent:
                wordList[i] = "<unk>"
        return wordList

    def reindexRules(self):
        d={}
        for key in self.pcfg.rules:
            for terms in self.pcfg.rules[key]:
                if len(terms)==2:
                    if terms in d:
                        d[terms].append(key)
                    else:
                        l=[]
                        l.append(key)
                        d[terms]=l
        self.nRules = d
        """for key in d:
            print key,d[key]"""

    def makeNode(self,backP,label,i,j):

        if i+1==j:
            node_label = label
            childNode = Node(backP[i][j][label][0],[])
            pnode = Node(node_label, [])
            pnode.insert_child(0,childNode)
            return pnode
        else:
            node_label = label
            print backP[i][j][label][0]
            pnode = Node(node_label, [])
            lchild = backP[i][j][label][0]
            rchild = backP[i][j][label][1]
            pnode.insert_child(0, self.makeNode(backP, lchild[0], lchild[1], lchild[2]))
            pnode.insert_child(1, self.makeNode(backP, rchild[0], rchild[1], rchild[2]))
            return pnode

    def buildTree(self,ptable,backP):

        max_index = len(ptable[0])
        root_node = self.makeNode(backP,"TOP",0,max_index-1)
        parseTree = Tree(root_node)
        print parseTree
        return parseTree

    def parseLine(self,line):
        global NoParse
        global outFile
        wordList = self.parseLinetoWords(line)
        p = Table(len(wordList))
        backP = Table(len(wordList))
        allWordsPresent,wordsAbsent = self.checkWordsinTermList(wordList)
        print wordsAbsent
        if not allWordsPresent:
            print "All Words are not present"
            wordList = self.fillUnknowns(wordsAbsent,wordList)
        for j in range(1,len(wordList)+1):
            word = wordList[j-1]
            for key in self.pcfg.rules:
                if (word,) in self.pcfg.rules[key]:
                    #print key, word
                    #print self.pcfg.rules[key]
                    p.table[j-1][j][key] = self.pcfg.rProbDict[key+" --> "+str((word,))]
                    backP.table[j-1][j][key] = (word,)

        #print p.table
        for span in range(2,len(wordList)+1):
            for begin in range(0,len(wordList)-span+1):
                end = begin + span
                for split in range(begin+1,end):
                    #print "begin = ",begin," split = ",split," end = ",end
                    bList = p.table[begin][split].keys()
                    cList = p.table[split][end].keys()
                    permuteList = []
                    aList = []
                    if not bList or not cList:
                        continue
                    else:
                        permuteList = [(item1,item2) for item1 in bList for item2 in cList]
                    for item in permuteList:
                        if item in self.nRules:
                            for item1 in self.nRules[item]:
                                key_string = item1+" --> "+str(item)
                                #print item1,item,key_string
                                aList.append((item1,item[0],item[1],self.pcfg.rProbDict[key_string]))
                    for item in aList:
                        pScore = p.table[begin][split][item[1]] + p.table[split][end][item[2]] + item[3]
                        if item[0] in p.table[begin][end].keys():
                            if pScore > p.table[begin][end][item[0]]:
                                p.table[begin][end][item[0]] = pScore
                                backP.table[begin][end][item[0]] = ((item[1],begin,split),(item[2],split,end))
                        else:
                            p.table[begin][end][item[0]] = pScore
                            backP.table[begin][end][item[0]] = ((item[1], begin, split), (item[2], split, end))
        #p.printTable()
        #backP.printTable()

        if "TOP" in p.table[0][len(p.table[0])-1]:
            parseTree = self.buildTree(p.table,backP.table)
            outFile.write(str(parseTree)+'\n')
        else:
            print "No Parse present"
            outFile.write('\n')
            NoParse+=1


    def parseLinetoWords(self,line):
        return line.split(" ")

if __name__ == "__main__":
    global NoParse
    p = pcfgCreator()
    for line in fileinput.input():
        #print line
        #print line
        p.parseLine(line)
    p.generatePCFG()
    #p.pcfg.printPCFG(4)
    pc = parserCreator(deepcopy(p.pcfg))
    pc.logProb()
    #pc.pcfg.printPCFG(4)
    pc.reindexRules()
    f1 = open("dev.strings",'r')
    for line in f1:
        print line
        pc.parseLine(line.strip())
    print "No Parse Count is: ", NoParse
    """line = "I would like it to have a stop in New York and I would like a flight that serves breakfast ."
    pc.parseLine(line)"""
