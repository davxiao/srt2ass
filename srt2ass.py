#!user/bin/env python
#-*- coding:utf-8 -*-
'''
convert .srt to .ass 

David Xiao
Oct 18, 2014
'''

import sys
 
def coded(str):
    try:
        try:
            try:
                try:
                    try:
                        ans=str.decode('gb2312')
                    except:
                        ans=str.decode('gbk')
                except:
                    ans=str.decode('cp936')
            except:
                ans=str.decode('utf-8')
        except:
            ans=str.decode('big5')
    except:
        ans=None
    return ans
 
def main(name):
    import re
    extract=re.compile('\d+\s+([0-9:,]+)\s--?>\s([0-9:,]+)\s+(.*?)\r?\n(.*?)\r?\n')
    gettime=re.compile('(\d+):(\d+):(\d+),(\d+)')
    def trs(tim):
        i,j,k,t=[int(x) for x in gettime.match(tim).groups()]
        t=t/10+1 if t%10>=5 else t/10
        if t>99:
            k,t=k+1,0
        if k>59:
            j,k=j+1,0
        if j>59:
            i,j=i+1,0
        return (i,j,k,t)
         
    with open(name,'rb') as file:
        data=coded(file.read())
        if not data:return
        sub=extract.findall(data)
        n1,n2,n3,n4=sub.pop(0)
        merge=[(trs(n1),trs(n2),n3,n4)]
        for n1,n2,n3,n4 in sub:
            p1,p2,p3,p4=merge[-1]
            n1,n2=trs(n1),trs(n2)
            if p3==n3:
                if p2[0]==n1[0] and p2[1]==n1[1] and p2[2]==n1[2]:
                    if n1[3]-p2[3]<=5:
                        merge[-1]=(p1,n2,p3,p4)
                        continue
            merge.append((n1,n2,n3,n4))
    lst=name.split('.')
    lst[-1]='ass'
    name='.'.join(lst)
    with open(name,'w') as file:
        file.write('''[Script Info]
;
;
Title:
Original Script:
Synch Point:0
ScriptType:v4.00+
Collisions:Normal
Timer:100.0000
 
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,方正黑体_GBK,18,&H00FFFFFF,&HF0000000,&H00000000,&H32000000,0,0,0,0,100,100,0,0.00,1,2,1,2,5,5,2,134

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
'''
        )
        for n1,n2,n3,n4 in merge:
            n1='%d:%02d:%02d.%02d'%n1
            n2='%d:%02d:%02d.%02d'%n2
            line='Dialogue: 0,%s,%s,*Default,NTP,0,0,0,,%s'%(n1,n2,n3)
            file.write(line.encode('utf-8'))
            if n4:
                file.write('''\N{\\fn微软雅黑}{\\b0}{\\fs14}{\\3c&H202020&}{\\shad1}''')
                file.write(n4.encode('utf-8'))
            file.write('\n')

if __name__=='__main__':
    if len(sys.argv)>1:
        for name in sys.argv[1:]:
            main(name)
    else:
        print('Usage: %s [file1] [file2] [file3]...'%sys.argv[0])



