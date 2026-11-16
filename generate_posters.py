#!/usr/bin/env python3
"""Generate 1200x1200 LinkedIn announcement posters for TNJUG chapter leaders.

Reads content/leaders/*.md and content/chapters/*.md, embeds photos/logos as
base64, renders each poster with headless Chrome into
~/Downloads/chapter_leader_poster/<slug>.png.
"""
import base64
import glob
import html
import os
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.dirname(__file__))
OUT_DIR = os.path.expanduser(os.environ.get("POSTER_OUT_DIR", "~/Downloads/chapter_leader_poster_v2"))
TNJUG_LOGO = os.path.join(ROOT, "static/tamil_jug.jpeg")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# keyword in leader's `chapter` field -> (chapter file slug, short name)
CHAPTER_KEYS = {
    "guindy": ("anna-university", "Anna University (CEG)"),
    "kongu": ("kongu-engineering-college", "Kongu Engineering College"),
    "psna": ("psna-college", "PSNA CET"),
    "eshwar": ("sri-eshwar-college", "Sri Eshwar College of Engineering"),
    "vet": ("vet-institute", "VET Institute of Arts & Science"),
}

MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}


def data_uri(path):
    ext = path.rsplit(".", 1)[-1].lower()
    with open(path, "rb") as f:
        return f"data:{MIME.get(ext, 'image/png')};base64,{base64.b64encode(f.read()).decode()}"


def frontmatter(path):
    data, in_fm = {}, False
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip() == "---":
                if in_fm:
                    break
                in_fm = True
            elif in_fm and ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip("\"'")
    return data


def load_chapters():
    chapters = {}
    for path in glob.glob(os.path.join(ROOT, "content/chapters/*.md")):
        slug = os.path.splitext(os.path.basename(path))[0]
        fm = frontmatter(path)
        chapters[slug] = {
            "full": fm.get("college_name") or fm.get("title", slug),
            "city": fm.get("city", "Tamil Nadu"),
            "logo": os.path.join(ROOT, "static", fm.get("logo", "").lstrip("/")),
        }
    return chapters


def match_chapter(name, chapters):
    low = name.lower()
    for key, (slug, short) in CHAPTER_KEYS.items():
        if key in low and slug in chapters:
            return {**chapters[slug], "short": short}
    return None


def style_for(leader):
    role, status = leader.get("role", ""), leader.get("status", "active")
    base = dict(title="CHAPTER LEADER", tenure="TENURE 2026 – 2027", pill="#0B1F3A")
    if "Head of Chapters" in role:
        return {**base, "label": "HEAD OF CHAPTERS", "title": "HEAD OF CHAPTERS", "pill": "#C2410C"}
    if status == "past":
        return {**base, "label": "CAMPUS LEADER", "tenure": "TENURE 2024 – 2025"}
    if "Professional" in role:
        return {**base, "label": "FACULTY CHAPTER LEADER"}
    return {**base, "label": "CAMPUS LEADER"}


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:1200px;overflow:hidden}
:root{--red:#E11D2E;--red2:#B3101E;--black:#0B0B0C;--white:#fff;--grey:#6B7280}
body{position:relative;background:#fff;color:var(--black);
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif}
.abs{position:absolute}
.wm{position:absolute;inset:-200px;background-size:170px;background-repeat:repeat;opacity:.05;transform:rotate(-14deg)}
.redc{left:480px;top:140px;width:740px;height:740px;border-radius:50%;
 background:radial-gradient(circle at 35% 30%,#FF4A55,var(--red) 45%,var(--red2))}
.blackc{left:-170px;top:-190px;width:320px;height:320px;border-radius:50%;background:var(--black)}
.ringd{left:520px;top:180px;width:660px;height:660px;border-radius:50%;border:3px dashed rgba(255,255,255,.55)}
.ringw{left:575px;top:235px;width:550px;height:550px;border-radius:50%;border:14px solid rgba(255,255,255,.18)}
.dot{border-radius:50%}
.portrait{left:630px;top:280px;width:440px;height:440px;border-radius:50%;padding:10px;background:#fff;
 box-shadow:0 0 0 12px var(--black),0 30px 60px rgba(0,0,0,.45)}
.portrait div{width:100%;height:100%;border-radius:50%;overflow:hidden;background:#eee}
.portrait img{width:100%;height:100%;object-fit:cover;object-position:center top;display:block}
.sticker{left:945px;top:625px;width:128px;height:128px;border-radius:50%;background:#fff;border:6px solid var(--black);
 box-shadow:0 12px 28px rgba(0,0,0,.4);transform:rotate(10deg);display:flex;align-items:center;justify-content:center;overflow:hidden;z-index:6}
.sticker img{width:150%;height:150%;object-fit:contain}
.header{left:56px;right:56px;top:36px;display:flex;justify-content:space-between;align-items:center;z-index:8}
.brand{display:flex;align-items:center;gap:14px}
.card{background:#fff;border-radius:18px;height:84px;display:flex;align-items:center;justify-content:center;
 box-shadow:0 8px 24px rgba(0,0,0,.18);border:2px solid var(--black)}
.tn{width:84px;padding:6px}.tn img{width:100%;height:100%;object-fit:contain}
.col{max-width:250px;min-width:84px;height:100px;padding:8px 18px}.col img{max-height:80px;max-width:210px;object-fit:contain}
.cseal{left:640px;top:776px;width:450px;height:96px;border-radius:20px;background:#fff;border:4px solid var(--black);z-index:6;
 box-shadow:8px 8px 0 var(--red);display:flex;align-items:center;justify-content:center;padding:8px 20px}
.cseal img{max-width:400px;max-height:76px;object-fit:contain}
.cpill{left:664px;top:756px;z-index:7;background:var(--red);color:#fff;font-size:12px;font-weight:900;letter-spacing:2px;
 padding:5px 14px;border-radius:30px;border:3px solid var(--black)}
.brand h1{font-size:19px;font-weight:900;letter-spacing:.8px;line-height:1.2;color:var(--black)}
.brand h1 b{color:var(--red)}
.brand p{font-size:13px;font-weight:600;color:var(--grey);margin-top:3px}
.cb{text-align:right}.cb h2{font-size:18px;font-weight:900;line-height:1.2;color:var(--black)}
.cb p{font-size:12.5px;font-weight:800;color:var(--red);letter-spacing:1px;text-transform:uppercase;margin-top:3px}
.kicker{left:64px;top:176px;background:var(--black);color:#fff;font-size:15px;font-weight:800;letter-spacing:3px;
 padding:9px 22px 9px 18px;border-radius:30px;z-index:5}
.kicker i{color:var(--red);font-style:normal;margin-right:8px}
.title{left:60px;top:228px;font-size:118px;font-weight:900;line-height:.9;letter-spacing:-3px;color:var(--black);z-index:5}
.title span{color:var(--red)}
.title.long{font-size:80px;line-height:.98}
.stamp{left:64px;top:490px;transform:rotate(-3deg);z-index:5;display:flex;align-items:center;background:var(--red);
 color:#fff;border-radius:14px;padding:10px 26px 10px 18px;gap:14px;box-shadow:6px 6px 0 var(--black)}
.stamp small{font-size:12px;letter-spacing:3px;font-weight:800;writing-mode:vertical-rl;transform:rotate(180deg);opacity:.9}
.stamp b{font-size:40px;font-weight:900;letter-spacing:1px}
.rib{left:-30px;transform:skewX(-10deg);z-index:7}
.rib span{display:inline-block;transform:skewX(10deg)}
.nameb{top:612px;background:var(--black);color:#fff;padding:14px 60px 14px 94px;font-size:58px;font-weight:900;letter-spacing:-1px;
 line-height:1.05;border-right:10px solid var(--red)}
.nameb.long{font-size:48px}
.roleb{top:716px;left:-30px;background:var(--red);color:#fff;padding:9px 40px 9px 94px;font-size:17px;font-weight:900;letter-spacing:3px}
.desig{left:64px;top:792px;width:560px;font-size:26px;line-height:1.35;font-weight:600;color:#1f2937;z-index:5}
.band{left:0;right:0;top:872px;height:330px;background:var(--red);clip-path:polygon(0 24%,100% 0,100% 100%,0 100%);z-index:3}
.band2{left:0;right:0;top:890px;height:312px;background:var(--black);clip-path:polygon(0 24%,100% 0,100% 100%,0 100%);z-index:4}
.inst{left:64px;bottom:76px;display:flex;align-items:center;gap:20px;z-index:9;width:760px}
.badge{height:132px;width:210px;background:#fff;border-radius:22px;padding:10px 16px;box-shadow:8px 8px 0 var(--red);display:flex;align-items:center;justify-content:center;flex-shrink:0;
 border:3px solid var(--red)}
.badge img{max-height:110px;max-width:178px;object-fit:contain}
.inst-label{font-size:12px;font-weight:800;letter-spacing:2.5px;color:#FF5A66}
.inst-name{font-size:28px;font-weight:900;line-height:1.2;margin-top:4px;color:#fff}
.inst-meta{font-size:16px;color:#D1D5DB;margin-top:5px;font-weight:500}
.footer{left:64px;bottom:34px;display:flex;gap:28px;font-size:15px;font-weight:700;color:#fff;z-index:9}
.seal{right:56px;bottom:30px;z-index:9;display:flex;align-items:center;gap:14px;color:#fff;text-align:right}
.seal .t{font-size:15px;font-weight:800;line-height:1.25;letter-spacing:.4px}
.seal .t b{color:#FF5A66;display:block;font-size:12px;letter-spacing:2px}
.seal .c{width:104px;height:104px;border-radius:50%;background:#fff;border:5px solid var(--red);display:flex;align-items:center;justify-content:center;overflow:hidden}
.seal .c img{width:140%;height:140%;object-fit:contain}
"""


def poster_html(leader, chapter, tn_b64, logo_b64, photo_b64):
    s, e = style_for(leader), html.escape
    name = leader["title"]
    if s["title"] == "CHAPTER LEADER":
        title_html, title_cls = "CHAPTER<br><span>LEADER</span>", "title"
    else:
        title_html, title_cls = "HEAD OF<br><span>CHAPTERS</span>", "title long"
    name_cls = "nameb long" if len(name) > 20 else "nameb"
    years = s["tenure"].replace("TENURE ", "")
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="wm" style="background-image:url({tn_b64})"></div>
<div class="abs blackc"></div>
<div class="abs dot" style="left:1090px;top:170px;width:34px;height:34px;background:#fff"></div>
<div class="abs dot" style="left:520px;top:690px;width:22px;height:22px;background:var(--black)"></div>
<div class="abs dot" style="left:1120px;top:520px;width:16px;height:16px;background:var(--black)"></div>
<div class="abs portrait"><div><img src="{photo_b64}"></div></div>
<div class="abs cseal"><img src="{logo_b64}"></div>
<div class="abs cpill">COLLEGIATE CHAPTER</div>
<div class="abs sticker"><img src="{tn_b64}"></div>
<div class="abs header">
 <div class="brand"><div class="card tn"><img src="{tn_b64}"></div>
  <div><h1>TAMIL NADU<br><b>JAVA</b> USER GROUP</h1><p>Collegiate Chapter Network</p></div></div>
 <div class="brand"><div class="cb"><h2>{e(chapter['short'])}</h2><p>Collegiate Chapter</p></div>
  <div class="card col"><img src="{logo_b64}"></div></div>
</div>
<div class="abs kicker"><i>★</i>PROUDLY RECOGNIZING</div>
<div class="abs {title_cls}">{title_html}</div>
<div class="abs stamp"><small>TENURE</small><b>{years}</b></div>
<div class="abs rib {name_cls}"><span>{e(name)}</span></div>
<div class="abs rib roleb"><span>{s['label']}</span></div>
<div class="abs desig">{e(leader.get('designation', ''))}</div>
<div class="abs band"></div><div class="abs band2"></div>
<div class="abs inst"><div class="badge"><img src="{logo_b64}"></div>
 <div><div class="inst-label">{"COLLEGIATE CHAPTER ALUMNI" if leader.get("status") == "past" else "ACTIVE COLLEGIATE CHAPTER"}</div><div class="inst-name">{e(chapter['full'])}</div>
 <div class="inst-meta">📍 {e(chapter['city'])}, Tamil Nadu</div></div></div>
<div class="abs footer"><span>🌐 tamilnadujug.org</span><span>💼 linkedin.com/company/tamil-jug</span></div>
<div class="abs seal"><div class="t"><b>TNJUG</b>Empowering Collegiate<br>Java Communities</div><div class="c"><img src="{tn_b64}"></div></div>
</body></html>"""


def render(html_text, out_png):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "poster.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html_text)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,1200",
                        f"--screenshot={out_png}", f"file://{page}"],
                       capture_output=True, text=True, timeout=120)
    return os.path.exists(out_png)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters = load_chapters()
    tn_b64 = data_uri(TNJUG_LOGO)
    ok = failed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "content/leaders/*.md"))):
        slug = os.path.splitext(os.path.basename(path))[0]
        leader = frontmatter(path)
        if not (leader.get("leader_type") == "chapter" or "Head of Chapters" in leader.get("role", "")):
            continue
        chapter = match_chapter(leader.get("chapter", ""), chapters)
        photo = os.path.join(ROOT, "static", leader.get("photo", "").lstrip("/"))
        if not chapter or not os.path.isfile(chapter["logo"]) or not os.path.isfile(photo):
            print(f"SKIP {slug}: missing chapter/logo/photo")
            failed += 1
            continue
        out = os.path.join(OUT_DIR, f"{slug}.png")
        page = poster_html(leader, chapter, tn_b64, data_uri(chapter["logo"]), data_uri(photo))
        if render(page, out):
            print(f"OK   {slug}")
            ok += 1
        else:
            print(f"FAIL {slug}")
            failed += 1
    print(f"\n{ok} posters in {OUT_DIR} ({failed} failed/skipped)")


if __name__ == "__main__":
    main()
