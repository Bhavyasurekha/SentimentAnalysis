import requests
import pandas as pd
import time

GRAPH_API_BASE = "https://graph.facebook.com/v17.0"

def get_page_posts(page_id: str, access_token: str, limit=100):
    posts = []
    url = f"{GRAPH_API_BASE}/{page_id}/posts"
    params = {
        "access_token": access_token,
        "limit": limit,
        "fields": "id,message,created_time,permalink_url"
    }
    while url:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("data", []):
            posts.append(item)
        # pagination
        paging = data.get("paging", {})
        url = paging.get("next")
        params = {}  # subsequent calls already include token in 'next' url
        time.sleep(0.5)
    return pd.DataFrame(posts)

def get_comments_for_post(post_id: str, access_token: str, limit=100):
    url = f"{GRAPH_API_BASE}/{post_id}/comments"
    params = {
        "access_token": access_token,
        "limit": limit,
        "fields": "id,message,created_time,from"
    }
    comments = []
    while url:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        comments.extend(data.get("data", []))
        paging = data.get("paging", {})
        url = paging.get("next")
        params = {}
        time.sleep(0.5)
    return pd.DataFrame(comments)

if __name__ == "__main__":
    PAGE_ID = "your_page_id"
    ACCESS_TOKEN = "your_user_or_page_access_token"
    posts_df = get_page_posts(PAGE_ID, ACCESS_TOKEN, limit=100)
    posts_df.to_csv("../data/raw_posts.csv", index=False)
    print("Saved posts:", posts_df.shape)
