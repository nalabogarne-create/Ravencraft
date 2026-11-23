import json,os,urllib.request,hashlib,pathlib
UA={"User-Agent":"RavencraftGame/1.0 (GitHub Actions; Poly Haven CC0)"}
def get(url):
 req=urllib.request.Request(url,headers=UA)
 with urllib.request.urlopen(req,timeout=90) as response:return response.read()
def download(asset,filename):
 data=json.loads(get("https://api.polyhaven.com/files/"+asset))
 formats=data.get("gltf",{})
 if not formats:raise RuntimeError(asset+": glTF format unavailable")
 res="1k" if "1k" in formats else sorted(formats)[0]
 fmt=formats[res]["gltf"]
 folder=pathlib.Path("build-assets")/asset
 folder.mkdir(parents=True,exist_ok=True)
 (folder/(asset+".gltf")).write_bytes(get(fmt["url"]))
 for rel,dep in fmt.get("include",{}).items():
  p=folder/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(get(dep["url"]))
 print(asset,res,"gltf bytes", (folder/(asset+".gltf")).stat().st_size,"dependencies",len(fmt.get("include",{})))
 return str(folder/(asset+".gltf"))
with open(os.environ["GITHUB_OUTPUT"],"a") as o:
 for asset,key in [("GothicBed_01","bed"),("GothicCabinet_01","cabinet")]:
  path=download(asset,key)
  o.write(key+"="+path+"\n")
