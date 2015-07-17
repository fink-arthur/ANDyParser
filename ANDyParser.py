# coding=utf-8

import Colours, Variables, Places, Transitions, Edges, Functions
import os
import optparse

class Parser:
    """
    This class will generate the .colextpn file to create a coloured extented petri net
    from the definitions given in the file at the address given as an argument for this file
    """
    
    def __init__(self, address):        
        with open(address, 'r') as f:
            self.string = f.read().split("%%")
        self.entities = self.string[0].rstrip().lstrip()
        self.potential = self.string[1].rstrip().lstrip()
        self.mandatory = self.string[2].rstrip().lstrip()
        self.initial = self.string[3].rstrip().lstrip()
        
        self.colours = Colours.Colours(self.entities, self.potential, self.mandatory).makeText()
        self.variables = Variables.Variables(self.entities, self.potential, self.mandatory).makeText()
        self.places = Places.Places(self.entities, self.potential, self.mandatory, self.initial).makeText()
        self.transitions = Transitions.Transitions(self.potential).makeText()
        self.edges = Edges.Edges(self.entities, self.potential, self.mandatory).makeText()
        self.functions = Functions.Functions(self.entities, self.potential, self.mandatory).makeText()
            
    def makeFile(self, output):
        with open("start.txt", 'r') as f:
            start = f.read()
        with open(output, 'w') as f:
            f.write(self.places + self.transitions + self.edges + start + "\n" + self.colours + self.variables + self.functions)
        return
        
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-i', action = "store", dest = "input", help= "Setting an input file for the parser", default = "test.txt")
    parser.add_option('-o', action = "store", dest = "output", help = "Setting an output file for the parser", default = "test.colextpn")
    options, args = parser.parse_args()
    if (options.input[-4:] == ".txt"):
        parser = Parser(options.input)
        i = options.input
    else:
        parser = Parser(options.input + ".txt")
        i = options.input + ".txt"
    if (options.output[-9:] == ".colextpn"):
        parser.makeFile(options.output)
        o = options.output
    else:
        parser.makeFile(options.output + ".colextpn")
        o = options.output + ".colextpn"
    os.remove("places.c")
    os.remove("transitions.c")
    print("The file " + o + " has been successfully generated from the input " + i)
