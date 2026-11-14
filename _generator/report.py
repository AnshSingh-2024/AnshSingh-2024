from common import *

# ---------------- timestamp section headers ----------------
heads = [("h01", "09:00", "AM", "STAND-UP", "who I am, in one page", 270),
         ("h02", "11:30", "AM", "DEEP WORK", "things I built and shipped", 345),
         ("h03", "02:00", "PM", "THE STACK", "what I build with", 60),
         ("h04", "05:00", "PM", "TROPHY CASE", "wins, ranks, experience", 150),
         ("h05", "08:00", "PM", "CONTEST HOUR", "competitive programming", 240),
         ("h06", "02:37", "AM", "NIGHT SHIFT", "real GitHub activity, rebuilt every week", 78)]
for fn, hhmm, ap, title, sub, hdeg in heads:
    st = '''.sw{animation:sw 5s ease-in-out infinite} @keyframes sw{0%{transform:translateX(-200px)}100%{transform:translateX(1100px)}}'''
    df = f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{SAFF}" stop-opacity="0"/><stop offset=".5" stop-color="{SAFF}" stop-opacity=".9"/><stop offset="1" stop-color="{SAFF}" stop-opacity="0"/></linearGradient>'
    cx, cy = 40, 36
    mdeg = int(hhmm[3:]) * 6
    bd = [f'<clipPath id="hc"><rect width="1000" height="72" rx="14"/></clipPath>',
          f'<rect width="1000" height="72" rx="14" fill="{BG}" stroke="{LINE}"/>',
          clock_face(cx, cy, 22, SAFF, False, False, PANEL),
          f'<line x1="{cx}" y1="{cy}" x2="{cx + 11*math.sin(math.radians(hdeg)):.1f}" y2="{cy - 11*math.cos(math.radians(hdeg)):.1f}" stroke="{TEXT}" stroke-width="2.6" stroke-linecap="round"/>',
          hand(cx, cy, 17, 1.6, MAG, 4, mdeg),
          f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{MAG}"/>',
          T(78, 47, hhmm, 30, SAFF, 800),
          T(78 + 5*18 + 6, 47, ap, 13, SAFF, 800),
          T(210, 46, title, 24, TEXT, 800, cls="sans", extra='letter-spacing="1.5"'),
          T(210 + len(title)*24*0.66 + 18, 46, f"— {sub}", 13.5, MUTED, 500),
          f'<g clip-path="url(#hc)"><rect class="sw" x="0" y="69" width="200" height="3" fill="url(#g)"/></g>']
    save(f"{fn}.svg", svg(1000, 72, "\n".join(bd), st, f"{hhmm} {ap} — {title}", df))

# ---------------- timesheet (about) ----------------
rows = [("09:02", "identity", "Ansh Singh · Bengaluru · B.E. Information Science @ MSRIT (2024 –) · CGPA 9.29", TEXT),
        ("09:30", "day job", "ML Project Intern @ IIIT Allahabad · FastAPI, PostgreSQL, React, RAG, XAI", SAFF),
        ("10:00", "community", "Core member · CodeRIT, the competitive coding club of MSRIT", "#C7A6FF"),
        ("10:45", "open source", "GSSoC 2026 contributor · GirlScript Summer of Code", MINT),
        ("13:10", "algorithms", "ICPC Asia West Regionalist '26 · LeetCode Knight (max 2033) · CF Specialist", CYAN),
        ("15:40", "builds", "CNN + ViT fusion models · RAG pipelines · real-time trading platforms", MAG),
        ("18:00", "certified", "ML Specialization · Operating Systems · MCP (Claude Academy) · IIT Madras BS", MUTED)]
W = 1000; RH = 46; Y0 = 84; H = Y0 + RH*len(rows) + 64
st = f'''
.row{{animation:row .6s cubic-bezier(.2,.8,.2,1) both}} @keyframes row{{from{{opacity:0;transform:translateX(-16px)}}}}
.now{{animation:now 14s linear infinite}} @keyframes now{{from{{transform:translateY(0)}}to{{transform:translateY({RH*len(rows)}px)}}}}
.dot{{animation:dot 1.2s ease-in-out infinite}} @keyframes dot{{50%{{opacity:.2}}}}
.prog{{transform-box:fill-box;transform-origin:left;animation:prog 14s linear infinite}} @keyframes prog{{from{{transform:scaleX(0)}}}}
'''
b = [frame(W, H, 16, PANEL)]
b.append(T(28, 40, "stand-up notes", 14, TEXT, 700))
b.append(T(160, 40, "who I am, in seven lines", 12, MUTED, 500))
b.append(f'<circle class="dot" cx="{W-110}" cy="35" r="5" fill="{MINT}"/>')
b.append(T(W-28, 40, "ON SHIFT", 11, MINT, 800, "end", extra='letter-spacing="2"'))
b.append(f'<line x1="44" y1="{Y0-14}" x2="44" y2="{Y0 + RH*len(rows) - 14}" stroke="{LINE}" stroke-width="2"/>')
for i, (t, k, v, c) in enumerate(rows):
    y = Y0 + i*RH
    g = [f'<rect x="20" y="{y-14}" width="{W-40}" height="{RH-6}" rx="10" fill="{PANEL2 if i%2==0 else PANEL}"/>',
         f'<circle cx="44" cy="{y+7}" r="6" fill="{BG}" stroke="{c}" stroke-width="2"/>',
         T(64, y+12, k, 12, MUTED, 700, extra='letter-spacing="1"'),
         T(176, y+12, v, 13.5, c if c != MUTED else TEXT, 500)]
    b.append(f'<g class="row" style="animation-delay:{.15 + i*.18:.2f}s">' + "".join(g) + '</g>')
b.append(f'<g class="now"><line x1="20" y1="{Y0-16}" x2="{W-20}" y2="{Y0-16}" stroke="{MAG}" stroke-opacity=".7" stroke-dasharray="2 4"/>'
         f'<rect x="{W-74}" y="{Y0-26}" width="50" height="18" rx="9" fill="{MAG}"/>' + T(W-49, Y0-13, "NOW", 10, BG, 900, "middle") + '</g>')
yb = Y0 + RH*len(rows) + 18
b.append(T(28, yb + 6, "day progress", 11, MUTED, 600))
b.append(f'<rect x="130" y="{yb-2}" width="{W-300}" height="8" rx="4" fill="{LINE}"/>')
b.append(f'<rect class="prog" x="130" y="{yb-2}" width="{W-300}" height="8" rx="4" fill="{SAFF}"/>')
b.append(T(W-28, yb + 6, "next: night shift →", 11.5, SAFF, 700, "end"))
save("about.svg", svg(W, H, "\n".join(b), st, "About Ansh Singh, B.E. ISE @ MSRIT (CGPA 9.29), ML Project Intern @ IIIT Allahabad, core member of CodeRIT, GSSoC 2026 contributor, ICPC Asia West Regionalist, LeetCode Knight, Codeforces Specialist"))

# ---------------- flip-clock stats ----------------
tiles = [("2033", "LEETCODE MAX", "Knight · top 2.19%", MINT),
         ("1300", "DSA SOLVED", "problems, 6 judges", SAFF),
         ("269", "ICPC RANK", "Asia West Amritapuri", MAG),
         ("9921", "VAL. ACCURACY", "RupeeGuard AI · 99.21%", CYAN),
         ("929", "CGPA", "9.29 / 10 · MSRIT", MINT)]
W2, H2 = 1000, 168
tw = (W2 - 4*12) / 5
st = '''
.fl{transform-box:fill-box;transform-origin:center;animation:fl 10s cubic-bezier(.3,.7,.3,1) infinite both}
@keyframes fl{0%{transform:scaleY(0)}6%{transform:scaleY(1.06)}8%,100%{transform:scaleY(1)}}
'''
b2 = []
for i, (val, lab, sub, c) in enumerate(tiles):
    x = i * (tw + 12)
    b2.append(f'<rect x="{x+1}" y="1" width="{tw-2}" height="{H2-2}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
    b2.append(T(x + tw/2, 28, lab, 10.5, c, 800, "middle", extra='letter-spacing="1.5"'))
    n = len(val); cw = 32; gap = 5
    sx = x + (tw - (n*cw + (n-1)*gap)) / 2
    for k, d in enumerate(val):
        dx = sx + k*(cw+gap)
        dl = .1 + i*.25 + k*.12
        b2.append(f'<g class="fl" style="animation-delay:{dl:.2f}s"><rect x="{dx:.1f}" y="44" width="{cw}" height="52" rx="6" fill="#151C33" stroke="{LINE}"/>'
                  + T(f"{dx+cw/2:.1f}", 83, d, 36, TEXT, 800, "middle") + '</g>')
        b2.append(f'<line x1="{dx:.1f}" y1="70" x2="{dx+cw:.1f}" y2="70" stroke="{BG}" stroke-width="2"/>')
    # punctuation overlays
    if val == "9921":
        b2.append(f'<circle cx="{sx + 2*cw + 1.5*gap:.1f}" cy="92" r="3" fill="{c}"/>')
    if val == "929":
        b2.append(f'<circle cx="{sx + cw + .5*gap:.1f}" cy="92" r="3" fill="{c}"/>')
    if val == "1300":
        b2.append(T(sx + n*(cw+gap) + 2, 66, "+", 22, c, 900))
    b2.append(T(x + tw/2, 128, sub, 12, TEXT, 600, "middle"))
    b2.append(f'<rect x="{x + tw/2 - 18}" y="144" width="36" height="3" rx="1.5" fill="{c}"/>')
save("stats.svg", svg(W2, H2, "\n".join(b2), st, "LeetCode max 2033 · 1300+ DSA solved · ICPC rank 269 · 99.21% validation accuracy · CGPA 9.29"))
