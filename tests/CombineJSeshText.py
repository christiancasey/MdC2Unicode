# -*- coding: utf-8 -*-

import os
import glob
import re

vFilesGly = glob.glob("JSeshTexts/a.gly")
vFilesHie = glob.glob("JSeshTexts/*.hie")
vFiles = vFilesGly + vFilesHie
vFiles.sort()

sAll = ''
for sFile in vFiles:
    
    with open(sFile,'rb') as f:
        sText = f.read()#.decode('utf-8')#.decode('latin-1')
        try:
            sText = sText.decode('utf-8')
        except:
            sText = sText.decode('latin-1')
        
        sText = sText.strip()
        
        sTextSep = '++' + '~'*75 + '+s'
        sTitleSep = '++' + '-'*75 + '+s'
        
        _, sFile = os.path.split(sFile)
        print(sFile)
        
        sAll = "%s%s\n++ File: %s\t\t+s\n%s\n-!\n%s\n-!\n-!\n" % (sAll, sTextSep, sFile, sTitleSep, sText)

# sAll = re.sub(r'!([^\n])', r'!\n\1', sAll)

f = open('JSeshAll.txt','w')
f.write(sAll)
f.close()