"""Reintenta las llamadas con error de una corrida, mismos parámetros. Uso: reintentar.py CARPETA_CORRIDA
Imprime solo código y ok/ERROR (no revela el modelo)."""
import os,sys,json,time,hashlib,datetime
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.environ.get("LLM_LEDGER_PATH","./ledger"))
from llamar import llamar,PROMPT,PRECIO,KEY
from ledger import record
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.abspath(sys.argv[1])
FUENTES={"A0b":"A0b_transcripcion_literal_claude.txt","B1":"B1_tecleado.txt","C1":"C1_pulido.txt","D0":"D0_pensamientos_coronavirus_2020.txt"}
MAPA=OUT+"/_mapa_NO_ABRIR_hasta_terminar_lectura.json"; mapa=json.load(open(MAPA)); gastado=0.0
for intento in (1,2,3):
  for code,m in mapa.items():
    if not m["error"]: continue
    prov,model,params=m["proveedor"],m["modelo_pedido"],m["parametros"]; precio=PRECIO[model]
    texto=open(BASE+"/celdas/"+FUENTES[m["fuente"]],encoding="utf-8").read().strip()
    t0=time.time(); ts=datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    try: txt,mid,tin,tout=llamar(prov,model,params,texto,(m.get("instruccion",PROMPT.strip())+"\n\n")); err=None
    except Exception as e: txt,mid,tin,tout,err="",None,0,0,type(e).__name__+" "+str(getattr(e,"code",""))
    lat=int((time.time()-t0)*1000); costo=(tin*precio[0]+tout*precio[1])/1e6; gastado+=costo
    fp=hashlib.sha256(os.environ[KEY[prov]].encode()).hexdigest()[:12] if prov in KEY else None
    try: record(project="los-limites",caller="experimento/autorreporte-multimodelo",kind="experimento",provider=prov,model=model,
                input_tokens=tin,output_tokens=tout,latency_ms=lat,**({"key_fp":fp} if fp else {}))
    except Exception as e: print("ledger:",type(e).__name__)
    m.setdefault("reintentos",[]).append({"fecha_hora":ts,"error":err})
    if not err:
        json.dump({"codigo":code,"fuente":m["fuente"],"instruccion":m.get("instruccion",PROMPT.strip())+"\n\n","salida":txt},open(f"{OUT}/salidas/{code}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
        m.update(modelo_respondio=mid,fecha_hora=ts,tokens_in=tin,tokens_out=tout,costo_aprox_usd=round(costo,4),error=None,nota="reintento %d"%intento)
    json.dump(mapa,open(MAPA,"w"),ensure_ascii=False,indent=1)
    print(intento,code,"ok" if not err else "ERROR",len(txt.split()),"palabras",flush=True)
  if all(not m["error"] for m in mapa.values()): break
  time.sleep(120)
print("pendientes:",sum(1 for m in mapa.values() if m["error"]),"gasto reintento USD %.2f"%gastado)
