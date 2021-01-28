# -*- coding: utf-8 -*-

from MdCUnicodeFunctions import *


def parseLineNumbers(sMdC):
    sMdC = sMdC.strip()
    reLineNumbers = re.compile('\\|(?:\\\\\\-|[^\\-])*')
    vLineNumbers = []
    iEnd = 0
    vMatches = reLineNumbers.finditer(sMdC)
    for m in vMatches:
        sPre = sMdC[iEnd:m.start()].strip()
        if sPre:
            vLineNumbers.append((0, sPre))
        
        iEnd = m.end()
        sLN = sMdC[m.start():iEnd].strip()
        sLN = sLN[1:]       # Remove leading |
        if sLN:
            vLineNumbers.append((1, sLN))
    sPost = sMdC[iEnd:].strip()
    if sPost:
        vLineNumbers.append((0, sPost))
    return vLineNumbers

def parseSeparators(sMdC):
    sMdC = sMdC.strip()
    # reSeparators = re.compile('((&{3}|\\^{3}|\\*{1,2}|#{2}|[\\-:])|([^\\[&]|^)&([^\\]&]|$))')
    # TODO: Handle parens properly
    # reSeparators = re.compile('([\(\)]|(&{3}|\\^{3}|\\*{1,2}|#{2}|[\\-:])|([^\\[&]|^)&([^\\]&]|$))')
    sMdC = sMdC.replace('&&&', '¶¶¶')
    sMdC = sMdC.replace('[&', '[£')
    sMdC = sMdC.replace('&]', '£]')
    sMdC = sMdC.replace('[(', '[«')
    sMdC = sMdC.replace(')]', '»]')
    # reSeparators = re.compile('(\\n|[\(\)]|(¶{3}|\\^{3}|\\*{1,2}|#{2}|[\\-:])|(^|[^\\[&])&|()&([^\\]&]|$))')
    reSeparators = re.compile('((\\n)|([\(\)])|(¶{3})|(\\^{3})|(\\*{1,2})|(#{2})|([\\-:])|(&+))')
    vSeparators = []
    iEnd = 0
    vMatches = reSeparators.finditer(sMdC)
    for m in vMatches:        
        iStart = m.start()
        sPre = sMdC[iEnd:iStart].strip()
        if sPre:
            vSeparators.append((0, sPre))
        
        iEnd = m.end()
        sMatch = sMdC[iStart:iEnd].strip()
        if sMatch:
            vSeparators.append((2, sMatch))
        
    sPost = sMdC[iEnd:].strip()
    if sPost:
        vSeparators.append((0, sPost))
    
    return vSeparators

def parseNonGlyphs(t):
    sSpecial = '(\\.{1,2}|!{1,2}|([oO])|sic)'
    sArrows = '(PF[1-5])'
    sShading = '(#[be])'
    sRotate = '([vh]{0,1}/{1,2})'
    sColors = '(\\$[rb])'
    sCartouche = '(<(([0-2SH]|([sh][0-3])){0,1})|(([0-2]|([sh][0-3])){0,1})>)'
    sBrackets = '(\\[[\\[\\{\\(\\?&"\']|[\\]\\}\\)\\?&"\']\\])'
    sTogether = '^(' + sSpecial + '|' \
                + sArrows + '|' \
                + sShading + '|' \
                + sRotate + '|' \
                + sColors + '|' \
                + sCartouche + '|' \
                + sBrackets + ')$'
    reNonGlyphs = re.compile(sTogether)
    reNonGlyphs = re.compile('asdfasdf')
    if reNonGlyphs.match(t[1]):
        t = (3, t[1])
    return t

def parseGlyph(sMdC):
    
    reGlyphAttributes = re.compile('(\\{\\{\\d+,\\d+,\\d+\\}\\}|v|\\\\(([rt]\\d)|R\\d+|\\d+|red|i|l|sic){0,1}|(_+)|(#[1-4]+))+$')
    
    vGlyphParts = []
    iEnd = 0
    vMatches = reGlyphAttributes.finditer(sMdC)
    for m in vMatches:
        sPre = sMdC[iEnd:m.start()].strip()
        if sPre:
            vGlyphParts.append((0, sPre))
        iEnd = m.end()
        s = sMdC[m.start():iEnd].strip()
        if s:
            vGlyphParts.append((4, s))
    sPost = sMdC[iEnd:].strip()
    if sPost:
        vGlyphParts.append((0, sPost))
    
    # Deal with the stupid "grammar" attribute (=A1)
    if sMdC and sMdC[0] == '=':
        vGlyphParts[0] = (0, vGlyphParts[0][1][1:])
        vGlyphParts = [(4, '=')] + vGlyphParts
    
    return vGlyphParts

def parseHieroglyphic(sMdC):
    sMdC = sMdC.strip()
    
    vMdCParse = []
    
    vLineNumbers = parseLineNumbers(sMdC)
    for tLineNumber in vLineNumbers:
        if tLineNumber[0] == 0:     # Not yet marked, so not a line number
            
            vSeparators = parseSeparators(tLineNumber[1])
            
            # Mark non-glyph characters
            for i in range(len(vSeparators)):
                if vSeparators[i][0] == 0:
                    vSeparators[i] = parseNonGlyphs(vSeparators[i])
            
            # Parse the individual glyphs themselves
            vGlyphs = []
            for i in range(len(vSeparators)):
                if vSeparators[i][0] == 0:
                    vGlyphs += parseGlyph(vSeparators[i][1])
                else:
                    vGlyphs.append(vSeparators[i])
            
            vMdCParse += vGlyphs
        else:
            vMdCParse.append(tLineNumber)
    
    for i in range(len(vMdCParse)):
        if not vMdCParse[i][0]:
            sOriginal = vMdCParse[i][1]
            dGlyphEncodings = { 'Original': sOriginal, 'Phonetic': '', 'Gardiner': '', 'UnicodeHex': '', 'UnicodeDec': None, 'Unicode': '' }
            
            if sOriginal in dPhoneticToGardiner.keys():
                dGlyphEncodings['Phonetic'] = sOriginal
                sGardiner = dPhoneticToGardiner[sOriginal]
                dGlyphEncodings['Gardiner'] = sGardiner
            else:
                sGardiner = sOriginal
            
            if sGardiner in dGardinerToUnicodeHex.keys():
                dGlyphEncodings['Gardiner'] = sGardiner
                dGlyphEncodings['UnicodeHex'] = dGardinerToUnicodeHex[sGardiner]
                dGlyphEncodings['UnicodeDec'] = int(dGlyphEncodings['UnicodeHex'], 16)
                dGlyphEncodings['Unicode'] = chr(dGlyphEncodings['UnicodeDec'])
            
            vMdCParse[i] = (5, dGlyphEncodings)
    
    return vMdCParse



if __name__ == '__main__':
    
    
    printspace(100)
    s = "+s-|6-nwn-|7-n:f-!A-|8-sw-t:nf-|9-Hr:w-A40-|10-=A1__\\120\\R270\\red\\l\\sic\\i#124-((p:t-p)-((o:o)*1):t):pt-Q3*t:pt+s"""
    s = "++asdfasdfasdf+sb:n_-n:f_:mw_-n:Sd_&&&(d:t*W_)-n:s*anx__-nTrw-(A1-A1)-nn-300-!+s"
    
    v = procMdC(s)
                    
    printspace(3)
    print(s)
    print(recomposeHieroglyphic(v,False,True))
    print(recomposeHieroglyphic(v,False,False))
    print(recomposeHieroglyphic(v,True,True))
    print(recomposeHieroglyphic(v,True,False))


if __name__ == 'asf':#'__main__':
    dMdCToUnicode = pickle.load( open( "data/MdCToUnicode.p", "rb" ) )
    dGardinerToUnicodeHex = dMdCToUnicode['GardinerToUnicodeHex']
    dPhoneticToGardiner = dMdCToUnicode['PhoneticToGardiner']

    print('\n'*100)
    sFile = 'JSeshTexts/PNorthumberland1.gly'
    sFile = 'JSeshAll.txt'

    s = ''
    with open(sFile,'r') as f:
        s = f.read()
        f.close()
    # s = s[:500]
    # s = '+s-' + s + '-!'
    s = s.strip()

    vTextStateCodes = ' +stlib'
    vTextStateLabels = ['unknown_state', 'comment', 'hieroglyphic', 'transliteration', 'latin', 'italic', 'bold']

    reTextStates = re.compile('\\+[\\+stlib](?:\\\\\\+|[^\\+])*')
    vStatesMatches = reTextStates.findall(s)
    vStates = []
    for i, sStateMatch in enumerate(vStatesMatches):
        iState = vTextStateCodes.index(sStateMatch[1])
        sStateMatch = sStateMatch[2:].strip()
        if sStateMatch:
            vStates.append((iState, sStateMatch))
            print('%i\t%s' % (iState, sStateMatch.replace('\n','•')))


    sLeftOvers = reTextStates.sub('', s)
    print('%i Leftovers: %s' % (len(sLeftOvers),sLeftOvers))


    ## Start processing the Hieroglyphic sections
    vMdCParseLabels = [ 'unknown_MdC', 'line_number', 'separator', 'non-glyph_character', 'glyph_attributes', 'glyph' ]


    import pyperclip
    vAll = []
    print('\n'*100)
    iHieroglyphic = vTextStateLabels.index('hieroglyphic')
    for tState in vStates:
        vTextStateLabels[tState[0]]
        if tState[0] == iHieroglyphic:
            vMdCParse = parseHieroglyphic(tState[1])
            # vAll += vMdCParse
            vAll.append((iHieroglyphic, vMdCParse))
            # print(vMdCParse)
        else:
            vAll.append(tState)

    sXML = ''
    for tState in vAll:
        sStateLabel = vTextStateLabels[tState[0]]
        if tState[0] == iHieroglyphic:
            sContent = ''
            iGlyph = vMdCParseLabels.index('glyph')
            for tParse in tState[1]:
                sParseLabel = vMdCParseLabels[tParse[0]]
                sStatus = 'not-parsed'
                if tParse[0] == iGlyph:
                    sParseContent = tParse[1]['Unicode']
                    if sParseContent:
                        sStatus = 'parsed'
                    else:
                        sParseContent = tParse[1]['Original']
                    sXMLParse = '<span class="%s %s">%s</span>' % (sParseLabel, sStatus, sParseContent)
                else:
                    sParseContent = tParse[1]
                    sXMLParse = '<span class="%s">%s</span>' % (sParseLabel, sParseContent)
                    # sXMLParse = ''
                
                sContent += sXMLParse
        else:
            sContent = str(tState[1])
        sXMLState = '<div class="%s">%s</div>\n' % (sStateLabel, sContent)
        sXML += sXMLState

    pyperclip.copy(sXML)

    sHTML = sXML
    sHTML = sHTML.replace('<span class="non-glyph_character">!</span>', '<span class="non-glyph_character">!</span><br>')
    sStyle = """<html><head><style>
                body { background-color: #101010; }
                .not-parsed { color: red; }
                .parsed { color: blue; }
                .line_number { color: lightblue; }
                .separator { color: orange; }
                .non-glyph_character { color: green; }
                .glyph_attributes { color: teal; }
                .bold { color: white; font-weight: bold; }
                .italic { color: white; font-style: italic; }
                .latin { color: white; }
                .transliteration { color: grey; font-style: italic;}
                .comment { color: gray; }
                </style></head><body>"""
    f = open('JSeshAll.html', 'w')
    f.write(sStyle + sHTML + '</body></html>')
    f.close()








