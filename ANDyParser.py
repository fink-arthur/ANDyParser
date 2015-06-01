# coding=utf-8

import Colours

class Parser:
    """
    This class will generate the .colextpn file to create a coloured extented petri net
    from the definitions given in the file at the address given as an argument for this file
    """
    
    def __init__(self, address):
        self.colours = Colours.Colours()
        with open(address, 'r') as f:
            self.string = f.read()
            
    def makeFile(self):
        with open("start.txt", 'r') as f:
            start = f.read()
        with open("end.txt", 'r') as f:
            end = f.read()
        with open("test.colextpn", 'w') as f:
            entities = self.string.split("%%")[0].rstrip().lstrip()
            potential = self.string.split("%%")[1].rstrip().lstrip()
            mandatory = self.string.split("%%")[2].rstrip().lstrip()
            f.write(start + "\n" + self.colours.makeText(entities, potential, mandatory) + end)
        return 1
        
if __name__ == '__main__':
    parser = Parser("test.txt")
    print(parser.makeFile())