# Tamil Nadu Java User Group (TNJUG) Website

The official, production-quality website for the **Tamil Nadu Java User Group (TNJUG)**, built with [Hugo](https://gohugo.io/).

- **Presentation / Content**: Hugo (Extended) + Vanilla CSS (zero framework bloat, fast load times).
- **Registration & Ticketing**: External via [Luma](https://luma.com/calendar/manage/cal-pUXuk1OFUWQFQEk). No proprietary registration or backend database required.
- **Deployment**: Automated GitHub Actions workflow deploying to GitHub Pages.

---

## 1. Project Structure

```
tamilnadujug.github.io/
├── .github/
│   └── workflows/
│       └── hugo.yml           # Automated GitHub Pages CI/CD pipeline
├── archetypes/                # Content templates for `hugo new`
│   ├── chapters.md            # Archetype for college chapters
│   ├── events.md              # Archetype for meetups & workshops
│   ├── leaders.md             # Archetype for core team & chapter leads
│   └── open-source.md         # Archetype for OSS projects
├── assets/
│   └── css/
│       └── style.css          # Design system & responsive styles
├── content/                   # Markdown content collections
│   ├── chapters/              # College & regional chapters
│   ├── community/             # Values, Code of Conduct & CFP guidelines
│   ├── events/                # Upcoming & past meetups (with Luma links)
│   ├── leaders/               # Core team and chapter leadership
│   └── open-source/           # Community open-source projects
├── layouts/                   # Hugo templates & reusable partials
│   ├── _default/              # baseof.html, single.html, list.html
│   ├── chapters/              # Chapter list & single layout
│   ├── community/             # Community guide layout
│   ├── events/                # Events list (upcoming/past tabs) & single layout
│   ├── leaders/               # Leaders layout (Core + Chapter leads)
│   ├── open-source/           # Open source projects layout
│   ├── partials/              # Modular cards: event, chapter, leader, etc.
│   └── index.html             # Homepage layout
├── static/                    # Static assets copied directly to site root
│   ├── images/
│   ├── logos/                 # College & chapter SVG logos
│   ├── photos/                # Leader & speaker avatars
│   └── tamil_jug.jpeg         # Official TNJUG logo & favicon
└── hugo.toml                  # Site configuration, menus & taxonomies
```

---

## 2. How to Run Locally

### Prerequisites

Install **Hugo Extended** (version 0.125.0 or later):

```bash
# macOS (via Homebrew)
brew install hugo

# Linux (Debian / Ubuntu)
sudo apt-get install hugo
# Or download extended deb from https://github.com/gohugoio/hugo/releases

# Windows (via Chocolatey or Scoop)
choco install hugo-extended
```

Verify the installation:

```bash
hugo version
```

### Start Development Server

Clone the repository and run Hugo server:

```bash
# Clone the repository
git clone https://github.com/tamilnadujug/tamilnadujug.github.io.git
cd tamilnadujug.github.io

# Start the local live-reload server
hugo server -D
```

Open `http://localhost:1313/` in your browser.

---

## 3. How to Add an Event

All event registrations are powered externally by **Luma**. To add a new event:

### Option A: Using Hugo CLI

```bash
hugo new events/spring-ai-meetup.md
```

### Option B: Create Manually in `content/events/<slug>.md`

```markdown
---
title: "Spring AI & Modern Concurrency Meetup"
date: 2026-11-20T10:00:00+05:30
start_time: "10:00 AM"
end_time: "01:30 PM"
venue: "Sri Eshwar College Auditorium"
city: "Coimbatore"
description: "Hands-on masterclass on Spring AI vector stores and Loom virtual threads."
speaker: "Speaker Name"
event_type: "Meetup"          # Meetup | Workshop | Conference | Hackathon
chapter: "Sri Eshwar College of Engineering"
luma_url: "https://lu.ma/your-event-slug"  # Direct external Luma registration link
recording_url: ""
slides_url: ""
photos_url: ""
status: "upcoming"            # upcoming | past | sold-out
featured: true                # Set true to spotlight on the homepage
---

### Agenda

- 10:00 AM: Welcome and community kick-off
- 10:30 AM: Deep Dive Presentation
- 12:30 PM: Networking & Q&A
```

---

## 4. How to Add a Chapter

Create a markdown file in `content/chapters/<institution-slug>.md`:

```markdown
---
title: "Government College of Technology"
college_name: "Government College of Technology"
city: "Coimbatore"
established_year: "2026"
logo: "/logos/gct-logo.svg"    # Place logo file inside static/logos/
status: "Active Chapter"
email: "chapter@gct.ac.in"
description: "Student chapter focusing on JVM internals, Spring Boot, and open source."
faculty_leader:
  name: "Dr. Faculty Name"
  designation: "Associate Professor & Head"
  experience: "15+ years"
  about: "Faculty advisor passionate about mentoring students in Java development."
  email: "faculty@gct.ac.in"
student_leader:
  name: "Student Lead Name"
  year: "3rd Year CSE"
  about: "Student organizer coordinating local workshops and hackathons."
  email: "lead@gct.ac.in"
---

### About the Chapter

Detailed description of chapter facilities, upcoming student initiatives, and contact guidelines.
```

---

## 5. How to Add a Leader

Create a markdown file in `content/leaders/<leader-name>.md`:

```markdown
---
title: "Karthik Subramanian"
role: "Community Organizer"
type: "core"                   # "core" for Core Team, "chapter" for Chapter Leaders
chapter: "Tamil Nadu Java User Groups"   # Or college name for chapter leads
bio: "Staff engineer passionate about Java community building, mentorship, and high-concurrency systems."
photo: "/photos/karthik.svg"   # Place avatar inside static/photos/
linkedin: "https://linkedin.com/in/karthik"
github: "https://github.com/karthik"
twitter: "https://twitter.com/karthik"
website: "https://karthik.dev"
---
```

---

## 6. How to Deploy

The site uses **GitHub Actions** for fully automated deployment to **GitHub Pages**.

### Continuous Deployment via Git Push

1. Commit and push your changes to the `main` branch:
   ```bash
   git add .
   git commit -m "feat: add upcoming meetup at Coimbatore"
   git push origin main
   ```
2. The workflow in `.github/workflows/hugo.yml` automatically triggers:
   - Sets up Hugo Extended
   - Minifies CSS and compiles the site into `./public`
   - Deploys the static bundle to GitHub Pages (`https://tamilnadujug.github.io/`)

### Manual Production Build

To test a production build locally before committing:

```bash
hugo --gc --minify
```

The compiled production assets will be output in the `public/` directory.