#!/usr/bin/env python

import sys, fileinput
import tree

def unhMarkov(node):
    index = node.label.find("[")
    if index != -1:
        node.label = node.label[:index]+"*"
    for child in node.children:
        unhMarkov(child)
def unvMarkov(node):
    if node.label.find("^") != -1:
        node.label = node.label.split("^")[0]
    for child in node.children:
        unvMarkov(child)

if __name__ == "__main__":
    
    for line in fileinput.input():
        t = tree.Tree.from_str(line)
        if t.root is None:
            print
            continue
        t.restore_unit()
        unhMarkov(t.root)
        t.unbinarize()
        #unvMarkov(t.root)
        print t
