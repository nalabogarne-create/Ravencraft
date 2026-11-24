import json,os,urllib.request,pathlib,time
UA={"User-Agent":"Ravencraft-CC0-Importer/1.0"}
ASSETS={"Chandelier_03":"chandelier","GothicCommode_01":"commode","GothicCoffeeTable":"coffee-table","large_castle_door":"castle-door","ornate_mirror_01":"mirror","vintage_grandfather_clock_01":"clock","wooden_candlestick":"candlestick"}
def get(url):
 for n in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120) as f:return f.read()
  except Exception:
   if n==2:raise
   time.sleep(2+n*3)
def main():
 out=pathlib.Path("build-assets");out.mkdir(exist_ok=True)
 with open(os.environ["GITHUB_OUTPUT"],"a") as outputs:
  for asset,name in ASSETS.items():
   try:
    data=json.loads(get("https://api.polyhaven.com/files/"+asset))
    versions=data.get("gltf",{})
    if not versions:raise RuntimeError("no gltf")
    res="1k" if "1k" in versions else sorted(versions)[0]
    package=versions[res]["gltf"]
    folder=out/name;folder.mkdir(parents=True,exist_ok=True)
    model=folder/(asset+".gltf")
    model.write_bytes(get(package["url"]))
    for rel,dep in package.get("include",{}).items():
     dest=folder/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(get(dep["url"]))
    outputs.write(name.replace("-","_")+"="+str(model)+"\n")
    print("SUCCESS",asset,res,flush=True)
   except Exception as e:print("SKIP",asset,repr(e),flush=True)
main()
