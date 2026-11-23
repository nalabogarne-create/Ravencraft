import json, urllib.request, pathlib, time
HEADERS={"User-Agent":"Ravencraft/1.0 (GitHub Actions; CC0 asset importer)"}
ASSETS={"stone_brick_wall_001":"wall","wood_floor_deck":"floor","dark_wood":"wood","castle_wall_slates":"stone"}
OUT=pathlib.Path("assets/pbr");OUT.mkdir(parents=True,exist_ok=True)
def fetch(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=90) as f:return f.read()
  except Exception:
   if attempt==2:raise
   time.sleep(2+attempt*3)
def choose(node):
 if not isinstance(node,dict):return None
 for resolution in ("1k","2k"):
  sub=node.get(resolution,{})
  if isinstance(sub,dict):
   for ext in ("jpg","png","webp"):
    val=sub.get(ext)
    if isinstance(val,dict) and val.get("url"):return val["url"]
 for v in node.values():
  if isinstance(v,dict) and v.get("url") and (".jpg" in v["url"] or ".png" in v["url"]):return v["url"]
 return None
success=0
for asset,label in ASSETS.items():
 try:
  data=json.loads(fetch("https://api.polyhaven.com/files/"+asset))
  for suffix,keys in [("color",("Diffuse","diffuse")),("normal",("nor_gl","Normal GL","normal_gl")),("rough",("Rough","rough"))]:
   link=next((choose(data[k]) for k in keys if k in data and choose(data[k])),None)
   if not link:continue
   ext="png" if ".png" in link.split("?")[0] else "jpg"
   target=OUT/(label+"_"+suffix+"."+ext)
   target.write_bytes(fetch(link));print(target,len(target.read_bytes()));success+=1
 except Exception as e:print("SKIP",asset,str(e))
if success<2:raise RuntimeError("Insufficient PBR assets fetched")
