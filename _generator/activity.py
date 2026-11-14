"""
Night-shift activity renderer.

Pulls REAL data from the GitHub GraphQL API and redraws the contribution heatmap SVG:
  assets/contrib.svg       - last-year contribution heatmap that builds itself

Run by .github/workflows/night-shift.yml every night. Needs GITHUB_TOKEN.
  python3 activity.py                 -> live data (env GITHUB_TOKEN, GH_USER)
  python3 activity.py --placeholder   -> "first sync pending" frames
  python3 activity.py --mock          -> synthetic data, for local layout tests only
Standard library only.
"""
import os, sys, json, math, random, datetime as dt, urllib.request
from collections import Counter
from common import *

USER = os.environ.get("GH_USER", "AnshSingh-2024")
TZ = dt.timezone(dt.timedelta(hours=5, minutes=30))  # IST
NIGHT = {22, 23, 0, 1, 2, 3, 4, 5}

# --------------------------------------------------------------- data
def gql(query, variables):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json",
                 "User-Agent": "night-shift-readme"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    if out.get("errors"):
        raise SystemExit(f"GraphQL error: {out['errors']}")
    return out["data"]

Q_USER = """query($login:String!){ user(login:$login){ id
  contributionsCollection{ contributionCalendar{ totalContributions
    weeks{ contributionDays{ date contributionCount weekday } } } } } }"""
Q_REPOS = """query($login:String!,$id:ID!,$cursor:String){ user(login:$login){
  repositories(first:50, after:$cursor, ownerAffiliations:OWNER, orderBy:{field:PUSHED_AT,direction:DESC}){
    pageInfo{ hasNextPage endCursor }
    nodes{ name isFork stargazerCount primaryLanguage{ name color }
      defaultBranchRef{ target{ ... on Commit{ history(first:100, author:{id:$id}){ totalCount nodes{ authoredDate } } } } } } } } }"""

def fetch_live():
    u = gql(Q_USER, {"login": USER})["user"]
    cal = u["contributionsCollection"]["contributionCalendar"]
    repos, cursor = [], None
    for _ in range(4):
        r = gql(Q_REPOS, {"login": USER, "id": u["id"], "cursor": cursor})["user"]["repositories"]
        for n in r["nodes"]:
            ref = n.get("defaultBranchRef") or {}
            hist = (ref.get("target") or {}).get("history") or {"totalCount": 0, "nodes": []}
            repos.append({"name": n["name"], "stars": n["stargazerCount"],
                          "lang": (n.get("primaryLanguage") or {}).get("name") or "—",
                          "color": (n.get("primaryLanguage") or {}).get("color") or MUTED,
                          "commits": hist["totalCount"], "times": [x["authoredDate"] for x in hist["nodes"]]})
        if not r["pageInfo"]["hasNextPage"]: break
        cursor = r["pageInfo"]["endCursor"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return {"total": cal["totalContributions"], "weeks": cal["weeks"], "days": days, "repos": repos}

def fetch_mock():
    random.seed(4)
    today = dt.date.today(); start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    weeks, days = [], []
    for w in range(53):
        wk = []
        for d in range(7):
            day = start + dt.timedelta(days=w*7 + d)
            if day > today: break
            c = max(0, int(random.gauss(2, 3))) if random.random() > .35 else 0
            e = {"date": day.isoformat(), "contributionCount": c, "weekday": d}; wk.append(e); days.append(e)
        weeks.append({"contributionDays": wk})
    hours = [0,1,2,2,3,23,22,1,14,15,16,11,2,3,1,0,21,22,23,20,10,2,1,3,4]
    repos = []
    for name, lang, color, n in [("RupeeGuard-AI","JavaScript","#f1e05a",64),("FinSocial","JavaScript","#f1e05a",41),
                                 ("COMMIT.ENV","JavaScript","#f1e05a",23),("stock-market-portfolio-tracker","Java","#b07219",4),
                                 ("Technical-Report-Emergent-Behaviors-in-LLMs","TeX","#3D6117",6),("Project-Gamora","HTML","#e34c26",1)]:
        times = [f"2026-0{random.randint(1,9)}-1{random.randint(0,9)}T{(random.choice(hours)-5)%24:02d}:{random.randint(0,59):02d}:00Z" for _ in range(n)]
        repos.append({"name": name, "stars": random.randint(0,3), "lang": lang, "color": color, "commits": n, "times": times})
    return {"total": sum(d["contributionCount"] for d in days), "weeks": weeks, "days": days, "repos": repos}

# --------------------------------------------------------------- stats
def streaks(days):
    best = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] > 0 else 0; best = max(best, cur)
    tail = list(days)
    if tail and tail[-1]["contributionCount"] == 0: tail = tail[:-1]   # today not over yet
    now = 0
    for d in reversed(tail):
        if d["contributionCount"] > 0: now += 1
        else: break
    return best, now

def hours_hist(repos):
    h = Counter()
    for r in repos:
        for t in r["times"]:
            when = dt.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(TZ)
            h[when.hour] += 1
    return [h.get(i, 0) for i in range(24)]

# --------------------------------------------------------------- renderers
def shell(w, h, title, sub):
    return [frame(w, h, 16, PANEL), T(28, 42, title, 16, TEXT, 800, cls="sans"), T(28, 62, sub, 11.5, MUTED, 500)]

def stamp(w):
    now = dt.datetime.now(TZ).strftime("%d %b %Y · %H:%M IST")
    return T(w - 28, 42, f"synced {now}", 11, DIM, 600, "end")

def render_clock(hist):
    W, H = 1000, 490
    cx, cy, r0, rmax = 250, 290, 66, 160
    total = sum(hist); mx = max(hist) or 1
    late = sum(hist[i] for i in (0, 1, 2, 3, 4, 5)); night = sum(hist[i] for i in NIGHT)
    peak = max(range(24), key=lambda i: hist[i]) if total else 2
    cans = round(late / 3)
    st = '''.bar{transform-box:fill-box;transform-origin:bottom;animation:grow 14s cubic-bezier(.2,.8,.2,1) infinite both}
@keyframes grow{0%{transform:scaleY(0)}12%,92%{transform:scaleY(1)}100%{transform:scaleY(1);opacity:.4}}
.cn{animation:cdrop 14s cubic-bezier(.3,1.4,.5,1) infinite both} @keyframes cdrop{0%{transform:translateY(-60px);opacity:0}6%,94%{transform:none;opacity:1}100%{opacity:0}}
.pk{animation:pk 1.6s ease-in-out infinite} @keyframes pk{50%{opacity:.35}}'''
    b = shell(W, H, "the commit clock", "every commit I authored, placed on a 24-hour dial (IST)") + [stamp(W)]
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{rmax+14}" fill="{BG}" stroke="{LINE}"/>')
    # night arc shading 22:00 -> 06:00
    def pt(hr, rr):
        a = math.radians(hr * 15); return cx + rr*math.sin(a), cy - rr*math.cos(a)
    x1, y1 = pt(22, rmax+14); x2, y2 = pt(6, rmax+14)
    b.append(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{rmax+14},{rmax+14} 0 0,1 {x2:.1f},{y2:.1f} Z" fill="{MINT}" fill-opacity=".05"/>')
    for g in (.33, .66, 1):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r0 + (rmax-r0)*g:.0f}" fill="none" stroke="{LINE}" stroke-dasharray="2 4"/>')
    for i, v in enumerate(hist):
        ln = 4 + (rmax - r0 - 4) * v / mx
        col = MINT if i in NIGHT else SAFF
        b.append(f'<g transform="rotate({i*15 + 7.5} {cx} {cy})"><rect class="bar" style="animation-delay:{i*.06:.2f}s" x="{cx-7}" y="{cy - r0 - ln:.1f}" width="14" height="{ln:.1f}" rx="4" fill="{col}" fill-opacity="{.35 + .65*(v/mx):.2f}"/></g>')
    for hr, lab in [(0, "00"), (3, "03"), (6, "06"), (9, "09"), (12, "12"), (15, "15"), (18, "18"), (21, "21")]:
        x, y = pt(hr, rmax + 30); b.append(T(f"{x:.1f}", f"{y+4:.1f}", lab, 11, MUTED if hr % 6 else TEXT, 700, "middle"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r0-6}" fill="{PANEL2}" stroke="{LINE}"/>')
    b.append(hand(cx, cy, rmax + 6, 1.4, MAG, 24, 0))
    b.append(T(cx, cy - 8, f"{peak:02d}:00", 22, MINT if peak in NIGHT else SAFF, 800, "middle"))
    b.append(T(cx, cy + 12, "peak hour", 10, MUTED, 600, "middle"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{MAG}"/>')
    # right column: numbers
    rx = 500
    def big(y, val, lab, col):
        y += 20
        return T(rx, y, val, 34, col, 800, cls="sans") + T(rx, y + 20, lab, 11.5, MUTED, 600)
    b.append(big(140, f"{total}", "commits analysed (latest 100 per repo)", TEXT))
    b.append(big(214, f"{(100*night/total if total else 0):.0f}%", "of them between 22:00 and 06:00", MINT))
    b.append(big(288, f"{late}", "commits after midnight", SAFF))
    b.append(T(rx, 364, f"≈ {cans} cans of energy drink", 17, MAG, 800, cls="sans"))
    b.append(T(rx, 384, "1 can per 3 after-midnight commits (very unscientific)", 11, MUTED, 500))
    show = min(cans, 11)
    for k in range(show):
        b.append(can(rx + k*38, 462, "", [MINT, SAFF, CYAN, MAG][k % 4], .78, "cn", f"animation-delay:{.4 + k*.18:.2f}s"))
    if cans > show:
        b.append(T(rx + show*38 + 6, 446, f"+{cans-show}", 15, MAG, 800))
    return svg(W, H, "\n".join(b), st, f"Commit clock: {total} commits, peak hour {peak:02d}:00 IST, {late} after midnight")

def render_contrib(data):
    weeks = data["weeks"]; days = data["days"]
    W, H = 1000, 300
    best, now = streaks(days)
    vals = sorted(d["contributionCount"] for d in days if d["contributionCount"] > 0)
    q = [vals[int(len(vals)*f)] if vals else 1 for f in (.25, .5, .75)]
    def lvl(c):
        if c == 0: return 0
        return 1 + sum(c > x for x in q)
    shades = [LINE, "#3B5A1E", "#5E8F25", "#89C934", MINT]
    top = max(days, key=lambda d: d["contributionCount"]) if days else {"date": "-", "contributionCount": 0}
    wd = Counter()
    for d in days: wd[d["weekday"]] += d["contributionCount"]
    busiest = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][max(range(7), key=lambda i: wd[i])] if days else "-"
    st = '''.wk{animation:wk 16s ease infinite both} @keyframes wk{0%{opacity:0;transform:translateY(6px)}4%,92%{opacity:1;transform:none}100%{opacity:.25}}'''
    b = shell(W, H, "a year of shifts", "contribution calendar, last 12 months · builds one week at a time") + [stamp(W)]
    cell, gap = 13, 3; gx = 100; gy = 96
    for i, n in enumerate(["Mon", "Wed", "Fri"]):
        b.append(T(gx - 10, gy + (1 + 2*i)*(cell+gap) + 10, n, 9.5, MUTED, 600, "end"))
    last_m = None
    for wi, w in enumerate(weeks[-53:]):
        cells = []
        for d in w["contributionDays"]:
            y = gy + d["weekday"]*(cell+gap)
            cells.append(f'<rect x="{gx + wi*(cell+gap)}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{shades[lvl(d["contributionCount"])]}"><title>{d["date"]}: {d["contributionCount"]}</title></rect>')
            m = d["date"][5:7]
            if d["weekday"] == 0 and m != last_m:
                last_m = m
                b.append(T(gx + wi*(cell+gap), gy - 10, dt.date(2000, int(m), 1).strftime("%b"), 9.5, MUTED, 600))
        b.append(f'<g class="wk" style="animation-delay:{wi*.05:.2f}s">' + "".join(cells) + '</g>')
    lx = W - 28 - (5*16 + 70)
    b.append(T(lx, 74, "less", 9.5, MUTED, 600))
    for i, c in enumerate(shades):
        b.append(f'<rect x="{lx + 30 + i*16}" y="{64}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>')
    b.append(T(lx + 30 + 5*16 + 4, 74, "more", 9.5, MUTED, 600))
    yl = gy + 7*(cell+gap) + 40
    slot = (W - 56) / 5
    for i, (val, lab, col) in enumerate([(data["total"], "contributions", TEXT), (best, "longest streak (days)", MINT), (now, "current streak", SAFF),
                          (top["contributionCount"], f"best day · {top['date']}", CYAN), (busiest, "busiest weekday", MAG)]):
        x = 28 + i*slot
        b.append(f'<rect x="{x}" y="{yl-26}" width="{slot-12:.0f}" height="54" rx="10" fill="{BG}" stroke="{LINE}"/>')
        b.append(T(x + 14, yl + 2, str(val), 20, col, 800, cls="sans") + T(x + 14, yl + 19, lab, 10, MUTED, 600))
    return svg(W, H, "\n".join(b), st, f"{data['total']} contributions in the last year; longest streak {best} days")

def render_pulse(repos):
    rs = sorted([r for r in repos if r["commits"] > 0], key=lambda r: -r["commits"])[:7]
    W = 1000; RH = 40; H = 100 + RH*max(1, len(rs)) + 10
    mx = max([r["commits"] for r in rs] or [1])
    st = '''.pb{transform-box:fill-box;transform-origin:left;animation:pb 12s cubic-bezier(.2,.8,.2,1) infinite both}
@keyframes pb{0%{transform:scaleX(0)}14%,92%{transform:scaleX(1)}100%{transform:scaleX(1);opacity:.4}}
.pn{animation:pn 12s ease infinite both} @keyframes pn{0%,10%{opacity:0}16%,100%{opacity:1}}'''
    b = shell(W, H, "repo pulse", "where my commits actually go · bars grow in commit order") + [stamp(W)]
    for i, r in enumerate(rs):
        y = 92 + i*RH
        nm = r["name"] if len(r["name"]) <= 30 else r["name"][:28] + "…"
        bw = 520 * r["commits"] / mx
        b.append(f'<circle cx="34" cy="{y+12}" r="5" fill="{r["color"]}"/>')
        b.append(T(48, y + 16, nm, 13, TEXT, 600))
        b.append(T(48 + 0, y + 31, f'{r["lang"]} · ★ {r["stars"]}', 10, MUTED, 500))
        b.append(f'<rect x="310" y="{y+2}" width="520" height="20" rx="6" fill="{BG}"/>')
        b.append(f'<rect class="pb" style="animation-delay:{.2 + i*.22:.2f}s" x="310" y="{y+2}" width="{max(bw,6):.1f}" height="20" rx="6" fill="{[MINT, SAFF, CYAN, MAG][i % 4]}" fill-opacity=".85"/>')
        b.append(f'<g class="pn" style="animation-delay:{.2 + i*.22:.2f}s">' + T(310 + max(bw, 6) + 10, y + 17, f'{r["commits"]} commit' + ('s' if r['commits'] != 1 else ''), 12, TEXT, 700) + '</g>')
    return svg(W, H, "\n".join(b), st, "Repo pulse: " + ", ".join(f'{r["name"]} {r["commits"]}' for r in rs))

def render_placeholder(name, w, h, title):
    st = '''.sp{transform-box:fill-box;transform-origin:center;animation:sp 2s linear infinite} @keyframes sp{to{transform:rotate(360deg)}}
.pl{animation:pl 1.4s ease-in-out infinite} @keyframes pl{50%{opacity:.3}}'''
    b = [frame(w, h, 16, PANEL), T(28, 42, title, 16, TEXT, 800, cls="sans"),
         clock_face(w/2, h/2 - 14, 34, SAFF, True, False, BG), hand(w/2, h/2 - 14, 26, 2, MAG, 2, 0),
         f'<circle cx="{w/2}" cy="{h/2-14}" r="3" fill="{MAG}"/>',
         f'<g class="pl">{T(w/2, h/2 + 44, "first sync pending", 14, TEXT, 700, "middle")}</g>',
         T(w/2, h/2 + 64, "the Night Shift workflow redraws this from real GitHub data every week", 11.5, MUTED, 500, "middle")]
    save(name, svg(w, h, "\n".join(b), st, f"{title} (waiting for first sync)"))

if __name__ == "__main__":
    if "--placeholder" in sys.argv:
        render_placeholder("contrib.svg", 1000, 300, "a year of shifts")
        sys.exit()
    data = fetch_mock() if "--mock" in sys.argv else fetch_live()
    pre = "mock-" if "--mock" in sys.argv else ""
    save(pre + "contrib.svg", render_contrib(data))
