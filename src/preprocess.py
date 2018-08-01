#!/usr/bin/env python

import sys, fileinput
import tree


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

def vhMarkov(node):
    if node.label.find("*") != -1:
        siblingLabel = None
        if node.label[:2] == "SQ":
            siblingLabel = node.parent.children[0].label.split("^")[0]
        else:
            siblingLabel = node.parent.children[1].label.split("^")[0]
        node.label = node.label[:-1] +"["+siblingLabel+"]"
    for child in node.children:
        vhMarkov(child)

def vMarkov(node):
    #print "Working on ",node.label
    if node.parent != None and len(node.children)!=0 and node.label in ["NP","VP","PP","S","SBAR"]:  # "ADJP and SBAR removed for now" ["NP","VP","PP","S","ADJP","SBAR"]
        #print node.children
        if (len(node.children) == 1 and len(node.children[0].children) != 0) or len(node.children)>1:
            nList = node.parent.label.split("^")
            if len(nList)>1:
                node.label = node.label+"^"+nList[0]  ### for v2 remove +"^"+nList[1]
            else:
                node.label = node.label+"^"+node.parent.label
    for child in node.children:
        vMarkov(child)

for line in fileinput.input():
    t = tree.Tree.from_str(line)
    #print line
    #Vertical Markovization
    #vMarkov(t.root)

    # Binarize, inserting 'X*' nodes.
    t.binarize()

    # Horizontal Markovization
    hMarkov(t.root)# if doing only hMarkov. If doing with in conjunction to vMarkov. use vhMarkov
    #vhMarkov(t.root)

    # Remove unary nodes
    t.remove_unit()

    # The tree is now strictly binary branching, so that the CFG is in Chomsky normal form.

    # Make sure that all the roots still have the same label.
    assert t.root.label == 'TOP'

    print t
    
    
