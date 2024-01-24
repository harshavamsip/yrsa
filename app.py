# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

# # Set your YouTube Data API key here
# YOUTUBE_API_KEY ="AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# # Initialize the YouTube Data API client
# youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# # Function to search for videos and retrieve video details
# def search_and_recommend_videos(query, max_results=10):
#     response = youtube.search().list(
#         q=query,
#         type="video",
#         part="id,snippet",
#         maxResults=max_results,
#         videoCaption="any",
#     ).execute()

#     video_details = []
#     for item in response.get("items", []):
#         video_id = item["id"]["videoId"]
#         title = item["snippet"]["title"]

#         # Use a separate request to get video statistics
#         video_statistics = youtube.videos().list(
#             part="statistics",
#             id=video_id
#         ).execute()

#         likes = 0
#         views = 0

#         if "items" in video_statistics:
#             statistics = video_statistics["items"][0]["statistics"]
#             likes = int(statistics.get("likeCount", 0))
#             views = int(statistics.get("viewCount", 0))

#         link = f"https://www.youtube.com/watch?v={video_id}"

#         video_details.append((title, video_id, likes, views, link))

#     return video_details

# # Function to fetch video comments using the video ID
# def get_video_comments(video_id):
#     comments = []
#     results = youtube.commentThreads().list(
#         part="snippet",
#         videoId=video_id,
#         textFormat="plainText",
#         maxResults=100
#     ).execute()

#     while "items" in results:
#         for item in results["items"]:
#             comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#             comments.append(comment)
#         if "nextPageToken" in results:
#             results = youtube.commentThreads().list(
#                 part="snippet",
#                 videoId=video_id,
#                 textFormat="plainText",
#                 maxResults=100,
#                 pageToken=results["nextPageToken"]
#             ).execute()
#         else:
#             break

#     return comments

# # Function to perform sentiment analysis and categorize comments
# def analyze_and_categorize_comments(comments):
#     categorized_comments = {
#         "Positive": [],
#         "Negative": [],
#         "Neutral": []
#     }

#     for comment in comments:
#         analysis = TextBlob(comment)
#         sentiment_polarity = analysis.sentiment.polarity

#         # Categorize based on polarity
#         if sentiment_polarity > 0.2:
#             categorized_comments["Positive"].append(comment)
#         elif sentiment_polarity < -0.2:
#             categorized_comments["Negative"].append(comment)
#         else:
#             categorized_comments["Neutral"].append(comment)

#     return categorized_comments

# # Function to generate a word cloud from comments
# def generate_word_cloud(comments):
#     all_comments = ' '.join(comments)
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     return plt

# # Streamlit web app
# st.set_page_config(
#     page_title="YouTube Video Analyzer",
#     page_icon="📺",
#     layout="wide"
# )

# st.title("YouTube Video Analyzer")
# st.sidebar.header("Select Task")

# task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Generate Word Cloud"])

# if task == "Search Video Details":
#     search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

#     if st.sidebar.button("Search"):
#         video_details = search_and_recommend_videos(search_query)
#         st.subheader("Search Results:")
#         if video_details:
#             for video in video_details:
#                 st.write(f"**{video[0]}**")
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}")
#                 st.write(f"Watch Video: [Link]({video[4]})")

# if task == "Sentiment Analysis":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")
#         categorized_comments = analyze_and_categorize_comments(comments)
#         for sentiment, sentiment_comments in categorized_comments.items():
#             st.write(sentiment)
#             for comment in sentiment_comments:
#                 st.write(comment)

# if task == "Generate Word Cloud":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Generate Word Cloud"):
#         comments = get_video_comments(video_id)
#         st.subheader("Word Cloud")
#         wordcloud = generate_word_cloud(comments)
#         st.pyplot(wordcloud)



import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import plotly.express as px

# Add user authentication (use a simple example for illustration)
user_authenticated = st.checkbox("User Authenticated")

# Set your YouTube Data API key here
YOUTUBE_API_KEY ="AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# Initialize the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Function to search for videos and retrieve video details
def search_and_recommend_videos(query, max_results=10):
    response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=max_results,
        videoCaption="any",
    ).execute()

    video_details = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        
        # Use a separate request to get video statistics
        video_statistics = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

        likes = 0
        views = 0

        if "items" in video_statistics:
            statistics = video_statistics["items"][0]["statistics"]
            likes = int(statistics.get("likeCount", 0))
            views = int(statistics.get("viewCount", 0))

        link = f"https://www.youtube.com/watch?v={video_id}"

        video_details.append((title, video_id, likes, views, link))

    return video_details

# Function to fetch video details including duration and upload date
def get_video_details(video_id):
    video_details = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    ).execute()

    if "items" in video_details:
        details = video_details["items"][0]
        title = details["snippet"]["title"]
        duration = details["contentDetails"]["duration"]
        upload_date = details["snippet"]["publishedAt"]
        thumbnail_url = details["snippet"]["thumbnails"]["default"]["url"]

        return title, duration, upload_date, thumbnail_url
    else:
        return None, None, None, None

# Function to fetch video comments using the video ID
def get_video_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    ).execute()

    while "items" in results:
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        if "nextPageToken" in results:
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=results["nextPageToken"]
            ).execute()
        else:
            break

    return comments

# Function to perform sentiment analysis and categorize comments
def analyze_and_categorize_comments(comments):
    categorized_comments = {
        "Positive": [],
        "Negative": [],
        "Neutral": []
    }

    for comment in comments:
        analysis = TextBlob(comment)
        sentiment_polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        # Categorize based on polarity
        if sentiment_polarity > 0.2:
            categorized_comments["Positive"].append((comment, subjectivity))
        elif sentiment_polarity < -0.2:
            categorized_comments["Negative"].append((comment, subjectivity))
        else:
            categorized_comments["Neutral"].append((comment, subjectivity))

    return categorized_comments

# Function to generate a word cloud from comments
def generate_word_cloud(comments, custom_params=None):
    all_comments = ' '.join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    return plt

# Function to generate sentiment over time plot
def generate_sentiment_over_time_plot(sentiment_data):
    df = pd.DataFrame(sentiment_data)
    fig = px.line(df, x='Timestamp', y=['Positive', 'Neutral', 'Negative'], title='Sentiment Analysis Over Time')
    st.plotly_chart(fig)

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

# Add personalized dashboard for each authenticated user
if user_authenticated:
    user_name = st.sidebar.text_input("Enter Your Name")
    st.sidebar.write(f"Welcome, {user_name}!")

task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Generate Word Cloud"])

if task == "Search Video Details":
    search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

    if st.sidebar.button("Search"):
        video_details = search_and_recommend_videos(search_query)
        st.subheader("Search Results:")
        if video_details:
            for video in video_details:
                st.write(f"**{video[0]}**")
                st.write(f"Video ID: {video[1]}")
                st.write(f"Likes: {video[2]}, Views: {video[3]}")
                st.write(f"Watch Video: [Link]({video[4]})")

if task == "Sentiment Analysis":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Analyze Sentiment"):
        comments = get_video_comments(video_id)
        st.subheader("Sentiment Analysis")
        categorized_comments = analyze_and_categorize_comments(comments)
        sentiment_data = {"Positive": [], "Negative": [], "Neutral": []}
        for sentiment, sentiment_comments in categorized_comments.items():
            st.write(sentiment)
            for comment, subjectivity in sentiment_comments:
                st.write(f"Comment: {comment}")
                st.write(f"Subjectivity: {subjectivity}")
                st.write("----")

                # Collect data for sentiment over time plot
                sentiment_data[sentiment].append({
                    'Timestamp': datetime.now(),
                    sentiment: subjectivity
                })

        # Generate sentiment over time plot
        generate_sentiment_over_time_plot(sentiment_data)

if task == "Generate Word Cloud":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Generate Word Cloud"):
        comments = get_video_comments(video_id)
        st.subheader("Word Cloud")
        wordcloud = generate_word_cloud(comments)
        st.pyplot(wordcloud)

