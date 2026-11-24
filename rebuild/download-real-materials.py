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
  score=sum((8 if hint in id.lower() else 3) for hint in hints if hint in desc)
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
targets={"wall":["stone wall","stone brick","stone_block_wall","stone_brick_wall","castle wall"],"floor":["wood floor","wooden floor","wood planks","wood_floor"],"wood":["dark wood","aged wood","old wood","wood panel"]}
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
