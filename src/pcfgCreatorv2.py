from Stack import Stack
from collections import defaultdict
import sys,fileinput
from tree import Node,Tree

class PCFG:
    def __init__(self):
        self.terms=[]
        self.nterms = []
        self.S = "S"
        self.rules = {}
        self.rProbDict = {}
        self.numRules =0

    def printPCFG(self,mode):
        printTerminals = False
        printNonTerminals = False
        printRules = False
        if mode == 1 or mode == 4 or mode == 5:
            printTerminals = True
        if mode == 2 or mode == 4 or mode == 5:
            printNonTerminals = True
        if mode == 3 or mode == 5:
            printRules = True

        if printTerminals:
            print "Number of Rules are:- ",self.numRules
            print "-----Printing Terminals------"
            print self.terms
            print self.rules["WP"]
            print len(self.rules["WP"])
        if printNonTerminals:
            print "-----Printing Non Terminals------"
            print self.nterms
        if printRules:
            print "-----Printing rules and their probabilities-------"
            for key in self.rules:
                for items in self.rules[key]:
                    key_string = key + " --> " + str(items)
                    print key, " --> ", items, " --> ",self.rProbDict[key_string]



class pcfgCreator:
    def __init__(self):
        self.dcount = defaultdict(int)
        self.ruleDict = {}
        self.pcfg = PCFG()

    def pushString(self,s, str1):
        if len(str1) != 0:
            s.push(str1)
            # print "Pushed " + str1
        return ""

    def makeRule(self,lhs, rhs):
        # print lhs,rhs,type(lhs),type(rhs)
        rhsList = []
        if isinstance(rhs, str):
            new_rhs = (rhs,)
        else:
            new_rhs = tuple(rhs)
        if lhs in self.ruleDict:
            if new_rhs not in self.ruleDict[lhs]:
                self.ruleDict[lhs].append(new_rhs)
        else:
            rhsList.append(new_rhs)
            self.ruleDict[lhs] = rhsList
        ruleString = lhs + " --> " + str(new_rhs)
        #print lhs + " --> " + str(new_rhs)
        self.dcount[lhs] += 1
        self.dcount[ruleString]+=1

    def parseRule(self,rList, rStack):
        if len(rList) == 1:
            pushWord = rList[0]
            ruleWord = rList[0]
            a = rStack.pop()
            #print "rStack :- ", rStack
            count = 1
            newList = []
            while count != 0:
                pop_value = rStack.pop()
                #print "Pop value is =",pop_value
                if pop_value == ")":
                    count += 1
                elif pop_value == "(":
                    count -= 1
                else:
                    newList.append(pop_value)
            #print "rStack :- ", rStack
            rStack.push("(")
            rStack.push(pushWord)
            rStack.push(")")
            #print "rStack :- ", rStack
            self.makeRule(ruleWord, list(reversed(newList[0:-1])))
        else:
            self.makeRule(rList[-1], list(reversed(rList[0:-1])))

        return 0

    def parseLine(self,line):
        s = Stack()
        rStack = Stack()
        str1 = ""
        for char in line:
            if char == " ":
                self.pushString(rStack, str1)
                #print "rStack :- ",rStack
                self.pushString(s, str1)
                str1 = ""
                #print "sStack :- ",s
            elif char == "(":
                s.push(char)
                #print "sStack :- ", s
                rStack.push(char)
                #print "rStack :- ", rStack
            elif char == ")":
                str1 = self.pushString(s, str1)
                #print "sStack :- ", s
                rStack.push(")")
                #print "rStack :- ", rStack
                rList = []
                while True:
                    a = s.pop()
                    #print "Popped "+a
                    if a == "(":
                        break
                    rList.append(a)
                #print "sStack :- ", s
                d = self.parseRule(rList, rStack)
            else:
                #if char != "*":
                str1 = str1 + char

    def populateTermsandnTerms(self):
        for key in self.ruleDict:
            if key not in self.pcfg.nterms:
                self.pcfg.nterms.append(key)
        for key1 in self.ruleDict:
            self.pcfg.numRules += len(self.ruleDict[key1])
            for items in self.ruleDict[key1]:
                for term in items:
                    #print term,term.isupper()
                    if term not in self.pcfg.nterms:
                        if term not in self.pcfg.terms:
                            self.pcfg.terms.append(term)

    def calcRuleProb(self):
        lhs = ""
        rhs = ""
        for key in self.ruleDict:
            count_lhs = self.dcount[key]
            for items in self.ruleDict[key]:
                key_string = key + " --> " + str(items)
                #print key_string
                count_rhs = self.dcount[key_string]
                self.pcfg.rProbDict[key_string] = float(count_rhs)/float(count_lhs)

    def generatePCFG(self):
        self.pcfg.rules = self.ruleDict
        self.populateTermsandnTerms()
        self.calcRuleProb()

    def traverse(self,node):
        if node.parent != None and len(node.children) > 1:
            nList = node.parent.label.split("^")
            if len(nList) > 1:
                node.label = node.label + "^" + nList[0]
            else:
                node.label = node.label + "^" + node.parent.label
        for child in node.children:
            self.traverse(child)

if __name__ == "__main__":
    p = pcfgCreator()
    """line = "(TOP (SBARQ (WHNP_WHNP (WDT What) (NNS flights)) (SQ (VBP do) (SQ* (NP_PRP you) (VP (VP* (VP* (VB have) (PP (IN from) (NP_NNP Burbank))) (X_TO to)) (PP (TO to) (NP (NP_NNP Tacoma) (NP_NNP Washington))))))) (PUNC ?))"
    p.parseLine(line)"""
    for line in fileinput.input():
        #print line
        t = Tree.from_str(line)
        p.traverse(t.root)
        newLine = str(t)
        #print line
        p.parseLine(newLine)
    p.generatePCFG()
    p.pcfg.printPCFG(5)
    """for key in p.dcount:
        if key.startswith("NP"):
            print key ,p.dcount[key]
    print p.pcfg.terms
    print p.pcfg.nterms
    for key in p.pcfg.rProbDict:
        print p.pcfg.rProbDict[key]
    print p.pcfg.rProbDict
    for line in fileinput.input():
        p.parseLine(line)"""
