# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# import plotly.express as px
# from sklearn.externals import joblib



# # Set your YouTube Data API key here
# YOUTUBE_API_KEY = "AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# # Initialize the YouTube Data API client
# youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# # Function to search for videos and retrieve video details sorted by views
# def search_and_recommend_videos(query, max_results=10):
#     try:
#         response = youtube.search().list(
#             q=query,
#             type="video",
#             part="id,snippet",
#             maxResults=max_results,
#             videoCaption="any",
#             order="viewCount"  # Sort by views
#         ).execute()

#         video_details = []
#         for item in response.get("items", []):
#             video_id = item["id"]["videoId"]
#             title = item["snippet"]["title"]

#             # Use a separate request to get video statistics and content details
#             video_info = youtube.videos().list(
#                 part="statistics,contentDetails,snippet",
#                 id=video_id
#             ).execute()

#             snippet_info = video_info.get("items", [])[0]["snippet"]
#             statistics_info = video_info.get("items", [])[0]["statistics"]
#             content_details = video_info.get("items", [])[0].get("contentDetails", {})

#             likes = int(statistics_info.get("likeCount", 0))
#             views = int(statistics_info.get("viewCount", 0))
#             comments = int(statistics_info.get("commentCount", 0))
#             duration = content_details.get("duration", "N/A")
#             upload_date = snippet_info.get("publishedAt", "N/A")
#             channel_title = snippet_info.get("channelTitle", "N/A")
#             thumbnail_url = snippet_info.get("thumbnails", {}).get("default", {}).get("url", "N/A")

#             link = f"https://www.youtube.com/watch?v={video_id}"

#             video_details.append((title, video_id, likes, views, comments, duration, upload_date, channel_title, link, thumbnail_url))

#         return video_details
#     except googleapiclient.errors.HttpError as e:
#         st.error(f"Error fetching videos: {e}")
#         return []

# # Function to fetch video comments using the video ID
# def get_video_comments(video_id):
#     try:
#         comments = []
#         results = youtube.commentThreads().list(
#             part="snippet",
#             videoId=video_id,
#             textFormat="plainText",
#             maxResults=100
#         ).execute()

#         while "items" in results:
#             for item in results["items"]:
#                 comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#                 comments.append(comment)
#             if "nextPageToken" in results:
#                 results = youtube.commentThreads().list(
#                     part="snippet",
#                     videoId=video_id,
#                     textFormat="plainText",
#                     maxResults=100,
#                     pageToken=results["nextPageToken"]
#                 ).execute()
#             else:
#                 break

#         return comments
#     except googleapiclient.errors.HttpError as e:
#         st.error(f"Error fetching comments: {e}")
#         return []

# # Placeholder function for sentiment analysis
# def analyze_and_categorize_comments(comments):
#     # Replace this placeholder with your actual sentiment analysis logic
#     categorized_comments = {'Positive': [], 'Negative': [], 'Neutral': []}
#     for comment in comments:
#         analysis = TextBlob(comment)
#         polarity = analysis.sentiment.polarity
#         subjectivity = analysis.sentiment.subjectivity

#         if polarity > 0:
#             categorized_comments['Positive'].append((comment, polarity, subjectivity))
#         elif polarity < 0:
#             categorized_comments['Negative'].append((comment, polarity, subjectivity))
#         else:
#             categorized_comments['Neutral'].append((comment, polarity, subjectivity))

#     return categorized_comments

# # Streamlit web app
# st.set_page_config(
#     page_title="YouTube Video Analyzer",
#     page_icon="📺",
#     layout="wide"
# )

# st.title("YouTube Video Analyzer")
# st.sidebar.header("Select Task")

# task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis"])

# if task == "Search Video Details":
#     search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

#     if st.sidebar.button("Search"):
#         video_details = search_and_recommend_videos(search_query)
#         st.subheader("Search Results:")
#         if video_details:
#             for video in video_details:
#                 st.write(f"**{video[0]}**")
#                 st.write(f"<img src='{video[9]}' alt='Thumbnail' style='max-height: 150px;'>", unsafe_allow_html=True)
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}, Comments: {video[4]}")
#                 st.write(f"Duration: {video[5]}, Upload Date: {video[6]}")
#                 st.write(f"Channel: {video[7]}")
#                 st.write(f"Watch Video: [Link]({video[8]})")

# if task == "Sentiment Analysis":
#     # Provide a valid video ID or update the input method based on your needs
#     video_id = st.sidebar.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")

#         # Check if there are comments before analysis
#         if comments:
#             # Use the placeholder function for sentiment analysis
#             categorized_comments = analyze_and_categorize_comments(comments)

#             # Display additional metrics
#             st.write(f"Total Comments: {len(comments)}")
#             st.write(f"Average Sentiment Polarity: {sum(s[1] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")
#             st.write(f"Average Sentiment Subjectivity: {sum(s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")

#             # Display sentiment distribution chart
#             sentiment_df = []
#             for sentiment, sentiment_comments in categorized_comments.items():
#                 sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

#             sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
#             st.plotly_chart(sentiment_chart)

#             # Display categorized comments
#             for sentiment, sentiment_comments in categorized_comments.items():
#                 st.subheader(sentiment)
#                 for comment in sentiment_comments:
#                     st.write(comment[0])
#         else:
#             st.warning("No comments found for the given video.")

# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# import plotly.express as px
# from wordcloud import WordCloud
# from nltk.corpus import stopwords
# from transformers import pipeline

# # Set your YouTube Data API key here
# YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# # Initialize the YouTube Data API client
# youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# # Function to search for videos and retrieve video details sorted by views
# def search_and_recommend_videos(query, max_results=10):
#     try:
#         response = youtube.search().list(
#             q=query,
#             type="video",
#             part="id,snippet",
#             maxResults=max_results,
#             videoCaption="any",
#             order="viewCount"  # Sort by views
#         ).execute()

#         video_details = []
#         for item in response.get("items", []):
#             video_id = item["id"]["videoId"]
#             title = item["snippet"]["title"]

#             # Use a separate request to get video statistics and content details
#             video_info = youtube.videos().list(
#                 part="statistics,contentDetails,snippet",
#                 id=video_id
#             ).execute()

#             snippet_info = video_info.get("items", [])[0]["snippet"]
#             statistics_info = video_info.get("items", [])[0]["statistics"]
#             content_details = video_info.get("items", [])[0].get("contentDetails", {})

#             likes = int(statistics_info.get("likeCount", 0))
#             views = int(statistics_info.get("viewCount", 0))
#             comments = int(statistics_info.get("commentCount", 0))
#             duration = content_details.get("duration", "N/A")
#             upload_date = snippet_info.get("publishedAt", "N/A")
#             channel_title = snippet_info.get("channelTitle", "N/A")
#             thumbnail_url = snippet_info.get("thumbnails", {}).get("default", {}).get("url", "N/A")

#             link = f"https://www.youtube.com/watch?v={video_id}"

#             video_details.append((title, video_id, likes, views, comments, duration, upload_date, channel_title, link, thumbnail_url))

#         return video_details
#     except googleapiclient.errors.HttpError as e:
#         st.error(f"Error fetching videos: {e}")
#         return []

# # Function to fetch video comments using the video ID
# def get_video_comments(video_id):
#     try:
#         comments = []
#         results = youtube.commentThreads().list(
#             part="snippet",
#             videoId=video_id,
#             textFormat="plainText",
#             maxResults=100
#         ).execute()

#         while "items" in results:
#             for item in results["items"]:
#                 comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#                 comments.append(comment)
#             if "nextPageToken" in results:
#                 results = youtube.commentThreads().list(
#                     part="snippet",
#                     videoId=video_id,
#                     textFormat="plainText",
#                     maxResults=100,
#                     pageToken=results["nextPageToken"]
#                 ).execute()
#             else:
#                 break

#         return comments
#     except googleapiclient.errors.HttpError as e:
#         st.error(f"Error fetching comments: {e}")
#         return []

# # Placeholder function for sentiment analysis
# def analyze_and_categorize_comments(comments):
#     categorized_comments = {'Positive': [], 'Negative': [], 'Neutral': []}
#     for comment in comments:
#         analysis = TextBlob(comment)
#         polarity = analysis.sentiment.polarity
#         subjectivity = analysis.sentiment.subjectivity

#         if polarity > 0:
#             categorized_comments['Positive'].append((comment, polarity, subjectivity))
#         elif polarity < 0:
#             categorized_comments['Negative'].append((comment, polarity, subjectivity))
#         else:
#             categorized_comments['Neutral'].append((comment, polarity, subjectivity))

#     return categorized_comments

# # Function to perform keyword extraction and generate word cloud
# def analyze_and_visualize_keywords(comments):
#     try:
#         all_comments_text = ' '.join(comments)
#         stop_words = set(stopwords.words('english'))
#         all_comments_text = ' '.join([word for word in all_comments_text.split() if word.lower() not in stop_words])

#         wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments_text)

#         st.subheader("Word Cloud")
#         st.image(wordcloud.to_array(), use_container_width=True)
#     except Exception as e:
#         st.error(f"Error during keyword extraction and word cloud generation: {e}")

# # Function for Named Entity Recognition (NER)
# def perform_ner_on_comments(comments):
#     try:
#         all_comments_text = ' '.join(comments)
#         ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", tokenizer="dbmdz/bert-large-cased-finetuned-conll03-english")
#         entities = ner_pipeline(all_comments_text)

#         st.subheader("Named Entity Recognition (NER) Results")
#         for entity in entities:
#             st.write(f"Entity: {entity['word']}, Label: {entity['entity']}, Score: {entity['score']}")
#     except Exception as e:
#         st.error(f"Error during Named Entity Recognition (NER): {e}")

# # Function for Summary Generation using Transformers
# def generate_summary(comments):
#     try:
#         all_comments_text = ' '.join(comments)
#         summarization_pipeline = pipeline("summarization", model="t5-base", tokenizer="t5-base")
#         summary = summarization_pipeline(all_comments_text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)

#         st.subheader("Summary Generation using Transformers")
#         st.write(summary[0]['summary_text'])
#     except Exception as e:
#         st.error(f"Error during summary generation using Transformers: {e}")

# # Streamlit web app
# st.set_page_config(
#     page_title="YouTube Video Analyzer",
#     page_icon="📺",
#     layout="wide"
# )

# st.title("YouTube Video Analyzer")
# st.sidebar.header("Select Task")

# task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis"])

# if task == "Search Video Details":
#     search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

#     if st.sidebar.button("Search"):
#         video_details = search_and_recommend_videos(search_query)
#         st.subheader("Search Results:")
#         if video_details:
#             for video in video_details:
#                 st.write(f"**{video[0]}**")
#                 st.write(f"<img src='{video[9]}' alt='Thumbnail' style='max-height: 150px;'>", unsafe_allow_html=True)
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}, Comments: {video[4]}")
#                 st.write(f"Duration: {video[5]}, Upload Date: {video[6]}")
#                 st.write(f"Channel: {video[7]}")
#                 st.write(f"Watch Video: [Link]({video[8]})")

# if task == "Sentiment Analysis":
#     video_id = st.sidebar.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")

#         if comments:
#             categorized_comments = analyze_and_categorize_comments(comments)

#             st.write(f"Total Comments: {len(comments)}")
#             st.write(f"Average Sentiment Polarity: {sum(s[1] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")
#             st.write(f"Average Sentiment Subjectivity: {sum(s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")

#             sentiment_df = []
#             for sentiment, sentiment_comments in categorized_comments.items():
#                 sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

#             sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
#             st.plotly_chart(sentiment_chart)

#             for sentiment, sentiment_comments in categorized_comments.items():
#                 st.subheader(sentiment)
#                 for comment in sentiment_comments:
#                     st.write(comment[0])

#             analyze_and_visualize_keywords(comments)
#             perform_ner_on_comments(comments)
#             generate_summary(comments)
#         else:
#             st.warning("No comments found for the given video.")


import os
import numpy as np
import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
import plotly.express as px
from profanity_check import predict
from sklearn.externals import joblib
from transformers import pipeline
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set your YouTube Data API key here
YOUTUBE_API_KEY =  "AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# Initialize the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Load the pre-trained profanity check model
model_path = os.path.join(os.path.dirname(__file__), 'profanity_check_model', 'model.joblib')
gbc = joblib.load(model_path)

# Create a vectorizer to convert input text into feature vectors
vec = joblib.load(os.path.join(os.path.dirname(__file__), 'profanity_check_model', 'vectorizer.joblib'))

# Load the feature names
feature_names_path = os.path.join(os.path.dirname(__file__), 'profanity_check_model', 'feature_names.npy')
feature_names = np.load(feature_names_path)

# Set up transformers pipeline for summary generation
summarization_pipeline = pipeline("summarization")

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

# Function to search for videos and retrieve video details sorted by views
def search_and_recommend_videos(query, max_results=10):
    try:
        response = youtube.search().list(
            q=query,
            type="video",
            part="id,snippet",
            maxResults=max_results,
            videoCaption="any",
            order="viewCount"  # Sort by views
        ).execute()

        video_details = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]

            # Use a separate request to get video statistics and content details
            video_info = youtube.videos().list(
                part="statistics,contentDetails,snippet",
                id=video_id
            ).execute()

            snippet_info = video_info.get("items", [])[0]["snippet"]
            statistics_info = video_info.get("items", [])[0]["statistics"]
            content_details = video_info.get("items", [])[0].get("contentDetails", {})

            likes = int(statistics_info.get("likeCount", 0))
            views = int(statistics_info.get("viewCount", 0))
            comments = int(statistics_info.get("commentCount", 0))
            duration = content_details.get("duration", "N/A")
            upload_date = snippet_info.get("publishedAt", "N/A")
            channel_title = snippet_info.get("channelTitle", "N/A")
            thumbnail_url = snippet_info.get("thumbnails", {}).get("default", {}).get("url", "N/A")

            link = f"https://www.youtube.com/watch?v={video_id}"

            video_details.append((title, video_id, likes, views, comments, duration, upload_date, channel_title, link, thumbnail_url))

        return video_details
    except googleapiclient.errors.HttpError as e:
        st.error(f"Error fetching videos: {e}")
        return []

# Function to fetch video comments using the video ID
def get_video_comments(video_id):
    try:
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
    except googleapiclient.errors.HttpError as e:
        st.error(f"Error fetching comments: {e}")
        return []

# Placeholder function for sentiment analysis
def analyze_and_categorize_comments(comments):
    # Replace this placeholder with your actual sentiment analysis logic
    categorized_comments = {'Positive': [], 'Negative': [], 'Neutral': []}
    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        if polarity > 0:
            categorized_comments['Positive'].append((comment, polarity, subjectivity))
        elif polarity < 0:
            categorized_comments['Negative'].append((comment, polarity, subjectivity))
        else:
            categorized_comments['Neutral'].append((comment, polarity, subjectivity))

    return categorized_comments

# Function to filter comments based on sentiment
def filter_comments_by_sentiment(comments, sentiment):
    filtered_comments = [comment for comment in comments if analyze_sentiment(comment) == sentiment]
    return filtered_comments

# Function to analyze sentiment of a single comment
def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Function to generate word cloud from comments
def generate_wordcloud(comments):
    text = ' '.join(comments)
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color='white').generate(text)
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    st.pyplot(plt)

# Function to perform abuse and spam detection
def abuse_and_spam_detection(comments):
    # Replace this with your actual abuse and spam detection logic
    # For now, using a placeholder function
    labels = [predict([comment]) for comment in comments]
    return labels

# Function to display results of abuse and spam detection
def display_abuse_and_spam_results(labels, comments):
    st.subheader("Abuse and Spam Detection Results")
    st.write("Number of comments analyzed:", len(comments))
    st.write("Abusive/Spam comments detected:", sum(labels))
    st.write("Percentage of Abusive/Spam comments:", (sum(labels) / len(comments)) * 100)

# Task 1: Search Video Details
def video_details_search_task():
    st.sidebar.header("Task 1: Search Video Details")
    st.sidebar.subheader("Enter the topic of interest:")
    search_query = st.sidebar.text_input("", value="Python Tutorial")
    
    if st.sidebar.button("Search"):
        video_details = search_and_recommend_videos(search_query)
        st.subheader("Search Results:")
        if video_details:
            for video in video_details:
                st.write(f"**{video[0]}**")
                st.write(f"<img src='{video[9]}' alt='Thumbnail' style='max-height: 150px;'>", unsafe_allow_html=True)
                st.write(f"Video ID: {video[1]}")
                st.write(f"Likes: {video[2]}, Views: {video[3]}, Comments: {video[4]}")
                st.write(f"Duration: {video[5]}, Upload Date: {video[6]}")
                st.write(f"Channel: {video[7]}")
                st.write(f"Watch Video: [Link]({video[8]})")

# Task 2: Sentiment Analysis
def sentiment_analysis_task():
    st.sidebar.header("Task 2: Sentiment Analysis")
    st.sidebar.subheader("Enter Video ID:")
    video_id_sentiment = st.sidebar.text_input("", value="YOUR_VIDEO_ID")

    if st.sidebar.button("Analyze Sentiment"):
        comments_sentiment = get_video_comments(video_id_sentiment)
        st.subheader("Sentiment Analysis")

        # Check if there are comments before analysis
        if comments_sentiment:
            # Provide options to filter comments
            sentiment_option = st.radio("Filter Comments By Sentiment:", options=["All", "Positive", "Negative", "Neutral"], index=0)

            # Filter comments based on sentiment option
            if sentiment_option == "All":
                display_comments = comments_sentiment
            else:
                display_comments = filter_comments_by_sentiment(comments_sentiment, sentiment_option.lower())

            # Display sentiment distribution chart
            sentiment_df = []
            for sentiment, sentiment_comments in analyze_and_categorize_comments(display_comments).items():
                sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

            sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
            st.plotly_chart(sentiment_chart)

            # Display categorized comments
            for sentiment, sentiment_comments in analyze_and_categorize_comments(display_comments).items():
                st.subheader(sentiment)
                for comment in sentiment_comments:
                    st.write(comment[0])
        else:
            st.warning("No comments found for the given video.")

# Task 3: Word Cloud Generation
def wordcloud_generation_task():
    st.sidebar.header("Task 3: Word Cloud Generation")
    st.sidebar.subheader("Enter Video ID:")
    video_id_wordcloud = st.sidebar.text_input("", value="YOUR_VIDEO_ID")

    if st.sidebar.button("Generate Word Cloud"):
        comments_wordcloud = get_video_comments(video_id_wordcloud)
        st.subheader("Word Cloud Generation")

        # Check if there are comments before generating word cloud
        if comments_wordcloud:
            generate_wordcloud(comments_wordcloud)
        else:
            st.warning("No comments found for the given video.")

# Task 4: Abuse and Spam Detection
def abuse_and_spam_detection_task():
    st.sidebar.header("Task 4: Abuse and Spam Detection")
    st.sidebar.subheader("Enter Video ID:")
    video_id_abuse_spam = st.sidebar.text_input("", value="YOUR_VIDEO_ID")

    if st.sidebar.button("Detect Abuse and Spam"):
        comments_abuse_spam = get_video_comments(video_id_abuse_spam)
        st.subheader("Abuse and Spam Detection")

        # Check if there are comments before abuse and spam detection
        if comments_abuse_spam:
            labels_abuse_spam = abuse_and_spam_detection(comments_abuse_spam)
            display_abuse_and_spam_results(labels_abuse_spam, comments_abuse_spam)
        else:
            st.warning("No comments found for the given video.")

# Task 5: Summary Generation
def summary_generation_task():
    st.sidebar.header("Task 5: Summary Generation")
    st.sidebar.subheader("Enter Video ID:")
    video_id_summary = st.sidebar.text_input("", value="YOUR_VIDEO_ID")

    if st.sidebar.button("Generate Summary"):
        comments_summary = get_video_comments(video_id_summary)
        st.subheader("Summary Generation")

        # Check if there are comments before summary generation
        if comments_summary:
            # Use the first comment as input for summary generation
            text_for_summary = comments_summary[0]
            summary = summarization_pipeline(text_for_summary, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)
            st.write("Original Text:")
            st.write(text_for_summary)
            st.write("Generated Summary:")
            st.write(summary[0]['summary_text'])
        else:
            st.warning("No comments found for the given video.")

# Function to handle different tasks based on user selection
def handle_tasks():
    st.title("YouTube Video Analyzer")

    task_options = ["Search Video Details", "Sentiment Analysis", "Word Cloud Generation", "Abuse and Spam Detection", "Summary Generation"]
    task = st.sidebar.selectbox("Select Task", task_options)

    if task == task_options[0]:
        video_details_search_task()
    elif task == task_options[1]:
        sentiment_analysis_task()
    elif task == task_options[2]:
        wordcloud_generation_task()
    elif task == task_options[3]:
        abuse_and_spam_detection_task()
    elif task == task_options[4]:
        summary_generation_task()

# Run the app
if __name__ == '__main__':
    handle_tasks()

