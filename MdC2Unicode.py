# -*- coding: utf-8 -*-

import pickle
import re

vStates = '+stlib'

dCommentStyles = { 'html': '<!-- %s -->', 'C': '//* %s *//', 'Python': '# %s' }

dMdCToUnicode = pickle.load( open( "data/MdC2Unicode.p", "rb" ) )
dPhoneticToGardiner = dMdCToUnicode['PhoneticToGardiner']
dGardinerToUnicodeHex = dMdCToUnicode['GardinerToUnicodeHex']
dAscii2Transliteration = { '!': 'H', '#': 'Ḫ', '$': 'H̲', '%': 'S', '&': 'T', '*': 'Ṯ', '+': 'Ḏ', '@': 'Ḥ', 'A': 'ꜣ', 'C': 'Ś', 'D': 'ḏ', 'H': 'ḥ', 'O': 'Q', 'Q': 'Ḳ', 'S': 'š', 'T': 'ṯ', 'V': 'h̭', 'X': 'ẖ', '\\': '𓏞', '^': 'Š', '_': 'D', 'a': 'ꜥ', 'c': 'ś', 'i': 'ỉ', 'o': 'q', 'q': 'ḳ', 'v': 'ṱ', 'x': 'ḫ' }

# Non-glyph elements in the MdC
dBrackets = { '[[': '[', ']]': ']', '[&': '〈', '&]': '〉', '["': '〚', '"]': '〛', '[\'': '⸂', '\']': '⸃', '[{': '{', '}]': '}', '[(': '(', ')]': ')', '[?': '⸢', '?]': '⸣' }
dSpecial = { '.': ' ', '..': '  ', 'o': '○', 'O': '●', '!': '\n', '!!': '\n\n', 'sic': 'sic' }
dArrows = { 'PF1': '←', 'PF2': '→', 'PF3': '↓', 'PF4': '↙︎', 'PF5': '↘︎' }
dShading = { '#b': '▧⭆', '#e': '⭅▨', 'v/': '▥', 'h/': '▤', '//': '▦', '/': '◍'  }
dCartouches = { '<h0': '<h0', '<h1': '<h1', '<h2': '<h2', '<h3': '<h3', 'h0>': 'h0>', 'h1>': 'h1>', 'h2>': 'h2>', 'h3>': 'h3>', '<s0': '<s0', '<s1': '<s1', '<s2': '<s2', '<s3': '<s3', 's0>': 's0>', 's1>': 's1>', 's2>': 's2>', 's3>': 's3>', '<0': '<0', '<1': '<1', '<2': '<2', '0>': '0>', '1>': '1>', '2>': '2>', '<S': '<S', '<H': '<H', '<': '<', '>': '>' }
dColors = { '$b': '', '$r': '' }
dNonGlyphLookup = { '[[': '[', ']]': ']', '[&': '〈', '&]': '〉', '["': '〚', '"]': '〛', '[\'': '⸂', '\']': '⸃', '[{': '{', '}]': '}', '[(': '(', ')]': ')', '[?': '⸢', '?]': '⸣',
                    '.': ' ', '..': '  ', 'o': '○', 'O': '●', '!': '\n', '!!': '\n\n', 'sic': 'sic',
                    'PF1': '←', 'PF2': '→', 'PF3': '↓', 'PF4': '↙︎', 'PF5': '↘︎',
                    '#b': '▧⭆', '#e': '⭅▨', 'v/': '▥', 'h/': '▤', '//': '▦', '/': '◍' ,
                    '<h0': '', '<h1': '', '<h2': '', '<h3': '', 'h0>': '', 'h1>': '', 'h2>': '', 'h3>': '', '<s0': '', '<s1': '', '<s2': '', '<s3': '', 's0>': '', 's1>': '', 's2>': '', 's3>': '', '<0': '', '<1': '', '<2': '', '0>': '', '1>': '', '2>': '', '<S': '', '<H': '', '<': '', '>': '',
                    '$b': '', '$r': '' }

# Sequences allowed in JSesh which do not map to single signs
dMissingGlyphs = { 'nTrw': 'R8-R8-R8', 'nn': 'M22-M22', '200': 'V1-V1', '30': 'V20-V20-V20', '300': 'V1-V1-V1', '4': 'Z1-Z1-Z1-Z1', '40': 'V20-V20-V20-V20' }

# Simple helper functions for debugging
def printList(l):
    if not isinstance(l,list):
        l = list(l)
    print(str(l).replace('), ', '),\n'))

def printspace(n=10):
    print('\n'*n)

# Sign list lookups
def luPhonetic2Gardiner(sMdC):
    if sMdC in dPhoneticToGardiner.keys():
        return dPhoneticToGardiner[sMdC]
    return ''

def luGardiner2UnicodeHex(sMdC):
    if sMdC in dGardinerToUnicodeHex.keys():
        return dGardinerToUnicodeHex[sMdC]
    return ''

def luPhonetic2Unicode(sMdC):
    
    sGardiner = luPhonetic2Gardiner(sMdC)
    if sGardiner:
        sHex = luGardiner2UnicodeHex(sGardiner)
    else:
        sHex = luGardiner2UnicodeHex(sMdC)
    
    if sHex:
        return chr(int(sHex,16))
    return None

def luNonGlyph(sMdC):
    if sMdC in dNonGlyphLookup.keys():
        return dNonGlyphLookup[sMdC]
    return None

def luMdC2Unicode(sMdC):
    
    # Have non matches return None to distinguish from an empty match string
    # Some non-glyphs should match an empty string and should not be included in the output
    # Unmatched glyphs should be included as sign codes
    s = luNonGlyph(sMdC)
    if s is None:
        s = luPhonetic2Unicode(sMdC)
    if s is None:
        return sMdC
    return s



def getTextStates(s):
    s = s+'+s'
    vTextStates = []
    iStart = 0
    sState = 's'
    for i, c in enumerate(s):
        if c == '+':
            if i and s[i-1] == '\\' or s[i-1] == '+':
                continue
            
            if i < len(s)-1 and s[i+1] in vStates:
                sContent = s[iStart:i]
                if sContent:
                    vTextStates.append((sState, sContent))
                
                iStart = i+2
                sState = s[i+1]
    
    return vTextStates

def getLineNumbers(s):
    vLineNumbers = []
    iStart = None
    iEnd = 0
    for i, c in enumerate(s):
        if c == '|':
            iStart = i
            # Don't keep an empty string
            if iStart > iEnd:
                t = (0, s[iEnd:iStart])
                vLineNumbers.append(t)
        elif c == '-' and iStart is not None:
            if i and not s[i-1] == '\\':
                iEnd = i
                t = (1, s[iStart+1:iEnd])
                iStart = None
                vLineNumbers.append(t)
    if iStart:
        t = (1, s[iStart:])
    else:
        t = (0, s[iEnd:])
    vLineNumbers.append(t)
    return vLineNumbers

def getSeparators(s):
    """This is where the MdC string is split up into control characters (separators)
    and Glyphs (Gardiner sign codes or phonetic sequences)"""
    
    vSeparators = []
    vSepChars = '-:*&^#'
    dPossible = { '-': ['-'], ':': [':'], '*': ['**', '*'], '#': ['##'], '&': ['&&&', '&'], '^': ['^^^']}
    n = len(s)
    iStart = None
    iEnd = 0
    i = -1
    while i < len(s)-1:
        i += 1
        c = s[i]
        if c in vSepChars:
            
            # Avoid the issue with the ambiguity of & in brackets: [& &]
            if c == '&':
                if i > 0 and s[i-1] == '[':
                    continue
                if i < n-1 and s[i+1] == ']':
                    continue
            
            for sPossible in dPossible[c]:
                k = len(sPossible)
                if not i+k > n:
                    if sPossible == ''.join([ s[j] for j in range(i,i+k) ]):
                        iStart = i
                        if iStart > iEnd:
                            t = (0, s[iEnd:iStart])
                            vSeparators.append(t)
                    
                        t = (1, sPossible)
                        vSeparators.append(t)
                        iEnd = i+k
                        i = i+k-1
                        break
    if iEnd < n:
        t = (0, s[iEnd:])
        vSeparators.append(t)
    return vSeparators

def parseParens(s, iDepth=0):
    v = []
    sCollector = ''
    n = len(s)
    i = -1
    while i < n-1:
        i += 1
        c = s[i]
        if c == '(':
            # Deal with the ambiguity with the brackets [( )]
            if i and s[i-1] == '[':
                sCollector += c
                continue
            
            if sCollector:
                v.append(sCollector)
            sCollector = ''
            vSub, iOffset = parseParens(s[i+1:], iDepth+1)
            # This check prevents an issue where, when the parentheses are not closed
            # the recursive function returns the initial value of i (-1), thus causing the loop to stick in place
            if len(vSub):
                i += iOffset
                v.append(vSub)
            
        elif c == ')':
            # Deal with the ambiguity with the brackets [( )]
            if i+1 < n and s[i+1] == ']':
                sCollector += c
                continue
            
            if sCollector:
                v.append(sCollector)
            
            # Deal with malformed inputs that begin a glyph section with a (
            if iDepth:
                return (v, i+1)
        else:
            sCollector += c
        
    if sCollector:
        v.append(sCollector)
    return (v, i)

def parseGlyph(sMdC):
    sMdC = sMdC.strip()
    
    vGlyphParts = []
    
    
    reNonGlyph = re.compile('^(' + re.escape( '•'.join(list(dNonGlyphLookup.keys())) ).replace('•','|') + ')')
    reGardiner = re.compile('^[A-Z][af]{0,1}\d+[A-Z]{0,1}')
    rePhonetic = re.compile('^[A-Za-z0-9]+')
    reGlyphAttributes = re.compile('((\\{\\{\\d+,\\d+,\\d+\\}\\})|(v)|(\\\\(([rt]\\d)|(R\\d+)|(\\d+)|(red)|(i)|(l)|(sic)){1})|(_+)|(#[1-4]+))')
    
    
    mGardiner = reGardiner.match(sMdC)
    mPhonetic = rePhonetic.match(sMdC)
    mNonGlyph = reNonGlyph.match(sMdC)
    if mGardiner:
        sGardiner = mGardiner[0]
        vGlyphParts.append((0, sGardiner))
        sMdC = reGardiner.sub('', sMdC)
    elif mPhonetic:
        sPhonetic = mPhonetic[0]
        vGlyphParts.append((0, sPhonetic))
        sMdC = rePhonetic.sub('', sMdC)
    elif mNonGlyph:
        sNonGlyph = mNonGlyph[0]
        vGlyphParts.append((0, sNonGlyph))
        sMdC = reNonGlyph.sub('', sMdC)
    
    iEnd = 0
    vMatches = reGlyphAttributes.finditer(sMdC)        
    for i, m in enumerate(vMatches):
        sPre = sMdC[iEnd:m.start()].strip()
        if sPre:
            vGlyphParts.append((2, sPre))
        iEnd = m.end()
        s = sMdC[m.start():iEnd].strip()
        if s:
            vGlyphParts.append((1, s))
    sPost = sMdC[iEnd:].strip()
    if sPost:
        vGlyphParts.append((2, sPost))
    
    # Deal with the stupid "grammar" attribute (=A1)
    if sMdC and sMdC[0] == '=':
        vGlyphParts[0] = (0, vGlyphParts[0][1][1:])
        vGlyphParts = [(1, '=')] + vGlyphParts
    
    return vGlyphParts
    
def parseNestedGlyphs(vMdC):
    vParsed = []
    for oMdC in vMdC:
        if isinstance(oMdC, list):
            v = parseNestedGlyphs(oMdC)
            vParsed.append((2, v))
        elif isinstance(oMdC, str):
            v = getSeparators(oMdC)
            for i, t in enumerate(v):
                if t[0] == 0:
                    v[i] = (0, parseGlyph(t[1]))
                    
            vParsed += v
    return vParsed

def matchNestedGlyphs(vMdC):
    for i, t in enumerate(vMdC):
        if t[0] == 0: # Glyph part lists
            vGlyph = []
            for tGlyphPart in t[1]:
                if tGlyphPart[0] == 0:      # A glyph, not an attr
                    sUnicode = luMdC2Unicode(tGlyphPart[1])
                    tGlyphPart = (tGlyphPart[0], tGlyphPart[1], sUnicode)
                vGlyph.append(tGlyphPart)
            vMdC[i] = (t[0], vGlyph)
        elif t[0] == 1: # Separator
            pass
        elif t[0] == 2: # Glyph sub list
            vMdC[i] = (t[0], matchNestedGlyphs(t[1]))
    return vMdC

def fixMissingGlyphs(sMdC):
    """ JSesh includes some shortcuts for sequences.
    These cannot be replaced until the formatting is known.
    This function separates the input, replaces the shortcuts with full forms
    and recomposes the MdC text to be processed again."""
    
    v = getSeparators(sMdC)
    vNew = []
    for i, t in enumerate(v):
        if t[0] == 0 and t[1] in dMissingGlyphs.keys():
            vNew.append( (0, '('+dMissingGlyphs[t[1]]+')') )
        else:
            vNew.append(t)
    
    sRecomp = ''
    for t in vNew:
        sRecomp += t[1]
    return sRecomp

def recomposeHieroglyphic(v, bUnicode=True, bFormatting=False):
    """ Reconstructs the original text or creates a Unicode version"""
    
    s = ''
    for tHiero in v:
        # Line numbers
        if tHiero[0] == 1:
            s += tHiero[1]
        # Glyphs
        elif tHiero[0] == 0:
            for t in tHiero[1]:
                if t[0] == 0:
                    for tGlyph in t[1]:
                        if tGlyph[0] == 0:
                            s += tGlyph[2 if bUnicode else 1]
                        elif tGlyph[0] == 1 and bFormatting:
                            s += tGlyph[1]
                elif t[0] == 1 and bFormatting:
                    s += t[1]
                elif t[0] == 2:
                    s += ('(' if bFormatting else '') \
                        + recomposeHieroglyphic(t[1], bUnicode, bFormatting) \
                        + (')' if bFormatting else '')
    return s

def parseMdC(sMdC):
    
    vParse = []
    
    vTextStates = getTextStates(sMdC)
    for tTextState in vTextStates:
        
        if tTextState[0] == 's':
            sHieroglyphs = tTextState[1]
            
            # Always have a separator for !\n or the first character in the next line will be deleted
            sHieroglyphs = re.sub(r'!\n([^\-])', r'!\n-\1', sHieroglyphs)
            
            vLineNumbers = getLineNumbers(sHieroglyphs)
            vParseHieroglyphic = []
            for tLineNumbers in vLineNumbers:
                if tLineNumbers[0] == 0:    # glyph section
                    # print(tLineNumbers[1])
                    sFixed = tLineNumbers[1]
                    sFixed = fixMissingGlyphs(sFixed)
                    
                    vGlyphParse, _ = parseParens(sFixed)
                    vGlyphParse = parseNestedGlyphs(vGlyphParse)
                    vGlyphParse = matchNestedGlyphs(vGlyphParse)
                    
                    vParseHieroglyphic.append((tLineNumbers[0], vGlyphParse))
                elif tLineNumbers[0] == 1:  # line number section
                    vParseHieroglyphic.append(tLineNumbers)
                
            vParse.append((tTextState[0], vParseHieroglyphic))
            
        else:  # All other states (comments, transliteration, latin text, etc...)
            vParse.append(tTextState)
    
    return vParse

def unicodeTransliteration(sAscii):
    """Convert ASCII transliteration into Unicode"""
    
    sUnicode = ''
    for i, c in enumerate(sAscii):
        if c in dAscii2Transliteration.keys():
            sUnicode += dAscii2Transliteration[c]
        else:
            sUnicode += c
    return sUnicode


def MdC2Unicode(sMdC, sCommentStyle = 'none', bKeepFormatting = False):
    vParse = parseMdC(sMdC)
    
    sUnicodeOut = ''
    for tParse in vParse:
        # Comment
        if tParse[0] == '+' and not sCommentStyle == 'none':
            sUnicodeOut += dCommentStyles[sCommentStyle] % tParse[1].strip() + '\n'
        # Hieroglyphic
        elif tParse[0] == 's':
            sUnicodeOut += recomposeHieroglyphic(tParse[1], True, bKeepFormatting)
        # Transliteration
        elif tParse[0] == 't':
            sUnicodeOut += convertTransliteration(tParse[1])
        # Latin, Italic, and Bold
        # TODO: Change the output for each one
        elif tParse[0] in 'lib':
            sUnicodeOut += tParse[1]
    
    # sUnicodeOut = re.sub(r'\n+', '\n', sUnicodeOut)
    return sUnicodeOut








