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


import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
import plotly.express as px
from transformers import pipeline
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Set your YouTube Data API key here
YOUTUBE_API_KEY ="AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

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

# Function for Named Entity Recognition (NER) Task
def ner_task(comments):
    st.subheader("Named Entity Recognition (NER) Task")
    st.write("This task uses a pre-trained NER model to identify named entities in the video comments.")
    st.write("The named entities may include persons, organizations, locations, etc.")

    # Perform Named Entity Recognition (NER)
    ner_model = pipeline("ner")
    entities = ner_model(comments)

    st.write("Detected Entities:")
    for entity in entities:
        st.write(f"Entity: {entity['word']}, Label: {entity['entity']}, Score: {entity['score']}")

# Function for Summary Generation using Transformers Task
def summary_generation_task(comments):
    st.subheader("Summary Generation using Transformers Task")
    st.write("This task uses a pre-trained transformer model to generate a summary of the video comments.")
    st.write("The generated summary provides a concise representation of the overall sentiment and key points.")

    # Perform Summary Generation using Transformers
    summarizer = pipeline("summarization")
    summary = summarizer(comments, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

    st.write("Generated Summary:")
    st.write(summary[0]['summary'])

# Function to extract keywords from comments
def extract_keywords(comments):
    st.subheader("Keyword Extraction Task")
    st.write("This task extracts keywords from the video comments using TF-IDF (Term Frequency-Inverse Document Frequency).")
    st.write("The extracted keywords represent the most important terms in the comments.")

    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = [word for comment in comments for word in word_tokenize(comment.lower()) if word.isalnum() and word not in stop_words]

    # Create a document-term matrix using TF-IDF
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([' '.join(word_tokens)])
    feature_names = vectorizer.get_feature_names_out()

    # Sort features based on TF-IDF score
    sorted_indices = X.sum(axis=0).argsort()[0, ::-1]

    # Extract top keywords
    top_keywords = [feature_names[i] for i in sorted_indices[:10]]

    st.write("Top Keywords:")
    st.write(', '.join(top_keywords))

# Function to generate word cloud from comments
def generate_word_cloud(comments):
    st.subheader("Word Cloud Generation Task")
    st.write("This task generates a word cloud from the video comments.")
    st.write("The word cloud visually represents the most frequently occurring words in the comments.")

    # Concatenate all comments into a single text
    text = ' '.join(comments)

    # Generate Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display Word Cloud using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

# Task selection dropdown
task_options = ["Video Details Search Task", "Sentiment Analysis Task", "NER Task", "Summary Generation Task", "Keyword Extraction Task", "Word Cloud Generation Task"]
task = st.sidebar.selectbox("Select Task", task_options)

# Execute the selected task
if task == "Video Details Search Task":
    video_details_search_task()

elif task == "Sentiment Analysis Task":
    sentiment_analysis_task()

elif task == "NER Task":
    video_id_ner = st.text_input("Enter Video ID for NER Task", value="YOUR_VIDEO_ID_NER")
    if st.button("Perform NER Task"):
        comments_ner = get_video_comments(video_id_ner)
        if comments_ner:
            ner_task(comments_ner)
        else:
            st.warning("No comments found for the given video.")

elif task == "Summary Generation Task":
    video_id_summary = st.text_input("Enter Video ID for Summary Generation Task", value="YOUR_VIDEO_ID_SUMMARY")
    if st.button("Generate Summary"):
        comments_summary = get_video_comments(video_id_summary)
        if comments_summary:
            summary_generation_task(comments_summary)
        else:
            st.warning("No comments found for the given video.")

elif task == "Keyword Extraction Task":
    video_id_keywords = st.text_input("Enter Video ID for Keyword Extraction Task", value="YOUR_VIDEO_ID_KEYWORDS")
    if st.button("Extract Keywords"):
        comments_keywords = get_video_comments(video_id_keywords)
        if comments_keywords:
            extract_keywords(comments_keywords)
        else:
            st.warning("No comments found for the given video.")

elif task == "Word Cloud Generation Task":
    video_id_wordcloud = st.text_input("Enter Video ID for Word Cloud Generation Task", value="YOUR_VIDEO_ID_WORDCLOUD")
    if st.button("Generate Word Cloud"):
        comments_wordcloud = get_video_comments(video_id_wordcloud)
        if comments_wordcloud:
            generate_word_cloud(comments_wordcloud)
        else:
            st.warning("No comments found for the given video.")

