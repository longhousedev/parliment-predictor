import xml.etree.ElementTree as ET
from nltk import download
from nltk.tokenize import word_tokenize

#Only uncomment this for first time run!!!
#download('all')


def gen_tokens(xml):
    root = ET.parse(xml).getroot()
    memlist = []
    speechlist = []
    speechdict = {}
    memdict = {}
    for child in root:
        for contents in child.iter('housecommons'):
            for debates in contents.iter('debates'):
                for debate in debates.iter('section'):
                    for speech in debate.iter('p'):
                        for member in speech.iter('member'):
                            memlist.append(member.text)
                        for contribution in speech.iter('membercontribution'):
                            if contribution.text is not None:
                                formatted = contribution.text[1:]
                                formatted = word_tokenize(formatted)
                            else:
                                formatted = None #Dummy Var
                            speechlist.append(formatted)
    length = min(len(memlist), len(speechlist))
    for i in range(0, length):
        if speechlist[i] is not None:
            speechdict[memlist[i]] = speechlist[i]
            print (memlist[i], speechdict[memlist[i]])
    return speechlist

tokens = gen_tokens('thefile.xml')
