from tree import Node,Tree
import fileinput
from copy import deepcopy

def vMarkov(node):
    #print "WOrking on ",node.label
    if node.parent != None and len(node.children)!=0 and node.label in["NP","VP","PP","S","ADJP","SBAR"]:
        #print node.children
        if (len(node.children) == 1 and len(node.children[0].children) != 0) or len(node.children)>1:
            nList = node.parent.label.split("^")
            if len(nList)>1:
                node.label = node.label+"^"+nList[0]  ### for v2 remove +"^"+nList[1]
            else:
                node.label = node.label+"^"+node.parent.label
    for child in node.children:
        vMarkov(child)

def hMarkov(node):
    if node.label.find("*") != -1:
        siblingLabel = None
        if node.label[:2] == "SQ":
            siblingLabel = node.parent.children[0].label
        else:
            siblingLabel = node.parent.children[1].label
        node.label = node.label[:-1] +"["+siblingLabel+"]"
    for child in node.children:
        hMarkov(child)

if __name__ == "__main__":
    #f = open("train.treesv2","w")
    """line = "(TOP (S (VP (VB List) (NP (NP (DT the) (NNS flights)) (PP (IN from) (NP (NNP Baltimore))) (PP (TO to) (NP (NNP Seattle))) (SBAR (WHNP (WDT that)) (S (VP (VBP stop) (PP (IN in) (NP (NNP Minneapolis))))))))) (PUNC .))"
    print line
    t = Tree.from_str(line)
    vMarkov(t.root)
    newLine = str(t)
    print newLine"""
    """for line in fileinput.input():
        #print line
        t = Tree.from_str(line)
        vMarkov(t.root)
        newLine = str(t)
        f.write(newLine)
        f.write('\n')"""
    line = "(TOP (S_VP (VB List) (NP (NP* (NP* (NP (DT the) (NNS flights)) (PP (IN from) (NP_NNP Baltimore))) (PP (TO to) (NP_NNP Seattle))) (SBAR (WHNP_WDT that) (S_VP (VBP stop) (PP (IN in) (NP_NNP Minneapolis)))))) (PUNC .))"
    t = Tree.from_str(line)
    hMarkov(t.root)
    print t
