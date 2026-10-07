# Cole Gordan 3-5 word captions, per spec PARTS 3-4.
import json,sys,math,re
words_all=json.load(open('words.json'))
W,H=1920,1080
FIX={'5day':'5 day','[snorts]':'','50':'15','swap':'swept'}
PHRASE_FIX=[]
def correct(w):
    k=w.lower()
    return FIX.get(k,w)
def build(clipStart,clipEnd,out,speed=1.0):
    dur=(clipEnd-clipStart)/speed
    ws=[{'w':correct(x['w']).replace('&','and').replace('{','').replace('}','').strip(),'s':(x['s']-clipStart)/speed}
        for x in words_all if clipStart<=x['s']<=clipEnd]
    ws=[x for x in ws if x['w']]
    # phrase fixes (sequence-level ASR repairs)
    for a,b in PHRASE_FIX:
        a_=a.split(); b_=b.split()
        i=0
        while i<=len(ws)-len(a_):
            if [re.sub(r'[^a-z0-9]','',x['w'].lower()) for x in ws[i:i+len(a_)]]==a_:
                times=[x['s'] for x in ws[i:i+len(a_)]]
                new=[{'w':t,'s':times[min(k,len(times)-1)] if k<len(times) else times[-1]} for k,t in enumerate(b_)]
                # keep trailing punctuation of last original word
                tail=re.sub(r'.*?([.,!?]*)$',r'\1',ws[i+len(a_)-1]['w']); new[-1]['w']+=tail
                ws[i:i+len(a_)]=new; i+=len(b_)
            else: i+=1
    n=len(ws)
    def endOf(i):
        return ws[i+1]['s'] if (i+1<n and ws[i+1]['s']-ws[i]['s']<0.7) else min(ws[i]['s']+0.35,dur)
    MAXW,MAXC=6,48
    blocks=[];cur=[]
    for i in range(n):
        if cur and (len(cur)>=MAXW or len(' '.join(ws[j]['w'] for j in cur+[i]))>MAXC):
            blocks.append(cur);cur=[]
        cur.append(i)
        pause=(ws[i+1]['s']-ws[i]['s']) if i+1<n else 99
        if (len(cur)>=2 and pause>0.4) or re.search(r'[.!?]$',ws[i]['w']):
            blocks.append(cur);cur=[]
    if cur: blocks.append(cur)
    k=len(blocks)-1
    while k>0:
        b=blocks[k]
        if len(b)==1 and len(' '.join(ws[j]['w'] for j in blocks[k-1]+b))<=MAXC:
            blocks[k-1]+=b; del blocks[k]
        k-=1
    def sizes(L):
        if L<=5: return [L]
        m=math.ceil(L/5);base=L//m;rem=L%m
        return [base+1]*rem+[base]*(m-rem)
    def ts(t):
        t=max(0,t);cs=int(round(t*100));h=cs//360000;m=cs//6000%60;s=cs//100%60;c=cs%100
        return f"{h}:{m:02d}:{s:02d}.{c:02d}"
    ev=[]
    for bi,b in enumerate(blocks):
        pos=0;chs=[]
        for sz in sizes(len(b)): chs.append(b[pos:pos+sz]);pos+=sz
        for ci,ch in enumerate(chs):
            st=ws[ch[0]]['s']
            if ci+1<len(chs): en=ws[chs[ci+1][0]]['s']
            else:
                en=max(st+0.1,endOf(ch[-1]))+0.30
                if bi+1<len(blocks):
                    ns=ws[blocks[bi+1][0]]['s']
                    if ns-en<0.40: en=ns
                    en=min(en,ns) if ns>st else en
            en=min(en,dur)
            text=' '.join(ws[j]['w'] for j in b[:b.index(ch[-1])+1])
            ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},WH,,0,0,0,,{text}")
    fs=round(H*0.0806);sh=round(3*H/720,1);ml=round(W*0.11);mv=round(H*0.097)
    hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WH,{sys.argv[1] if len(sys.argv)>1 else 'Inter Medium'},{fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,88,100,0,0,1,0,{sh:g},2,{ml},{ml},{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open(out,'w').write(hdr+'\n'.join(ev)+'\n')
    return len(ws),len(ev),dur
