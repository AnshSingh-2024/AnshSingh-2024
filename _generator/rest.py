from common import *
import random
random.seed(3)

# ================= ARCHITECTURE: stack as a neural network =================
W, H = 1000, 470
layers = [
    ("INPUT", "languages", MINT, ["C++", "Java", "Python", "JavaScript"]),
    ("ENCODER", "backend", CYAN, ["FastAPI", "Node.js", "Express", "REST · JWT"]),
    ("MEMORY", "data", SAFF, ["PostgreSQL", "MongoDB", "MySQL", "Redis", "pgvector", "FAISS"]),
    ("ATTENTION", "AI / ML", MAG, ["PyTorch", "EffNet · ViT", "RAG", "GradCAM · SHAP", "XGBoost", "Gemini API"]),
    ("OUTPUT", "ships", MINT, ["React", "Tailwind", "Docker", "HF Spaces", "Git"]),
]
colx = [22, 218, 414, 610, 806]; PW = 166; PH = 30
top, bot = 92, 440
nodes = []
for li, (n, sub, c, items) in enumerate(layers):
    k = len(items); gap = (bot - top - k*PH) / (k + 1)
    ys = [top + gap*(i+1) + PH*i + PH/2 for i in range(k)]
    nodes.append([(colx[li], y, it, c) for y, it in zip(ys, items)])

st = '''
.n{transform-box:fill-box;transform-origin:center;animation:np 4s ease-in-out infinite}
@keyframes np{0%,100%{stroke-opacity:.45}50%{stroke-opacity:1}}
.e{stroke-opacity:.09}
.hl{stroke-dasharray:4 7;animation:fl 1.2s linear infinite;stroke-opacity:.5}
@keyframes fl{to{stroke-dashoffset:-11}}
.lbl{opacity:0;animation:fi .6s ease forwards} @keyframes fi{to{opacity:1}}
'''
b = [frame(W, H, 16, PANEL)]
b.append(T(24, 34, "ansh.forward(problem) → product", 14, TEXT, 700))
b.append(T(W-24, 34, "params: 30+ tools · activation: curiosity", 11, MUTED, 500, "end"))
for li, (n, sub, c, _) in enumerate(layers):
    x = colx[li] + PW/2
    b.append(T(x, 66, n, 11, c, 800, "middle", extra='letter-spacing="2.5"'))
    b.append(T(x, 81, sub, 10, MUTED, 500, "middle"))
edges = []
for li in range(len(nodes)-1):
    for (x1, y1, _, c1) in nodes[li]:
        for (x2, y2, _, c2) in nodes[li+1]:
            sx, ex = x1 + PW, x2
            d = f"M{sx},{y1:.0f} C{sx+40},{y1:.0f} {ex-40},{y2:.0f} {ex},{y2:.0f}"
            edges.append((d, c2))
            b.append(f'<path class="e" d="{d}" fill="none" stroke="{c1}"/>')
sel = random.sample(edges, 26)
for i, (d, c) in enumerate(sel[:10]):
    b.append(f'<path class="hl" d="{d}" fill="none" stroke="{c}"/>')
for i, (d, c) in enumerate(sel):
    dur = 1.6 + random.random()*1.2
    b.append(f'<circle r="2.6" fill="{c}"><animateMotion dur="{dur:.2f}s" begin="{random.random()*2:.2f}s" repeatCount="indefinite" path="{d}"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur:.2f}s" repeatCount="indefinite"/></circle>')
for li, col in enumerate(nodes):
    for ni, (x, y, it, c) in enumerate(col):
        dl = (li*0.35 + ni*0.12)
        b.append(f'<rect class="n" style="animation-delay:{dl:.2f}s" x="{x}" y="{y-PH/2:.0f}" width="{PW}" height="{PH}" rx="{PH/2}" fill="{BG}" stroke="{c}"/>')
        b.append(f'<circle cx="{x+14}" cy="{y:.0f}" r="3.5" fill="{c}"/>')
        b.append(T(x + PW/2 + 6, y + 4.5, it, 12.5, TEXT, 600, "middle"))
save("arch.svg", svg(W, H, "\n".join(b), st, "Tech stack as a neural network: languages, backend, data, AI/ML, deployment"))

# ================= ARENA: competitive programming =================
W, H = 1000, 340
st = '''
.rise{animation:rise 2.4s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:bottom}
@keyframes rise{from{transform:scaleY(0)}}
.mk{animation:fi .5s ease 2.2s both} @keyframes fi{from{opacity:0}}
.spin{transform-box:fill-box;transform-origin:center;animation:sp 18s linear infinite} @keyframes sp{to{transform:rotate(360deg)}}
.spin2{animation-direction:reverse;animation-duration:26s}
.pulse{animation:pu 2s ease-in-out infinite} @keyframes pu{50%{opacity:.35}}
.bfs{animation:bfs 4s infinite} @keyframes bfs{0%{fill:#0B1016;stroke-opacity:.4}12%,60%{fill:currentColor;stroke-opacity:1}100%{fill:#0B1016;stroke-opacity:.4}}
.be{stroke-opacity:.15;animation:be 4s infinite} @keyframes be{12%,60%{stroke-opacity:.8}0%,100%{stroke-opacity:.15}}
'''
b = [frame(W, H, 16, PANEL)]
PWd = 312
def panel(x, title, c):
    return (f'<rect x="{x}" y="18" width="{PWd}" height="{H-36}" rx="12" fill="{BG}" stroke="{c}" stroke-opacity=".35"/>'
            + T(x+18, 44, title, 11, c, 800, extra='letter-spacing="2"'))
# --- LeetCode tier gauge
x0 = 18; b.append(panel(x0, "LEETCODE · CONTEST", MINT))
gx, gy0, gy1 = x0+40, 290, 70   # rating 1400..2400 mapped
def ry(r): return gy0 - (r-1400)/(2400-1400)*(gy0-gy1)
tiers = [(1400, 1850, "rated", DIM), (1850, 2150, "KNIGHT", MINT), (2150, 2400, "GUARDIAN", SAFF)]
for lo, hi, lab, c in tiers:
    b.append(f'<rect x="{gx}" y="{ry(hi):.0f}" width="26" height="{ry(lo)-ry(hi):.0f}" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".4"/>')
    b.append(T(gx+36, (ry(lo)+ry(hi))/2+4, lab, 10, c, 700))
for r in (1400, 1850, 2150, 2400):
    b.append(T(gx-6, ry(r)+4, str(r), 9, MUTED, 500, "end"))
b.append(f'<rect class="rise" x="{gx+6}" y="{ry(2033):.0f}" width="14" height="{gy0-ry(2033):.0f}" rx="3" fill="{MINT}"/>')
b.append(f'<g class="mk"><line x1="{gx-2}" y1="{ry(2033):.0f}" x2="{x0+PWd-20}" y2="{ry(2033):.0f}" stroke="{MINT}" stroke-dasharray="3 3"/>'
         + T(x0+PWd-20, ry(2033)-8, "max 2033", 20, TEXT, 800, "end") + '</g>')
b.append(T(x0+PWd-20, ry(2033)+22, "top 2.19% worldwide", 11, MINT, 600, "end"))
b.append(T(x0+PWd-20, 300, "Ansh_Singh5245", 10, MUTED, 500, "end"))
# --- ICPC badge
x1 = 18 + PWd + 16; b.append(panel(x1, "ICPC · ASIA WEST", MAG))
cx, cy = x1 + PWd/2, 160
def hexp(r):
    return " ".join(f"{cx + r*math.cos(math.radians(60*i-90)):.1f},{cy + r*math.sin(math.radians(60*i-90)):.1f}" for i in range(6))
b.append(f'<g class="spin"><circle cx="{cx}" cy="{cy}" r="92" fill="none" stroke="{MAG}" stroke-opacity=".5" stroke-dasharray="2 6"/></g>')
b.append(f'<g class="spin spin2"><circle cx="{cx}" cy="{cy}" r="82" fill="none" stroke="{SAFF}" stroke-opacity=".4" stroke-dasharray="18 10 4 10"/></g>')
b.append(f'<polygon points="{hexp(70)}" fill="{MAG}" fill-opacity=".08" stroke="{MAG}" stroke-width="2"/>')
b.append(f'<polygon points="{hexp(60)}" fill="none" stroke="{MAG}" stroke-opacity=".4"/>')
b.append(T(cx, cy-14, "REGIONALIST", 10.5, MAG, 800, "middle", extra='letter-spacing="2"'))
b.append(T(cx, cy+18, "2026", 30, TEXT, 900, "middle", "sans"))
b.append(T(cx, cy+38, "Amritapuri", 10, MUTED, 600, "middle"))
b.append(T(cx, 290, "Rank 269 · Asia West Amritapuri Regional", 11.5, TEXT, 700, "middle"))
b.append(f'<g class="pulse">{T(cx, 306, "the olympics of college programming", 10, MUTED, 500, "middle")}</g>')
# --- Codeforces / BFS
x2 = x1 + PWd + 16; b.append(panel(x2, "CODEFORCES · +5 JUDGES", CYAN))
gnodes = {0: (x2+156, 92)}
lvl = [[0]]; nid = 1; edges = []
for L, cnt in enumerate([3, 5, 6]):
    row = []
    for i in range(cnt):
        x = x2 + 30 + (PWd-60) * (i + .5) / cnt; y = 92 + (L+1)*44
        gnodes[nid] = (x, y); par = min(lvl[-1], key=lambda p: abs(gnodes[p][0]-x)); edges.append((par, nid, L+1)); row.append(nid); nid += 1
    lvl.append(row)
for a, c_, L in edges:
    (ax, ay), (cx2, cy2) = gnodes[a], gnodes[c_]
    b.append(f'<line class="be" style="animation-delay:{L*.45:.2f}s" x1="{ax:.0f}" y1="{ay}" x2="{cx2:.0f}" y2="{cy2}" stroke="{CYAN}"/>')
depth = {0: 0}
for a, c_, L in edges: depth[c_] = L
for k, (x, y) in gnodes.items():
    b.append(f'<circle class="bfs" style="color:{CYAN};animation-delay:{depth[k]*.45:.2f}s" cx="{x:.0f}" cy="{y}" r="8" fill="{PANEL}" stroke="{CYAN}" stroke-width="1.5"/>')
b.append(T(x2+PWd-18, 44, "BFS(1300+)", 10, MUTED, 600, "end"))
b.append(T(x2+18, 262, "SPECIALIST", 20, CYAN, 900, extra='letter-spacing="1"'))
b.append(T(x2+18, 282, "on Codeforces · Learn2SolveP", 11, MUTED, 500))
b.append(T(x2+18, 302, "1300+ solved · LC · CF · CC · AZ · HR · TUF", 10, TEXT, 500))
save("arena.svg", svg(W, H, "\n".join(b), st, "Competitive programming: LeetCode Knight max 2033, ICPC Asia West Regionalist 2026 rank 269 (Asia West Amritapuri Regional), Codeforces Specialist, 1300+ problems"))

