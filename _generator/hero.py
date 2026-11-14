from common import *
import random
random.seed(11)

W, H = 1000, 440
defs = f'''
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#070A14"/><stop offset=".7" stop-color="#0E1530"/><stop offset="1" stop-color="#1A1730"/>
</linearGradient>
<radialGradient id="lamp" cx=".78" cy="1" r=".7"><stop offset="0" stop-color="{SAFF}" stop-opacity=".22"/><stop offset="1" stop-color="{SAFF}" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="{MOON}" stop-opacity=".35"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></radialGradient>
<path id="ring" d="M190,212 m-118,0 a118,118 0 1,1 236,0 a118,118 0 1,1 -236,0"/>
<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F2F4F7"/><stop offset=".28" stop-color="#9AA1AD"/><stop offset=".5" stop-color="#E4E7EC"/><stop offset=".72" stop-color="#6C7380"/><stop offset="1" stop-color="#C9CED6"/></linearGradient>
<linearGradient id="chrome2" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#7D8491"/><stop offset="1" stop-color="#E3E6EB"/></linearGradient>
<linearGradient id="side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3B414D"/><stop offset=".5" stop-color="#8E95A2"/><stop offset="1" stop-color="#4A505C"/></linearGradient>
<radialGradient id="face" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#FBF7EC"/><stop offset=".75" stop-color="#EFE7D3"/><stop offset="1" stop-color="#CFC5AE"/></radialGradient>
<radialGradient id="glass" cx=".5" cy=".5" r=".5"><stop offset=".8" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<clipPath id="flip"><rect x="0" y="0" width="1000" height="440" rx="20"/></clipPath>
'''
style = f'''
.tw{{animation:tw 3s ease-in-out infinite}} @keyframes spin{{to{{transform:rotate(360deg)}}}} @keyframes orb{{to{{stroke-dashoffset:-234}}}} @keyframes tw{{50%{{opacity:.15}}}}
.ringt{{transform-box:view-box;transform-origin:190px 212px;animation:rr 40s linear infinite}} @keyframes rr{{to{{transform:rotate(-360deg)}}}}
.drop{{animation:drop 12s cubic-bezier(.3,1.4,.5,1) infinite both}}
@keyframes drop{{0%{{transform:translateY(-120px);opacity:0}}6%{{transform:none;opacity:1}}92%{{transform:none;opacity:1}}100%{{transform:none;opacity:0}}}}
.bub{{animation:bub 2.4s ease-in infinite}} @keyframes bub{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:.9}}100%{{transform:translateY(-46px);opacity:0}}}}
.dig{{animation:dig 9s steps(1) infinite}} @keyframes dig{{0%{{transform:translateY(0)}}33.3%{{transform:translateY(-70px)}}66.6%{{transform:translateY(-140px)}}}}
.flap{{transform-box:fill-box;transform-origin:bottom;animation:flap 3s ease-in infinite}}
@keyframes flap{{0%,88%{{transform:scaleY(0)}}94%{{transform:scaleY(1)}}100%{{transform:scaleY(0)}}}}
.colon{{animation:col 1s steps(1) infinite}} @keyframes col{{50%{{opacity:.15}}}}
.cnt{{animation:cnt 12s steps(1) infinite}}
@keyframes cnt{{0%{{transform:translateY(0)}}8%{{transform:translateY(-16px)}}16%{{transform:translateY(-32px)}}24%{{transform:translateY(-48px)}}32%{{transform:translateY(-64px)}}40%,100%{{transform:translateY(-80px)}}}}
.cur{{animation:col 1s steps(1) infinite}}
'''
b = [f'<g clip-path="url(#flip)">', f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
# stars
for i in range(70):
    x, y = random.uniform(0, W), random.uniform(0, 300)
    r = random.choice([.6, .8, 1, 1.3])
    b.append(f'<circle class="tw" style="animation-delay:{random.uniform(0,3):.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" fill-opacity=".7"/>')
# moon drifting along an arc
b.append(f'<g><circle r="46" fill="url(#moonglow)"/><circle r="17" fill="{MOON}"/><circle cx="6" cy="-4" r="15" fill="#0B1022"/>'
         f'<animateMotion dur="60s" repeatCount="indefinite" path="M780,96 Q870,26 965,70"/></g>')
b.append(f'<rect width="{W}" height="{H}" fill="url(#lamp)"/>')
# desk
b.append(f'<rect x="0" y="372" width="{W}" height="68" fill="#0C1122"/><line x1="0" y1="372" x2="{W}" y2="372" stroke="{SAFF}" stroke-opacity=".35"/>')
# ---- orbiting chrome wall-clock (roman dial, blueprint gears, two orbit rings)
cx, cy = 186, 206
SERIF = "Georgia,'Times New Roman',Times,serif"
def gear(gx, gy, ro, ri, n, hole):
    pts = []
    for k in range(n*4):
        a = 2*math.pi*k/(n*4)
        rr = ro if k % 4 in (1, 2) else ri
        pts.append(f"{gx + rr*math.cos(a):.1f},{gy + rr*math.sin(a):.1f}")
    return f'M{" L".join(pts)}Z M{gx+hole},{gy} a{hole},{hole} 0 1,0 {-2*hole},0 a{hole},{hole} 0 1,0 {2*hole},0'
# blueprint layer: big tick dial + slowly turning gears
bp = [f'<circle cx="{cx}" cy="{cy}" r="172" fill="none" stroke="{SAFF}" stroke-opacity=".14"/>',
      f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{SAFF}" stroke-opacity=".08" stroke-dasharray="2 5"/>']
for i in range(120):
    a = math.radians(i*3); L = 10 if i % 10 == 0 else 4
    bp.append(f'<line x1="{cx+172*math.sin(a):.1f}" y1="{cy-172*math.cos(a):.1f}" x2="{cx+(172-L)*math.sin(a):.1f}" y2="{cy-(172-L)*math.cos(a):.1f}" stroke="{SAFF}" stroke-opacity="{.35 if L>4 else .15}"/>')
b.append('<g>' + "".join(bp) + '</g>')
for gx, gy, ro, ri, n, hole, dur, op in [(70, 330, 46, 38, 14, 12, 30, .16), (318, 92, 34, 27, 11, 9, -22, .14), (330, 330, 24, 19, 9, 6, 16, .12)]:
    d = "reverse" if dur < 0 else "normal"
    b.append(f'<g style="transform-box:fill-box;transform-origin:center;animation:spin {abs(dur)}s linear infinite {d}">'
             f'<path d="{gear(gx, gy, ro, ri, n, hole)}" fill="none" stroke="{SAFF}" stroke-opacity="{op}" stroke-width="1.2" fill-rule="evenodd"/></g>')
# sparkle dots
for (dx, dy, rr) in [(40, 120, 1.6), (338, 168, 1.2), (60, 250, 1.1), (300, 300, 1.8), (128, 52, 1.2), (250, 372, 1.4)]:
    b.append(f'<circle class="tw" style="animation-delay:{(dx%7)/3:.1f}s" cx="{dx}" cy="{dy}" r="{rr}" fill="{SAFF}"/>')

# orbit rings: split into back / front halves so the clock sits "inside" them
def ring_arc(rx, ry, rot, front):
    # ellipse param: back half = upper arc (t in pi..2pi), front = lower arc
    pts = []
    t0, t1 = (0, math.pi) if front else (math.pi, 2*math.pi)
    for k in range(61):
        t = t0 + (t1 - t0)*k/60
        x, y = rx*math.cos(t), ry*math.sin(t)
        ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pts.append(f"{cx + x*ca - y*sa:.1f},{cy + x*sa + y*ca:.1f}")
    return "M" + " L".join(pts)
rings = [(168, 50, -22, SAFF, "ro"), (176, 40, 14, CYAN, "rb")]
for rx, ry, rot, c, gid in rings:
    b.append(f'<path d="{ring_arc(rx, ry, rot, False)}" fill="none" stroke="{c}" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>')

# clock body: depth shadow + side band (slight 3/4 view), chrome bezel, cream face
R = 112
b.append(f'<ellipse cx="{cx+10}" cy="{cy+16}" rx="{R+20}" ry="{R+14}" fill="#000" fill-opacity=".35" filter="url(#soft)"/>')
b.append(f'<circle cx="{cx-9}" cy="{cy+5}" r="{R+14}" fill="url(#side)"/>')
for k in range(10):   # side rivets / ridges
    a = math.radians(150 + k*9)
    b.append(f'<line x1="{cx-9+(R+14)*math.cos(a):.1f}" y1="{cy+5+(R+14)*math.sin(a):.1f}" x2="{cx-3+(R+12)*math.cos(a):.1f}" y2="{cy+(R+12)*math.sin(a):.1f}" stroke="#2A2F3A" stroke-width="1.2"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R+14}" fill="url(#chrome)" stroke="#5B6270" stroke-width="1.2"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R+6}" fill="none" stroke="url(#chrome2)" stroke-width="5"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R+2}" fill="url(#face)" stroke="#8A8577" stroke-width="1"/>')
# minute track
for i in range(60):
    a = math.radians(i*6); big = i % 5 == 0
    r1, r2 = (R-8, R-1) if big else (R-5, R-1)
    b.append(f'<line x1="{cx+r1*math.sin(a):.1f}" y1="{cy-r1*math.cos(a):.1f}" x2="{cx+r2*math.sin(a):.1f}" y2="{cy-r2*math.cos(a):.1f}" stroke="#1D1B17" stroke-width="{1.6 if big else .7}"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R-9}" fill="none" stroke="#1D1B17" stroke-width=".6"/>')
# roman numerals, radially oriented
romans = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
for i, rn in enumerate(romans):
    a = i*30; rr = R - 25
    x = cx + rr*math.sin(math.radians(a)); y = cy - rr*math.cos(math.radians(a))
    b.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{19 if len(rn)<4 else 16}" fill="#15130F" font-family="{SERIF}" font-weight="700" text-anchor="middle" dominant-baseline="central" transform="rotate({a} {x:.1f} {y:.1f})" style="font-family:{SERIF}">{rn}</text>')
# inner seconds ring with small numbers
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R-46}" fill="none" stroke="#6E685B" stroke-width=".6"/>')
for i in range(12):
    a = math.radians(i*30); rr = R - 56
    b.append(T(f"{cx+rr*math.sin(a):.1f}", f"{cy-rr*math.cos(a)+3:.1f}", str(60 if i == 0 else i*5), 7, "#6E685B", 600, "middle"))
b.append(T(cx, cy+30, "NIGHT SHIFT", 6.5, "#6E685B", 700, "middle", extra='letter-spacing="1.5"'))
b.append(T(cx, cy-24, "A · S", 8, "#15130F", 700, "middle", extra=f'style="font-family:{SERIF}" letter-spacing="2"'))
# hands (black, spade style) + orange seconds
def spade(L, w):
    return (f"M{cx-w*.35},{cy+12} L{cx-w},{cy-L*.55} L{cx},{cy-L*.62} L{cx-w*.5},{cy-L*.7} "
            f"L{cx},{cy-L} L{cx+w*.5},{cy-L*.7} L{cx},{cy-L*.62} L{cx+w},{cy-L*.55} L{cx+w*.35},{cy+12} Z")
def rot(svgel, start, dur):
    return (f'<g transform="rotate({start} {cx} {cy})">{svgel}'
            f'<animateTransform attributeName="transform" type="rotate" from="{start} {cx} {cy}" to="{start+360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>')
b.append(rot(f'<path d="{spade(58, 5)}" fill="#14120E"/>', 112, 720))
b.append(rot(f'<path d="{spade(86, 3.6)}" fill="#14120E"/>', 282, 60))
b.append(rot(f'<line x1="{cx}" y1="{cy+22}" x2="{cx}" y2="{cy-96}" stroke="{MAG}" stroke-width="1.4" stroke-linecap="round"/><circle cx="{cx}" cy="{cy+18}" r="3.4" fill="{MAG}"/>', 0, 12))
b.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#2B2822"/><circle cx="{cx}" cy="{cy}" r="2" fill="#C9C2B0"/>')
# glass glare
b.append(f'<path d="M{cx-R+18},{cy-30} A{R-12},{R-12} 0 0,1 {cx+38},{cy-R+16} A{R+40},{R+40} 0 0,0 {cx-R+18},{cy-30} Z" fill="#fff" fill-opacity=".16"/>')
b.append(f'<circle cx="{cx}" cy="{cy}" r="{R+2}" fill="url(#glass)"/>')
# crown / knob on top-right
b.append(f'<rect x="{cx+R+8}" y="{cy-60}" width="9" height="14" rx="2" fill="url(#chrome2)" transform="rotate(30 {cx+R+12} {cy-53})"/>')
# front halves of the rings + travelling sparks
for i, (rx, ry, rot_, c, gid) in enumerate(rings):
    d = ring_arc(rx, ry, rot_, True)
    b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="3.4" stroke-linecap="round"/>')
    b.append(f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1" stroke-dasharray="14 220" style="animation:orb {3 + i}s linear infinite"/>')
    b.append(f'<circle r="4" fill="{c}"><animateMotion dur="{3 + i*.8:.1f}s" repeatCount="indefinite" path="{d}"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" dur="{3 + i*.8:.1f}s" repeatCount="indefinite"/></circle>')

# ---- name + flip clock
b.append(T(372, 92, "// it's late. the code is still compiling.", 12.5, MUTED, 500))
b.append(T(368, 158, "Ansh Singh", 64, TEXT, 800, cls="sans", extra='letter-spacing="1"'))
b.append(T(372, 192, "ML engineer · full-stack builder · ICPC regionalist", 16, SAFF, 600, cls="sans"))
b.append(T(372, 218, "B.E. ISE @ MSRIT  ·  ML intern @ IIIT Allahabad  ·  GSSoC '26 contributor", 12, MUTED, 500))
# flip clock 03:47 (last digit rolls 7→8→9)
fx, fy = 372, 246; cw, chh = 46, 70
def card(x, digit_svg, roll=False):
    o = [f'<rect x="{x}" y="{fy}" width="{cw}" height="{chh}" rx="7" fill="#151C33" stroke="{LINE}"/>']
    o.append(f'<clipPath id="cc{x}"><rect x="{x}" y="{fy}" width="{cw}" height="{chh}" rx="7"/></clipPath>')
    o.append(f'<g clip-path="url(#cc{x})">{digit_svg}')
    if roll:
        o.append(f'<rect class="flap" x="{x}" y="{fy}" width="{cw}" height="{chh/2}" fill="#1B2440"/>')
    o.append('</g>')
    o.append(f'<line x1="{x}" y1="{fy+chh/2}" x2="{x+cw}" y2="{fy+chh/2}" stroke="{BG}" stroke-width="2"/>')
    return "".join(o)
def dig(x, d, col=TEXT): return T(x + cw/2, fy + 52, d, 50, col, 800, "middle")
b.append(card(fx, dig(fx, "0")))
b.append(card(fx+52, dig(fx+52, "3")))
b.append(f'<g class="colon"><circle cx="{fx+112}" cy="{fy+24}" r="4" fill="{SAFF}"/><circle cx="{fx+112}" cy="{fy+46}" r="4" fill="{SAFF}"/></g>')
b.append(card(fx+124, dig(fx+124, "4")))
roll = f'<g class="dig">' + "".join(T(fx+176+cw/2, fy+52+i*70, d, 50, TEXT, 800, "middle") for i, d in enumerate("789")) + '</g>'
b.append(card(fx+176, roll, roll=True))
b.append(T(fx+236, fy+30, "AM", 15, SAFF, 800))
b.append(T(fx+236, fy+50, "IST", 11, DIM, 700))
# ---- cans on the desk
cans_x = [778, 820, 862, 904, 946]
labels = ["DSA", "ICPC", "RAG", "DEPLOY", "PR"]
for i, (x, lab) in enumerate(zip(cans_x, labels)):
    b.append(can(x, 368, lab, [MINT, SAFF, CYAN, MAG, MINT][i], 1.0, "drop", f"animation-delay:{i*.9:.1f}s"))
# bubbles over the last can
for k in range(4):
    b.append(f'<circle class="bub" style="animation-delay:{k*.6:.1f}s" cx="{961 + (k%2)*4}" cy="296" r="{1.5+k%2}" fill="{MINT}"/>')
# can counter
b.append(T(778, 404, "cans tonight:", 11, MUTED, 600))
b.append(f'<clipPath id="cn"><rect x="866" y="390" width="20" height="18"/></clipPath>')
b.append(f'<g clip-path="url(#cn)"><g class="cnt">' + "".join(T(868, 404 + i*16, str(n), 13, MINT, 800) for i, n in enumerate(range(0, 6))) + '</g></g>')
b.append(T(890, 404, "· regrets: 0", 11, MUTED, 600))
# terminal line
b.append(T(372, 352, "$ while (!sunrise) { code(); sip(); ship(); }", 13, MINT, 500))
b.append(f'<rect class="cur" x="{372 + 46*7.8:.0f}" y="341" width="8" height="14" fill="{MINT}"/>')
b.append(T(372, 404, "LeetCode Knight 2033 · CF Specialist · 1300+ solved", 12, TEXT, 600))
b.append('</g>')
b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="none" stroke="{LINE}"/>')
save("hero.svg", svg(W, H, "\n".join(b), style, "Ansh Singh — ML engineer, full-stack builder, ICPC regionalist. Night shift at 03:47 AM.", defs))
