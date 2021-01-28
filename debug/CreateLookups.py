# -*- coding: utf-8 -*-

import re
import csv
import pickle

dGardinerToUnicodeHex = {}
csvfile = open('../data/GardinerToUnicode.csv', newline='\n')
reader = csv.DictReader(csvfile, delimiter='\t')
for row in reader:
    if row['GardinerSignCode']:
        dGardinerToUnicodeHex[row['GardinerSignCode']] = row['UnicodeHex']
csvfile.close()

dPhoneticToGardiner = {}
csvfile = open('../data/PhoneToGardiner_Unicode.csv', newline='\n')
reader = csv.DictReader(csvfile, delimiter='\t')
for row in reader:
    if row['FirstPhonetic']:
        dPhoneticToGardiner[row['FirstPhonetic']] = row['GardinerSignCode']
csvfile.close()


dMdCToUnicode = {   'GardinerToUnicodeHex': dGardinerToUnicodeHex,
                    'PhoneticToGardiner': dPhoneticToGardiner, }

pickle.dump( dMdCToUnicode, open( '../data/MdC2Unicode.p', 'wb' ) )


