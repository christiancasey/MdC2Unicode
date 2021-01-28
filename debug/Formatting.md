

## Font
 - [x] `++`    Comment
 - [x] `+s`    Hieroglyphic
 - [x] `+t`    Transliteration
 - [x] `+l`    Latin
 - [x] `+i`    Italic
 - [x] `+b`    Bold


# MdC Proper


## Line Numbers
 - [x] `|(*|\-)*-`    line number (dash in number escaped as \-)


## Philological Markup

### Brackets
 - [x] `[[...]]`    square brackets    [G]
 - [x] `[&...&]`    angle brackets    <G>
 - [x] `["..."]`    square doubled [|G|]
 - [x] `['...']`    upper ticks    'G'
 - [x] `[{...}]`    curly    {G}
 - [x] `[(...)]`    parentheses    (G)
 - [x] `[?...?]`    upper half brackets    'G'

dBrackets = { '[[': '[', ']]': ']', '[&': '〈', '&]': '〉', '["': '〚', '"]': '〛', '[\'': '⸂', '\']': '⸃', '[{': '{', '}]': '}', '[(': '(', ')]': ')', '[?': '⸢', '?]': '⸣' }

(\[[\[\{\(\?&"']|[\]\}\)\?&"']\])
(\[[\[\{\(\?&"']|[\]\}\)\?&"']\])|(&{3}|\^{3}|\*{1,2}|#{2}|[\-:])

### Cartouches
 - [x] `<-G->`    normal    (G)|
 - [x] `<1-G-2>`    normal    (G)|
 - [x] `<0-G-2>`    normal with open start    G)|
 - [x] `<1-G-0>`    normal with open finish    (G
 - [x] `<1-G-1>`    no flat line    (G)
 - [x] `<2-G-2>`    flat lines on both ends    |(G)|
 - [x] `<S-G->`    serekh (with hatching at end)
 - [x] `<s1-G-s2>`    serekh (with hatching at end)
 - [x] `<s1-G-s3>`    serekh with normal start and tight finish
 - [x] `<s0-G-s3>`    serekh open on front end and tight finish    G]
 - [x] `<H-G->`    𓉗 sign around glyphs with box at far end
 - [x] `<h1-G-h2>`    𓉗 box on bottom at far end    [G_] [Gd
 - [x] `<h1-G-h3>`    𓉗 box on top at far end    [Gº] [Gq
 - [x] `<h0-G-h1>`    𓉗 box open on front end

'<s0', '<0', '<1', '<2', 

vCartouches = ['<h0', '<h1', '<h2', '<h3', 'h0>', 'h1>', 'h2>', 'h3>', '<s0', '<s1', '<s2', '<s3', 's0>', 's1>', 's2>', 's3>', '<0', '<1', '<2', '0>', '1>', '2>', '<S', '<H', '<', '>']

((\[[\[\{\(\?&"']|[\]\}\)\?&"']\])|([^\[&]|^)&([^\]&]|$))
((&{3}|\^{3}|\*{1,2}|#{2}|[\-:])|([^\[&]|^)&([^\]&]|$))

'-:*&^#'
** &&& ^^^ ##
 ## Separators
 - [x] `-`    simple side-by-side
 - [x] `:`    on top of
 - [x] `*`    join together    p*t:pt
 - [x] `**`    join-exactly positioned glyphs    `G{{,,}}**G{{,,}}`
 - [x] `&`    fit inside larger sign    D&d
 - [x] `&&&`    join group inside    D&&&(t:tA)
 - [x] `^^^`    stack on top of arm shape    p^^^D40
 - [x] `##`    superimpose    Hwt##D



# Full Glyph Characters

## Special Glyphs

- [x] `.`    single-width space
- [x] `..`    double-width space
- [x] `o`    red circle
- [x] `O`    black circle
- [x] `!`    new line
- [x] `!!`    page break (horizontal divider)
- [x] `sic`    sic

dSpecial = { '.': ' ', '..': '  ', 'o': '○', 'O': '●', '!': '\\n', '!!': '\\n\\n', 'sic': 'sic' }
### Arrows

- [x] `PF1`    left ←
- [x] `PF2`    right →
- [x] `PF3`    down ↓
- [x] `PF4`    left-down ┤ ↙︎
- [x] `PF5`    right-down ├ ↘︎

dArrows = { 'PF1': '←', 'PF2': '→', 'PF3': '↓', 'PF4': '↙︎', 'PF5': '↘︎' }

### Space Hatching
 - [x] `#b`    begin hatching
 - [x] `#e`    end hatching
 - [x] `v/`    vertical hatching
 - [x] `h/`    horizontal hatching
 - [x] `/`    small hatching
 - [x] `//`    full cadrat hatching

dShading = { '#b': '▧⭆', '#e': '⭅▨', 'v/': '▥', 'h/': '▤', '//': '▦', '/': '◍'  }

### Color
 - [x] `$r`    begin red
 - [x] `$b`    begin black

vColor = ['$b', '$r']

# Sub-Glyph Markup


- [x] `()`    group set of glyphs


## Positioning

### Precise
 - [x] `G{{x,y,z}}` ** G{{12,23,34}}    exact position

### Rotations
 - [x] `G\`    flip sign horizontal
 - [x] `G\r1-3`    rotate (\R270 - \R90)
 - [x] `G\t1-3`    flip and rotate (\\R270 - \\R90)
 - [x] `G\R123`    rotate by degrees
 - [x] `Gv`    rotate by 270 degrees (≈ `G\R270`)


### Zoom (Relative)
 - [x] `G\120`    scale 120% relative to other signs in group    n\120:h*A

### Color
 - [x] `G\red`    make the previous glyph red
 - [x] `G\i`    ignored sign

## Other
 - [x] `G_`    sign at end of word
 - [x] `G__`    sign at end of sentence
 - [x] `=G`    "grammar"
 - [x] `G\l`    make the group long
 - [x] `G\sic`    unknown


## Glyph Hatching
 - [x] `G#13`    left vertical hatching
 - [x] `G#24`    right vertical hatching
 - [x] `G#12`    top half hatching
 - [x] `G#34`    bottom half hatching
 - [x] `G#n`    (1=top-left,2=top-right,3=bottom-left,4=bottom-right)









