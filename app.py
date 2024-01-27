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

# Set your YouTube Data API key here
YOUTUBE_API_KEY = "AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

# Initialize the YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Function for Video Details Search Task
def video_details_search_task():
    st.subheader("Video Details Search Task")
    st.write("This task allows you to search for videos based on a topic and displays relevant details.")
    
    # Input for searching videos
    search_query = st.text_input("Enter the topic of interest", value="Python Tutorial")

    # Button to initiate the search
    if st.button("Search"):
        # Call the function to search and recommend videos
        video_details = search_and_recommend_videos(search_query)

        # Display search results
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

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

# Sidebar color adjustment
st.markdown(
    """
    <style>
        div[data-testid="stSidebar"] {
            background-color: #1f1f1f;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content color adjustment
st.markdown(
    """
    <style>
        div[data-testid="stBlock"] {
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
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

# Function for Sentiment Analysis Task
def sentiment_analysis_task():
    st.subheader("Sentiment Analysis Task")
    st.write("This task allows you to analyze the sentiment of comments on a YouTube video.")
    
    # Input for video ID
    video_id_sentiment = st.sidebar.text_input("Enter Video ID for Sentiment Analysis", value="YOUR_VIDEO_ID")

    # Button to initiate sentiment analysis
    if st.sidebar.button("Analyze Sentiment"):
        # Call the function to fetch video comments
        comments = get_video_comments(video_id_sentiment)
        st.subheader("Sentiment Analysis")

        # Check if there are comments before analysis
        if comments:
            # Use the placeholder function for sentiment analysis
            categorized_comments = analyze_and_categorize_comments(comments)

            # Display additional metrics
            st.write(f"Total Comments: {len(comments)}")
            st.write(f"Average Sentiment Polarity: {sum(s[1] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")
            st.write(f"Average Sentiment Subjectivity: {sum(s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")

            # Display sentiment distribution chart
            sentiment_df = []
            for sentiment, sentiment_comments in categorized_comments.items():
                sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

            sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
            st.plotly_chart(sentiment_chart)

            # Display categorized comments
            for sentiment, sentiment_comments in categorized_comments.items():
                st.subheader(sentiment)
                for comment in sentiment_comments:
                    st.write(comment[0])
        else:
            st.warning("No comments found for the given video.")

# Function for Named Entity Recognition (NER) Task
def named_entity_recognition_task():
    st.subheader("Named Entity Recognition (NER) Task")
    st.write("This task allows you to perform Named Entity Recognition (NER) on the transcript of a YouTube video.")
    
    # Input for video ID
    video_id_ner = st.sidebar.text_input("Enter Video ID for NER Task", value="YOUR_VIDEO_ID")

    # Button to initiate NER
    if st.sidebar.button("Perform NER"):
        # Call the function to fetch video comments
        comments_ner = get_video_comments(video_id_ner)

        # Check if there are comments before NER
        if comments_ner:
            # Concatenate comments into a single text for NER
            text_for_ner = " ".join(comments_ner)

            # Use the transformers library for NER
            ner_pipeline = pipeline("ner")
            entities = ner_pipeline(text_for_ner)

            # Display NER results
            st.subheader("Named Entity Recognition (NER) Results")
            for entity in entities:
                st.write(f"Entity: {entity['word']}, Label: {entity['entity']}, Score: {entity['score']}")
        else:
            st.warning("No comments found for the given video.")

# Function for Summary Generation Task
def summary_generation_task():
    st.subheader("Summary Generation Task")
    st.write("This task allows you to generate a summary of the transcript of a YouTube video using transformers.")

    # Input for video ID
    video_id_summary = st.sidebar.text_input("Enter Video ID for Summary Generation Task", value="YOUR_VIDEO_ID")

    # Button to generate summary
    if st.sidebar.button("Generate Summary"):
        # Call the function to fetch video comments
        comments_summary = get_video_comments(video_id_summary)

        # Check if there are comments before summary generation
        if comments_summary:
            # Concatenate comments into a single text for summarization
            text_for_summary = " ".join(comments_summary)

            # Use the transformers library for summarization
            summarization_pipeline = pipeline("summarization")
            summary = summarization_pipeline(text_for_summary, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)

            # Display summary
            st.subheader("Generated Summary")
            st.write(summary[0]['summary_text'])
        else:
            st.warning("No comments found for the given video.")

# Placeholder function for keyword extraction
def extract_keywords(text):
    # Replace this placeholder with your actual keyword extraction logic
    # For simplicity, this placeholder function just splits the text into words
    return text.split()

# Function for Keyword Extraction Task
def keyword_extraction_task():
    st.subheader("Keyword Extraction Task")
    st.write("This task allows you to extract keywords from the transcript of a YouTube video.")

    # Input for video ID
    video_id_keywords = st.sidebar.text_input("Enter Video ID for Keyword Extraction Task", value="YOUR_VIDEO_ID")

    # Button to extract keywords
    if st.sidebar.button("Extract Keywords"):
        # Call the function to fetch video comments
        comments_keywords = get_video_comments(video_id_keywords)

        # Check if there are comments before keyword extraction
        if comments_keywords:
            # Concatenate comments into a single text for keyword extraction
            text_for_keywords = " ".join(comments_keywords)

            # Use the placeholder function for keyword extraction
            keywords = extract_keywords(text_for_keywords)

            # Display keywords
            st.subheader("Extracted Keywords")
            st.write(", ".join(keywords))
        else:
            st.warning("No comments found for the given video.")

# Function to handle different tasks based on user selection
def handle_tasks():
    task = st.sidebar.selectbox("Select Task", ["Video Details Search", "Sentiment Analysis", "NER Task", "Summary Generation Task", "Keyword Extraction Task"])

    if task == "Video Details Search":
        video_details_search_task()
    elif task == "Sentiment Analysis":
        sentiment_analysis_task()
    elif task == "NER Task":
        named_entity_recognition_task()
    elif task == "Summary Generation Task":
        summary_generation_task()
    elif task == "Keyword Extraction Task":
        keyword_extraction_task()

# Execute the main tasks
handle_tasks()

