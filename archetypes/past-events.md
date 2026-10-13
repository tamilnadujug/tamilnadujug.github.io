---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date.Format "2006-01-02" }}
event_date: "{{ .Date.Format "2006-01-02" }}"
event_time: "10:00 AM – 1:00 PM IST"
location: "Coimbatore, Tamil Nadu"
event_type: "Community Meetup"
summary: "A concise overview of the event theme, target audience, and key technologies presented."
banner: "/images/past-events/{{ .Name }}/banner.svg"
speakers:
  - name: "Speaker Name"
    role: "Senior Java Engineer"
    organization: "Company or Institution"
    photo: "/photos/default-avatar.png"
highlights:
  - "Technical presentation on modern JVM architectures"
  - "Hands-on code walkthrough and community discussion"
  - "Open Q&A and networking session"
gallery:
  - image: "/images/past-events/{{ .Name }}/photo-1.svg"
    caption: "Technical presentation session"
  - image: "/images/past-events/{{ .Name }}/photo-2.svg"
    caption: "Audience participation and discussions"
recording_url: ""
slides_url: ""
repo_url: ""
draft: false
---

## About the Event

Detailed background and objectives of the meetup or workshop.

## Sessions and Discussions

### Session 1: Title
Overview of the topics and code examples presented.

### Session 2: Title
Overview of subsequent technical deep-dives or labs.

## Community Highlights

Key moments, attendee engagement, and community discussions.

## Key Takeaways

1. Core architectural or conceptual takeaway.
2. Practical engineering recommendation.

## Acknowledgements

Recognition for speakers, student volunteers, faculty advisors, and venue organizers.
