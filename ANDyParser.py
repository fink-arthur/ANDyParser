# coding=utf-8

import Colours, Variables

class Parser:
    """
    This class will generate the .colextpn file to create a coloured extented petri net
    from the definitions given in the file at the address given as an argument for this file
    """
    
    def __init__(self, address):
        with open(address, 'r') as f:
            self.string = f.read()
        self.entities = self.string.split("%%")[0].rstrip().lstrip()
        self.potential = self.string.split("%%")[1].rstrip().lstrip()
        self.mandatory = self.string.split("%%")[2].rstrip().lstrip()
        
        self.colours = Colours.Colours().makeText(self.entities, self.potential, self.mandatory)
        self.variables = Variables.Variables().makeText(self.entities, self.potential, self.mandatory)
            
    def makeFile(self):
        with open("start.txt", 'r') as f:
            start = f.read()
        with open("end.txt", 'r') as f:
            end = f.read()
        with open("test.colextpn", 'w') as f:
            f.write(start + "\n" + self.colours + self.variables + end)
        return 1
        
if __name__ == '__main__':
    parser = Parser("test.txt")
    print(parser.makeFile())