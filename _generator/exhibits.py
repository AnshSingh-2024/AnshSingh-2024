from common import *
import random
random.seed(7)

BASE_STYLE = '''
.draw{stroke-dasharray:1000;stroke-dashoffset:1000;animation:draw 5s ease infinite}
@keyframes draw{0%{stroke-dashoffset:1000;opacity:1}45%,90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.pulse{animation:pulse 1.6s ease-in-out infinite} @keyframes pulse{50%{opacity:.25}}
.hov{transition:all .3s}
'''

def card_shell(w, h, accent, exhibit, case):
    b = [frame(w, h, 16, PANEL), corners(10, 10, w-20, h-20, 12, accent, 1.5, .6)]
    b.append(f'<rect x="24" y="24" width="8" height="8" fill="{accent}"/>')
    b.append(T(40, 32, exhibit, 11, accent, 700, extra='letter-spacing="2"'))
    b.append(T(w-24, 32, case, 10, DIM, 600, "end", extra='letter-spacing="1.5"'))
    return b

# =============== RupeeGuard (featured) ===============
W, H = 1000, 380
acc = MAG
st = BASE_STYLE + f'''
.scan{{animation:scan 3s ease-in-out infinite alternate}} @keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY(176px)}}}}
.hm{{animation:hm 3s ease-in-out infinite alternate}} @keyframes hm{{from{{opacity:.15}}to{{opacity:.85}}}}
.pk{{offset-rotate:0deg}}
.flow{{stroke-dasharray:5 6;animation:flow 1s linear infinite}} @keyframes flow{{to{{stroke-dashoffset:-11}}}}
.lit{{animation:lit 5s infinite}} @keyframes lit{{0%,100%{{stroke-opacity:.35}}10%,30%{{stroke-opacity:1}}}}
'''
df = f'''<radialGradient id="hA"><stop offset="0" stop-color="{MAG}"/><stop offset=".5" stop-color="{SAFF}" stop-opacity=".6"/><stop offset="1" stop-color="{SAFF}" stop-opacity="0"/></radialGradient>
<linearGradient id="nt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#11241F"/><stop offset="1" stop-color="#1C1712"/></linearGradient>
<linearGradient id="sl" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset="1" stop-color="{MINT}" stop-opacity=".7"/></linearGradient>
<clipPath id="nc"><rect x="34" y="78" width="330" height="180" rx="10"/></clipPath>'''
b = card_shell(W, H, acc, "PROJECT 01 · FLAGSHIP", "● LIVE ON HUGGING FACE")
# mini note visual
b.append(f'<rect x="34" y="78" width="330" height="180" rx="10" fill="url(#nt)" stroke="{MINT}" stroke-opacity=".35"/>')
b.append('<g clip-path="url(#nc)">')
for k in range(12):
    b.append(f'<path d="{wave(34, 364, 210+k*2, 10, .04, k*.3, 5)}" fill="none" stroke="{SAFF}" stroke-opacity=".14" stroke-width=".7"/>')
b.append(f'<path d="{hypotrochoid(110, 160, 60, 18, 38, .9, 500)}" fill="none" stroke="{MINT}" stroke-opacity=".4" stroke-width=".6"/>')
b.append(f'<rect x="290" y="78" width="9" height="180" fill="{CYAN}" fill-opacity=".35"/>')
b.append(T(225, 128, "SPECIMEN", 18, TEXT, 800, "middle", "sans", 'fill-opacity=".8" letter-spacing="3"'))
b.append(T(225, 148, "input: note_0427.jpg", 10, MUTED, 500, "middle"))
b.append(f'<ellipse class="hm" cx="110" cy="160" rx="70" ry="62" fill="url(#hA)"/>')
b.append(f'<ellipse class="hm" style="animation-delay:1.5s" cx="294" cy="200" rx="34" ry="70" fill="url(#hA)"/>')
b.append(f'<g class="scan"><rect x="34" y="62" width="330" height="20" fill="url(#sl)"/><rect x="34" y="81" width="330" height="1.5" fill="#DFFFF2"/></g>')
b.append('</g>')
b.append(corners(40, 84, 140, 150, 10, MAG, 1.5))
b.append(T(34, 280, "GradCAM + occlusion maps", 11, MUTED, 500))
b.append(T(364, 280, "fake-class recall 1.00", 11, MAG, 700, "end"))
# title area
b.append(T(400, 92, "RupeeGuard AI", 34, TEXT, 800, cls="sans"))
b.append(T(400, 118, "Counterfeit Indian-currency detection that explains itself — heatmaps show", 12.5, MUTED))
b.append(T(400, 136, "where it looked, and a RAG layer writes an RBI-grounded forensic report.", 12.5, MUTED))
# pipeline
nodes = [("image", 400, MUTED), ("EffNet-B4", 486, MINT), ("ViT-B/16", 486, CYAN), ("cross-attn", 600, SAFF), ("verdict", 712, MAG), ("FAISS+Gemini", 818, MINT)]
pos = {}
for i, (lab, x, c) in enumerate(nodes):
    y = 168 if lab != "ViT-B/16" else 206
    if lab in ("image",): y = 187
    if lab in ("cross-attn", "verdict", "FAISS+Gemini"): y = 187
    w = len(lab) * 7.0 + 18
    pos[lab] = (x, y, w)
    b.append(f'<rect class="lit" style="animation-delay:{i*.5}s" x="{x}" y="{y-13}" width="{w:.0f}" height="26" rx="6" fill="{c}" fill-opacity=".07" stroke="{c}"/>')
    b.append(T(x + w/2, y + 4, lab, 11.5, c, 600, "middle"))
def edge(a, bb, c):
    x1, y1, w1 = pos[a]; x2, y2, _ = pos[bb]
    sx, ex = x1 + w1, x2
    d = f"M{sx:.0f},{y1} C{(sx+ex)/2:.0f},{y1} {(sx+ex)/2:.0f},{y2} {ex:.0f},{y2}"
    return d, f'<path class="flow" d="{d}" fill="none" stroke="{c}" stroke-opacity=".7" stroke-width="1.4"/>'
paths = []
for a, bb, c in [("image", "EffNet-B4", MINT), ("image", "ViT-B/16", CYAN), ("EffNet-B4", "cross-attn", MINT), ("ViT-B/16", "cross-attn", CYAN), ("cross-attn", "verdict", SAFF), ("verdict", "FAISS+Gemini", MAG)]:
    d, s = edge(a, bb, c); paths.append((d, c)); b.append(s)
for i, (d, c) in enumerate(paths):
    b.append(f'<circle r="3.2" fill="{c}"><animateMotion dur="1.4s" begin="{i*.25}s" repeatCount="indefinite" path="{d}"/></circle>')
# metrics
mx = 400
for big, small, c in [("99.21%", "val. accuracy · EffNet-B4", MINT), ("CNN ⊕ ViT", "cross-attention fusion", CYAN), ("RAG", "FAISS + Gemini reports", SAFF)]:
    b.append(T(mx, 264, big, 22, c, 800))
    b.append(T(mx, 282, small, 10.5, MUTED))
    mx += 196
b.append(chips(34, 312, ["PyTorch", "timm", "GradCAM", "FastAPI", "React", "FAISS", "Gemini", "Docker", "HF Spaces"], MAG, 11.5))
b.append(T(W-30, 348, "▶ open live demo", 13, MINT, 700, "end", extra='class="pulse"'))
save("ex-rupeeguard.svg", svg(W, H, "\n".join(b), st, "RupeeGuard AI — counterfeit currency detection with explainable AI and RAG", df))

# =============== small cards ===============
CW_, CH_ = 490, 360
def small(name, acc, exhibit, case, title, desc, visual, chiplist, metric, st_extra="", df=""):
    b = card_shell(CW_, CH_, acc, exhibit, case)
    b.append(T(24, 72, title, 25, TEXT, 800, cls="sans"))
    for i, ln in enumerate(desc):
        b.append(T(24, 96 + i*17, ln, 12, MUTED))
    b.append(f'<rect x="24" y="134" width="{CW_-48}" height="112" rx="10" fill="{BG}" stroke="{LINE}"/>')
    b.append(visual)
    b.append(chips(24, 260, chiplist, acc, 11, maxw=CW_-48))
    b.append(f'<line x1="24" y1="{CH_-38}" x2="{CW_-24}" y2="{CH_-38}" stroke="{LINE}"/>')
    b.append(T(24, CH_-17, metric, 11.5, acc, 700))
    b.append(T(CW_-24, CH_-17, "view repo →", 11.5, MUTED, 600, "end"))
    save(name, svg(CW_, CH_, "\n".join(b), BASE_STYLE + st_extra, title, df))

# --- FinSocial: candlesticks + live chat
v = []
price = 200; xs = 40
for i in range(16):
    o = price; c = o + random.uniform(-14, 18); hi = max(o, c) + random.uniform(2, 8); lo = min(o, c) - random.uniform(2, 8)
    price = c
    col = MINT if c >= o else MAG
    x = xs + i * 15
    y = lambda p: 300 - p * 0.7  # map
    v.append(f'<g style="animation:cin 6s {i*0.18:.2f}s infinite both">'
             f'<line x1="{x+4}" y1="{y(hi):.0f}" x2="{x+4}" y2="{y(lo):.0f}" stroke="{col}"/>'
             f'<rect x="{x}" y="{min(y(o),y(c)):.0f}" width="8" height="{max(2,abs(y(o)-y(c))):.0f}" fill="{col}"/></g>')
msgs = [("@arjun", "bought 10 × TCS", MINT), ("@riya", "RAG says: hold", SAFF), ("@dev", "P/L +4.2% today", CYAN)]
for i, (u, m, c) in enumerate(msgs):
    y = 150 + i * 30
    v.append(f'<g style="animation:min 6s {1+i*0.8:.1f}s infinite both">'
             f'<rect x="296" y="{y}" width="170" height="24" rx="12" fill="{PANEL2}" stroke="{c}" stroke-opacity=".5"/>'
             + T(306, y+16, u, 10, c, 700) + T(306 + len(u)*6.2 + 6, y+16, m, 10, TEXT) + '</g>')
v.append(f'<circle class="pulse" cx="282" cy="148" r="4" fill="{MAG}"/>' + T(274, 152, "LIVE", 9, MAG, 700, "end"))
fs_st = '''@keyframes cin{0%{opacity:0;transform:translateY(6px)}6%,85%{opacity:1;transform:none}100%{opacity:0}}
@keyframes min{0%{opacity:0;transform:translateX(12px)}8%,85%{opacity:1;transform:none}100%{opacity:0}}'''
small("ex-finsocial.svg", CYAN, "PROJECT 02", "● LIVE DEMO", "FinSocial",
      ["Social paper-trading brokerage: portfolios, live", "community chat, AI insights via Gemini + pgvector."],
      "".join(v), ["React", "Node", "Express", "PostgreSQL", "pgvector", "Redis", "Socket.IO", "Docker"],
      "16 relational tables · real-time via Redis + WS", fs_st)

# --- HomeHarvest: pantry scanner + growing sprout
v = []
for i in range(6):
    x = 44 + (i % 3) * 58; y = 146 + (i // 3) * 48
    c = [SAFF, MINT, MAG, CYAN, SAFF, MINT][i]
    v.append(f'<rect x="{x}" y="{y+6}" width="40" height="34" rx="6" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".6"/>'
             f'<rect x="{x+6}" y="{y}" width="28" height="8" rx="2" fill="{c}" fill-opacity=".5"/>')
v.append(f'<g style="animation:pscan 4s ease-in-out infinite">{corners(38, 140, 52, 52, 8, MINT, 2)}</g>')
v.append(T(222, 160, "scan → recipe", 10, MUTED, 600))
v.append(T(222, 178, "detected: 6 items", 10, MINT, 600))
# sprout
v.append(f'<path d="M380,236 Q378,200 382,170" fill="none" stroke="{MINT}" stroke-width="3" class="draw" pathLength="1000"/>')
v.append(f'<path d="M381,196 Q350,180 346,160 Q372,166 381,192" fill="{MINT}" fill-opacity=".25" stroke="{MINT}" class="draw" pathLength="1000" style="animation-delay:.6s"/>')
v.append(f'<path d="M382,180 Q410,160 420,140 Q392,146 382,176" fill="{MINT}" fill-opacity=".25" stroke="{MINT}" class="draw" pathLength="1000" style="animation-delay:1s"/>')
v.append(f'<path d="M340,238 H430" stroke="{SAFF}" stroke-width="2"/>')
v.append(T(440, 160, "plant", 9, MUTED, 600, "end") + T(440, 174, "healthy ✓", 10, MINT, 700, "end"))
hh_st = '''@keyframes pscan{0%,100%{transform:translate(0,0)}25%{transform:translate(58px,0)}50%{transform:translate(116px,48px)}75%{transform:translate(0,48px)}}'''
small("ex-homeharvest.svg", MINT, "PROJECT 03", "REPO: COMMIT.ENV", "HomeHarvest AI",
      ["Garden-to-table app: scan your pantry, diagnose", "plants from photos, chat with an AI gardener."],
      "".join(v), ["FastAPI", "MongoDB", "Motor", "Gemini Vision", "Tailwind", "JavaScript"],
      "vision + streaming chat · async pipelines", hh_st)

# --- Emergent behaviors: emergence curve
v = [f'<line x1="50" y1="232" x2="440" y2="232" stroke="{DIM}"/><line x1="50" y1="232" x2="50" y2="146" stroke="{DIM}"/>',
     T(440, 244, "model scale →", 9, MUTED, 600, "end"), T(56, 152, "capability", 9, MUTED, 600)]
pts = []
for i in range(80):
    x = 52 + i * 4.9; s = 1 / (1 + math.exp(-(i - 52) / 3.2))
    pts.append(f"{x:.1f},{228 - s*76 + random.uniform(-1.5,1.5):.1f}")
v.append(f'<path d="M{" L".join(pts)}" fill="none" stroke="{SAFF}" stroke-width="2.4" class="draw" pathLength="1000"/>')
v.append(f'<line x1="306" y1="146" x2="306" y2="232" stroke="{MAG}" stroke-dasharray="3 4"/>')
v.append(T(300, 166, "emergence", 10, MAG, 700, "end"))
v.append(f'<g class="pulse">{T(380, 190, "CoT ✦", 10, MINT, 700)}</g>')
small("ex-llm.svg", SAFF, "PROJECT 04", "RESEARCH REPORT", "Emergent Behaviors in LLMs",
      ["Report on abilities that appear abruptly with", "scale: CoT, forecasting, evaluation, AI safety."],
      "".join(v), ["LaTeX", "Survey", "Scaling laws", "Chain-of-thought", "AI safety"],
      "technical report · typeset in LaTeX")

# --- Portfolio tracker: Swing table with ticking P/L
v = [f'<rect x="36" y="144" width="418" height="18" rx="4" fill="{PANEL2}"/>',
     T(46, 157, "TICKER", 9, MUTED, 700), T(170, 157, "QTY", 9, MUTED, 700), T(260, 157, "AVG", 9, MUTED, 700), T(444, 157, "P/L", 9, MUTED, 700, "end")]
rows = [("INFY", 40, 1462.5, ["+2.14%", "+2.31%", "+1.98%"]), ("TCS", 12, 3890.0, ["-0.62%", "-0.41%", "+0.08%"]),
        ("HDFCBANK", 25, 1601.2, ["+0.93%", "+1.12%", "+0.87%"]), ("RELIANCE", 18, 2874.4, ["-1.05%", "-1.30%", "-0.94%"])]
for i, (tk, q, avg, pl) in enumerate(rows):
    y = 180 + i * 17
    v.append(T(46, y, tk, 10.5, TEXT, 600) + T(170, y, str(q), 10.5, MUTED) + T(260, y, f"{avg:,.1f}", 10.5, MUTED))
    for j, p in enumerate(pl):
        c = MINT if p.startswith("+") else MAG
        v.append(f'<text x="444" y="{y}" font-size="10.5" fill="{c}" font-weight="700" text-anchor="end" style="opacity:{1 if j==0 else 0};animation:tick 9s {j*3}s infinite both">{p}</text>')
v.append(f'<rect x="36" y="238" width="418" height="3" fill="{LINE}"/><rect x="36" y="238" width="418" height="3" fill="{SAFF}" style="transform-box:fill-box;transform-origin:left;animation:ref 3s linear infinite"/>')
pt_st = '''@keyframes tick{0%{opacity:0}2%,31%{opacity:1}34%,100%{opacity:0}}
@keyframes ref{from{transform:scaleX(0)}to{transform:scaleX(1)}}'''
small("ex-portfolio.svg", SAFF, "PROJECT 05", "JAVA · DBMS", "Stock Portfolio Tracker",
      ["Desktop trading desk: multi-portfolio P/L, BUY/", "SELL at weighted-avg cost, simulated market feed."],
      "".join(v), ["Java 17", "Swing", "JDBC", "MySQL 8", "DAO pattern"],
      "prices refresh every 10s · layered MVC + DAO", pt_st)
