# coding=utf-8

import Colours, Variables, Places, Transitions, Edges

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
        
        self.colours = Colours.Colours(self.entities, self.potential, self.mandatory).makeText()
        self.variables = Variables.Variables(self.entities, self.potential, self.mandatory).makeText()
        self.places = Places.Places(self.entities, self.potential, self.mandatory).makeText()
        self.transitions = Transitions.Transitions(self.potential).makeText()
        self.edges = Edges.Edges(self.potential, self.mandatory).makeText()
            
    def makeFile(self):
        with open("start.txt", 'r') as f:
            start = f.read()
        with open("end.txt", 'r') as f:
            end = f.read()
        with open("test.colextpn", 'w') as f:
            f.write(self.places + self.transitions + self.edges + start + "\n" + self.colours + self.variables + end)
        return 1
        
if __name__ == '__main__':
    parser = Parser("test.txt")
    print(parser.makeFile())