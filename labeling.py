import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def vader_label(text):
    vs = analyzer.polarity_scores(text)
    c = vs["compound"]
    if c >= 0.05:
        return "positive"
    elif c <= -0.05:
        return "negative"
    else:
        return "neutral"

if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_posts.csv")
    df['label'] = df['cleaned'].apply(vader_label)
    df.to_csv("../data/labeled_vader.csv", index=False)
    print("Labelled (vader) saved:", df['label'].value_counts())
