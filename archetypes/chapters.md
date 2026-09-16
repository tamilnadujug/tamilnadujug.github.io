---
title: "{{ replace .Name "-" " " | title }}"
college_name: "{{ replace .Name "-" " " | title }}"
city: "Coimbatore"
established_year: "2026"
logo: "/logos/default-logo.svg"
status: "Active Chapter"
email: "chapter@institution.edu.in"
description: "Brief summary about this institution's TNJUG student chapter."
# Note: Chapter leaders are managed independently in content/leaders/*.md
# and linked automatically by setting `chapter: "{{ replace .Name "-" " " | title }}"`
---

### Chapter Overview

Detailed write-up about chapter activities, campus facilities, and community impact.
