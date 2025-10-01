import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible)"}

def fetch_public_page_mobile(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text

def parse_simple_posts(html):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    # Example: mobile view layout; this will be brittle and may break
    for post in soup.select("div[data-ft]"):
        text = post.get_text(separator=" ", strip=True)
        posts.append({"text": text})
    return pd.DataFrame(posts)

if __name__ == "__main__":
    url = "https://m.facebook.com/yourpublicpage"
    html = fetch_public_page_mobile(url)
    df = parse_simple_posts(html)
    df.to_csv("../data/raw_posts.csv", index=False)
    print("Saved", len(df), "posts")
