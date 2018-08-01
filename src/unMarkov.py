from tree import Node,Tree
import fileinput
from copy import deepcopy

def unMarkov(node):
    if node.label.find("^") != -1:
        node.label = node.label.split("^")[0]
    for child in node.children:
        unMarkov(child)

def unhMarkov(node):
    index = node.label.find("[")
    if index != -1:
        node.label = node.label[:index]+"*"
    for child in node.children:
        unhMarkov(child)

if __name__ == "__main__":
    #f = open("dev.parsesv2.post","w")
    line = "(TOP (S_VP (VB List) (NP (NP[SBAR] (NP[PP] (NP (DT the) (NNS flights)) (PP (IN from) (NP_NNP Baltimore))) (PP (TO to) (NP_NNP Seattle))) (SBAR (WHNP_WDT that) (S_VP (VBP stop) (PP (IN in) (NP_NNP Minneapolis)))))) (PUNC .))"
    print line
    t = Tree.from_str(line)
    unhMarkov(t.root)
    print t
    """for line in fileinput.input():
        if line == '\n':
            f.write('\n')
        else:
            t = Tree.from_str(line)
            unMarkov(t.root)
            newLine = str(t)
            f.write(newLine)
            f.write('\n')"""