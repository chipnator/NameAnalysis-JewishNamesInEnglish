# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:10:52 2015

@author: chipnator
"""
import io
import operator

def openFileGetText(inFName,encode=""):
    """Open text file, return string"""
    if encode=="utf-8":
        inFile=io.open(inFName,"r",encoding="utf-8")
    elif encode=="ascii":
        inFile=io.open(inFName,"r",encoding="ascii")
    else:
        inFile=io.open(inFName,"r")
    inData=inFile.read()
    inFile.close()
    return inData
    
def makeGoodTextList(inItem):
    """Clean the input of bad characters, handels str and list input"""
    if type(inItem)==type([]):
        retL=[]
        for itr in range(len(inItem)):
            tempS=""
            for ch in inItem[itr]:
                if ch.isalpha() or ch==" ":
                    tempS+=ch
            retL.append(tempS.rstrip().lstrip())
        return retL
    else:
        try:
            tempS=""
            for ch in inItem:
                if ch.isalpha() or ch==" ":
                    tempS+=ch
            inItem=tempS
        except:
            for ch in "<>!&{}[] \n \r () \\ \" \' \/ \| ?&:.~@!$%^*;=+-_,#1234567890":
                inItem=inItem.replace(ch," ")
        return inItem.split()   
    
def getDataFromText(inFName):
    """input file name, filter testL for words that are not names, 
    outputs names without caps"""
    text=openFileGetText(inFName,encode="utf-8")
    textLu=makeGoodTextList(text)
    textL = []
    for word in textLu:
        try:
            # common exceptoon: character that can't be converted to ascii
            textL.append(word.encode('ascii'))
        except:
            pass
    nameL=[word.lower() for word in textL if word.isupper() and len(word)>1]
    return nameL
        
def getCommonEndings(inList,printRev=False):
    """for each possible substring in each name with length greather than 3,
    count it's occurance throughout the entire list of names, return dictionary
    with substrings and their occurances"""
    nameD=dict()
    for name in inList:
        for itr in range(len(name)-1):
            ending=name[-1*itr:len(name)]
            if len(ending)>3:
                if not ending in nameD.keys():
                    nameD[ending]=1
                else:
                    nameD[ending]=nameD[ending]+1
    return nameD       

def printNameData(endingD,printType=3):
    """an attractive print method for dictionaries with multiple display options"""
    print "\n"+"~"*20+"\nBases of Jewish Names\n"+"~"*20
    if printType==1:
        for (key,val) in endingD:
            print "Ending: "+key+" Occurances: "+val
    if printType==2:
        procD=dict()
        for key,val in endingD:
            # procD[key+" ~ "+str(val)]=len(key)
            procD[key]=len(key)
            #if val>1:
            #    print "Ending: "+key+" Value: "+str(val)+" Length: "+str(len(key))
        print "~"*20
        procD=reversed(sorted(procD.items(), key=operator.itemgetter(1)))
        counter=0
        for key,val in procD: #procD for order by length
            counter+=1
            if counter%2==0:
                print key+" ~ "+str(val)
            else:
                #print "| ", #looks good when sorted by length
                print key+" ~ "+str(val)+" |",
    if printType==3:
            counter=0
            for key,val in endingD:
                counter+=1
                temstr=key+" ~ "+str(val)
                if counter%4==0:
                    print temstr
                else:
                    if len(temstr)>12:
                        print temstr+"\t",
                    else:
                        print temstr+"\t\t",          
    print "~"*20+"\n"
    
def getEnglish():
    #get dictionary 
    dicDoc=open("UKACD17.TXT","r")
    dicL=list(dicDoc)
    dicDoc.close()
    return dicL
    
def compare(endingD,englishDictL):
    print "\n"+"~"*20+"\nComparing ending dictionary with list of English",
    print "words, Names, and common phrases\n"+"~"*20
    for key, val in endingD:
        if len(key)>3 and val>=3:
            print key+" ~ "+str(val)
            for eWord in englishDictL:
                if key in eWord.lower() and eWord[0].isupper():
                    print "\t"+eWord
    
def main():
    print "~"*20+"\n"
    print "Common bases within Jewish names are found via analysis of html of",
    print "a webpage with common Jewish names. Those bases are then compared",
    print "to a list of English words, Names, and common phrases to see the", 
    print "relative commonality between 'typical' English names/words and",
    print "names that are distinctly Jewish. I created this program to",
    print "satisfy my curiosity about how common words/names with Jewish",
    print "bases are within the English language. The goal and purpose of",
    print "this program has subsequently become to demonstrate my",
    print "capabilities as a python programmer."
    nameL=getDataFromText("Behind the Name_ Jewish Surnames.html")
    endingD=getCommonEndings(nameL)
    endingD=sorted(endingD.items(), key=operator.itemgetter(1))
    # nameD=reversed(nameD) #Print in reverse numerical order
    printNameData(endingD,printType=3)
    raw_input("Hit Enter/Return")
    englishDictL=makeGoodTextList(getEnglish())
    #testWordItr=randrange(len(englishDictL))
    #print englishDictL[testWordItr:testWordItr+randrange(5,10)]
    compare(endingD,englishDictL)

main()