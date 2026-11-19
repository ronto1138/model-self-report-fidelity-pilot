"""Celda E: «Edita este texto y al final dime qué cambiaste:» sobre C1 y D0, 6 modelos × 3. Imprime solo código y ok/ERROR."""
import os,sys,json,time,random,hashlib,datetime
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.environ.get("LLM_LEDGER_PATH","./ledger"))
from llamar import llamar,MODELOS,KEY
from ledger import record
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=BASE+"/multimodelo_2026-11-04_E"
os.makedirs(OUT+"/salidas",exist_ok=True)
FUENTES={"C1":"C1_pulido.txt","D0":"D0_pensamientos_coronavirus_2020.txt"}
PROMPT="Edita este texto y al final dime qué cambiaste:\n\n"
TOPE=50.0; gastado=0.0
corridas=[(m,f,c) for m in MODELOS for f in FUENTES for c in (1,2,3)]
codigos=random.sample(range(100,1000),len(corridas)); mapa={}; random.shuffle(corridas)
for (prov,model,params,precio),fuente,c in corridas:
    if gastado>=TOPE: print("TOPE"); break
    texto=open(BASE+"/celdas/"+FUENTES[fuente],encoding="utf-8").read().strip()
    code="Z%d"%codigos.pop(); t0=time.time(); ts=datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    try: txt,mid,tin,tout=llamar(prov,model,params,texto,PROMPT); err=None
    except Exception as e: txt,mid,tin,tout,err="",None,0,0,type(e).__name__+" "+str(getattr(e,"code",""))
    lat=int((time.time()-t0)*1000); costo=(tin*precio[0]+tout*precio[1])/1e6; gastado+=costo
    fp=hashlib.sha256(os.environ[KEY[prov]].encode()).hexdigest()[:12] if prov in KEY else None
    try: record(project="los-limites",caller="experimento/autorreporte-multimodelo",kind="experimento",provider=prov,model=model,
                input_tokens=tin,output_tokens=tout,latency_ms=lat,**({"key_fp":fp} if fp else {}))
    except Exception as e: print("ledger:",type(e).__name__)
    json.dump({"codigo":code,"fuente":fuente,"instruccion":PROMPT,"salida":txt},open(f"{OUT}/salidas/{code}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    mapa[code]={"proveedor":prov,"modelo_pedido":model,"modelo_respondio":mid,"parametros":params,"fuente":fuente,"corrida":c,"fecha_hora":ts,
               "canal":"API","instruccion":PROMPT.strip(),"tokens_in":tin,"tokens_out":tout,"costo_aprox_usd":round(costo,4),"error":err}
    json.dump(mapa,open(OUT+"/_mapa_NO_ABRIR_hasta_terminar_lectura.json","w"),ensure_ascii=False,indent=1)
    print(code,"ok" if not err else "ERROR",len(txt.split()),"palabras",flush=True)
print("gasto aprox USD %.2f"%gastado)
