import streamlit as st
import googleapiclient.discovery
from textblob import TextBlob
import plotly.express as px
from transformers import pipeline
import profanity_check

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

# Function to check profanity in comments
def check_profanity(comments):
    try:
        profanity_predictions = profanity_check.predict(comments)
        return profanity_predictions
    except Exception as e:
        st.error(f"Error checking profanity: {e}")
        return []

# Streamlit web app
st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Video Analyzer")
st.sidebar.header("Select Task")

tasks = ["Search Video Details", "Sentiment Analysis", "Profanity Check", "Word Cloud", "Named Entity Recognition (NER)", "Summary Generation", "Abuse and Spam Detection"]
task = st.sidebar.selectbox("Task", tasks)

# Function to generate word cloud from comments
def generate_word_cloud(comments):
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        # Combine all comments into a single string
        text = " ".join(comments)

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, max_words=200, background_color="white").generate(text)

        # Display the word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        # Display the word cloud using Streamlit
        st.image(wordcloud.to_image())
    except Exception as e:
        st.error(f"Error generating word cloud: {e}")

# Function for named entity recognition (NER)
def perform_ner(comments):
    try:
        import spacy
        from spacy import displacy

        # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")

        # Combine all comments into a single string
        text = " ".join(comments)

        # Process the text with spaCy NLP pipeline
        doc = nlp(text)

        # Render named entities using spaCy's displacy
        st.subheader("Named Entity Recognition (NER)")
        st.markdown("Named Entity Recognition (NER) identifies entities (e.g., names of people, organizations, locations) in the text.")
        st.markdown("Here is a visualization of named entities in the comments:")
        st.write(displacy.render(doc, style="ent", jupyter=False))
    except Exception as e:
        st.error(f"Error performing Named Entity Recognition (NER): {e}")

# Function for summary generation using Transformers
def generate_summary(text):
    try:
        summarization_pipeline = pipeline("summarization")
        summary = summarization_pipeline(text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)
        st.subheader("Summary Generation")
        st.markdown("Summary generation provides a concise representation of the main content.")
        st.markdown("Generated Summary:")
        st.write(summary[0]['summary_text'])
    except Exception as e:
        st.error(f"Error generating summary: {e}")

# Function for abuse and spam detection using DL models
def abuse_and_spam_detection(comments):
    # Placeholder function for abuse and spam detection
    st.warning("Abuse and Spam Detection: This feature is under development.")

# Handle tasks based on user selection
def handle_tasks():
    if task == "Search Video Details":
        video_details_search_task()

    elif task == "Sentiment Analysis":
        video_sentiment_analysis_task()

    elif task == "Profanity Check":
        profanity_check_task()

    elif task == "Word Cloud":
        word_cloud_task()

    elif task == "Named Entity Recognition (NER)":
        ner_task()

    elif task == "Summary Generation":
        summary_generation_task()

    elif task == "Abuse and Spam Detection":
        abuse_and_spam_detection_task()

def video_details_search_task():
    # Implementation for the "Search Video Details" task
    st.subheader("Search Video Details")
    st.markdown("Enter the topic of interest below to search for relevant YouTube videos.")
    search_query = st.text_input("Enter the topic of interest", value="Python Tutorial")

    if st.button("Search"):
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

def video_sentiment_analysis_task():
    # Implementation for the "Sentiment Analysis" task
    st.subheader("Sentiment Analysis")
    st.markdown("Analyze the sentiment of comments for a given YouTube video. Enter the video ID below.")

    video_id = st.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

    if st.button("Analyze Sentiment"):
        comments = get_video_comments(video_id)
        st.subheader("Sentiment Analysis")

        if comments:
            categorized_comments = analyze_and_categorize_comments(comments)
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

def profanity_check_task():
    # Implementation for the "Profanity Check" task
    st.subheader("Profanity Check")
    st.markdown("Check for profanity in comments for a given YouTube video. Enter the video ID below.")

    video_id = st.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

    if st.button("Check Profanity"):
        comments = get_video_comments(video_id)
        if comments:
            profanity_predictions = check_profanity(comments)
            st.subheader("Profanity Check Results")

            for i, prediction in enumerate(profanity_predictions):
                st.write(f"Comment {i + 1}: {'Profane' if prediction else 'Not Profane'}")
        else:
            st.warning("No comments found for the given video.")

def word_cloud_task():
    # Implementation for the "Word Cloud" task
    st.subheader("Word Cloud")
    st.markdown("Generate a word cloud from comments for a given YouTube video. Enter the video ID below.")

    video_id = st.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

    if st.button("Generate Word Cloud"):
        comments = get_video_comments(video_id)
        if comments:
            generate_word_cloud(comments)
        else:
            st.warning("No comments found for the given video.")

def ner_task():
    # Implementation for the "Named Entity Recognition (NER)" task
    st.subheader("Named Entity Recognition (NER)")
    st.markdown("Perform Named Entity Recognition (NER) on comments for a given YouTube video. Enter the video ID below.")

    video_id = st.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

    if st.button("Perform NER"):
        comments = get_video_comments(video_id)
        if comments:
            perform_ner(comments)
        else:
            st.warning("No comments found for the given video.")

def summary_generation_task():
    # Implementation for the "Summary Generation" task
    st.subheader("Summary Generation Task")
    st.markdown("Generate a summary of the transcript of a YouTube video using transformers.")

    video_id = st.text_input("Enter Video ID", value="YOUR_VIDEO_ID")

    if st.button("Generate Summary"):
        comments = get_video_comments(video_id)
        if comments:
            text_for_summary = " ".join(comments)
            generate_summary(text_for_summary)
        else:
            st.warning("No comments found for the given video.")

def abuse_and_spam_detection_task():
    # Implementation for the "Abuse and Spam Detection" task
    st.subheader("Abuse and Spam Detection")
    st.warning("Abuse and Spam Detection: This feature is under development.")

# Main app execution
if __name__ == "__main__":
    handle_tasks()
