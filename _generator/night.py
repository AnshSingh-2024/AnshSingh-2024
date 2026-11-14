from common import *
import random
random.seed(5)

# ======================= NIGHT FUEL SHELF =======================
nights = [("ICPC", "ICPC Regional", "Asia West '26", SAFF),
          ("GRiD", "Flipkart GRiD", "semi-finals", MINT),
          ("FIDE", "Fidelity Hack", "top 12 / 1700+", CYAN),
          ("NER", "NER Hackathon", "top 60 / 2000+", MAG),
          ("SSCBS", "INVICTA", "rank 27 / 1500+", SAFF),
          ("IITR", "Trading Heist", "national final", MINT),
          ("GSSoC", "GSSoC '26", "open-source PRs", CYAN),
          ("v1.0", "RupeeGuard", "first deploy", MAG)]
W, H = 1000, 330
st = '''
.cd{animation:cd 16s cubic-bezier(.3,1.5,.5,1) infinite both}
@keyframes cd{0%{transform:translateY(-140px);opacity:0}5%,93%{transform:none;opacity:1}100%{opacity:0}}
.glow{animation:glow 16s ease-in-out infinite both} @keyframes glow{0%,30%{opacity:0}40%,88%{opacity:.55}100%{opacity:0}}
.bub{animation:bub 2.2s ease-in infinite} @keyframes bub{0%{transform:translateY(0);opacity:0}25%{opacity:.9}100%{transform:translateY(-40px);opacity:0}}
.tick{animation:tick 1s steps(1) infinite} @keyframes tick{50%{opacity:.2}}
'''
df = "".join(f'<radialGradient id="gl{i}"><stop offset="0" stop-color="{c}" stop-opacity=".9"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>' for i, (_, _, _, c) in enumerate(nights))
b = [frame(W, H, 16, PANEL)]
b.append(T(28, 42, "night fuel", 16, TEXT, 800, cls="sans"))
b.append(T(28, 62, "one can for every deadline that ran past midnight", 11.5, MUTED, 500))
b.append(f'<g class="tick">{T(W-28, 42, "02:37 AM", 13, SAFF, 800, "end")}</g>')
slot = (W - 56) / len(nights)
base = 236
for i, (lab, name, sub, c) in enumerate(nights):
    x = 28 + i*slot + (slot - 51)/2
    dl = .3 + i*.35
    b.append(f'<ellipse class="glow" style="animation-delay:{dl:.2f}s" cx="{x+25.5:.1f}" cy="{base-50}" rx="56" ry="70" fill="url(#gl{i})"/>')
    b.append(can(x, base, lab, c, 1.5, "cd", f"animation-delay:{dl:.2f}s"))
    for k in range(3):
        b.append(f'<circle class="bub" style="animation-delay:{dl + k*.7:.2f}s" cx="{x + 18 + k*8:.1f}" cy="{base-100}" r="{1.4 + k%2}" fill="{c}"/>')
    b.append(T(x + 25.5, base + 34, name, 11.5, TEXT, 700, "middle"))
    b.append(T(x + 25.5, base + 52, sub, 10.5, MUTED, 500, "middle"))
b.append(f'<rect x="20" y="{base+2}" width="{W-40}" height="8" rx="3" fill="#2A2238"/><rect x="20" y="{base+2}" width="{W-40}" height="2" fill="{SAFF}" fill-opacity=".4"/>')
save("fuel.svg", svg(W, H, "\n".join(b), st, "Night fuel: one energy-drink can per late-night milestone — ICPC regional, Flipkart GRiD, Fidelity hackathon, NER hackathon, INVICTA, Trading Heist, GSSoC 2026, RupeeGuard deploy", df))

# ======================= PROJECT CONSTELLATION (graph that builds itself) =======================
W, H = 1000, 480
projects = [("Emergent LLMs", 120, SAFF), ("RupeeGuard AI", 310, MAG), ("FinSocial", 500, CYAN), ("HomeHarvest AI", 690, MINT), ("Portfolio Tracker", 880, SAFF)]
top = [("LaTeX", 70), ("LLMs", 175), ("PyTorch", 270), ("FAISS", 360), ("RAG", 450), ("Gemini", 555), ("pgvector", 660), ("Redis", 760), ("Socket.IO", 870)]
bot = [("Docker", 205), ("React", 300), ("FastAPI", 395), ("Node·Express", 505), ("PostgreSQL", 615), ("MongoDB", 710), ("Tailwind", 795), ("Java", 872), ("MySQL", 945)]
edges = {"Emergent LLMs": ["LaTeX", "LLMs"],
         "RupeeGuard AI": ["LLMs", "PyTorch", "FAISS", "RAG", "Gemini", "Docker", "React", "FastAPI"],
         "FinSocial": ["LLMs", "RAG", "Gemini", "pgvector", "Redis", "Socket.IO", "Docker", "React", "Node·Express", "PostgreSQL"],
         "HomeHarvest AI": ["LLMs", "Gemini", "FastAPI", "MongoDB", "Tailwind"],
         "Portfolio Tracker": ["Java", "MySQL"]}
PY, TY, BY = 250, 112, 392
tpos = {n: (x, TY) for n, x in top}; tpos.update({n: (x, BY) for n, x in bot})
deg = {}
for p, ts in edges.items():
    for t in ts: deg[t] = deg.get(t, 0) + 1
first = {}
st = '''
.ed{stroke-dasharray:1;stroke-dashoffset:1;animation:ed 14s ease infinite both}
@keyframes ed{0%{stroke-dashoffset:1;opacity:1}8%,90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.nd{transform-box:fill-box;transform-origin:center;animation:nd 14s cubic-bezier(.3,1.6,.5,1) infinite both}
@keyframes nd{0%{transform:scale(0);opacity:0}4%,92%{transform:scale(1);opacity:1}100%{opacity:0}}
.sig{animation:sig 14s infinite both} @keyframes sig{0%,45%{opacity:0}50%,92%{opacity:1}100%{opacity:0}}
'''
b = [frame(W, H, 16, PANEL)]
b.append(T(28, 42, "how my projects connect", 16, TEXT, 800, cls="sans"))
b.append(T(28, 62, "five projects, the tools they share · the graph re-draws itself every 14s", 11.5, MUTED, 500))
order = ["RupeeGuard AI", "FinSocial", "HomeHarvest AI", "Emergent LLMs", "Portfolio Tracker"]
pmap = {n: (x, c) for n, x, c in projects}
t = 1.0; edge_svg = []; sig_svg = []
for p in order:
    px, c = pmap[p]
    for tn in edges[p]:
        tx, ty = tpos[tn]
        sy = PY - 22 if ty < PY else PY + 22
        ey = ty + 14 if ty < PY else ty - 14
        d = f"M{px},{sy} C{px},{(sy+ey)/2:.0f} {tx},{(sy+ey)/2:.0f} {tx},{ey}"
        edge_svg.append(f'<path class="ed" pathLength="1" style="animation-delay:{t:.2f}s" d="{d}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="1.6"/>')
        sig_svg.append(f'<circle class="sig" r="2.6" fill="{c}"><animateMotion dur="{2.2 + random.random():.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
        first.setdefault(tn, t + .35)
        t += .14
    t += .25
b += edge_svg + sig_svg
for n, x, c in projects:
    w = len(n)*8.4 + 30
    b.append(f'<g class="nd" style="animation-delay:{.2 + order.index(n)*.15:.2f}s"><rect x="{x - w/2:.0f}" y="{PY-22}" width="{w:.0f}" height="44" rx="12" fill="{BG}" stroke="{c}" stroke-width="2"/>'
             + T(x, PY + 5, n, 13.5, c, 800, "middle") + '</g>')
for n, (x, y) in tpos.items():
    w = len(n)*7.2 + 22; d = deg.get(n, 0); hot = d >= 2
    col = TEXT if hot else MUTED
    g = (f'<rect x="{x - w/2:.0f}" y="{y-14}" width="{w:.0f}" height="28" rx="14" fill="{PANEL2}" stroke="{SAFF if hot else LINE}"/>'
         + T(x, y + 4.5, n, 12, col, 600 if hot else 500, "middle"))
    if hot:
        bx = x + w/2 - 4; by = y - 14
        g += f'<circle cx="{bx:.0f}" cy="{by}" r="9" fill="{SAFF}"/>' + T(f"{bx:.0f}", by + 4, f"×{d}", 9, BG, 900, "middle")
    b.append(f'<g class="nd" style="animation-delay:{first.get(n, 1):.2f}s">{g}</g>')
b.append(T(28, H - 22, "most reused:", 11.5, MUTED, 600))
hot = sorted([(v, k) for k, v in deg.items() if v >= 2], reverse=True)
b.append(T(122, H - 22, "  ·  ".join(f"{k} ×{v}" for v, k in hot), 11.5, SAFF, 700))
save("constellation.svg", svg(W, H, "\n".join(b), st, "Graph of projects and shared tools: RupeeGuard AI, FinSocial, HomeHarvest AI, Emergent LLMs report, Portfolio Tracker"))

# ======================= TROPHY CABINET =======================
# (result, event, detail line, colour, metal, object)
items = [("REGIONALIST", "ICPC Asia West 2026", "Rank 269 · Asia West Amritapuri Regional", MAG, "gold", "cup"),
         ("KNIGHT · 2033", "LeetCode · CF Specialist", "top 2.19% worldwide · 1300+ problems", MINT, "gold", "medal"),
         ("SEMI-FINALIST", "Flipkart GRiD 8.0", "among 1.65 lakh+ applicants", SAFF, "gold", "cup"),
         ("TOP 12", "Fidelity India Hackathon", "Fidelity Investments · 1700+ teams", CYAN, "gold", "star"),
         ("WINNER", "Idearise", "M.S. Ramaiah Inst. of Technology", SAFF, "gold", "cup"),
         ("CORE MEMBER", "CodeRIT, MSRIT", "the college's competitive coding club", "#C7A6FF", "bronze", "shield:{ }"),
         ("CONTRIBUTOR", "GSSoC 2026", "GirlScript Summer of Code", MINT, "bronze", "shield:PR"),
         ("ML INTERN", "IIIT Allahabad", "May 2026 – now · FastAPI, RAG, XAI", CYAN, "bronze", "shield:ML"),
         ("NATIONAL FINALIST", "Trading Heist", "IIT Roorkee", MAG, "silver", "medal"),
         ("3RD RUNNER-UP", "Case Crunch", "NIT Rourkela", SAFF, "silver", "medal"),
         ("RANK 27", "INVICTA", "SSCBS, New Delhi · 1500+ teams", CYAN, "silver", "star"),
         ("TOP 60", "NER Tech Hackathon 2.0", "among 2000+ teams", MAG, "silver", "star")]
W = 1000; ROWH = 232; TOP = 96; H = TOP + 3*ROWH + 16
st = f'''.sp{{animation:sp 10s ease-in-out infinite alternate}} @keyframes sp{{from{{transform:translateX(-390px)}}to{{transform:translateX(390px)}}}}
.gl{{animation:gl 3.2s ease-in-out infinite}} @keyframes gl{{50%{{opacity:.15}}}}
.pop{{transform-box:fill-box;transform-origin:50% 100%;animation:pop .8s cubic-bezier(.3,1.6,.5,1) both}} @keyframes pop{{from{{transform:scale(0)}}}}
.plq{{animation:plq .6s ease both}} @keyframes plq{{from{{opacity:0;transform:translateY(8px)}}}}
.sw{{transform-box:fill-box;transform-origin:50% 0;animation:sw 4s ease-in-out infinite}} @keyframes sw{{0%,100%{{transform:rotate(-4deg)}}50%{{transform:rotate(4deg)}}}}'''
df = '''<linearGradient id="gold" x1="0" x2="1"><stop offset="0" stop-color="#8C5A12"/><stop offset=".35" stop-color="#FFD27A"/><stop offset=".6" stop-color="#E0A23A"/><stop offset="1" stop-color="#7A4B0C"/></linearGradient>
<linearGradient id="silver" x1="0" x2="1"><stop offset="0" stop-color="#5D6470"/><stop offset=".4" stop-color="#F2F4F7"/><stop offset=".65" stop-color="#AAB1BC"/><stop offset="1" stop-color="#4E5562"/></linearGradient>
<linearGradient id="bronze" x1="0" x2="1"><stop offset="0" stop-color="#5A2E14"/><stop offset=".4" stop-color="#E39B63"/><stop offset=".7" stop-color="#B0683A"/><stop offset="1" stop-color="#4A2510"/></linearGradient>
<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE8B0" stop-opacity=".2"/><stop offset="1" stop-color="#FFE8B0" stop-opacity="0"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A4528"/><stop offset="1" stop-color="#2E1D10"/></linearGradient>
<linearGradient id="back" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1222"/><stop offset="1" stop-color="#151026"/></linearGradient>'''
b = [frame(W, H, 16, "url(#back)")]
b.append(T(28, 42, "the trophy cabinet", 17, TEXT, 800, cls="sans"))
b.append(T(28, 63, "gold = top finishes  ·  bronze = roles & open source  ·  silver = finals & ranks", 11.5, MUTED, 500))
for i, (lab, c) in enumerate([("gold", "#FFD27A"), ("bronze", "#E39B63"), ("silver", "#E6E9EE")]):
    b.append(f'<circle cx="{W-215 + i*68}" cy="44" r="7" fill="url(#{lab})"/>' + T(W-204 + i*68, 48, lab, 10, c, 800))
def trophy(x, base, metal, kind, c, res):
    m = f"url(#{metal})"
    if kind == "cup":
        return (f'<path d="M{x-28},{base-120} H{x+28} V{base-102} Q{x+28},{base-70} {x},{base-64} Q{x-28},{base-70} {x-28},{base-102} Z" fill="{m}"/>'
                f'<path d="M{x-28},{base-112} q-20,0 -15,17 q4,13 17,11" fill="none" stroke="{m}" stroke-width="4.5"/>'
                f'<path d="M{x+28},{base-112} q20,0 15,17 q-4,13 -17,11" fill="none" stroke="{m}" stroke-width="4.5"/>'
                f'<rect x="{x-4}" y="{base-64}" width="8" height="14" fill="{m}"/><rect x="{x-20}" y="{base-50}" width="40" height="9" rx="2" fill="{m}"/>'
                f'<rect x="{x-14}" y="{base-41}" width="28" height="5" fill="#2A1A0A"/>')
    if kind == "medal":
        return (f'<g class="sw"><path d="M{x-15},{base-128} L{x-5},{base-90} L{x+5},{base-90} L{x+15},{base-128}" fill="{c}" fill-opacity=".85"/>'
                f'<circle cx="{x}" cy="{base-74}" r="24" fill="{m}"/><circle cx="{x}" cy="{base-74}" r="16" fill="none" stroke="#000" stroke-opacity=".25"/>'
                + T(x, base-68, "★", 15, "#3A2A0A", 900, "middle") + '</g>'
                f'<rect x="{x-16}" y="{base-44}" width="32" height="8" rx="2" fill="#2A2238"/>')
    if kind == "star":
        pts = " ".join(f"{x + (28 if j%2==0 else 12)*math.sin(math.radians(j*36)):.1f},{base-90 - (28 if j%2==0 else 12)*math.cos(math.radians(j*36)):.1f}" for j in range(10))
        return f'<polygon points="{pts}" fill="{m}"/><rect x="{x-3}" y="{base-64}" width="6" height="16" fill="{m}"/><rect x="{x-18}" y="{base-48}" width="36" height="9" rx="2" fill="{m}"/>'
    emb = kind.split(":")[1]
    return (f'<path d="M{x-26},{base-124} H{x+26} V{base-94} Q{x+26},{base-66} {x},{base-54} Q{x-26},{base-66} {x-26},{base-94} Z" fill="{m}"/>'
            f'<path d="M{x-19},{base-117} H{x+19} V{base-94} Q{x+19},{base-72} {x},{base-63} Q{x-19},{base-72} {x-19},{base-94} Z" fill="none" stroke="#2A1A0A" stroke-opacity=".45"/>'
            + T(x, base-86, emb, 15, "#2A1A0A", 900, "middle") + f'<rect x="{x-16}" y="{base-50}" width="32" height="8" rx="2" fill="#2A1A0A" fill-opacity=".6"/>')
colx = [137, 379, 621, 863]
for row in range(3):
    base = TOP + 140 + row*ROWH      # shelf line
    b.append(f'<rect x="18" y="{base}" width="{W-36}" height="14" rx="3" fill="url(#wood)"/><rect x="18" y="{base}" width="{W-36}" height="2" fill="#9A7050"/>')
    for col in range(4):
        i = row*4 + col; res, ev, det, c, metal, kind = items[i]
        x = colx[col]
        b.append(f'<ellipse class="gl" style="animation-delay:{i*.27:.2f}s" cx="{x}" cy="{base-70}" rx="58" ry="62" fill="{c}" fill-opacity=".07"/>')
        b.append(f'<g class="pop" style="animation-delay:{.15 + i*.1:.2f}s">{trophy(x, base, metal, kind, c, res)}</g>')
        # plaque with full details
        pw, ph = 236, 64; py = base + 22
        g = (f'<rect x="{x-pw/2}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="#17121F" stroke="{c}" stroke-opacity=".55"/>'
             f'<rect x="{x-pw/2+6}" y="{py+6}" width="{pw-12}" height="{ph-12}" rx="5" fill="none" stroke="#fff" stroke-opacity=".05"/>'
             + T(x, py+21, res, 14 if len(res) < 15 else 12.5, c, 900, "middle", "sans", 'letter-spacing=".5"')
             + T(x, py+38, ev, 12, TEXT, 700, "middle", "sans")
             + T(x, py+53, det, 10 if len(det) < 36 else 9.3, MUTED, 500, "middle"))
        b.append(f'<g class="plq" style="animation-delay:{.3 + i*.1:.2f}s">{g}</g>')
b.append(f'<g class="sp"><path d="M500,74 L320,{H-12} L680,{H-12} Z" fill="url(#cone)"/><rect x="486" y="66" width="28" height="12" rx="3" fill="#3A4256"/><circle cx="500" cy="80" r="3" fill="#FFE8B0"/></g>')
save("trophies.svg", svg(W, H, "\n".join(b), st, "Trophy cabinet: " + "; ".join(f"{r} — {e} ({d})" for r, e, d, *_ in items), df))

# ======================= SUNRISE FOOTER =======================
W, H = 1000, 270
df = f'''<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2348"/><stop offset=".6" stop-color="#7A4A6B"/><stop offset="1" stop-color="#FFB547"/></linearGradient>
<linearGradient id="nite" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070A14"/><stop offset="1" stop-color="#121A36"/></linearGradient>
<radialGradient id="sun"><stop offset="0" stop-color="#FFE3A3"/><stop offset=".45" stop-color="{SAFF}"/><stop offset="1" stop-color="{SAFF}" stop-opacity="0"/></radialGradient>
<clipPath id="fc"><rect width="{W}" height="{H}" rx="18"/></clipPath>'''
st = '''
.dw{animation:dw 12s ease-in-out infinite both} @keyframes dw{0%,15%{opacity:0}55%,90%{opacity:1}100%{opacity:0}}
.sun{animation:sun 12s ease-in-out infinite both} @keyframes sun{0%,15%{transform:translateY(90px)}60%,90%{transform:translateY(0)}100%{transform:translateY(90px)}}
.d1{animation:dg 12s steps(1) infinite} @keyframes dg{0%{transform:translateY(0)}50%,100%{transform:translateY(-60px)}}
.cur{animation:c 1s steps(1) infinite} @keyframes c{50%{opacity:0}}
'''
b = ['<g clip-path="url(#fc)">', f'<rect width="{W}" height="{H}" fill="url(#nite)"/>', f'<rect class="dw" width="{W}" height="{H}" fill="url(#dawn)"/>',
     f'<g class="sun"><circle cx="820" cy="215" r="90" fill="url(#sun)"/><circle cx="820" cy="215" r="34" fill="#FFD27A"/></g>',
     f'<path d="M0,226 Q180,196 360,222 T720,214 T1000,208 V270 H0 Z" fill="#0A0E1A"/>',
     f'<path d="M0,238 Q220,222 440,240 T1000,230 V270 H0 Z" fill="#070A14"/>']
b.append(T(40, 62, "06:00 AM — LOG OFF", 12, SAFF, 800, extra='letter-spacing="3"'))
b.append(T(40, 104, "Night shift complete.", 32, TEXT, 800, cls="sans"))
b.append(T(40, 136, "Open to SDE / ML internships. Let's build something.", 17, TEXT, 600, cls="sans"))
b.append(T(40, 170, "$ git push origin sunrise", 13, MINT, 500))
b.append(f'<rect class="cur" x="{40 + 25*7.85 + 6:.0f}" y="159" width="8" height="15" fill="{MINT}"/>')
# flip clock 05:59 -> 06:00
fx, fy = 560, 50
def card(x, inner):
    return (f'<rect x="{x}" y="{fy}" width="40" height="60" rx="6" fill="#151C33" stroke="{LINE}"/>'
            f'<clipPath id="f{x}"><rect x="{x}" y="{fy}" width="40" height="60" rx="6"/></clipPath><g clip-path="url(#f{x})">{inner}</g>'
            f'<line x1="{x}" y1="{fy+30}" x2="{x+40}" y2="{fy+30}" stroke="{BG}" stroke-width="2"/>')
def roll(x, a, bb): return f'<g class="d1">' + T(x+20, fy+45, a, 42, TEXT, 800, "middle") + T(x+20, fy+105, bb, 42, TEXT, 800, "middle") + '</g>'
b.append(card(fx, T(fx+20, fy+45, "0", 42, TEXT, 800, "middle")))
b.append(card(fx+46, roll(fx+46, "5", "6")))
b.append(f'<circle cx="{fx+98}" cy="{fy+20}" r="3.5" fill="{SAFF}"/><circle cx="{fx+98}" cy="{fy+40}" r="3.5" fill="{SAFF}"/>')
b.append(card(fx+108, roll(fx+108, "5", "0")))
b.append(card(fx+154, roll(fx+154, "9", "0")))
b.append(T(fx+204, fy+26, "AM", 13, SAFF, 800))
b.append('</g>')
b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="{LINE}"/>')
save("footer.svg", svg(W, H, "\n".join(b), st, "06:00 AM — night shift complete. Open to SDE / ML internships.", df))
