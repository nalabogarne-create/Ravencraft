#!/usr/bin/env python3
"""Download REAL CC0 photographic PBR maps. Fail rather than silently substitute flat colors."""
import requests, pathlib, io
from PIL import Image
S=requests.Session();S.headers.update({"User-Agent":"Ravencraft-Gothic-Game-Asset-Importer/2.0"})
ROOT=pathlib.Path("assets/pbr");ROOT.mkdir(parents=True,exist_ok=True)
def api(path):
 r=S.get("https://api.polyhaven.com/"+path,timeout=90);r.raise_for_status();return r.json()
assets=api("assets?type=textures")
def select(hints):
 scored=[]
 for id,info in assets.items():
  desc=" ".join([id,info.get("name",""),str(info.get("category",""))," ".join(str(tag) for tag in (info.get("tags") or []))]).lower()
  score=sum((30-i*8 if hint in (id+" "+info.get("name","")).lower() else 1) for i,hint in enumerate(hints) if hint in desc)
  if score:scored.append((score,id))
 if not scored:raise RuntimeError("No matching texture for "+str(hints))
 return sorted(scored,reverse=True)[0][1]
def file_for(files,keys):
 for key in keys:
  node=next((v for k,v in files.items() if k.lower()==key.lower()),{})
  for res in ("1k","2k","4k"):
   for ext in ("jpg","png","webp"):
    obj=node.get(res,{}).get(ext)
    if obj and obj.get("url"):return obj["url"]
 return None
targets={"wall":["castle wall variation","medieval wall","stone wall"],"floor":["old wooden floor","oak wood planks","wood floor"],"wood":["dark paneled wood","medieval wood","old wood"]}
for name,hints in targets.items():
 id=select(hints);files=api("files/"+id)
 print(name,id,flush=True)
 for suffix,keys in [("color",["Diffuse","diffuse","diff"]),("normal",["nor_gl","normal_gl","normal","Normal GL"]),("rough",["Rough","rough","roughness"])]:
  url=file_for(files,keys)
  if not url:
   if suffix=="color":raise RuntimeError("Missing diffuse map for "+id)
   continue
  r=S.get(url,timeout=150);r.raise_for_status()
  im=Image.open(io.BytesIO(r.content)).convert("RGB")
  im.thumbnail((1024,1024))
  out=ROOT/(name+"_"+suffix+".jpg")
  im.save(out,format="JPEG",quality=88,optimize=True)
  print(out,out.stat().st_size,flush=True)
