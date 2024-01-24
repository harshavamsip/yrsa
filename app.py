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
from nltk.corpus import stopwords
from langdetect import detect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from langdetect import detect_langs

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
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()

        if "items" in video_statistics:
            details = video_statistics["items"][0]
            duration = details["contentDetails"]["duration"]
            upload_date = details["snippet"]["publishedAt"]
            thumbnail_url = details["snippet"]["thumbnails"]["default"]["url"]
            channel_name = details["snippet"]["channelTitle"]
            likes = details["statistics"].get("likeCount", 0)
            views = details["statistics"].get("viewCount", 0)

            link = f"https://www.youtube.com/watch?v={video_id}"

            video_details.append((title, video_id, duration, upload_date, thumbnail_url, channel_name, likes, views, link))

    return video_details

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

    sentiment_data = {"Positive": [], "Negative": [], "Neutral": []}

    for comment in comments:
        analysis = TextBlob(comment)
        sentiment_polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        # Categorize based on polarity
        if sentiment_polarity > 0.2:
            categorized_comments["Positive"].append((comment, subjectivity))
            sentiment_data["Positive"].append(subjectivity)
        elif sentiment_polarity < -0.2:
            categorized_comments["Negative"].append((comment, subjectivity))
            sentiment_data["Negative"].append(subjectivity)
        else:
            categorized_comments["Neutral"].append((comment, subjectivity))
            sentiment_data["Neutral"].append(subjectivity)

    return categorized_comments, sentiment_data

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
    fig = px.line(df, title='Sentiment Analysis Over Time')
    st.plotly_chart(fig)

# Function to filter comments based on sentiment or other criteria
def filter_and_sort_comments(comments, sentiment_filter=None, sort_by=None):
    if sentiment_filter:
        comments = categorized_comments[sentiment_filter]
    if sort_by:
        comments.sort(key=lambda x: x[1][sort_by], reverse=True)
    return comments

# Function to extract keywords from comments
def extract_keywords(comments):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comments)
    
    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(X)
    
    feature_names = vectorizer.get_feature_names_out()
    top_keywords = [feature_names[i] for i in lda.components_[0].argsort()[-10:][::-1]]
    
    return top_keywords

# Function to get additional video details
def get_video_details(video_id):
    video_statistics = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    ).execute()

    if "items" in video_statistics:
        details = video_statistics["items"][0]
        title = details["snippet"]["title"]
        duration = details["contentDetails"]["duration"]
        upload_date = details["snippet"]["publishedAt"]
        thumbnail_url = details["snippet"]["thumbnails"]["default"]["url"]
        channel_name = details["snippet"]["channelTitle"]
        likes = details["statistics"].get("likeCount", 0)
        views = details["statistics"].get("viewCount", 0)

        return title, duration, upload_date, thumbnail_url, channel_name, likes, views

# Streamlit web app
st.set_page_config(
    page_title="Advanced YouTube Video Analyzer",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Advanced YouTube Video Analyzer")
st.sidebar.header("Select Task")

# Add personalized dashboard for each authenticated user
if user_authenticated:
    user_name = st.sidebar.text_input("Enter Your Name")
    st.sidebar.write(f"Welcome, {user_name}!")

task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Generate Word Cloud", "Advanced Features"])

if task == "Search Video Details":
    search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

    if st.sidebar.button("Search"):
        video_details = search_and_recommend_videos(search_query)
        st.subheader("Search Results:")
        if video_details:
            for video in video_details:
                st.write(f"**{video[0]}**")
                st.write(f"Video ID: {video[1]}")
                st.write(f"Duration: {video[2]}")
                st.write(f"Upload Date: {video[3]}")
                st.write(f"Channel Name: {video[5]}")
                st.write(f"Likes: {video[6]}, Views: {video[7]}")
                st.write(f"Watch Video: [Link]({video[8]})")

if task == "Sentiment Analysis":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Analyze Sentiment"):
        comments = get_video_comments(video_id)
        categorized_comments, sentiment_data = analyze_and_categorize_comments(comments)
        
        # Display sentiment analysis results
        st.subheader("Sentiment Analysis")
        for sentiment, sentiment_comments in categorized_comments.items():
            st.write(sentiment)
            for comment, subjectivity in sentiment_comments:
                st.write(f"Comment: {comment}")
                st.write(f"Subjectivity: {subjectivity}")
                st.write("----")

        # Generate sentiment over time plot
        generate_sentiment_over_time_plot(sentiment_data)

        # Comment filtering and sorting options
        sentiment_filter = st.sidebar.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])
        sort_by = st.sidebar.selectbox("Sort by", ["None", "Subjectivity"])
        
        # Filter and sort comments
        filtered_comments = filter_and_sort_comments(comments, sentiment_filter=sentiment_filter, sort_by=sort_by)

        # Display filtered and sorted comments
        st.subheader("Filtered and Sorted Comments")
        for comment, subjectivity in filtered_comments:
            st.write(f"Comment: {comment}")
            st.write(f"Subjectivity: {subjectivity}")
            st.write("----")

if task == "Generate Word Cloud":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Generate Word Cloud"):
        comments = get_video_comments(video_id)
        st.subheader("Word Cloud")
        wordcloud = generate_word_cloud(comments)
        st.pyplot(wordcloud)

if task == "Advanced Features":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Show Advanced Features"):
        st.subheader("Advanced Features")

        # Fetch additional video details
        title, duration, upload_date, thumbnail_url, channel_name, likes, views = get_video_details(video_id)

        st.write(f"Title: {title}")
        st.write(f"Duration: {duration}")
        st.write(f"Upload Date: {upload_date}")
        st.write(f"Channel Name: {channel_name}")
        st.write(f"Likes: {likes}")
        st.write(f"Views: {views}")

        # Thumbnail preview
        st.image(thumbnail_url, caption='Video Thumbnail', use_column_width=True)

        # Keyword extraction
        top_keywords = extract_keywords(comments)
        st.subheader("Top Keywords in Comments")
        for keyword in top_keywords:
            st.write(keyword)

        # Advanced Word Cloud Options
        st.sidebar.subheader("Advanced Word Cloud Options")
        custom_params = {
            "color_func": st.sidebar.color_picker("Choose a color for the word cloud", value="#1f77b4"),
            "max_words": st.sidebar.slider("Maximum number of words", min_value=50, max_value=500, value=200),
            # Add more customization options as needed
        }

        if st.sidebar.button("Generate Advanced Word Cloud"):
            wordcloud = generate_word_cloud(comments, custom_params)
            st.pyplot(wordcloud)

# Include other advanced features as needed
