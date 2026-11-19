"""Parte una salida con varias opciones. Uso: opciones.py SALIDA.json DESTINO_PREFIJO
Escribe PREFIJO.opN.md (cuerpo sin encabezado), PREFIJO.opN.nota.txt (encabezado + nota) y PREFIJO.general.txt.
Imprime el número de opciones (0 si la salida es una sola edición)."""
import sys,re,json
s=json.load(open(sys.argv[1],encoding="utf-8"))["salida"]; pref=sys.argv[2]
hdr=re.compile(r"(?im)^(#+\s*.*?(opci[oó]n|versi[oó]n)\s*\d.*|\**\s*(opci[oó]n|versi[oó]n)\s*\d.*)$")
cuts=[m.start() for m in hdr.finditer(s)]
if not cuts: print(0); sys.exit()
general=[s[:cuts[0]]]
for k,a in enumerate(cuts):
    b=cuts[k+1] if k+1<len(cuts) else len(s)
    blk=s[a:b]
    # lo que venga tras un encabezado no-opción (### Principales…) va a general
    nl=blk.find("\n")+1
    m=re.compile(r"(?m)^#+\s+(?!.*(opci[oó]n|versi[oó]n)\s*\d).*$").search(blk,nl)
    if m: general.append(blk[m.start():]); blk=blk[:m.start()]
    lines=blk.split("\n"); head=[lines[0]]; body=[]
    for ln in lines[1:]:
        t=ln.strip()
        if not body and (t.startswith("*") and t.endswith("*") or t.startswith("_") and t.endswith("_") or not t): head.append(ln); continue
        body.append(re.sub(r"^\s*>\s?","",ln))
    txt="\n".join(body); txt=re.sub(r"(?m)^\s*[-*_]{3,}\s*$","",txt).replace("**","")
    open(f"{pref}.op{k+1}.md","w",encoding="utf-8").write(txt)
    open(f"{pref}.op{k+1}.nota.txt","w",encoding="utf-8").write("\n".join(head))
open(pref+".general.txt","w",encoding="utf-8").write("\n\n".join(general))
print(len(cuts))
