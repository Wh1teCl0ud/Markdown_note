import sys, json, os, subprocess, traceback, base64, time
import requests
CODE = "DfNbIqsTDEw"
URL = f"https://www.instagram.com/reel/{CODE}/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
s = requests.Session()
s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
print("PROBE_START", URL, flush=True)
item = None
video_url = None
try:
    home=s.get("https://www.instagram.com/", timeout=20)
    print("HOME_STATUS", home.status_code, "COOKIE_NAMES", list(s.cookies.keys()), flush=True)
except Exception as e:
    print("HOME_ERROR", str(e)[:260], flush=True)
csrf=s.cookies.get("csrftoken", "")
h = {
    "User-Agent": UA,
    "X-IG-App-ID":"936619743392459",
    "X-CSRFToken": csrf,
    "X-Requested-With":"XMLHttpRequest",
    "Referer": URL,
    "Origin":"https://www.instagram.com",
}
variables={"shortcode":CODE, "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider":False}
for attempt in range(2):
    try:
        r=s.post("https://www.instagram.com/graphql/query", headers=h,
            data={"doc_id":"27128499623469141", "variables":json.dumps(variables,separators=(',',':'))},timeout=30)
        print("GRAPHQL",attempt,r.status_code, "LEN",len(r.content), "BODY",r.text[:500].replace("\n"," "), flush=True)
        j=r.json()
        wi=(j.get("data") or {}).get("xdt_api__v1__media__shortcode__web_info") or {}
        items=wi.get("items") or []
        if items:
            item=items[0]; break
    except Exception as e:
        print("GRAPHQL_ERROR",type(e).__name__,str(e)[:200],flush=True)
    time.sleep(2)
if item:
    print("MEDIA_FOUND", True,flush=True)
    print("AUTHOR", (item.get("user") or item.get("owner") or {}).get("username"),flush=True)
    print("DURATION",item.get("video_duration"),"TAKEN_AT",item.get("taken_at"), flush=True)
    cap=item.get("caption") or {}
    print("CAPTION",str(cap.get("text") if isinstance(cap,dict) else cap)[:10000],flush=True)
    versions=item.get("video_versions") or []
    if versions: video_url=versions[0].get("url")
else:
    print("MEDIA_FOUND",False,flush=True)
if not video_url:
    print("YTDLP_FALLBACK", flush=True)
    subprocess.run([sys.executable,"-m","pip","install","-q","yt-dlp"],check=False)
    p=subprocess.run([sys.executable,"-m","yt_dlp","--no-warnings","--no-playlist","--print-json", "-o","reel.%(ext)s", URL],
       capture_output=True,text=True,timeout=100)
    print("YTDLP_CODE",p.returncode,"STDERR",p.stderr[-1500:],"STDOUT_HEAD",p.stdout[:600],flush=True)
    if p.returncode==0:
        for f in os.listdir("."):
            if f.startswith("reel.") and f.endswith((".mp4",".mkv",".webm")):
                os.rename(f,"reel.mp4")
                break
else:
    try:
        v=s.get(video_url,timeout=60)
        print("VIDEO_HTTP",v.status_code,len(v.content),v.headers.get("content-type"),flush=True)
        if v.status_code==200 and len(v.content)>10000:
            open("reel.mp4","wb").write(v.content)
    except Exception as e:
        print("VIDEO_ERROR",str(e)[:250],flush=True)
if not os.path.isfile("reel.mp4"):
    print("RESULT_NO_VIDEO",flush=True); sys.exit(0)
print("VIDEO_DOWNLOADED",os.stat("reel.mp4").st_size,flush=True)
try:
    probe=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1","reel.mp4"],text=True).strip()
    dur=float(probe);print("DURATION_PROBED",dur,flush=True)
    frames=[]
    for idx in range(6):
        pos=max(0.1, dur*(idx+.5)/6)
        dest=f"frame{idx}.png"
        p=subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(pos),"-i","reel.mp4","-frames:v","1","-vf","scale=400:-1",dest],capture_output=True,text=True,timeout=20)
        if p.returncode==0 and os.path.isfile(dest): frames.append(dest)
    from PIL import Image,ImageDraw
    imlist=[Image.open(f).convert("RGB") for f in frames]
    if imlist:
        fw=max(im.width for im in imlist)
        fh=max(im.height for im in imlist)
        sheet=Image.new("RGB",(3*fw,2*(fh+30)),"white")
        d=ImageDraw.Draw(sheet)
        for i,img in enumerate(imlist):
            x=(i%3)*fw; y=(i//3)*(fh+30)
            sheet.paste(img,(x,y+30))
            d.text((x+10,y+5),f"Frame {i+1} / {len(imlist)}",fill="black")
        sheet.save("contact.jpg",quality=70,optimize=True)
        coded=base64.b64encode(open("contact.jpg","rb").read()).decode()
        print("CONTACT_IMAGE_BEGIN",flush=True)
        for i in range(0,len(coded),4000): print("B64:"+coded[i:i+4000],flush=True)
        print("CONTACT_IMAGE_END",flush=True)
except Exception as e:
    print("FRAMES_ERROR",repr(e),traceback.format_exc()[-800:],flush=True)
try:
    p=subprocess.run([sys.executable,"-m","pip","install","-q","faster-whisper"],capture_output=True,text=True,timeout=130)
    print("ASR_INSTALL",p.returncode,p.stderr[-300:],flush=True)
    if p.returncode==0:
        from faster_whisper import WhisperModel
        model=WhisperModel("base",device="cpu",compute_type="int8")
        segments, info=model.transcribe("reel.mp4",beam_size=5,vad_filter=True)
        print("ASR_LANG",info.language,info.language_probability,flush=True)
        print("TRANSCRIPT_BEGIN",flush=True)
        for seg in segments: print(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text}",flush=True)
        print("TRANSCRIPT_END",flush=True)
except Exception as e:
    print("ASR_ERROR",repr(e),traceback.format_exc()[-1000:],flush=True)
print("PROBE_END",flush=True)
