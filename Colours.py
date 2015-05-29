# coding=utf-8

class Colours:
    """
    This class will generate all the text in the correct "snoopy" format to initialize
    all the colour sets that will need to be used for the petri net (simple and compounded)
    """
    
    # the string that contains all the unchanging data when creating all the color sets
    #startString = "<metadataclass count=\"1\" name=\"Basic Colorset Class\">\n<metadata id=\"7035\" net=\"1\">\n<attribute name=\"Name\" id=\"7036\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"7037\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"7038\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
    
    def createSimpleColorSet(self, entityDefinition):
        """
        Creates all the simple color set needed for the petri net
        """
        numberOfLines = entityDefinition.count("\n") + 1
        numberOfColours = numberOfLines #2 * numberOfLines + 2
        lines = entityDefinition.split("\n")
        startString =  "<attribute name=\"ColorsetList\" type=\"ColList\" id=\"7039\" net=\"1\">\n<colList row_count=\"" + str(numberOfColours) + "\" col_count=\"5\" active_row=\"0\" active_col=\"0\">\n<colList_head>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n<colList_colLabel>\n<![CDATA[]]>\n</colList_colLabel>\n</colList_head>\n<colList_body>\n"
        accumulator = ""
        for i in range(numberOfLines):
            # A loop used to create the colors that will define the current level at which the entity is
            accumulator += "<colList_row nr=\"" + str(i) + "\">\n"
            accumulator += "<colList_col nr=\"1\">\n"
            accumulator += "<![CDATA[" + "l" + lines[i].split(":")[0].rstrip() + "]]>\n"
            accumulator += "</colList_col>\n<colList_col nr=\"1\">\n<![CDATA[int]]>\n</colList_col>\n<colList_col nr=\"2\">\n"
            accumulator += "<![CDATA[0-10]]>\n" # Calculer et mettre le nombre de niveau que l'entité a
            accumulator += "</colList_col>\n<colList_col nr=\"3\">\n<![CDATA[white]]>\n</colList_col>\n<colList_col nr=\"4\">\n<![CDATA[]]>\n</colList_col>\n</colList_row>\n"
        endString = "</colList_body>\n</colList>\n<graphics count=\"0\"/>\n</attribute>\n<graphics count=\"0\"/>\n</metadata>\n</metadataclass>\n"
        return startString + accumulator + endString
    
    def makeText(self, entityDefinition):
        startString = "<metadataclass count=\"1\" name=\"Basic Colorset Class\">\n<metadata id=\"7035\" net=\"1\">\n<attribute name=\"Name\" id=\"7036\" net=\"1\">\n<![CDATA[NewColorset]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"ID\" id=\"7037\" net=\"1\">\n<![CDATA[0]]>\n<graphics count=\"0\"/>\n</attribute>\n<attribute name=\"Comment\" id=\"7038\" net=\"1\">\n<![CDATA[]]>\n<graphics count=\"0\"/>\n</attribute>\n"
        return startString + self.createSimpleColorSet(entityDefinition)