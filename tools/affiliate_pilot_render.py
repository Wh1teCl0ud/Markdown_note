#!/usr/bin/env python3
"""Free, self-contained render of three original faceless Shorts.
Writes only original generated media, no reused or copyrighted videos.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import tempfile, subprocess, math, wave, struct, random, json

OUT=Path("media/affiliate-pilot");OUT.mkdir(parents=True,exist_ok=True)
W,H,FPS=720,1280,24
B="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MOVIES=[
 ("01_prompt_fix.mp4",
  [3.1,2.9,4.7,3.1,3.2],
  [("PROMPT FIX","STOP ASKING AI\nTO 'BE CREATIVE'.","It needs a better brief."),
   ("WHY IT FAILS","WEAK PROMPT:","'Write a sales email.'"),
   ("TRY THIS","GIVE AI THE\nCONSTRAINTS.","ROLE: B2B editor\nAUDIENCE: founders\nLIMIT: 80 words\nTONE: direct, no hype"),
   ("THINK FIRST","BETTER INPUT.\nCLEARER OUTPUT.","A prompt isn't a guarantee."),
   ("SAVE THIS","THE FULL TEMPLATE\nIS BELOW ↓","Test it on your own work.")]),
 ("02_notes_to_actions.mp4",
  [3.2,3.2,4.6,4.3,3.0],
  [("WORKFLOW 02","YOUR MEETING NOTES\nARE A MESS?","Turn fragments into a checklist."),
   ("RAW NOTES","CLIENT NEEDS DEMO.\nFRIDAY? PRICE TBD.","Not exactly a project plan."),
   ("THE PROMPT","ASK FOR A\nSTRUCTURED LIST.","Decisions / tasks\nOwner / deadline\nMissing information\nDo NOT invent facts"),
   ("THE OUTPUT","DEMO REQUESTED.\nOWNER: UNKNOWN.\nDATE: VERIFY.","PRICE: PENDING"),
   ("SAVE THIS","FULL PROMPT\nIN DESCRIPTION ↓","Check before sending.")]),
 ("03_video_to_short_ideas.mp4",
  [3.1,3.1,3.2,4.5,3.2,3.0],
  [("WORKFLOW 03","1 LONG VIDEO →\n5 SHORTS IDEAS","Use content you have rights to."),
   ("STEP ONE","START WITH A\nTIMESTAMPED TRANSCRIPT.","You need the source timestamps."),
   ("STEP TWO","ASK AI TO FIND\n5 STANDALONE MOMENTS.","No invented quotes or timecodes."),
   ("STEP THREE","REQUEST AN\nEDITING BLUEPRINT.","Exact timestamps\nTruthful hook\nMissing context\nSuggested cut"),
   ("CHECK THIS","VERIFY EVERY CUT\nAGAINST THE ORIGINAL.","A clip shouldn't distort its source."),
   ("GET THE PROMPT","COPY IT FROM\nTHE DESCRIPTION ↓","Use it with your own recordings.")])
]
def font(sz,bold=True):
    return ImageFont.truetype(B if bold else R,sz)
def wrap(d,s,f,maxw):
    out=[]
    for line in s.split("\n"):
        current=""
        for token in line.split():
            cand=(current+" "+token).strip()
            if d.textbbox((0,0),cand,font=f)[2]>maxw and current:
                out.append(current);current=token
            else: current=cand
        out.append(current)
    return out
def slide(step,total,topic,headline,note,target):
    im=Image.new("RGB",(W,H),(13,21,35));d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=(int(13+5*t),int(21+6*t),int(35+10*t)))
    for x in range(35,W,56):d.line((x,0,x,H),fill=(30,47,56),width=1)
    for y in range(38,H,56):d.line((0,y,W,y),fill=(30,47,56),width=1)
    mint=(103,253,187);white=(245,250,254);muted=(146,166,179)
    d.rounded_rectangle((58,76,108,126),radius=13,fill=mint)
    d.text((74,80),"↗",font=font(26),fill=(13,21,35))
    d.text((123,83),"AI FIELDNOTES",font=font(25),fill=white)
    d.text((60,147),topic,font=font(17),fill=muted)
    d.rounded_rectangle((552,81,660,124),radius=18,fill=(27,42,57),outline=(55,91,100),width=2)
    d.text((568,87),f"{step:02}/{total:02}",font=font(20),fill=mint)
    size=65
    while True:
        f=font(size)
        lines=wrap(d,headline,f,596)
        if len(lines)<=6 and all(d.textbbox((0,0),line,font=f)[2]<=600 for line in lines):break
        size-=2
    ypos=296 if len(note)<85 else 250
    for line in lines:
        d.text((59,ypos),line,font=f,fill=white)
        ypos+=int(size*1.2)
    if len(note)>85 or note.count("\n")>=2:
        py=max(605,ypos+25)
        d.rounded_rectangle((59,py,660,min(1095,py+370)),radius=26,fill=(24,37,55),outline=(61,96,104),width=3)
        d.text((90,py+25),"EXAMPLE PROMPT",font=font(17),fill=mint)
        y=py+80
        for line in wrap(d,note,font(30),525):
            d.text((90,y),line,font=font(30),fill=white)
            y+=51
    else:
        for line in wrap(d,note,font(31,False),570):
            d.text((61,max(660,ypos+47)),line,font=font(31,False),fill=muted)
            ypos=max(660,ypos+47)+49
    d.text((60,1146),"NO HYPE. JUST USEFUL WORKFLOWS.",font=font(15),fill=muted)
    d.rounded_rectangle((59,1192,660,1200),radius=4,fill=(34,58,68))
    d.rounded_rectangle((59,1192,59+int(601*step/total),1200),radius=4,fill=mint)
    im.save(target,quality=90)
def shell(args):
    subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=150)
def audio(duration,target):
    sr=22050; random.seed(2188); samples=[]
    beat=60/102
    phase=0
    for i in range(int(duration*sr)):
        t=i/sr
        step=int(t/beat)
        inbeat=t-step*beat
        root=[174.6,155.6,207.65,196][int(t/4)%4]
        pad=(math.sin(2*math.pi*root*t)+.34*math.sin(2*math.pi*root/2*t))*.045
        kick=(.19*math.sin(2*math.pi*(58*t-25*t*t)) * math.exp(-22*inbeat)) if step%2==0 and inbeat<.25 else 0
        clap=((random.random()*2-1)*.024*math.exp(-38*inbeat)) if step%4 in (1,3) and inbeat<.1 else 0
        fade=min(1,t/.3,max(0,(duration-t)/.7))
        samples.append(int(max(-1,min(1,(pad+kick+clap)*fade))*32767))
    with wave.open(str(target),"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(struct.pack("<"+str(len(samples))+"h",*samples))
def run():
    for name,durs,slides in MOVIES:
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);parts=[]
            for i,(dur,(topic,heading,note)) in enumerate(zip(durs,slides),1):
                png=p/f"s{i}.png";part=p/f"v{i}.mp4"
                slide(i,len(slides),topic,heading,note,png)
                shell(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-framerate",str(FPS),"-t",str(dur),"-i",str(png),"-vf",f"fade=t=in:st=0:d=0.25,fade=t=out:st={dur-.27:.2f}:d=0.27","-c:v","libx264","-threads","2","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-an",str(part)])
                parts.append(part)
                if i==1:Image.open(png).convert("RGB").save(OUT/name.replace(".mp4","_cover.jpg"),quality=85)
            lst=p/"concat.txt"
            lst.write_text("".join("file '"+str(x)+"'\n" for x in parts))
            v=p/"picture.mp4"
            shell(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(v)])
            aud=p/"original.wav"
            audio(sum(durs),aud)
            target=OUT/name
            shell(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(v),"-i",str(aud),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart",str(target)])
            print("RENDERED",target,target.stat().st_size)
if __name__=="__main__":run()
