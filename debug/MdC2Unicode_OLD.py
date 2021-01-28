# -*- coding: utf-8 -*-

import re
import pickle

dMdCToUnicode = pickle.load( open( "data/MdCToUnicode.p", "rb" ) )
dGardinerToUnicodeHex = dMdCToUnicode['GardinerToUnicodeHex']
dPhoneticToGardiner = dMdCToUnicode['PhoneticToGardiner']
dParseRegex = dMdCToUnicode['ParseRegex']
vPreprocess = dMdCToUnicode['Preprocess']


def dotMult(v, a):
    return [a*x for x in v]

def markParts(vParts, vPartMatch, reNewPart, iNewPart=0):
    vPartsNew = []
    vPartMatchNew = []
    
    # fix default part value if necessary
    if not iNewPart:
        iNewPart = max(vPartMatch)+1
    
    for i in range(len(vParts)):
        if vPartMatch[i] > 0:
            vPartsNew.append(vParts[i])
            vPartMatchNew.append(vPartMatch[i])
        else:
            vSubParts, vSubPartMatch = markPart(vParts[i], reNewPart, iNewPart)
            for j in range(len(vSubParts)):
                vPartsNew.append(vSubParts[j])
                vPartMatchNew.append(vSubPartMatch[j])
    return (vPartsNew, vPartMatchNew)

def markPart(sText, rePart, iPart):
    
    iMinStringLength = -100
    
    vParts = []
    vPartMatch = []
    
    vStart = [ m.start() for m in rePart.finditer(sText) ]
    vEnd = [ m.end() for m in rePart.finditer(sText) ]
    
    # Deal with no matches by returning the string and a zero match
    if not len(vStart):
        vParts = [ sText ]
        vPartMatch = [0]
    else:
        for i in range(len(vStart)):
                        
            # Add the beginning of the string
            if i == 0 and vStart[0] > 0:
                vParts.append(sText[0:vStart[0]])
                vPartMatch.append(0)
            # Add the previous non-matched area
            elif vStart[i] > vEnd[i-1]:
                vParts.append(sText[vEnd[i-1]:vStart[i]])
                vPartMatch.append(0)
            
            # Add the match
            if vEnd[i] > vStart[i]:
                vParts.append(sText[vStart[i]:vEnd[i]])
                vPartMatch.append(iPart)
            
            # Add the remains if this is the final matched group
            if i == len(vStart)-1 and vEnd[i] < len(sText):
                vParts.append(sText[vEnd[i]:])
                vPartMatch.append(0)
    
    return (vParts, vPartMatch)


def printMarked(vParts, vPartMatch, vPartColors):
    return
    sOut = ''
    for i in range(len(vParts)):
        sOut += ('\x1b[%sm%s\x1b[0m' % (vPartColors[vPartMatch[i]], vParts[i]))
    print(sOut)

def printMarkedHTML(vParts, vPartMatch, vPartColorsHTML):
    sOut = ''
    for i in range(len(vParts)):
        sOut += ('<font color="%s">%s</font>' % (vPartColorsHTML[vPartMatch[i]], vParts[i]))
    return sOut


def cleanUp(sText):
    sText = re.sub(r'\n+', r'\n', sText)
    return sText

def getSignCodeParts(sSignCode):
    reSignCodeParts = re.compile('([A-Z][a-z]{0,1})(\d+)([A-Z]*)')
    vSignCodeParts = reSignCodeParts.findall(sSignCode)
    if len(vSignCodeParts) > 0:
        return vSignCodeParts[0]

    return None


def markTextHeaders(sText):
    reHeaderLine = re.compile('\+\+(.*?)\+s(\-{0,1})')
    vHeaders = reHeaderLine.findall(sText)
    for tHeader in vHeaders:
        sHeader = '++%s+s%s' % tHeader
        # sHeaderMarked = '\n<meta>%s</meta>\n' % tHeader[0].strip()
        sHeaderMarked = '\n<meta>%s</meta>\n' % ''#tHeader[0].strip()
        sText = sText.replace(sHeader, sHeaderMarked)
    return sText

def markLineNumbers(sText):
    reFeature = re.compile('\|([^\-]+)\-')
    vMatches = reFeature.findall(sText)
    for tMatch in vMatches:
        sOriginal = '|%s-' % tMatch
        sMarked = '\n<line-number>%s</line-number>\n' % tMatch.strip()
        sMarked = '\n<line-number>%s</line-number>\n' % ''#tMatch.strip()
        sText = sText.replace(sOriginal, sMarked)
    return sText

def markOtherText(sText):
    reFeature = re.compile('\+([tlib])([^\+]*)')
    vMatches = reFeature.findall(sText)
    for tMatch in vMatches:
        sOriginal = '+%s%s' % tMatch
        # sMarked = '\n<text type="%s">%s</text>\n' % tMatch
        sMarked = '\n<text type="%s">%s</text>\n' % (tMatch[0],'')
        sText = sText.replace(sOriginal, sMarked)
    return sText

    

print('\n'*100)
sFile = 'JSeshTexts/PNorthumberland1.gly'
sFile = 'JSeshAll.txt'

s = ''
with open(sFile,'r') as f:
    s = f.read()
    f.close()
# s = s[:min(len(s),100000)]
# s += '           \n+s-!\n'

# Run preprocessing
for tFR in vPreprocess:
    s = s.replace(tFR[0],tFR[1])


vParts = [s]
vPartMatch = [0]

for iPart, sRegex in enumerate(dParseRegex):
    vParts, vPartMatch = markParts(vParts, vPartMatch, dParseRegex[sRegex], iPart+1)



vPartColors = []
for i in range(56):
    vPartColors.append('%i;%i;40' % (int(i/7), i%7+31))


print('\n'*10)
printMarked(vParts, vPartMatch, vPartColors)


iPhonetic = list(dParseRegex.keys()).index('Phonetic')+1
iGardiner = list(dParseRegex.keys()).index('Gardiner')+1

sPhoneticExtra = set()  # Keep track of sequences that don't match
for i in range(len(vParts)):
    if vPartMatch[i] == iPhonetic:
        sPhonetic = vParts[i]
        if sPhonetic in dPhoneticToGardiner.keys():
            vParts[i] = dPhoneticToGardiner[sPhonetic]
            vPartMatch[i] = iGardiner
        else:
            sPhoneticExtra.add(vParts[i])

print('\n'*10)
printMarked(vParts, vPartMatch, vPartColors)

sGardinerExtra = set()
iUnicodeHex = max(vPartMatch)+2
for i in range(len(vParts)):
    if vPartMatch[i] == iGardiner:
        sGardiner = vParts[i]
        if sGardiner in dGardinerToUnicodeHex.keys():
            vParts[i] = chr(int(dGardinerToUnicodeHex[sGardiner], 16))
            vPartMatch[i] = iUnicodeHex
        else:
            sGardinerExtra.add(vParts[i])

print('\n'*10)
printMarked(vParts, vPartMatch, vPartColors)


iSpecial = list(dParseRegex.keys()).index('Special')+1
sUnicodeText = ''
for i in range(len(vParts)):
    if vPartMatch[i] >= iSpecial:
        if vPartMatch[i] == iPhonetic:
            sUnicodeText += '<' + vParts[i] + '>'
        elif vPartMatch[i] == iGardiner:
            sUnicodeText += '[' + vParts[i] + ']'
        else:
            sUnicodeText += vParts[i]

sUnicodeText = sUnicodeText.replace('!', '\n')
sUnicodeText = sUnicodeText.replace('.', ' ')
f = open('JSeshAll_Unicode.txt','w')
f.write(sUnicodeText)
f.close()

# print('\n'*10)
# print(sUnicodeText)
# 
# vPartColorsHTML = ['Red', 'White', 'Cyan', 'Silver', 'Blue', 'Gray', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive', 'Red', 'White', 'Blue', 'Gray', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive']
# sHtml = printMarkedHTML(vParts, vPartMatch, vPartColorsHTML)
# sHtml = sHtml.replace('!\n', '\n<br>\n')
# sHtml = sHtml.replace('\n', '\n<br>\n')
# sHtml = sHtml.replace('!', '!\n<br>\n')
# f = open('JSeshAll.html','w')
# f.write(sHtml)
# f.close()


bDebug = False
if bDebug:
    # Output all remaining unmatched sequences
    vPhoneticExtra = list(sPhoneticExtra)
    vPhoneticExtra.sort()
    print('\n'*3)
    print('Phonetic sequences not found:')
    for sPhoneticExtra in vPhoneticExtra:
        print(sPhoneticExtra)

    vGardinerExtra = list(sGardinerExtra)
    vGardinerExtra.sort()
    print('\n'*3)
    print('Sign code sequences not found:')
    for sGardinerExtra in vGardinerExtra:
        print(sGardinerExtra)

