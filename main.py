import xml.etree.ElementTree as ET
from nltk import download
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import urllib

#Only uncomment this for first time run!!!
#download('all')

dup = {
    "Gregory Campbell",
    "Jeffrey Donaldson",
    "Nigel Doggs",
    "Paul Girvan",
    "Andrew Hunter",
    "Carla Lockhart",
    "William McCrea",
    "Johnny McQuade",
    "Ian Paisley",
    "Ian Paisley Jr",
    "Emma Pengelly",
    "Gavin Robinson",
    "Iris Robinson",
    "Peter Robinson",
    "Jim Shannon",
    "David Simpson",
    "Sammy Wilson"
}

sdlp = {
    "Gerry Fitt",
    "John Hume",
    "Seamus Mallon",
    "Eddie McGrady",
    "Joe Hendron",
    "Mark Durkan",
    "Alasdair, McDonnell",
    "Margaret Ritchie",
    "Colum Eastwood",
    "Claire Hanna"
}

left_ind = {
    'Peter Law',
    'Dai Davies',
    'George Galloway',
    'Richard Taylor',
    'Martin Bell',
    'Dick Taverne',
    'S.O. Davies',
    'John MacLeod'
}

right_ind = {
    'Douglas Carswell',
    'Mark Reckless',
    'David Robertson'
}

green = {
    "Caroline Lucas"
}

pc = {
    "Dafydd Wigley",
    "Elfyn Llwyd",
    "Hywel Williams",
    "Dafydd Elis-Thomas",
    "Ieuan Wyn Jones",
    "Jonathon Edwards",
    "Adam Price",
    "Gwynfor Evans",
    "Cynog Dafis",
    "Simon Thomas",
    "Liz Saville Roberts",
    "Ben Lake"
}


def get_mps(party):
    memset = set()
    page = BeautifulSoup(open(party+'.html', 'r'))
    for name in page.find_all('a'):
        test = str(name.get('title'))
        #if '(' not in test:
            #print(name.get('title'))
        memset.add(str(name.get('title')))
    return memset


def gen_tokens(xml, left, right, nat):
    root = ET.parse(xml).getroot()
    memlist = []
    speechlist = []
    x = 0
    finallist = []
    for child in root:
        for contents in child.iter('housecommons'):
            for debates in contents.iter('debates'):
                for debate in debates.iter('section'):
                    for speech in debate.iter('p'):
                        for member in speech.iter('member'):
                            name = member.text.replace("Mr.", "")
                            name = name.replace("Mrs.", "")
                            name = name.replace("Ms.", "")
                            name = name.replace("Dr.", "")
                            name = name.replace("Sir", "")
                            name = name.replace("Dame", "")
                            name = name.replace("Lord", "")
                            name = name.replace("Lady.", "")
                            memlist.append(name.lstrip())
                            #print(name.lstrip())
                            # try:
                            #     memlist.append(str(member.text).split('. ')[1])
                            # except IndexError:
                            #     x = x + 1
                            #     #print(member.text)
                            #     memlist.append(str(member.text))
                        for contribution in speech.iter('membercontribution'):
                            if contribution.text is not None:
                                formatted = contribution.text[1:]
                                formatted = word_tokenize(formatted)
                            else:
                                formatted = None #Dummy Var
                            speechlist.append(formatted)
    print(len(memlist))
    print(len(speechlist))
    length = min(len(memlist), len(speechlist))
    c = 0
    for i in range(0, length):
        if speechlist[i] is not None:
            party = ''
            #print(memlist[i])
            if any(memlist[i] in s for s in left):
                party = 'left'
            elif any(memlist[i] in s for s in right):
                party = 'right'
            elif any(memlist[i] in s for s in nat):
                party = 'nat'
            elif "The" in  memlist[i]:
                party = 'right'
            elif "Speaker" in memlist[i]:
                party = 'speaker'
            else:
                print(memlist[i])
                party = 'ERROR'
                c += 1
            #print(i)
            finallist.append([party, speechlist[i]])
            #print(memlist[i])
    print(c, len(finallist))
    return speechlist

right = set().union(get_mps('con'), get_mps('uup'), get_mps('dup'), get_mps('natlib'), )
left = set().union(get_mps('lab'), get_mps('lib'), get_mps('libdem'), green, sdlp)
nat = set().union(get_mps('snp'), pc, get_mps('nat'))
#print(len(right), len(left), len(nat))
tokens = gen_tokens('thefile.xml', left, right, nat)
print("Oonagh" in left)
