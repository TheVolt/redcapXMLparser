# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 08:37:54 2019

to parse xml redcap files into data dictionaries....

@author: cabxr
"""

# import libraries
import os
import csv
import xml.etree.ElementTree as ET

# set working directory
os.chdir('directory_path')

# check working diretory
print(os.getcwd())

# parse xml files
docTree = ET.parse("file.xml")

# get root items from xml
root = docTree.getroot()

# check if xml read
if (docTree):
    print("file loaded")
else:
    print("file not loaded")

# open a csv file for writing
xml_data = open('file.csv', 'w', encoding='utf-8')

# create csv writer object
csvwriter = csv.writer(xml_data, lineterminator='\n')

# create csv row headings
xml_head = []

xml_head.append("Variable / Field Name")
xml_head.append("Form Name")
#xml_head.append("Section Header")
xml_head.append("Field Type")
xml_head.append("Field Label")
xml_head.append("Choices, Calculations, OR Slider Labels")
#xml_head.append("Field Note")
#xml_head.append("Text Validation Type OR Show Slider")
#xml_head.append("Number")
#xml_head.append("Text Validation Min")
#xml_head.append("Text Validation Max")
#xml_head.append("Identifier?")
#xml_head.append("Branching Logic (Show field only if...")
#xml_head.append("Required Field?")
#xml_head.append("Custom Alignment")
#xml_head.append("Question Number (surveys only")
#xml_head.append("Matrix Group Name")
csvwriter.writerow(xml_head)


# iterate through roots
for member in root.findall('.//{http://www.cdisc.org/ns/odm/v1.3}ItemDef'):
    # create an empty list for variables information
    xml_variables = []
    
    var=member.attrib['Name']
    xml_variables.append(var)
    
    formName='formname'
    xml_variables.append(formName)
    
    fieldType=member.attrib['{https://projectredcap.org}FieldType']
    if fieldType == 'select':
        xml_variables.append('dropdown')
    else:
        xml_variables.append(fieldType)
    
    fieldLabel=member.find('.//{http://www.cdisc.org/ns/odm/v1.3}TranslatedText').text
    xml_variables.append(fieldLabel)
    
    codelist=member.find('.//{http://www.cdisc.org/ns/odm/v1.3}CodeListRef')
    if codelist == None:
        choices = ''
    else:
        choicesCode = codelist.attrib['CodeListOID']
        choicesStr = './/*[@OID=' + "'" + choicesCode + "'" + ']'
        #print(choicesStr)
        
        choices = []
        
        for options in root.findall(choicesStr):
            for items in options.findall('.//{http://www.cdisc.org/ns/odm/v1.3}CodeListItem'):
                codeVal = items.attrib['CodedValue']
                codeText = items.find('.//{http://www.cdisc.org/ns/odm/v1.3}TranslatedText').text
                itemText = codeVal + ', ' + codeText
                
                choices.append(itemText)
                
    choiceVals = ' | '.join(choices)
    xml_variables.append(choiceVals)
    
    csvwriter.writerow(xml_variables)

xml_data.close()
