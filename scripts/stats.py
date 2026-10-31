"""Genera las tarjetas de estadísticas del perfil (assets/stats.svg, assets/langs.svg,
assets/activity.svg) con el mismo estilo que el resto del README.

Se ejecuta a diario desde .github/workflows/stats.yml usando la API de GitHub.
Uso local:  GITHUB_TOKEN=xxx python scripts/stats.py
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date

USER = os.environ.get("GH_USER", "guilleeca")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT_DIR", "assets")

BG = "#0B1426"; BORDER = "#1E3A5F"; BLUE = "#3B82F6"; CYAN = "#38BDF8"
TXT = "#E6EDF7"; MUT = "#8BA3C7"; SH = "#1D4ED8"; DIM = "#16253F"
SANS = "'Segoe UI','Inter',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
LANG_COLORS = [BLUE, CYAN, "#6366F1", "#22D3EE", "#93C5FD", "#475569"]
MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


def api(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch():
    user = api(f"https://api.github.com/users/{USER}")
    repos = [r for r in api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
             if not r["fork"]]
    langs = Counter()
    for r in repos:
        for k, v in api(r["languages_url"]).items():
            langs[k] += v
    weeks, total = [], None
    if TOKEN:
        q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
               totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
        cal = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}})
        cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total = cal["totalContributions"]
        weeks = [(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"]))
                 for w in cal["weeks"]]
    return {
        "repos": len(repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": user["followers"],
        "since": user["created_at"][:4],
        "langs": langs,
        "weeks": weeks,
        "total": total,
    }


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def frame(w, h, inner, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="gv" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient></defs>
<rect x="10" y="10" width="{w-10}" height="{h-10}" rx="10" fill="{SH}" opacity=".55"/>
<rect x="1" y="1" width="{w-12}" height="{h-12}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<text x="28" y="40" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}" letter-spacing="2">{esc(label)}</text>
{inner}</svg>'''


def stats_svg(d):
    items = [("REPOS", d["repos"]), ("ESTRELLAS", d["stars"]), ("SEGUIDORES", d["followers"]),
             ("CONTRIBUCIONES", d["total"] if d["total"] is not None else "—"), ("EN GITHUB DESDE", d["since"])]
    s = ""
    for i, (k, v) in enumerate(items):
        y = 78 + i * 34
        s += f'<text x="28" y="{y}" font-family="{MONO}" font-size="12" fill="{MUT}" letter-spacing="1.5">{k}</text>'
        s += f'<line x1="205" y1="{y-4}" x2="320" y2="{y-4}" stroke="{DIM}" stroke-dasharray="2 4"/>'
        s += f'<text x="372" y="{y+1}" text-anchor="end" font-family="{SANS}" font-size="18" font-weight="800" fill="{TXT}">{esc(v)}</text>'
    return frame(410, 250, s, "◆ ESTADÍSTICAS")


def langs_svg(d):
    total = sum(d["langs"].values()) or 1
    top = d["langs"].most_common(5)
    rest = total - sum(v for _, v in top)
    if rest > 0:
        top.append(("Otros", rest))
    s, x, bw = "", 28, 354
    s += f'<rect x="28" y="62" width="{bw}" height="12" rx="6" fill="{DIM}"/>'
    s += f'<clipPath id="c"><rect x="28" y="62" width="{bw}" height="12" rx="6"/></clipPath><g clip-path="url(#c)">'
    for i, (k, v) in enumerate(top):
        w = bw * v / total
        s += f'<rect x="{x:.1f}" y="62" width="{w:.1f}" height="12" fill="{LANG_COLORS[i]}"/>'
        x += w
    s += "</g>"
    alias = {"Jupyter Notebook": "Jupyter"}
    for i, (k, v) in enumerate(top):
        k = alias.get(k, k)
        k = k if len(k) <= 12 else k[:11] + "…"
        col, row = i % 2, i // 2
        cx, cy = 34 + col * 180, 106 + row * 34
        s += f'<circle cx="{cx}" cy="{cy-5}" r="5" fill="{LANG_COLORS[i]}"/>'
        s += f'<text x="{cx+14}" y="{cy}" font-family="{SANS}" font-size="14" font-weight="600" fill="{TXT}">{esc(k)}</text>'
        s += f'<text x="{cx+150}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUT}">{100*v/total:.1f}%</text>'
    if not top:
        s += f'<text x="28" y="110" font-family="{SANS}" font-size="14" fill="{MUT}">Sin datos todavía</text>'
    return frame(410, 250, s, "◆ LENGUAJES MÁS USADOS")


def activity_svg(d):
    W, H = 840, 230
    weeks = d["weeks"][-52:]
    label = "◆ CONTRIBUCIONES · ÚLTIMO AÑO" + (f" · {d['total']}" if d["total"] is not None else "")
    if not weeks:
        s = f'<text x="28" y="120" font-family="{SANS}" font-size="14" fill="{MUT}">Se actualizará en la próxima ejecución diaria.</text>'
        return frame(W, H, s, label)
    x0, y0, ch, gap = 28, 190, 120, 14.6
    mx = max(c for _, c in weeks) or 1
    s = ""
    for i in range(4):
        y = y0 - ch * i / 3
        s += f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+gap*len(weeks)}" y2="{y:.1f}" stroke="{DIM}" stroke-dasharray="2 4"/>'
    last_m = None
    for i, (day, c) in enumerate(weeks):
        h = max(2, ch * c / mx) if c else 2
        x = x0 + i * gap
        s += f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="10" height="{h:.1f}" rx="2" fill="{"url(#gv)" if c else DIM}"/>'
        m = int(day[5:7])
        if m != last_m:
            s += f'<text x="{x:.1f}" y="{y0+20}" font-family="{MONO}" font-size="11" fill="{MUT}">{MESES[m-1]}</text>'
            last_m = m
    s += f'<text x="{W-40}" y="40" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUT}">máx. {mx}/semana</text>'
    return frame(W, H, s, label)


def main():
    d = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else fetch()
    d["langs"] = Counter(d["langs"])
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("stats", stats_svg), ("langs", langs_svg), ("activity", activity_svg)]:
        with open(f"{OUT}/{name}.svg", "w", encoding="utf-8") as f:
            f.write(fn(d))
    print("Tarjetas generadas", date.today())


if __name__ == "__main__":
    main()
