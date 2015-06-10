class Functions:
    """
    This class will generate all the text in the correct xml format to initialize
    all the functions that will be used by the petri net
    """
    
    def __init__(self, entityDefinition):
        self.entityDefinition = entityDefinition
        
    def makeFunction(self, rowNumber, returnType, name, attributes, functionDefinition):
        accumulator = ""
        accumulator += "<colList_row nr=\"" + str(rowNumber) + "\">\n<colList_col nr=\"0\">\n"
        accumulator += "<![CDATA[" + returnType + "]]>\n</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[" + name + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"2\">\n<![CDATA[" + attributes + "]]>\n</colList_col>\n"
        accumulator += "<colList_col nr=\"3\">\n<![CDATA[" + functionDefinition + "]]>\n"
        accumulator += "</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n<colList_col nr=\"5\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        return accumulator
    
    def makeDecayFunctionDefinition(self, entityDefintion):
        accumulator = ""
        splittedDefinition = entityDefintion.split(":")
        splittedLevel = splittedDefinition[1].rstrip().lstrip()[1:-1].split(",")
        accumulator += "[l=0]0"
        for i in range(1,len(splittedLevel)):
            accumulator += "++[l=" + str(i) + "]([u>=" + str(splittedLevel[i]) + "]" + str(i-1) + "++[u<" + str(splittedLevel[i]) + "]" + str(i) + ")"
        return accumulator
        
    
    def makeText(self):
        startString = "<metadataclass count=\"1\" name=\"Function Class\">\n<metadata id=\"10156\" net=\"1\">\n<attribute name=\"Name\" id=\"10157\" net=\"1\">\n<![CDATA[NewFunction]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"10158\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n"
        startString += "</attribute>\n<attribute name=\"Comment\" id=\"10159\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"FunctionList\" type=\"ColList\" id=\"10160\" net=\"1\">\n<colList row_count=\"0\" col_count=\"6\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n"
        startString += "<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>"
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n</metadataclasses>\n</Snoopy>"
        accumulator = ""
        
        splittedEntityDefinition = self.entityDefinition.split("\n")
        for i in range(len(splittedEntityDefinition)):
            name = splittedEntityDefinition[i].split(":")[0].rstrip().lstrip()
            accumulator += self.makeFunction(i, "l" + name, "decay" + name, "l" + name + " l, u" + name + " u", self.makeDecayFunctionDefinition(splittedEntityDefinition[i]))
        
        return startString + accumulator + endString