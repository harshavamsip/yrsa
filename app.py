import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

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

# Function to analyze and categorize comments
def analyze_and_categorize_comments(comments):
    categorized_comments = {"Positive": [], "Negative": [], "Neutral": []}

    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        if polarity > 0:
            categorized_comments["Positive"].append((comment, polarity, subjectivity))
        elif polarity < 0:
            categorized_comments["Negative"].append((comment, polarity, subjectivity))
        else:
            categorized_comments["Neutral"].append((comment, polarity, subjectivity))

    return categorized_comments

# Function to generate a word cloud from comments
def generate_word_cloud(comments):
    all_comments = ' '.join(comments)
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(all_comments)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    return plt

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Generate Word Cloud"])

if task == "Search Video Details":
    search_query = st.sidebar.text_input("Enter search query:")
    max_results = st.sidebar.slider("Max Results", min_value=1, max_value=50, value=10)

    if st.sidebar.button("Search"):
        videos = search_and_recommend_videos(search_query, max_results)
        if videos:
            st.header("Top Videos Matching the Query")
            for video in videos:
                st.subheader(video[0])
                st.write(f"**Video Link:** {video[8]}")
                st.image(video[9], use_column_width=True)
                st.write(f"**Likes:** {video[2]} | **Views:** {video[3]} | **Comments:** {video[4]}")
                st.write(f"**Duration:** {video[5]} | **Uploaded On:** {video[6]} | **Channel:** {video[7]}")
                st.write("---")
else:
    video_url = st.sidebar.text_input("Enter YouTube Video URL:")
    video_id = video_url.split("v=")[1] if "v=" in video_url else None

    if video_id and st.sidebar.button("Analyze"):
        st.header("YouTube Video Analysis")

        st.subheader("Video Details")

        # Display video details
        if video_id:
            video_info = youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()
            snippet_info = video_info.get("items", [])[0]["snippet"]
            st.image(snippet_info["thumbnails"]["default"]["url"], use_column_width=True)
            st.write(f"**Title:** {snippet_info['title']}")
            st.write(f"**Description:** {snippet_info.get('description', 'N/A')}")
            st.write("---")

        st.subheader("Sentiment Analysis")
        st.write(f"**Video ID:** {video_id}")

        # Display sentiment analysis
        if video_id:
            comments = get_video_comments(video_id)
            st.write(f"**Total Comments:** {len(comments)}")

            if comments:
                categorized_comments = analyze_and_categorize_comments(comments)

                st.write("Sentiment Distribution:")
                fig_sentiment = px.pie(
                    values=[len(categorized_comments["Positive"]), len(categorized_comments["Negative"]),
                            len(categorized_comments["Neutral"])],
                    names=["Positive", "Negative", "Neutral"],
                    title="Sentiment Distribution",
                )
                st.plotly_chart(fig_sentiment)

                st.write("Average Sentiment Polarity:")
                average_polarity = sum(s[1] for s in categorized_comments["Positive"] + categorized_comments["Negative"] +
                                      categorized_comments["Neutral"]) / len(comments)
                st.write(f"Average Sentiment Polarity: {average_polarity:.4f}")

                st.subheader("Word Cloud")
                st.pyplot(generate_word_cloud(comments))

                st.subheader("Comments Analysis")
                st.write("Select a category to display respective comments:")
                selected_category = st.selectbox("Select Category", ["Positive", "Negative", "Neutral"])

                if selected_category == "Positive":
                    st.write("Positive Comments:")
                    st.write("\n".join([comment[0] for comment in categorized_comments["Positive"]]))
                elif selected_category == "Negative":
                    st.write("Negative Comments:")
                    st.write("\n".join([comment[0] for comment in categorized_comments["Negative"]]))
                elif selected_category == "Neutral":
                    st.write("Neutral Comments:")
                    st.write("\n".join([comment[0] for comment in categorized_comments["Neutral"]]))
else:
    st.subheader("Word Cloud Generator")

    st.sidebar.subheader("Word Cloud Settings")
    max_words = st.sidebar.number_input("Max Words", min_value=10, max_value=500, value=200)
    width = st.sidebar.number_input("Width", min_value=100, max_value=2000, value=800)
    height = st.sidebar.number_input("Height", min_value=100, max_value=2000, value=400)
    background_color = st.sidebar.color_picker("Background Color", value="#FFFFFF")
    collocations = st.sidebar.checkbox("Enable Collocations", value=False)

    st.sidebar.subheader("Word Cloud Preview")
    word_cloud_preview = generate_word_cloud(["Sample Text"])
    st.sidebar.pyplot(word_cloud_preview)

    st.subheader("Generate Word Cloud")
    video_url_wc = st.text_input("Enter YouTube Video URL:")
    video_id_wc = video_url_wc.split("v=")[1] if "v=" in video_url_wc else None

    if video_id_wc and st.button("Generate"):
        st.header("Word Cloud Analysis")

        st.subheader("Word Cloud")
        wc_comments = get_video_comments(video_id_wc)
        st.pyplot(generate_word_cloud(wc_comments))
