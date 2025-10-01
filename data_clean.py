import pandas as pd
import re
import html
import contractions
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

STOPWORDS = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def remove_urls(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def remove_html_tags(text):
    return re.sub(r'<.*?>', '', html.unescape(text or ""))

def remove_emoji(text):
    # simple emoji strip (may not remove all)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U00002600-\U000026FF"  # misc symbols
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = html.unescape(text)
    text = contractions.fix(text)
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_emoji(text)
    text = re.sub(r'[^A-Za-z0-9\s\']', ' ', text)  # keep apostrophes
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def lemmatize_and_clean_tokens(text):
    tokens = [t for t in re.split(r'\s+', text) if t and t not in STOPWORDS]
    lemmas = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(lemmas)

def clean_df(df, text_col="message"):
    df = df.copy()
    df[text_col] = df[text_col].fillna("").astype(str)
    df["cleaned"] = df[text_col].apply(normalize_text)
    df = df[df["cleaned"].str.len() > 0].copy()
    df["is_english"] = df["cleaned"].apply(is_english)
    df = df[df["is_english"]].copy()
    df["cleaned"] = df["cleaned"].apply(lemmatize_and_clean_tokens)
    df.drop_duplicates(subset=["cleaned"], inplace=True)
    return df

if __name__ == "__main__":
    df = pd.read_csv("../data/raw_posts.csv")
    out = clean_df(df, text_col="message")   # or 'text'
    out.to_csv("../data/cleaned_posts.csv", index=False)
    print("Cleaned saved:", out.shape)
