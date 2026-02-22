import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import unquote

KEYWORDS = [
    "hiring react developer",
    "frontend developer hiring",
    "mern developer hiring",
    "software developer intern hiring"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

HOT_WORDS = [
    "apply here", "apply now", "registration", "google form",
    "forms.gle", "docs.google.com/forms", "careers", "job link"
]

WARM_WORDS = [
    "send resume", "share resume", "dm me", "inbox me",
    "email your cv", "looking for", "we are hiring"
]

def clean_link(href):
    if href and href.startswith("/url?q="):
        return unquote(href.split("/url?q=")[1].split("&")[0])
    return None

def classify(text, link):
    content = (text + " " + link).lower()

    if any(w in content for w in HOT_WORDS):
        return "HOT 🔥 Apply Fast"
    elif any(w in content for w in WARM_WORDS):
        return "WARM ⭐ Message HR"
    return "COLD"

def detect_role(text):
    text = text.lower()
    if "react" in text: return "React Developer"
    if "frontend" in text: return "Frontend Developer"
    if "mern" in text: return "MERN Developer"
    if "intern" in text: return "Intern"
    return "Developer"

def search():
    results = set()

    for keyword in KEYWORDS:
        url = f"https://www.google.com/search?q=site:linkedin.com/posts {keyword}&num=20&sort=date"
        html = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select("a"):
            link = clean_link(a.get("href"))
            if not link or "linkedin.com/posts" not in link:
                continue

            text = a.get_text(" ", strip=True)

            priority = classify(text, link)
            role = detect_role(text)

            results.add((priority, role, link))

    return sorted(results, reverse=True)

jobs = search()

with open("jobs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Priority", "Role", "Link"])
    writer.writerows(jobs)

print("Saved jobs.csv")
