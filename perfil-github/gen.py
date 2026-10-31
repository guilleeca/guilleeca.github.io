import os
A="assets"
BG="#0B1426"; BORDER="#1E3A5F"; BLUE="#3B82F6"; CYAN="#38BDF8"; TXT="#E6EDF7"; MUT="#8BA3C7"; SH="#1D4ED8"
SANS="'Segoe UI','Inter',Helvetica,Arial,sans-serif"
MONO="'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def save(n,s): open(f"{A}/{n}","w").write(s)
def defs(extra=""):
    return f'''<defs>
<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#16253F" stroke-width="1"/></pattern>
{extra}</defs>'''
def card(w,h,grid=True):
    return f'''<rect x="10" y="10" width="{w-10}" height="{h-10}" rx="10" fill="{SH}" opacity=".55"/>
<rect x="1" y="1" width="{w-12}" height="{h-12}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
{f'<rect x="2" y="2" width="{w-14}" height="{h-14}" rx="9" fill="url(#grid)" opacity=".7"/>' if grid else ''}'''

W,H=840,350
nodes=["INGEST","PROCESS","MODEL","SERVE"]
nx,ny0,gap=700,52,62
pipe=f'<line x1="{nx}" y1="{ny0}" x2="{nx}" y2="{ny0+gap*3}" stroke="{BORDER}" stroke-width="2"/>'
pipe+=f'<line x1="{nx}" y1="{ny0}" x2="{nx}" y2="{ny0+gap*3}" stroke="url(#g)" stroke-width="2" stroke-dasharray="6 10"><animate attributeName="stroke-dashoffset" from="32" to="0" dur="1.2s" repeatCount="indefinite"/></line>'
for i,n in enumerate(nodes):
    y=ny0+gap*i
    pipe+=f'''<rect x="{nx-62}" y="{y-17}" width="124" height="34" rx="8" fill="#0F1D36" stroke="{BLUE}" stroke-width="1.5"/>
<circle cx="{nx-46}" cy="{y}" r="4" fill="{CYAN}"><animate attributeName="opacity" values="1;.25;1" dur="2.4s" begin="{i*0.6}s" repeatCount="indefinite"/></circle>
<text x="{nx+6}" y="{y+5}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{TXT}" letter-spacing="1.5">{n}</text>'''
pipe+=f'<circle cx="{nx}" r="5" fill="{CYAN}"><animate attributeName="cy" values="{ny0};{ny0+gap*3}" dur="2.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" dur="2.4s" repeatCount="indefinite"/></circle>'
def bar(x,y,label,n=20,fill=17):
    s=f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="12" fill="{MUT}" letter-spacing="1.5">{label}</text>'
    for i in range(n):
        on=i<fill
        s+=f'<rect x="{x+i*17}" y="{y+10}" width="13" height="10" rx="2" fill="{"url(#g)" if on else "#16253F"}">'
        if on: s+=f'<animate attributeName="opacity" values="1;.45;1" dur="2s" begin="{i*0.08}s" repeatCount="indefinite"/>'
        s+='</rect>'
    return s
typed="> transformando datos en decisiones"
header=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{defs(f'<clipPath id="type"><rect x="48" y="238" height="30" width="0"><animate attributeName="width" values="0;330;330;0" keyTimes="0;.45;.9;1" dur="6s" repeatCount="indefinite"/></rect></clipPath>')}
{card(W,H)}
<text x="48" y="64" font-family="{MONO}" font-size="14" font-weight="700" fill="{CYAN}" letter-spacing="3">◆ DATA ENGINEER · BIG DATA · ML</text>
<text x="46" y="128" font-family="{SANS}" font-size="50" font-weight="800" fill="{TXT}">Guillermo</text>
<text x="46" y="182" font-family="{SANS}" font-size="50" font-weight="800" fill="url(#g)">Caminero Araus</text>
<text x="48" y="220" font-family="{SANS}" font-size="17" fill="{MUT}">Data Science &amp; Engineering student · UPM, Madrid</text>
<g clip-path="url(#type)"><text x="48" y="258" font-family="{MONO}" font-size="15" fill="{BLUE}">{esc(typed)}</text></g>
<rect x="48" y="244" width="9" height="18" fill="{CYAN}"><animate attributeName="x" values="48;380;380;48" keyTimes="0;.45;.9;1" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
{pipe}
{bar(48,298,"DATA ENGINEERING")}
{bar(440,298,"MACHINE LEARNING",fill=15)}
</svg>'''
save("header.svg",header)

icons={
"linkedin":f'<rect x="22" y="15" width="22" height="22" rx="4" fill="none" stroke="{CYAN}" stroke-width="2"/><text x="33" y="32" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="800" fill="{CYAN}">in</text>',
"email":f'<rect x="20" y="17" width="26" height="18" rx="3" fill="none" stroke="{CYAN}" stroke-width="2"/><path d="M21 19l12 9 12-9" fill="none" stroke="{CYAN}" stroke-width="2"/>',
"repos":f'<path d="M27 18l-7 8 7 8M39 18l7 8-7 8" fill="none" stroke="{CYAN}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
}
for k,label in [("linkedin","LINKEDIN"),("email","EMAIL"),("repos","PROYECTOS")]:
    save(f"btn-{k}.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="210" height="58" viewBox="0 0 210 58">
<rect x="6" y="6" width="204" height="52" rx="8" fill="{SH}" opacity=".55"/>
<rect x="1" y="1" width="202" height="50" rx="8" fill="{BG}" stroke="{BLUE}" stroke-width="1.5"/>
{icons[k]}<line x1="60" y1="12" x2="60" y2="40" stroke="{BORDER}"/>
<text x="132" y="32" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{TXT}" letter-spacing="2">{label}</text></svg>''')

for k,t,num in [("about","Sobre mí","01"),("stack","Stack","02"),("projects","Proyectos","03"),("activity","Actividad","04")]:
    save(f"title-{k}.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="70" viewBox="0 0 840 70">{defs()}
<text x="0" y="44" font-family="{MONO}" font-size="16" font-weight="700" fill="{BLUE}">{num}</text>
<rect x="34" y="27" width="4" height="22" rx="2" fill="url(#g)"/>
<text x="50" y="47" font-family="{SANS}" font-size="30" font-weight="800" fill="{TXT}">{esc(t)}</text>
<line x1="0" y1="64" x2="840" y2="64" stroke="{BORDER}" stroke-width="2" stroke-dasharray="8 6"/>
<line x1="0" y1="64" x2="120" y2="64" stroke="url(#g)" stroke-width="2"/></svg>''')

lines=[
 [("Soy Guillermo, estudiante de ",0),("Ciencia de Datos e Ingeniería",1),(" en la ",0),("UPM",1),(". Me interesa todo",0)],
 [("el ciclo de vida del dato: desde la ingesta y el procesamiento a escala hasta el",0)],
 [("modelado y la puesta en producción.",0)],
 [],
 [("▸ ",2),("Pipelines de datos ",1),("batch y en tiempo real con arquitecturas Big Data",0)],
 [("▸ ",2),("Machine Learning y Deep Learning ",1),("aplicados a problemas reales",0)],
 [("▸ ",2),("Herramientas de analítica ",1),("pensadas para el usuario final",0)],
 [("▸ ",2),("Aprendiendo: ",1),("cloud, orquestación y MLOps",0)],
]
h=70+len(lines)*27+40
body=""
for i,l in enumerate(lines):
    y=78+i*27
    if not l: continue
    body+=f'<text xml:space="preserve" x="44" y="{y}" font-family="{SANS}" font-size="16" fill="{MUT}">'
    for s,b in l:
        if b==1: body+=f'<tspan font-weight="700" fill="{TXT}">{esc(s)}</tspan>'
        elif b==2: body+=f'<tspan fill="{CYAN}">{esc(s)}</tspan>'
        else: body+=esc(s)
    body+='</text>'
save("about.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{h+20}" viewBox="0 0 840 {h+20}">{defs()}
<g transform="translate(0,20)">{card(840,h,grid=False)}</g>
<rect x="28" y="4" width="150" height="34" rx="6" fill="{BG}" stroke="{BLUE}" stroke-width="1.5"/>
<text x="103" y="27" text-anchor="middle" font-family="{MONO}" font-size="14" font-weight="700" fill="{CYAN}" letter-spacing="2">GUILLERMO</text>
<g transform="translate(0,20)">{body}</g></svg>''')

rows=[("LENGUAJES",["Python","SQL","Scala","JavaScript"]),
("DATA ENG",["Apache Spark","Kafka","Airflow","PostgreSQL","MongoDB"]),
("ML / IA",["Pandas","NumPy","scikit-learn","PyTorch","TensorFlow"]),
("TOOLS",["Docker","Git","Linux","Jupyter"])]
h=40+len(rows)*56+20
s=""
for i,(lab,items) in enumerate(rows):
    y=44+i*56
    s+=f'<text x="36" y="{y+22}" font-family="{MONO}" font-size="13" font-weight="700" fill="{CYAN}" letter-spacing="2">{lab}</text>'
    x=180
    for it in items:
        w=int(len(it)*9.4+36)
        s+=f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="#0F1D36" stroke="{BORDER}" stroke-width="1.5"/><circle cx="{x+16}" cy="{y+17}" r="4" fill="url(#g)"/><text x="{x+28}" y="{y+22}" font-family="{SANS}" font-size="14" font-weight="600" fill="{TXT}">{esc(it)}</text>'
        x+=w+10
save("stack.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{h}" viewBox="0 0 840 {h}">{defs()}{card(840,h,grid=False)}{s}</svg>''')

projs=[("01","STREAMING · ML · BIG DATA","Flight Delay Streaming Pipeline",
  ["Sistema end-to-end de Machine Learning en tiempo real con una arquitectura","Big Data completa: predice en streaming si un vuelo se retrasará."],["Streaming","Big Data","ML"],"flight"),
 ("02","DEEP LEARNING · COMPUTER VISION","Traducción de Imágenes Satelitales",
  ["Red cGAN (Pix2Pix) para traducción imagen a imagen entre fotografía","aérea/satelital y mapas cartográficos."],["Python","cGAN","Pix2Pix"],"sat"),
 ("03","WEB APP · ANALÍTICA","Hybrid",
  ["App integral de entrenamiento y analítica para atletas híbridos: planifica,","registra y optimiza tu rendimiento en un solo lugar."],["Web","Analítica","HTML"],"hybrid")]
for num,tag,title,desc,tags,key in projs:
    H=200
    t=f'<text x="36" y="48" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}" letter-spacing="2">{esc(tag)}</text>'
    t+=f'<text x="36" y="84" font-family="{SANS}" font-size="24" font-weight="800" fill="{TXT}">{esc(title)}</text>'
    for i,d in enumerate(desc): t+=f'<text x="36" y="{114+i*22}" font-family="{SANS}" font-size="15" fill="{MUT}">{esc(d)}</text>'
    x=36
    for tg in tags:
        w=int(len(tg)*7.6+22)
        t+=f'<rect x="{x}" y="152" width="{w}" height="24" rx="5" fill="#0F1D36" stroke="{BORDER}"/><text x="{x+w/2}" y="168" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{CYAN}">{esc(tg)}</text>'
        x+=w+8
    t+=f'<text x="790" y="92" text-anchor="end" font-family="{MONO}" font-size="64" font-weight="800" fill="{BLUE}" opacity=".18">{num}</text>'
    t+=f'<text x="790" y="170" text-anchor="end" font-family="{MONO}" font-size="13" font-weight="700" fill="{BLUE}" letter-spacing="1.5">VER REPO →</text>'
    save(f"project-{key}.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{H}" viewBox="0 0 840 {H}">{defs()}{card(840,H,grid=False)}
<rect x="1" y="20" width="4" height="60" rx="2" fill="url(#g)"/>{t}</svg>''')

save("footer.svg",f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="60" viewBox="0 0 840 60">{defs()}
<line x1="0" y1="20" x2="840" y2="20" stroke="{BORDER}" stroke-width="2"/>
<line x1="0" y1="20" x2="840" y2="20" stroke="url(#g)" stroke-width="2" stroke-dasharray="40 800"><animate attributeName="stroke-dashoffset" from="840" to="0" dur="4s" repeatCount="indefinite"/></line>
<text x="420" y="50" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUT}" letter-spacing="2">GRACIAS POR PASARTE · GUILLERMO CAMINERO</text></svg>''')
