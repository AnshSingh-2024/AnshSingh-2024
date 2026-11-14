import math, os, html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# "night shift" palette: midnight navy, desk-lamp amber, energy-drink lime, coral, sky
BG = "#0A0E1A"; PANEL = "#10172A"; PANEL2 = "#151E36"; LINE = "#22304F"
MINT = "#B4F34A"; SAFF = "#FFB547"; MAG = "#FF6B5B"; CYAN = "#6EA8FE"
TEXT = "#ECEFF6"; MUTED = "#8A93A8"; DIM = "#4A5573"; MOON = "#F3EBD3"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"

def esc(s): return html.escape(str(s), quote=True)

def svg(w, h, body, style="", title="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
text{{font-family:{MONO};}}
.sans{{font-family:{SANS};}}
{style}
</style>
<defs>{defs}</defs>
{body}
</svg>'''

def save(name, content):
    p = os.path.join(OUT, name)
    with open(p, "w") as f: f.write(content)
    print(f"{name:28s} {len(content)/1024:6.1f} KB")

def T(x, y, s, size=14, fill=TEXT, weight=400, anchor="start", cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{c} {extra}>{esc(s)}</text>'

def hypotrochoid(cx, cy, R, r, d, scale=1.0, n=900, turns=None):
    if turns is None:
        g = math.gcd(int(R), int(r)); turns = int(r) // g
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * turns * i / n
        x = (R - r) * math.cos(t) + d * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - d * math.sin((R - r) / r * t)
        pts.append(f"{cx + x*scale:.1f},{cy + y*scale:.1f}")
    return "M" + " L".join(pts) + "Z"

def wave(x0, x1, y, amp, freq, phase, step=6):
    pts = []
    x = x0
    while x <= x1:
        pts.append(f"{x:.0f},{y + amp*math.sin(x*freq + phase):.1f}")
        x += step
    return "M" + " L".join(pts)

def chip(x, y, label, color=MINT, size=12):
    w = len(label) * size * 0.62 + 18
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size+12}" rx="{(size+12)/2}" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-opacity="0.45"/>'
            f'{T(x + w/2, y + size + 3, label, size, color, 500, "middle")}'), w

def chips(x, y, labels, color=MINT, size=12, gap=8, maxw=None):
    out = []; cx = x; cy = y
    for l in labels:
        w = len(l) * size * 0.62 + 18
        if maxw and cx + w > x + maxw:
            cx = x; cy += size + 20
        s, w = chip(cx, cy, l, color, size); out.append(s); cx += w + gap
    return "".join(out)

def frame(w, h, rx=16, fill=PANEL, stroke=LINE):
    return f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def corners(x, y, w, h, L=14, color=MINT, sw=2, op=0.9):
    p = (f"M{x},{y+L} V{y} H{x+L} M{x+w-L},{y} H{x+w} V{y+L} "
         f"M{x+w},{y+h-L} V{y+h} H{x+w-L} M{x+L},{y+h} H{x} V{y+h-L}")
    return f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-opacity="{op}"/>'


def can(x, y, label="FUEL", glow=MINT, scale=1.0, cls="", style=""):
    """Generic energy-drink can (own design, no brand marks). x,y = bottom-left."""
    w, h = 34*scale, 66*scale
    top = y - h
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    bolt = (f"M{x+w*.58:.1f},{top+h*.26:.1f} L{x+w*.32:.1f},{top+h*.55:.1f} L{x+w*.5:.1f},{top+h*.55:.1f} "
            f"L{x+w*.4:.1f},{top+h*.8:.1f} L{x+w*.7:.1f},{top+h*.47:.1f} L{x+w*.52:.1f},{top+h*.47:.1f} Z")
    return (f'<g{c}{st}>'
            f'<rect x="{x:.1f}" y="{top+3*scale:.1f}" width="{w:.1f}" height="{h-6*scale:.1f}" rx="{5*scale:.1f}" fill="#141A14" stroke="{glow}" stroke-opacity=".9" stroke-width="{1.2*scale:.1f}"/>'
            f'<rect x="{x+2*scale:.1f}" y="{top+1*scale:.1f}" width="{w-4*scale:.1f}" height="{5*scale:.1f}" rx="{2*scale:.1f}" fill="#9AA3B5"/>'
            f'<rect x="{x+2*scale:.1f}" y="{y-5*scale:.1f}" width="{w-4*scale:.1f}" height="{4*scale:.1f}" rx="{2*scale:.1f}" fill="#7A8296"/>'
            f'<path d="{bolt}" fill="{glow}"/>'
            f'<rect x="{x+3*scale:.1f}" y="{top+8*scale:.1f}" width="{3*scale:.1f}" height="{h-18*scale:.1f}" rx="1" fill="#fff" fill-opacity=".12"/>'
            f'<text x="{x+w/2:.1f}" y="{y-9*scale:.1f}" font-size="{6.5*scale:.1f}" fill="{glow}" font-weight="800" text-anchor="middle" letter-spacing="{.6*scale:.1f}">{esc(label)}</text>'
            '</g>')

def clock_face(cx, cy, r, color=SAFF, ticks=True, numerals=False, face=PANEL):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{face}" stroke="{color}" stroke-opacity=".7" stroke-width="{max(1.2, r/40):.1f}"/>']
    if ticks:
        for i in range(60):
            a = math.radians(i*6); big = i % 5 == 0
            r1 = r*(.84 if big else .91); r2 = r*.96
            o.append(f'<line x1="{cx+r1*math.sin(a):.1f}" y1="{cy-r1*math.cos(a):.1f}" x2="{cx+r2*math.sin(a):.1f}" y2="{cy-r2*math.cos(a):.1f}" stroke="{TEXT if big else DIM}" stroke-width="{(r/55 if big else r/120):.2f}"/>')
    if numerals:
        for n in (12, 3, 6, 9):
            a = math.radians(n*30); rr = r*.7
            o.append(T(f"{cx+rr*math.sin(a):.1f}", f"{cy-rr*math.cos(a)+r*.07:.1f}", str(n), r*.17, MUTED, 700, "middle", "sans"))
    return "".join(o)

def hand(cx, cy, length, width, color, dur, start_deg=0, tail=0.0, cls=""):
    """rotating clock hand; SMIL rotate so it works in every renderer that animates."""
    return (f'<g transform="rotate({start_deg} {cx} {cy})"><line x1="{cx}" y1="{cy + length*tail:.1f}" x2="{cx}" y2="{cy-length:.1f}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="{start_deg} {cx} {cy}" to="{start_deg+360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>')
