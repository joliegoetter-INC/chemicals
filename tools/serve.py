#!/usr/bin/env python3
"""Local inventory app: serves inventory.html and saves manual adds/edits.
Run:  python3 tools/serve.py   then open http://localhost:8791/inventory.html
Edits go to readings/edits.json, new bottles to readings/manual.json, then everything is rebuilt."""
import json, os, re, subprocess, sys, datetime, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..")); PORT=int(os.environ.get("PORT",8791)); LOCK=threading.Lock()
FIELDS={"name","common_name","cas","vendor","catalog_no","size","unit","physical_state","purity","lot","location","received","opened","expiration","storage_note","category","subcategory","problems","recheck_done"}
def cas_ok(c):
    m=re.fullmatch(r"(\d{2,7})-(\d\d)-(\d)",c or "")
    return bool(m) and sum(int(x)*(i+1) for i,x in enumerate((m.group(1)+m.group(2))[::-1]))%10==int(m.group(3))
def load(p,d): return json.load(open(p)) if os.path.exists(p) else d
def rebuild():
    for cmd in (["tools/build_inventory.py","readings","Chemical_Inventory.xlsx"],["tools/build_html.py"]):
        r=subprocess.run([sys.executable]+cmd,cwd=ROOT,capture_output=True,text=True,timeout=600)
        if r.returncode: raise RuntimeError(r.stderr[-800:])
def clean(f):
    f={k:(v.strip() if isinstance(v,str) else v) for k,v in f.items() if k in FIELDS}
    if f.get("cas") and not cas_ok(f["cas"]): raise ValueError(f"CAS {f['cas']} is not valid (check digit fails). Re-read it from the label.")
    for k in ("received","opened"):
        if f.get(k) and not re.fullmatch(r"\d{4}-\d{2}",f[k]): raise ValueError(f"{k} must look like 2026-07")
    return f
class H(SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def out(self,code,obj):
        b=json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def end_headers(self): self.send_header("Cache-Control","no-store"); super().end_headers()
    def do_GET(self):
        if self.path.startswith("/api/ping"): return self.out(200,{"ok":True})
        super().do_GET()
    def do_POST(self):
        try:
            body=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))) or b"{}"); today=datetime.date.today().isoformat()
            with LOCK:
                if self.path=="/api/save":
                    p=os.path.join(ROOT,"readings","edits.json"); e=load(p,{}); cur=e.get(body["id"],{}); cur.update(clean(body["fields"])); cur["_edited"]=today; e[body["id"]]=cur
                    json.dump(e,open(p,"w"),indent=1,ensure_ascii=False)
                elif self.path=="/api/add":
                    f=clean(body["fields"])
                    if not (f.get("name") or f.get("common_name")): raise ValueError("Give the bottle a name or nickname.")
                    p=os.path.join(ROOT,"readings","manual.json"); m=load(p,[])
                    f.update(key="manual-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),source="manual",confidence="",t_start=10**6+len(m),_edited=today); m.append(f)
                    json.dump(m,open(p,"w"),indent=1,ensure_ascii=False)
                else: return self.out(404,{"ok":False,"error":"unknown"})
                rebuild()
            self.out(200,{"ok":True})
        except Exception as ex: self.out(400,{"ok":False,"error":str(ex)})
    def log_message(self,*a): pass
if __name__=="__main__":
    print(f"Inventory running at http://localhost:{PORT}/inventory.html  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
