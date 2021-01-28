
import re



def dotMult(v, a):
    return [a*x for x in v]


def markParts(s, r):
    
    vParts = []
    vPartMatch = []
    
    vStart = [ m.start() for m in r.finditer(s) ]
    vEnd = [ m.end() for m in r.finditer(s) ]

    for i in range(len(vStart)):
        
        # Add the beginning of the string
        if i == 0:
            # Don't add an empty string
            if vStart[0] > 0:
                sI = s[0:vStart[0]]
                vParts.append(sI)
                vPartMatch.append(0)
                # print(sI)
        
        # Add the previous non-matched area
        else:
            sI = s[vEnd[i-1]:vStart[i]]
            vParts.append(sI)
            vPartMatch.append(0)
            # print(' '*vEnd[i-1] + sI)
        
        # Add the match
        sI = s[vStart[i]:vEnd[i]]
        vParts.append(sI)
        vPartMatch.append(1)
        # print(' '*vStart[i] + sI)
        
        # Add the remains
        if i == len(vStart)-1:
            # Don't add an empty string
            if vEnd[i] < len(s):
                sI = s[vEnd[i]:]
                vParts.append(sI)
                vPartMatch.append(0)
                # print(' '*vEnd[i] + sI)
    
    return (vParts, vPartMatch)


s = '|1,x+2-t*Z7:r-km-m-t:niwt#12-A1:(d*t)+lTesting +s-#b-a:n-D55-i-#e-!'
# r = re.compile('(\w+[\-\:\&\*])')
# r = re.compile('#b.*?#e')
# r = re.compile('\([^\)]*\)')
r = re.compile('((\+)([stlib]))')
# a = r.finditer(s)
# for b in a:
#     print(b.groups())

print('\n'*100)
print(s)


vParts, vPartMatch = markParts(s, r)

print('\n'*10)
print(vParts)
print(dotMult(vPartMatch,999))

a = r.finditer(s)
# iStart = 0
for b in a:
    
    print(b.start())
    
    # dir_b = dir(b)
    # dir_b.sort()
    # print(dir_b)
    # print('\n'*4)
    # 
    # for c in dir_b:
    #     print('~~~~')
    #     if not c[0] == '_':
    #         print(c)
    #         d = getattr(b,c)
    #         if callable(d):
    #             try:
    #                 print('fn ' + c)
    #                 print(d())
    #             except:
    #                 pass
    #         else:
    #             print(d)
    



























