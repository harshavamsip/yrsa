
import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
import plotly.express as px
from profanity_check import predict
from wordcloud import WordCloud
from transformers import pipeline

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

# Placeholder function for profanity check
def check_profanity(comment):
    return predict([comment])[0]

# Placeholder function for word cloud generation
def generate_word_cloud(comments):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(comments))
    return wordcloud.to_image()

# Placeholder function for summary generation
def generate_summary(text):
    summarization_pipeline = pipeline("summarization")
    summary = summarization_pipeline(text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)[0]['summary_text']
    return summary

def handle_tasks():
    st.set_page_config(
        page_title="YouTube Video Analyzer",
        page_icon="📺",
        layout="wide"
    )

    st.title("YouTube Video Analyzer")
    st.sidebar.header("Select Task")

    task = st.sidebar.selectbox("Task", ["Search Video Details", "Sentiment Analysis", "Profanity Check", "Word Cloud", "Summary Generation"])

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

    elif task == "Sentiment Analysis":
        video_id = st.sidebar.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

        if st.sidebar.button("Analyze Sentiment"):
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

                sentiment_category = st.selectbox("Select sentiment category to display comments", list(categorized_comments.keys()))
                st.subheader(f"{sentiment_category} Comments:")
                for comment in categorized_comments[sentiment_category]:
                    st.write(comment[0])
            else:
                st.warning("No comments found for the given video.")

    elif task == "Profanity Check":
        video_id = st.sidebar.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

        if st.sidebar.button("Check Profanity"):
            comments = get_video_comments(video_id)
            st.subheader("Profanity Check")

            if comments:
                st.write("Comments:")
                for comment in comments:
                    st.write(comment)

                st.subheader("Profanity Results:")
                for comment in comments:
                    profanity_result = check_profanity(comment)
                    if profanity_result:
                        st.write(f"Profanity detected in comment: {comment}")
            else:
                st.warning("No comments found for the given video.")

    elif task == "Word Cloud":
        video_id = st.sidebar.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

        if st.sidebar.button("Generate Word Cloud"):
            comments = get_video_comments(video_id)
            st.subheader("Word Cloud Generation")

            if comments:
                wordcloud_image = generate_word_cloud(comments)
                st.image(wordcloud_image, caption="Word Cloud", use_column_width=True)
            else:
                st.warning("No comments found for the given video.")

    elif task == "Summary Generation":
        st.subheader("Summary Generation Task")
        st.warning("Please note that the summary generation task is a placeholder. Replace this with your actual logic.")

        transcript_text = st.text_area("Enter video transcript", "")
        if st.button("Generate Summary"):
            summary = generate_summary(transcript_text)
            st.write("Generated Summary:")
            st.write(summary)
    else:
        st.info("Please select a task and click 'Analyze' to see the results.")

if __name__ == "__main__":
    handle_tasks()
