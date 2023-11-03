# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

# # Set your YouTube Data API key here
# YOUTUBE_API_KEY = "AIzaSyCvtRnKGLMgtNexVGm0jN_weLQ3xogV4hM"

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
#         description = item["snippet"]["description"]
#         published_at = item["snippet"]["publishedAt"]

#         link = f"https://www.youtube.com/watch?v={video_id}"

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

#         video_details.append((title, link, video_id, description, published_at, likes, views))

#     return video_details

# # Function to fetch video comments
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
#     st.pyplot(plt.figure(figsize=(10, 5)))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     st.pyplot()

# # Streamlit web app
# st.set_page_config(
#     page_title="YouTube Video Analyzer",
#     page_icon="📺",
#     layout="wide"
# )

# st.title("YouTube Video Analyzer")
# st.sidebar.header("Search for Videos")

# search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

# if st.sidebar.button("Search"):
#     video_details = search_and_recommend_videos(search_query)
#     st.subheader("Search Results:")
#     if video_details:
#         for video in video_details:
#             st.write(f"**{video[0]}**")
#             st.write(f"Published at: {video[4]}")
#             st.write(f"Likes: {video[5]}, Views: {video[6]}")
#             st.write(f"Watch Video: [{video[0]}]({video[1]})]")
#             if st.button(f"Analyze {video[0]}"):
#                 selected_video_id = video[2]
#                 comments = get_video_comments(selected_video_id)
#                 categorized_comments = analyze_and_categorize_comments(comments)
#                 st.write(f"Video ID: {selected_video_id}")
#                 st.subheader("Sentiment Analysis")
#                 for sentiment, sentiment_comments in categorized_comments.items():
#                     st.write(sentiment)
#                     for comment in sentiment_comments:
#                         st.write(comment)
#                 st.subheader("Word Cloud")
#                 generate_word_cloud(comments)
#                 st.markdown(f"Watch Video: [Watch the video]({video[1]})")



import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set your YouTube Data API key here
YOUTUBE_API_KEY ="AIzaSyCvtRnKGLMgtNexVGm0jN_weLQ3xogV4hM"

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
        description = item["snippet"]["description"]
        published_at = item["snippet"]["publishedAt"]

        link = f"https://www.youtube.com/watch?v={video_id}"

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

        video_details.append((title, link, video_id, description, published_at, likes, views))

    return video_details

# Function to fetch video comments using the video URL
def get_video_comments(video_url):
    video_id = video_url.split("v=")[1]
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

        # Categorize based on polarity
        if sentiment_polarity > 0.2:
            categorized_comments["Positive"].append(comment)
        elif sentiment_polarity < -0.2:
            categorized_comments["Negative"].append(comment)
        else:
            categorized_comments["Neutral"].append(comment)

    return categorized_comments

# Function to generate a word cloud from comments
def generate_word_cloud(comments):
    all_comments = ' '.join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)
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
st.sidebar.header("Search for Videos")

search_query = st.sidebar.text_input("Enter the topic of interest", value="Python Tutorial")

if st.sidebar.button("Search"):
    video_details = search_and_recommend_videos(search_query)
    st.subheader("Search Results:")
    if video_details:
        for video in video_details:
            st.write(f"**{video[0]}**")
            st.write(f"Published at: {video[4]}")
            st.write(f"Likes: {video[5]}, Views: {video[6]}")
            st.write(f"Watch Video: [{video[0}]({video[1]})]")
            if st.button(f"Analyze {video[0]}"):
                selected_video_url = video[1]
                comments = get_video_comments(selected_video_url)
                categorized_comments = analyze_and_categorize_comments(comments)
                st.write(f"Video ID: {video[2]}")
                st.subheader("Sentiment Analysis")
                for sentiment, sentiment_comments in categorized_comments.items():
                    st.write(sentiment)
                    for comment in sentiment_comments:
                        st.write(comment)
                st.subheader("Word Cloud")
                generate_word_cloud(comments)
                st.write(f"Watch Video: [{video[0}]({selected_video_url})")
