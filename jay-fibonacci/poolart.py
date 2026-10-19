import random, math
R = random.Random(42)
out = []
def add(s): out.append(s)
def col(c, j=10):
    r,g,b = [int(c[i:i+2],16) for i in (1,3,5)]
    d = R.randint(-j,j)
    f = lambda v: max(0,min(255,v+d+R.randint(-2,2)))
    return '#%02x%02x%02x' % (f(r),f(g),f(b))
def poly(pts, fill, stroke='#2b2b2b', sw=1.2, op=1):
    add('<path d="M%s Z" fill="%s" stroke="%s" stroke-width="%s" opacity="%s"/>' % (' L'.join('%.1f %.1f'%p for p in pts), fill, stroke, sw, op))
def line(x1,y1,x2,y2,c,w=1,op=1):
    add('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%s" opacity="%s" stroke-linecap="round"/>'%(x1,y1,x2,y2,c,w,op))
def hatch(pts_fn, n, c, w, ln, ang, op=.6):
    for _ in range(n):
        x,y = pts_fn()
        a = math.radians(ang + R.uniform(-12,12)); l = R.uniform(ln*.6, ln)
        line(x,y,x+l*math.cos(a),y+l*math.sin(a),col(c,14),w,op)

GREENS = ['#1f5e25','#2e7d32','#3f9a3a','#5bb146','#7fc65a','#a6d97a']
def foliage(cx, cy, rx, ry, n=220, light=(-.5,-.6), base='#3f9a3a', outline=True):
    # base blob
    pts=[]
    for i in range(28):
        t=2*math.pi*i/28; rr=1+R.uniform(-.12,.12)
        pts.append((cx+rx*rr*math.cos(t), cy+ry*rr*math.sin(t)))
    poly(pts, base, '#1d4a1f' if outline else 'none', 1.1 if outline else 0, .95)
    for _ in range(n):
        t=R.uniform(0,2*math.pi); r=math.sqrt(R.random())
        x=cx+rx*r*math.cos(t)*.95; y=cy+ry*r*math.sin(t)*.95
        d=( (x-cx)/rx*light[0] + (y-cy)/ry*light[1] )  # >0 lit
        k = 2 + d*2.2 + R.uniform(-1,1)
        c = GREENS[max(0,min(5,int(round(k))))]
        a=R.uniform(0,2*math.pi); l=R.uniform(3,6)
        add('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round" opacity=".9"/>'%(x,y,l*math.cos(a)/2-2,l*math.sin(a)/2-2,l*math.cos(a),l*math.sin(a),c,R.uniform(1.4,2.4)))

def conifer(x, base, h, w):
    pts=[(x,base-h)]
    steps=9
    for i in range(1,steps+1):
        yy=base-h+h*i/steps; ww=w*(i/steps)**.85
        pts.append((x+ww+R.uniform(-2,2), yy-3)); pts.append((x+ww*.8, yy))
    right=pts[:]
    left=[(2*x-px,py) for px,py in reversed(right[1:])]
    poly(right+left, '#2e6f2f', '#173d1a', 1.2)
    for _ in range(int(h*w/8)):
        yy=R.uniform(base-h+4, base-2); frac=(yy-(base-h))/h; ww=w*frac**.85*.9
        xx=R.uniform(x-ww, x+ww); side=(xx-x)/max(ww,1)
        c = GREENS[2 if side<-.2 else (0 if side>.3 else 1)]
        line(xx,yy,xx+R.uniform(-3,3)-2*side,yy+R.uniform(3,6),c,1.4,.85)

# ---------- sky-ish blank, back hedges/trees ----------
for (cx,cy,rx,ry) in [(130,46,40,26),(205,40,34,24),(275,44,38,26),(350,40,36,24),(420,46,34,22)]:
    foliage(cx,cy,rx,ry,160)
conifer(34,120,104,22); conifer(78,118,84,18); conifer(462,118,86,18); conifer(506,122,108,24)

# ---------- timber fence ----------
FX0,FX1,FT,FB=40,500,58,124
x=FX0
while x<FX1:
    w=11; c=col('#c9925f',16)
    poly([(x,FT+R.uniform(-1,1)),(x+w,FT+R.uniform(-1,1)),(x+w,FB),(x,FB)], c, '#7a4a28', .9)
    for _ in range(3):
        gx=x+R.uniform(2,w-2); line(gx,FT+3,gx+R.uniform(-1,1),FB-3,col('#9b6436',10),.7,.6)
    x+=w
poly([(FX0-2,FT-4),(FX1+2,FT-4),(FX1+2,FT+1),(FX0-2,FT+1)],'#a8713f','#6b3f1e',1)
hatch(lambda:(R.uniform(FX0,FX1),R.uniform(FB-18,FB-2)),140,'#7a4a28',1,8,-60,.35)

# ---------- garden bed along fence ----------
for cx in range(70,420,34):
    foliage(cx+R.uniform(-6,6),118,24,14,70)
for (fx,fy) in [(110,112),(180,108),(300,110),(372,112)]:
    for i in range(7):
        a=math.radians(-150+i*20); line(fx,fy+8,fx+16*math.cos(a),fy+8+16*math.sin(a),'#2f7a27',1.6,.9)
for _ in range(26):
    x=R.uniform(70,420); y=R.uniform(104,124)
    add('<circle cx="%.1f" cy="%.1f" r="2" fill="%s" stroke="#7a2a50" stroke-width=".5"/>'%(x,y,R.choice(['#f2a7c3','#ffffff','#f6d04d'])))

# ---------- perspective concrete surround ----------
BY,FY=126,252
def P(u,v):
    v2=v**1.25
    bx=58+424*u; fx=-24+588*u
    return (bx+(fx-bx)*v2, BY+(FY-BY)*v2)
NU,NV=14,7
PU0,PU1,PV0,PV1=0.26,0.74,0.18,0.70
for i in range(NU):
    for j in range(NV):
        u0,u1=i/NU,(i+1)/NU; v0,v1=j/NV,(j+1)/NV
        uc,vc=(u0+u1)/2,(v0+v1)/2
        if PU0<uc<PU1 and PV0<vc<PV1: continue
        pts=[P(u0,v0),P(u1,v0),P(u1,v1),P(u0,v1)]
        poly(pts, col('#d9d4cb',10), '#8f897f', .8)
        x0=min(p[0] for p in pts); x1=max(p[0] for p in pts); y0=pts[0][1]; y1=pts[2][1]
        hatch(lambda:(R.uniform(x0,x1),R.uniform(y0,y1)),int((x1-x0)*(y1-y0)/60),'#b9b2a7',.8,7,-25,.45)
# pergola shadow on paving
poly([P(.80,.0),P(1.0,.0),P(1.0,.32),P(.84,.32)],'#000000','none',0,.08)

# ---------- pool coping + water ----------
cop=[P(PU0,PV0),P(PU1,PV0),P(PU1,PV1),P(PU0,PV1)]
poly(cop,'#f3f1ec','#5f5a52',1.6)
for k in range(1,9):
    u=PU0+(PU1-PU0)*k/9
    line(*P(u,PV0),*P(u,PV0+.035),'#a7a198',.7); line(*P(u,PV1-.04),*P(u,PV1),'#a7a198',.7)
inset=.028
wpts=[P(PU0+inset,PV0+.035),P(PU1-inset,PV0+.035),P(PU1-inset,PV1-.04),P(PU0+inset,PV1-.04)]
add('<defs><linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f79c4"/><stop offset=".55" stop-color="#36a3e6"/><stop offset="1" stop-color="#6fcdf4"/></linearGradient></defs>')
poly(wpts,'url(#wg)','#14507f',1.6)
# inner wall shadow strip
poly([wpts[0],wpts[1],(wpts[1][0]-3,wpts[1][1]+9),(wpts[0][0]+3,wpts[0][1]+9)],'#0e4e86','none',0,.45)
wx0=min(p[0] for p in wpts)+10; wx1=max(p[0] for p in wpts)-10; wy0=wpts[0][1]+12; wy1=wpts[2][1]-4
for _ in range(70):
    x=R.uniform(wx0,wx1); y=R.uniform(wy0,wy1)
    add('<path d="M%.1f %.1f q4 -3 8 0 t8 0" stroke="%s" stroke-width="%.1f" fill="none" opacity=".75" stroke-linecap="round"/>'%(x,y,R.choice(['#ffffff','#bfeaff','#9fdcff']),R.uniform(1,1.8)))
hatch(lambda:(R.uniform(wx0,wx1),R.uniform(wy0,wy1)),120,'#1a6fb6',1,9,-20,.35)
# pool steps (back right)
sx,sy=P(PU1-.07,PV0+.04)
for k in range(3):
    line(sx+k*3,sy+4+k*6,sx+30-k*2,sy+4+k*6,'#e8f7ff',1.4,.8)

# ---------- pergola + dining ----------
def post(x,yb,h):
    poly([(x,yb-h),(x+7,yb-h),(x+7,yb),(x,yb)],'#b07a46','#5c3517',1)
    line(x+2,yb-h+2,x+2,yb-2,'#d29a62',1,.7); line(x+5.5,yb-h+2,x+5.5,yb-2,'#7a4a24',1,.7)
post(410,170,112); post(508,166,110); post(436,140,86); post(530,138,84)
poly([(400,62),(538,50),(540,58),(402,70)],'#a86f3c','#5c3517',1.2)
poly([(426,52),(540,44),(540,50),(428,58)],'#a86f3c','#5c3517',1)
for k in range(9):
    x=404+k*16; line(x,44-k*.6,x+4,70-k*1.2,'#7a4a24',3.2)
# table & chairs
poly([(448,134),(500,132),(506,140),(444,142)],'#5a4a3c','#2b2b2b',1)
line(452,142,452,160,'#2b2b2b',1.6); line(498,140,500,158,'#2b2b2b',1.6)
for (cx,cy) in [(436,138),(458,146),(486,145),(512,136)]:
    poly([(cx,cy-16),(cx+12,cy-16),(cx+12,cy),(cx,cy)],'#3c3c3c','#1f1f1f',1,.95)
    poly([(cx-1,cy),(cx+13,cy),(cx+13,cy+3),(cx-1,cy+3)],'#d8cfc0','#1f1f1f',.8)
    line(cx,cy+3,cx,cy+14,'#1f1f1f',1.4); line(cx+12,cy+3,cx+12,cy+14,'#1f1f1f',1.4)
# string lights
add('<path d="M410 74 Q448 92 474 80 T538 64" stroke="#333" stroke-width=".9" fill="none"/>')
for k in range(8):
    t=k/7; x=410+128*t; y=74+14*math.sin(math.pi*t*1.3)-10*t
    add('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#ffd54a" stroke="#b8860b" stroke-width=".6"/><circle cx="%.1f" cy="%.1f" r="6" fill="#ffe38a" opacity=".25"/>'%(x,y+4,x,y+4))

# ---------- loungers on left ----------
for (lx,ly) in [(44,176),(78,196)]:
    poly([(lx,ly),(lx+44,ly-2),(lx+52,ly-16),(lx+46,ly-18),(lx+38,ly-6),(lx,ly-5)],'#f4f2ee','#3a3a3a',1.1)
    poly([(lx+3,ly-5),(lx+37,ly-6),(lx+37,ly-2),(lx+3,ly-1)],'#7cc04a','#2f6b23',.8)
    poly([(lx+41,ly-8),(lx+48,ly-15),(lx+50,ly-12),(lx+43,ly-5)],'#7cc04a','#2f6b23',.8)
    line(lx+2,ly,lx+2,ly+8,'#3a3a3a',1.4); line(lx+42,ly-1,lx+42,ly+7,'#3a3a3a',1.4)
    poly([(lx+2,ly+8),(lx+46,ly+6),(lx+46,ly+9),(lx+2,ly+11)],'#000','none',0,.12)

# ---------- stone planters front corners ----------
def stones(x0,y0,x1,y1):
    poly([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],'#bdb6aa','#4d4840',1.4)
    y=y0+2
    while y<y1-2:
        h=R.uniform(7,10); x=x0+R.uniform(-6,0)
        while x<x1-2:
            w=R.uniform(10,18); xa=max(x,x0+1); xb=min(x+w,x1-1)
            if xb-xa>3: poly([(xa+.8,y+.8),(xb-.8,y+.8),(xb-.8,min(y+h,y1-1)-.8),(xa+.8,min(y+h,y1-1)-.8)],col('#c9c2b6',18),'#6b655c',.7)
            x+=w
        y+=h
    poly([(x0-3,y0-5),(x1+3,y0-5),(x1+3,y0+1),(x0-3,y0+1)],'#e2ddd3','#4d4840',1.1)
    hatch(lambda:(R.uniform(x0+(x1-x0)*.55,x1),R.uniform(y0,y1)),40,'#5d574e',1,6,-60,.35)
stones(-4,206,48,262); stones(486,198,544,256)
foliage(18,186,34,24,170,base='#3a8c35')
for _ in range(14):
    x=R.uniform(-4,44); y=R.uniform(170,200)
    for k in range(5):
        a=2*math.pi*k/5; add('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#ffffff" stroke="#c9c9c9" stroke-width=".5"/>'%(x+3*math.cos(a),y+3*math.sin(a)))
for i in range(11):
    a=math.radians(-170+i*16); L=R.uniform(26,36)
    add('<path d="M515 200 q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="3" fill="none" stroke-linecap="round"/>'%(L*.5*math.cos(a)-4,L*.5*math.sin(a)-6,L*math.cos(a),L*math.sin(a),R.choice(GREENS[1:4])))

# ---------- lawn front ----------
add('<path d="M-10 252 L564 252 L564 285 L-10 285 Z" fill="#9bd77a" opacity=".55"/>')
for _ in range(900):
    x=R.uniform(-8,548); y=R.uniform(250,288)
    l=R.uniform(6,13); a=math.radians(-90+R.uniform(-25,25))
    line(x,y,x+l*math.cos(a),y+l*math.sin(a),R.choice(['#2e8b35','#3fa53c','#58bb45','#7ccf5a','#1f6e28']),R.uniform(.9,1.6),.85)

# ---------- garden lights ----------
for (gx,gy) in [(470,250),(60,250)]:
    line(gx,gy,gx,gy-14,'#2b2b2b',2); poly([(gx-4,gy-14),(gx+4,gy-14),(gx+3,gy-19),(gx-3,gy-19)],'#2b2b2b','#111',.8)

print('<svg class="art" viewBox="0 0 540 285" fill="none" stroke-linejoin="round"><g filter="url(#rough)">' + ''.join(out) + '</g></svg>')
