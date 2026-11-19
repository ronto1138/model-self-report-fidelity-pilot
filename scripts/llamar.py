"""Llamadas a los seis modelos del piloto. Las llaves llegan por entorno vía `ono-llaves run` (nunca se imprimen)."""
import os,json,urllib.request
PROMPT="Edita este texto:\n\n"
# precio aproximado (entrada, salida) por millón, solo para el tope
MODELOS=[
 ("anthropic","claude-sonnet-5-5",{"effort":"medium"},(2,10)),
 ("openai","gpt-5.6-sol",{"reasoning_effort":"medium"},(4,20)),
 ("gemini","gemini-3.5-flash",{"reasoning_effort":"medium"},(1.5,9)),
 ("xai","grok-4.7",{},(2,6)),
 ("deepseek","deepseek-v4-pro",{},(1.32,3.96)),
 ("ollama","qwen3.5:9b",{"num_ctx":8192},(0,0)),
]
PRECIO={m:p for _,m,_,p in MODELOS}
KEY={"anthropic":"ONO_CLAUDE","openai":"ONO_OPENAI","gemini":"ONO_GEMINI","xai":"ONO_GROK","deepseek":"ONO_DEEPSEEK"}
def post(url,h,body,t=600):
    r=urllib.request.Request(url,data=json.dumps(body).encode(),headers={**h,"content-type":"application/json"})
    return json.load(urllib.request.urlopen(r,timeout=t))
def llamar(prov,model,params,texto,prompt=PROMPT):
    msg=prompt+texto
    if prov=="anthropic":
        r=post("https://api.anthropic.com/v1/messages",{"x-api-key":os.environ[KEY[prov]],"anthropic-version":"2023-06-01"},
               {"model":model,"max_tokens":16000,"output_config":{"effort":params["effort"]},"messages":[{"role":"user","content":msg}]})
        txt="".join(b.get("text","") for b in r["content"] if b["type"]=="text")
        u=r["usage"]; return txt,r.get("model"),u.get("input_tokens",0)+u.get("cache_read_input_tokens",0),u.get("output_tokens",0)
    if prov=="ollama":
        r=post("http://192.168.0.156:11434/api/chat",{},{"model":model,"stream":False,"options":{"num_ctx":params["num_ctx"]},"messages":[{"role":"user","content":msg}]},t=1800)
        return r["message"]["content"],r.get("model"),r.get("prompt_eval_count",0),r.get("eval_count",0)
    url={"openai":"https://api.openai.com/v1/chat/completions","gemini":"https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
         "xai":"https://api.x.ai/v1/chat/completions","deepseek":"https://api.deepseek.com/chat/completions"}[prov]
    body={"model":model,"messages":[{"role":"user","content":msg}],**params}
    body["max_completion_tokens" if prov=="openai" else "max_tokens"]=16000
    r=post(url,{"Authorization":"Bearer "+os.environ[KEY[prov]]},body)
    u=r.get("usage",{}); return r["choices"][0]["message"].get("content") or "",r.get("model"),u.get("prompt_tokens",0),u.get("completion_tokens",0)
