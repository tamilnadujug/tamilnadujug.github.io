#!/usr/bin/env python3
import os
import glob
import base64
import subprocess
from PIL import Image

WORKSPACE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.expanduser("~/Downloads/chapter_leader_poster")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHAPTER_INFO = {
    "College of Engineering Guindy, Anna University": {
        "short_name": "Anna University (CEG)",
        "full_name": "College of Engineering, Guindy (CEG), Anna University",
        "city": "Chennai",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/ceg-logo.png")
    },
    "College of Engineering, Guindy (CEG), Anna University": {
        "short_name": "Anna University (CEG)",
        "full_name": "College of Engineering, Guindy (CEG), Anna University",
        "city": "Chennai",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/ceg-logo.png")
    },
    "Kongu Engineering College": {
        "short_name": "Kongu Engg College",
        "full_name": "Kongu Engineering College",
        "city": "Perundurai / Erode",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/kongu-logo.png")
    },
    "PSNA College of Engineering and Technology": {
        "short_name": "PSNA CET",
        "full_name": "PSNA College of Engineering and Technology",
        "city": "Dindigul",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/psna-logo.png")
    },
    "Sri Eshwar College of Engineering": {
        "short_name": "Sri Eshwar College of Engg",
        "full_name": "Sri Eshwar College of Engineering",
        "city": "Coimbatore",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/sece-logo.png")
    },
    "VET Institute of Arts and Science": {
        "short_name": "VET Institute of Arts & Science",
        "full_name": "VET Institute of Arts and Science (Co-education) College",
        "city": "Erode",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/vetias-logo.png")
    },
    "VET Institute of Arts and Science (Co-education) College": {
        "short_name": "VET Institute of Arts & Science",
        "full_name": "VET Institute of Arts and Science (Co-education) College",
        "city": "Erode",
        "logo": os.path.join(WORKSPACE_DIR, "static/logos/vetias-logo.png")
    }
}

TNJUG_LOGO_PATH = os.path.join(WORKSPACE_DIR, "static/tamil_jug.jpeg")

def to_base64_uri(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "rb") as f:
        data = f.read()
    ext = file_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

def parse_markdown_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    data = {}
    in_fm = False
    for line in lines:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break
        if in_fm and ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    return data

def build_poster_html(leader, tnjug_b64, college_logo_b64, photo_b64, ch_data):
    name = leader.get("title", "Chapter Leader")
    role_raw = leader.get("role", "Chapter Leader")
    designation = leader.get("designation", "")
    bio = leader.get("bio", "Fostering enterprise Java excellence, developer mentorship, and student open-source community growth.")
    status = leader.get("status", "active")
    
    # Role styling and titles
    if "Head of Chapters" in role_raw:
        role_label = "HEAD OF CHAPTERS"
        announcement_title = "HEAD OF CHAPTERS 2026 – 2027"
        tenure_label = "TENURE 2026 – 2027"
        role_badge_style = "background: rgba(245, 158, 11, 0.18); color: #FBBF24; border: 1.5px solid rgba(245, 158, 11, 0.5);"
    elif "Professional" in role_raw:
        role_label = "FACULTY CHAPTER LEADER"
        announcement_title = "CHAPTER LEADER 2026 – 2027"
        tenure_label = "TENURE 2026 – 2027"
        role_badge_style = "background: rgba(45, 212, 191, 0.16); color: #2DD4BF; border: 1.5px solid rgba(45, 212, 191, 0.5);"
    elif status == "past":
        role_label = "CAMPUS LEADER (ALUMNI)"
        announcement_title = "CHAPTER LEADER ALUMNI"
        tenure_label = "TENURE 2024 – 2025"
        role_badge_style = "background: rgba(167, 139, 250, 0.16); color: #A78BFA; border: 1.5px solid rgba(167, 139, 250, 0.5);"
    else:
        role_label = "CAMPUS LEADER"
        announcement_title = "CHAPTER LEADER 2026 – 2027"
        tenure_label = "TENURE 2026 – 2027"
        role_badge_style = "background: rgba(56, 189, 248, 0.16); color: #38BDF8; border: 1.5px solid rgba(56, 189, 248, 0.5);"

    college_short = ch_data.get("short_name", "Collegiate Chapter")
    college_full = ch_data.get("full_name", leader.get("chapter", "Engineering College"))
    college_city = ch_data.get("city", "Tamil Nadu")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1200px;
    height: 1200px;
    overflow: hidden;
    position: relative;
    background-color: #0A0F1D;
    background-image: 
      radial-gradient(circle at 12% 12%, rgba(231, 111, 81, 0.24) 0%, transparent 40%),
      radial-gradient(circle at 88% 88%, rgba(42, 157, 143, 0.22) 0%, transparent 45%),
      radial-gradient(circle at 50% 36%, rgba(59, 130, 246, 0.12) 0%, transparent 50%),
      linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #F8FAFC;
    padding: 44px 50px 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  /* Top Bar */
  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 8px;
  }}

  .header-tnjug {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .tnjug-box {{
    width: 74px;
    height: 74px;
    border-radius: 18px;
    background: #FFFFFF;
    padding: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    border: 2px solid rgba(255, 255, 255, 0.2);
  }}

  .tnjug-box img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 8px;
  }}

  .tnjug-text h1 {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #FFFFFF;
    text-transform: uppercase;
  }}

  .tnjug-text p {{
    font-size: 13px;
    font-weight: 600;
    color: #94A3B8;
    letter-spacing: 0.6px;
    margin-top: 3px;
  }}

  .header-college {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .college-badge-text {{
    text-align: right;
  }}

  .college-badge-text .cname {{
    font-size: 15px;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: 0.5px;
  }}

  .college-badge-text .csub {{
    font-size: 12px;
    font-weight: 600;
    color: #38BDF8;
    letter-spacing: 0.5px;
    margin-top: 2px;
  }}

  .college-box {{
    height: 74px;
    min-width: 80px;
    max-width: 180px;
    border-radius: 18px;
    background: #FFFFFF;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    border: 2px solid rgba(255, 255, 255, 0.2);
  }}

  .college-box img {{
    max-height: 56px;
    max-width: 148px;
    width: auto;
    height: auto;
    object-fit: contain;
  }}

  /* Main Body Content */
  .main-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    width: 100%;
    padding: 6px 0 18px;
  }}

  /* Announcement Banner */
  .announcement {{
    text-align: center;
  }}

  .ribbon {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(231, 111, 81, 0.25), rgba(244, 162, 97, 0.28));
    border: 1.5px solid rgba(244, 162, 97, 0.65);
    padding: 7px 26px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #F4A261;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(231, 111, 81, 0.15);
  }}

  .announcement-title {{
    margin-top: 8px;
    font-size: 39px;
    font-weight: 900;
    letter-spacing: 1px;
    background: linear-gradient(90deg, #FFFFFF 0%, #F8FAFC 45%, #E2E8F0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-transform: uppercase;
  }}

  /* Photo Section */
  .photo-wrapper {{
    position: relative;
    width: 320px;
    height: 320px;
  }}

  .glow-ring {{
    position: absolute;
    inset: -10px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E76F51, #F4A261, #2A9D8F);
    filter: blur(8px);
    opacity: 0.9;
  }}

  .photo-frame {{
    position: absolute;
    inset: -3px;
    border-radius: 50%;
    background: #0F172A;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
  }}

  .photo-frame img {{
    width: 314px;
    height: 314px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center top;
    border: 3.5px solid rgba(255, 255, 255, 0.25);
  }}

  /* Leader Information */
  .leader-info {{
    text-align: center;
    width: 100%;
  }}

  .leader-name {{
    font-size: 43px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    line-height: 1.15;
  }}

  .badge-row {{
    display: flex;
    justify-content: center;
    gap: 12px;
    align-items: center;
    margin-top: 10px;
  }}

  .role-badge {{
    {role_badge_style}
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 20px;
  }}

  .tenure-badge {{
    background: rgba(42, 157, 143, 0.18);
    color: #2DD4BF;
    border: 1.5px solid rgba(42, 157, 143, 0.45);
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 20px;
  }}

  .designation {{
    font-size: 20px;
    color: #CBD5E1;
    font-weight: 500;
    margin-top: 8px;
  }}

  /* Bio Quote */
  .bio-card {{
    background: rgba(255, 255, 255, 0.035);
    border: 1px dashed rgba(244, 162, 97, 0.4);
    border-radius: 14px;
    padding: 12px 32px;
    max-width: 980px;
    font-size: 15.5px;
    line-height: 1.45;
    color: #E2E8F0;
    font-style: italic;
    text-align: center;
  }}

  /* College Card */
  .college-card {{
    background: rgba(30, 41, 59, 0.75);
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 14px 28px;
    max-width: 980px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  }}

  .college-card-left {{
    display: flex;
    align-items: center;
    gap: 16px;
    text-align: left;
  }}

  .college-card-icon {{
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: rgba(231, 111, 81, 0.15);
    border: 1px solid rgba(231, 111, 81, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
  }}

  .college-card-title {{
    font-size: 18px;
    font-weight: 700;
    color: #F8FAFC;
  }}

  .college-card-city {{
    font-size: 13.5px;
    color: #94A3B8;
    margin-top: 2px;
  }}

  .chapter-status-pill {{
    background: rgba(42, 157, 143, 0.2);
    border: 1px solid rgba(42, 157, 143, 0.45);
    color: #2DD4BF;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 8px 16px;
    border-radius: 10px;
    white-space: nowrap;
  }}

  /* Bottom Bar */
  .footer {{
    width: calc(100% + 100px);
    margin: 0 -50px;
  }}

  .footer-line {{
    height: 5px;
    background: linear-gradient(90deg, #E76F51 0%, #F4A261 35%, #2A9D8F 70%, #3B82F6 100%);
  }}

  .footer-content {{
    padding: 16px 50px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(10, 15, 29, 0.98);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }}

  .footer-links {{
    display: flex;
    align-items: center;
    gap: 28px;
  }}

  .footer-link {{
    font-size: 14px;
    font-weight: 600;
    color: #E2E8F0;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .footer-tags {{
    font-size: 13px;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 0.6px;
  }}
</style>
</head>
<body>

  <!-- Top Bar -->
  <div class="header">
    <div class="header-tnjug">
      <div class="tnjug-box">
        <img src="{tnjug_b64}" alt="TNJUG Logo">
      </div>
      <div class="tnjug-text">
        <h1>TAMIL NADU JAVA USER GROUP</h1>
        <p>Official Collegiate Chapter Network</p>
      </div>
    </div>
    <div class="header-college">
      <div class="college-badge-text">
        <div class="cname">{college_short}</div>
        <div class="csub">Collegiate Chapter</div>
      </div>
      <div class="college-box">
        <img src="{college_logo_b64}" alt="{college_short} Logo">
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="main-content">
    <!-- Announcement Ribbon -->
    <div class="announcement">
      <div class="ribbon">★ WE PROUDLY ANNOUNCE ★</div>
      <div class="announcement-title">{announcement_title}</div>
    </div>

    <!-- Photo Section -->
    <div class="photo-wrapper">
      <div class="glow-ring"></div>
      <div class="photo-frame">
        <img src="{photo_b64}" alt="{name}">
      </div>
    </div>

    <!-- Leader Information -->
    <div class="leader-info">
      <div class="leader-name">{name}</div>
      <div class="badge-row">
        <span class="role-badge">{role_label}</span>
        <span class="tenure-badge">{tenure_label}</span>
      </div>
      <div class="designation">{designation}</div>
    </div>

    <!-- Bio Quote -->
    <div class="bio-card">
      “{bio}”
    </div>

    <!-- College Card -->
    <div class="college-card">
      <div class="college-card-left">
        <div class="college-card-icon">🏛️</div>
        <div>
          <div class="college-card-title">{college_full}</div>
          <div class="college-card-city">📍 {college_city}, Tamil Nadu</div>
        </div>
      </div>
      <div class="chapter-status-pill">Active Chapter</div>
    </div>
  </div>

  <!-- Bottom Bar -->
  <div class="footer">
    <div class="footer-line"></div>
    <div class="footer-content">
      <div class="footer-links">
        <span class="footer-link">🌐 tamilnadujug.org</span>
        <span class="footer-link">💼 linkedin.com/company/tamil-jug</span>
      </div>
      <div class="footer-tags">#TNJUG &nbsp;•&nbsp; #JavaCommunity &nbsp;•&nbsp; #Leadership2026</div>
    </div>
  </div>

</body>
</html>
"""
    return html

def main():
    tnjug_b64 = to_base64_uri(TNJUG_LOGO_PATH)
    
    leader_files = sorted(glob.glob(os.path.join(WORKSPACE_DIR, "content/leaders/*.md")))
    all_leaders = []
    for lf in leader_files:
        data = parse_markdown_frontmatter(lf)
        data["_slug"] = os.path.splitext(os.path.basename(lf))[0]
        
        # Check if chapter leader or Head of Chapters
        ltype = data.get("leader_type")
        role = data.get("role", "")
        ch = data.get("chapter", "")
        
        if ltype == "chapter" or "Chapter" in role or ch in CHAPTER_INFO:
            all_leaders.append(data)
            
    print(f"Found {len(all_leaders)} chapter leaders to render posters for.")
    
    generated = []
    for i, leader in enumerate(all_leaders, 1):
        slug = leader["_slug"]
        name = leader.get("title")
        chapter = leader.get("chapter")
        ch_data = CHAPTER_INFO.get(chapter, {
            "short_name": chapter,
            "full_name": chapter,
            "city": leader.get("city", "Tamil Nadu"),
            "logo": TNJUG_LOGO_PATH
        })
        
        # Leader photo
        photo_rel = leader.get("photo", "").lstrip("/")
        photo_path = os.path.join(WORKSPACE_DIR, "static", photo_rel)
        if not os.path.exists(photo_path):
            print(f"Warning: Photo not found for {name}: {photo_path}")
            continue
        photo_b64 = to_base64_uri(photo_path)
        
        # College logo
        logo_path = ch_data.get("logo")
        if not os.path.exists(logo_path):
            print(f"Warning: Logo not found: {logo_path}")
            logo_path = TNJUG_LOGO_PATH
        college_logo_b64 = to_base64_uri(logo_path)
        
        html_content = build_poster_html(leader, tnjug_b64, college_logo_b64, photo_b64, ch_data)
        
        temp_html_path = f"/tmp/poster_{slug}.html"
        output_png_path = os.path.join(OUTPUT_DIR, f"{slug}.png")
        
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"[{i}/{len(all_leaders)}] Rendering poster for {name} ({slug})...")
        res = subprocess.run([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--headless=new",
            "--disable-gpu",
            "--window-size=1200,1200",
            f"--screenshot={output_png_path}",
            f"file://{temp_html_path}"
        ], capture_output=True, text=True)
        
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
            
        if os.path.exists(output_png_path):
            img = Image.open(output_png_path)
            print(f"    -> Done: {output_png_path} ({img.size[0]}x{img.size[1]})")
            generated.append(output_png_path)
        else:
            print(f"    -> ERROR rendering {output_png_path}: {res.stderr}")

    print(f"\nSuccessfully generated {len(generated)} posters in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
