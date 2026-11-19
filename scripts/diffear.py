"""Separa texto editado / comentario y saca el diff contra la fuente.
Uso: diffear.py FUENTE.txt SALIDA(.json|.md) DESTINO_PREFIJO [--todo]
Escribe PREFIJO.texto.txt, PREFIJO.comentario.txt (NO leer hasta el paso 4) y PREFIJO.diff.md
--todo: todo el archivo es texto editado (cuerpos de opción ya separados por opciones.py)"""
import sys,re,json,difflib,unicodedata
fuente=open(sys.argv[1],encoding="utf-8").read()
raw=open(sys.argv[2],encoding="utf-8").read()
if sys.argv[2].endswith(".json"): raw=json.loads(raw)["salida"]
pref=sys.argv[3]
def norm(w):
    w=unicodedata.normalize("NFD",w.lower()); w="".join(c for c in w if unicodedata.category(c)[0] in "LN")
    return w
def toks(t): return [x for x in (norm(w) for w in t.split()) if x]
voc=set(toks(fuente))
paras=[p.strip() for p in re.split(r"\n\s*\n",raw) if p.strip()]
texto,coment=[],[]; fin=False
for p in paras:
    if re.fullmatch(r"[-*_ ]{3,}",p): continue
    ws=toks(p)
    if not ws: continue
    ov=sum(w in voc for w in ws)/len(ws)
    meta=bool(re.match(r"^\s*([-*•]|\d+[.)]|#+)\s",p)) or "→" in p or "->" in p or bool(re.match(r"^\W*(Dej[ée]|Cambi[ée]|Correg[íi]|Quit[ée]|Mantuve|Conserv[ée]|Not[ae]s?\b|Cambios|Si quieres|Algunos|Te |Aqu[íi] tienes|He |Hice|Ajust[ée]|Elimin[ée]|Agregu[ée]|Reorganic[ée]|Principales|Resumen|Observaciones|Sugerencias|¿Quieres)",p,re.I))
    if ov>=0.6 and not meta and not (texto and coment and coment[-1] is not None and fin):
        texto.append(p)
    else:
        coment.append(p)
        if texto: fin=True
if "--todo" in sys.argv: texto,coment=[p for p in paras if toks(p)],[]
T="\n\n".join(texto); C="\n\n".join(coment)
open(pref+".texto.txt","w",encoding="utf-8").write(T); open(pref+".comentario.txt","w",encoding="utf-8").write(C)
a=toks(fuente); b=toks(T)
# cambios de ortografía/puntuación quedan fuera porque se compara normalizado (sin tildes ni signos)
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
borr=agr=reem=0; ops=[]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal": continue
    if tag=="delete": borr+=i2-i1
    elif tag=="insert": agr+=j2-j1
    else: reem+=max(i2-i1,j2-j1)
    ops.append((tag," ".join(a[i1:i2])," ".join(b[j1:j2])))
with open(pref+".diff.md","w",encoding="utf-8") as f:
    f.write(f"palabras fuente {len(a)} · texto editado {len(b)} · comentario {len(toks(C))} palabras\n")
    f.write(f"conservadas {sum(i2-i1 for t,i1,i2,_,_ in sm.get_opcodes() if t=='equal')} · borradas {borr} · agregadas {agr} · reemplazadas {reem} · borrado neto {100*(len(a)-len(b))/len(a):.0f}%\n\n")
    for t,x,y in ops: f.write(f"- {t}: «{x}» → «{y}»\n")
print(pref.split('/')[-1], f"fuente={len(a)} editado={len(b)} borr={borr} agr={agr} reem={reem} coment={len(toks(C))}")
