# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# import plotly.express as px

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


import streamlit as st
import googleapiclient.discovery
from transformers import pipeline
from textblob import TextBlob
import plotly.express as px
import speech_recognition as sr
import moviepy.editor as mp
from profanity_check import predict
import os

# Set your YouTube Data API key here
YOUTUBE_API_KEY = "AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# Initialize the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

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

# New function for content summarization using transformers library (BART model)
def generate_video_summary(video_details):
    summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
    summaries = []
    for video in video_details:
        summary = summarization_pipeline(video[0], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summaries.append((video[0], summary[0]['summary_text']))
    return summaries

# New function for automatic transcription and speech recognition
def transcribe_and_recognize(video_url):
    recognizer = sr.Recognizer()
    
    # Use moviepy to extract audio from the video
    video_clip = mp.VideoFileClip(video_url)
    audio_clip = video_clip.audio

    # Save the audio as a temporary file
    audio_path = "temp_audio.wav"
    audio_clip.write_audiofile(audio_path)

    # Perform speech recognition on the audio file using Google Cloud Speech API
    client = speech.SpeechClient()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    transcription_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=audio_data.sample_rate,
        language_code="en-US",
    )

    audio = speech.RecognitionAudio(content=audio_data.frame_data.tobytes())
    response = client.recognize(config=transcription_config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    # Clean up: remove temporary audio file
    os.remove(audio_path)

    return transcription

# New function for abuse and spam detection
def detect_abuse_and_spam(comments):
    predictions = predict(comments)
    filtered_comments = [comment for i, comment in enumerate(comments) if not predictions[i]]
    return filtered_comments

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Content Summarization",
                                      "Transcription and Speech Recognition", "Abuse and Spam Detection"])

if task == "Search Video Details":
    search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

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

if task == "Sentiment Analysis":
    video_input = st.sidebar.text_input("Enter Video ID or URL", value="YOUR_VIDEO_ID_OR_URL")

    if st.sidebar.button("Analyze Sentiment"):
        # Extract video ID from the input (assuming it can be either ID or URL)
        video_id = get_video_id(video_input)
        comments = get_video_comments(video_id)
        st.subheader("Sentiment Analysis")

        if comments:
            categorized_comments = analyze_and_categorize_comments(comments)

            st.write(f"Total Comments: {len(comments)}")
            st.write(f"Average Sentiment Polarity: {sum(s[1] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")
            st.write(f"Average Sentiment Subjectivity: {sum(s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")

            sentiment_df = []
            for sentiment, sentiment_comments in categorized_comments.items():
                sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

            sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
            st.plotly_chart(sentiment_chart)

            for sentiment, sentiment_comments in categorized_comments.items():
                st.subheader(sentiment)
                for comment in sentiment_comments:
                    st.write(comment[0])
        else:
            st.warning("No comments found for the given video.")

# New task: Content Summarization
if task == "Content Summarization":
    st.sidebar.subheader("Content Summarization Task")
    if st.sidebar.button("Generate Video Summaries"):
        video_summaries = generate_video_summary(video_details)
        st.subheader("Generated Video Summaries:")
        if video_summaries:
            for video, summary in video_summaries:
                st.write(f"**{video}**")
                st.write(f"Summary: {summary}")

# New task: Transcription and Speech Recognition
if task == "Transcription and Speech Recognition":
    st.sidebar.subheader("Transcription and Speech Recognition Task")
    video_input = st.sidebar.text_input("Enter Video ID or URL for Transcription", value="YOUR_VIDEO_ID_OR_URL")
    if st.sidebar.button("Transcribe and Recognize Speech"):
        # Extract video ID from the input (assuming it can be either ID or URL)
        video_id = get_video_id(video_input)
        transcription = transcribe_and_recognize(video_id)
        st.subheader("Transcription and Speech Recognition Result:")
        st.write(f"Transcription: {transcription}")

# New task: Abuse and Spam Detection
if task == "Abuse and Spam Detection":
    st.sidebar.subheader("Abuse and Spam Detection Task")
    video_input = st.sidebar.text_input("Enter Video ID or URL for Abuse Detection", value="YOUR_VIDEO_ID_OR_URL")
    if st.sidebar.button("Detect Abuse and Spam"):
        # Extract video ID from the input (assuming it can be either ID or URL)
        video_id = get_video_id(video_input)
        comments = get_video_comments(video_id)
        filtered_comments = detect_abuse_and_spam(comments)
        st.subheader("Filtered Comments (Abuse/Spam Removed):")
        for comment in filtered_comments:
            st.write(comment)

