# -*- coding: utf-8 -*-

import sys
import os

from MdC2Unicode import *
# import MdC2Unicode



if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        raise Exception('Please specify a file to convert.')
    if len(sys.argv) >= 2:
        sFileIn = sys.argv[1]
    if len(sys.argv) >= 3:
        sFileOut = sys.argv[2]
    else:
        sRoot, sExt = os.path.splitext(sFileIn)
        sFileOut = sRoot + '_Unicode' + sExt

    with open(sFileIn,'r') as f:
        s = f.read()
        f.close()
        s = s.strip()
    
    sOut = MdC2Unicode(s, 'html')
    
    f = open(sFileOut, 'w')
    f.write(sOut)
    f.close()
    
