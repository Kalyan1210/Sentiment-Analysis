# Updated Twitter Sentiment Analysis Code

# %% Import required libraries
import tweepy
import re
from collections import Counter
import streamlit as st
import matplotlib.pyplot as plt
from transformers import pipeline

# API keys and tokens
API_KEY = "ES6I7qhgrwDUUIawZ28mGLMVu"
API_SECRET = "84V91gEvYHZClJPkwzcbZvNhwD0Ow7vMnLn8PCsGrSpKBFko7P"
ACCESS_TOKEN = "1869937631842258944-hxZPHSnOGuL8XhXbs3LdKlPrx76EDe"
ACCESS_TOKEN_SECRET = "vwTtZZFL3F1xotnMXkByzeGygKWwGcTcIJI9chutM7upS"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJeUxgEAAAAAJhEIueg9AS1%2BiQ5KW8Fy6TeQ%2FeI%3Dm2UZxCOCI6ymi8IzRkA8PJO9euGzj3l9upLkj5fYxpiTC8eqwI"

# Authenticate
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Streamlit UI
st.title("Twitter Sentiment Analysis and Trend Prediction")
company = st.selectbox("Select Company", ["Tesla", "Apple", "Google", "Amazon"])
query = company

if st.button("Fetch Tweets"):
    try:
        # Fetch tweets
        response = client.search_recent_tweets(query=query, max_results=50, tweet_fields=["public_metrics", "text"])
        tweets = response.data if response.data else []

        if not tweets:
            st.warning("No tweets found!")
        else:
            st.success("Tweets fetched successfully!")

            # Process tweets
            tweet_texts = [tweet.text for tweet in tweets]
            cleaned_tweets = [re.sub(r"http\S+|@\w+|[^A-Za-z0-9\s]", "", text).strip() for text in tweet_texts]

            # Sentiment Analysis
            sentiment_pipeline = pipeline("sentiment-analysis")
            sentiments = sentiment_pipeline(cleaned_tweets)
            sentiment_labels = [result["label"] for result in sentiments]

            # Display Sentiment Results
            st.subheader("Sentiment Distribution")
            counts = Counter(sentiment_labels)
            fig, ax = plt.subplots()
            ax.bar(counts.keys(), counts.values(), color=['green', 'red', 'gray'])
            st.pyplot(fig)

            # Emoji and Hashtag Analysis
            emojis = Counter([char for text in tweet_texts for char in text if char in re.findall(r"[^\w\s,]", text)])
            hashtags = Counter([word for text in tweet_texts for word in text.split() if word.startswith("#")])

            st.subheader("Emoji Sentiment Analysis")
            if emojis:
                emoji_fig, emoji_ax = plt.subplots()
                emoji_ax.bar(emojis.keys(), emojis.values(), color='blue')
                st.pyplot(emoji_fig)
            else:
                st.write("No emojis found in tweets.")

            st.subheader("Hashtag Frequency")
            if hashtags:
                hashtag_fig, hashtag_ax = plt.subplots()
                hashtag_ax.bar(hashtags.keys(), hashtags.values(), color='purple')
                st.pyplot(hashtag_fig)
            else:
                st.write("No hashtags found in tweets.")

            # Tweet Impact Score
            impact_scores = []
            for tweet in tweets:
                metrics = tweet.public_metrics
                score = metrics["retweet_count"] * 2 + metrics["like_count"] * 1.5 + metrics["reply_count"]
                impact_scores.append((tweet.text, score))
            sorted_scores = sorted(impact_scores, key=lambda x: x[1], reverse=True)

            st.subheader("Top 5 Impactful Tweets")
            for text, score in sorted_scores[:5]:
                st.write(f"Impact Score: {score}")
                st.write(f"Tweet: {text}")
                st.write("---")

            # Sentiment-Driven Recommendations
            st.subheader("Recommendations")
            if counts["NEGATIVE"] > counts["POSITIVE"]:
                st.write(f"Public sentiment around {query} is more negative. Consider addressing common concerns like:")
                st.write("- Enhancing customer service.")
                st.write("- Improving product quality.")
                st.write("- Clarifying recent controversies.")
            elif counts["POSITIVE"] > counts["NEGATIVE"]:
                st.write(
                    f"Public sentiment around {query} is mostly positive. Keep building on these positive aspects:")
                st.write("- Highlighting successful milestones.")
                st.write("- Amplifying customer satisfaction stories.")
            else:
                st.write(f"Public sentiment around {query} is neutral. It may help to:")
                st.write("- Increase engagement through positive PR campaigns.")
                st.write("- Address any potential concerns proactively.")

    except Exception as e:
        st.error(f"Try after 15 mins, Error fetching tweets: {e}")
        tweets = []
