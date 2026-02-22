import requests
from bs4 import BeautifulSoup
import csv

KEYWORDS = [
    "react developer",
    "frontend developer",
    "mern developer",
    "software developer intern"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

HOT_WORDS = [
    "apply", "form", "registration", "link", "careers",
    "forms.gle", "docs.google.com/forms"
]

WARM_WORDS = [
    "send resume", "share resume", "dm", "inbox",
    "email cv", "we are hiring", "looking for"
]

def classify(text):
    t = text.lower()
    if any(w in t for w in HOT_WORDS):
        return "HOT 🔥 Apply Fast"
    if any(w in t for w in WARM_WORDS):
        return "WARM ⭐ Message HR"
    return "COLD"

def fetch_posts(keyword):
    url = f"https://www.bing.com/search?q=site:linkedin.com/posts+{keyword}+hiring&count=20"
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    posts = []

    for a in soup.select("li.b_algo h2 a"):
        link = a.get("href")
        title = a.get_text(" ", strip=True)

        if "linkedin.com/posts" in link:
            priority = classify(title)
            posts.append((priority, keyword.title(), link))

    return posts

all_jobs = set()

for k in KEYWORDS:
    for job in fetch_posts(k):
        all_jobs.add(job)

with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Priority", "Role", "Link"])
    writer.writerows(sorted(all_jobs, reverse=True))

print("Saved jobs.csv")
