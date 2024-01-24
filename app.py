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




# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import plotly.express as px

# # Set your YouTube Data API key here
# YOUTUBE_API_KEY = "AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

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

#         # Use a separate request to get video statistics and content details
#         video_info = youtube.videos().list(
#             part="statistics,contentDetails,snippet",
#             id=video_id
#         ).execute()

#         snippet_info = video_info.get("items", [])[0]["snippet"]
#         statistics_info = video_info.get("items", [])[0]["statistics"]
#         content_details = video_info.get("items", [])[0].get("contentDetails", {})

#         likes = int(statistics_info.get("likeCount", 0))
#         views = int(statistics_info.get("viewCount", 0))
#         duration = content_details.get("duration", "N/A")
#         upload_date = snippet_info.get("publishedAt", "N/A")
#         channel_title = snippet_info.get("channelTitle", "N/A")
#         thumbnail_url = snippet_info.get("thumbnails", {}).get("default", {}).get("url", "N/A")

#         link = f"https://www.youtube.com/watch?v={video_id}"

#         video_details.append((title, video_id, likes, views, duration, upload_date, channel_title, link, thumbnail_url))

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
#         sentiment_subjectivity = analysis.sentiment.subjectivity

#         # Categorize based on polarity
#         if sentiment_polarity > 0.2:
#             categorized_comments["Positive"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         elif sentiment_polarity < -0.2:
#             categorized_comments["Negative"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         else:
#             categorized_comments["Neutral"].append((comment, sentiment_polarity, sentiment_subjectivity))

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
#                 st.image(video[8], caption="Thumbnail", use_column_width=True)
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}")
#                 st.write(f"Duration: {video[4]}, Upload Date: {video[5]}")
#                 st.write(f"Channel: {video[6]}")
#                 st.write(f"Watch Video: [Link]({video[7]})")

# if task == "Sentiment Analysis":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")
#         categorized_comments = analyze_and_categorize_comments(comments)

#         # Display additional metrics
#         st.write(f"Total Comments: {len(comments)}")
#         st.write(f"Average Sentiment Polarity: {sum([p[1] for p in categorized_comments['Positive'] + categorized_comments['Negative']]) / len(comments)}")
#         st.write(f"Average Sentiment Subjectivity: {sum([s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']]) / len(comments)}")

#         # Display sentiment distribution chart
#         sentiment_df = []
#         for sentiment, sentiment_comments in categorized_comments.items():
#             sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

#         sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
#         st.plotly_chart(sentiment_chart)

#         # Display categorized comments
#         for sentiment, sentiment_comments in categorized_comments.items():
#             st.subheader(sentiment)
#             for comment in sentiment_comments:
#                 st.write(comment[0])

# if task == "Generate Word Cloud":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Generate Word Cloud"):
#         comments = get_video_comments(video_id)
#         st.subheader("Word Cloud")
#         wordcloud = generate_word_cloud(comments)



# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import plotly.express as px

# # Set your YouTube Data API key here
# YOUTUBE_API_KEY ="AIzaSyDm2xduRiZ1bsm9T7QjWehmNE95_4WR9KY"

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

# # Function to generate a word cloud from comments
# def generate_word_cloud(comments):
#     all_comments = ' '.join(comments)
#     wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(all_comments)
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
#                 st.write(f"<img src='{video[9]}' alt='Thumbnail' style='max-height: 150px;'>", unsafe_allow_html=True)
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}, Comments: {video[4]}")
#                 st.write(f"Duration: {video[5]}, Upload Date: {video[6]}")
#                 st.write(f"Channel: {video[7]}")
#                 st.write(f"Watch Video: [Link]({video[8]})")

# if task == "Sentiment Analysis":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")
#         categorized_comments = analyze_and_categorize_comments(comments)

#         # Display additional metrics
#         st.write(f"Total Comments: {len(comments)}")
#         st.write(f"Average Sentiment Polarity: {sum(s[1] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")
#         st.write(f"Average Sentiment Subjectivity: {sum(s[2] for s in categorized_comments['Positive'] + categorized_comments['Negative']) / len(comments)}")

#         # Display sentiment distribution chart
#         sentiment_df = []
#         for sentiment, sentiment_comments in categorized_comments.items():
#             sentiment_df.extend([(sentiment, comment[1], comment[2]) for comment in sentiment_comments])

#         sentiment_chart = px.scatter(sentiment_df, x=1, y=2, color=0, labels={'1': 'Polarity', '2': 'Subjectivity'}, title='Sentiment Analysis')
#         st.plotly_chart(sentiment_chart)

#         # Display categorized comments
#         for sentiment, sentiment_comments in categorized_comments.items():
#             st.subheader(sentiment)
#             for comment in sentiment_comments:
#                 st.write(comment[0])

# if task == "Generate Word Cloud":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Generate Word Cloud"):
#         comments = get_video_comments(video_id)
#         st.subheader("Word Cloud")
#         wordcloud = generate_word_cloud(comments)
#         st.pyplot(wordcloud)



# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
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
#         sentiment_subjectivity = analysis.sentiment.subjectivity

#         # Categorize based on polarity
#         if sentiment_polarity > 0.2:
#             categorized_comments["Positive"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         elif sentiment_polarity < -0.2:
#             categorized_comments["Negative"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         else:
#             categorized_comments["Neutral"].append((comment, sentiment_polarity, sentiment_subjectivity))

#     return categorized_comments

# # Function to generate a word cloud from comments
# def generate_word_cloud(comments):
#     if not comments:
#         st.warning("No comments found for the given video.")
#         return None

#     all_comments = ' '.join(comments)
#     wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(all_comments)
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
#                 st.write(f"<img src='{video[9]}' alt='Thumbnail' style='max-height: 150px;'>", unsafe_allow_html=True)
#                 st.write(f"Video ID: {video[1]}")
#                 st.write(f"Likes: {video[2]}, Views: {video[3]}, Comments: {video[4]}")
#                 st.write(f"Duration: {video[5]}, Upload Date: {video[6]}")
#                 st.write(f"Channel: {video[7]}")
#                 st.write(f"Watch Video: [Link]({video[8]})")

# if task == "Sentiment Analysis":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")
#         categorized_comments = analyze_and_categorize_comments(comments)
#         for sentiment, sentiment_comments in categorized_comments.items():
#             st.write(sentiment)
#             for comment_info in sentiment_comments:
#                 st.write(f"Comment: {comment_info[0]}")
#                 st.write(f"Polarity: {comment_info[1]}")
#                 st.write(f"Subjectivity: {comment_info[2]}")
#                 st.write("---")

# if task == "Generate Word Cloud":
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Generate Word Cloud"):
#         comments = get_video_comments(video_id)
#         st.subheader("Word Cloud")
#         wordcloud = generate_word_cloud(comments)
#         if wordcloud:
#             st.pyplot(wordcloud)


# import streamlit as st
# import googleapiclient.discovery
# from textblob import TextBlob
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import plotly.express as px
# import pandas as pd

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

# # Function to perform sentiment analysis and categorize comments
# def analyze_and_categorize_comments(comments):
#     categorized_comments = {
#         "Positive": [],
#         "Negative": [],
#         "Neutral": []
#     }

#     sentiment_data = []

#     for comment in comments:
#         analysis = TextBlob(comment)
#         sentiment_polarity = analysis.sentiment.polarity
#         sentiment_subjectivity = analysis.sentiment.subjectivity

#         sentiment_data.append((comment, sentiment_polarity, sentiment_subjectivity))

#         # Categorize based on polarity
#         if sentiment_polarity > 0.2:
#             categorized_comments["Positive"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         elif sentiment_polarity < -0.2:
#             categorized_comments["Negative"].append((comment, sentiment_polarity, sentiment_subjectivity))
#         else:
#             categorized_comments["Neutral"].append((comment, sentiment_polarity, sentiment_subjectivity))

#     return categorized_comments, sentiment_data

# # Function to generate a word cloud from comments
# def generate_word_cloud(sentiment_data):
#     if not sentiment_data:
#         st.warning("No comments found for the given video.")
#         return None

#     df = pd.DataFrame(sentiment_data, columns=["Comment", "Polarity", "Subjectivity"])

#     fig = px.scatter(df, x="Polarity", y="Subjectivity", hover_data=["Comment"], title="Sentiment Analysis Visualization")
#     st.plotly_chart(fig)

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
#     video_id = st.sidebar.text_input("Enter Video ID")

#     if st.sidebar.button("Analyze Sentiment"):
#         comments = get_video_comments(video_id)
#         st.subheader("Sentiment Analysis")
#         categorized_comments, sentiment_data = analyze_and_categorize_comments(comments)
#         for sentiment, sentiment_comments in categorized_comments.items():
#             st.write(sentiment)
#             for comment_info in sentiment_comments:
#                 st.write(f"Comment: {comment_info[0]}")
#                 st.write(f"Polarity: {comment_info[1]}")
#                 st.write(f"Subjectivity: {comment_info[2]}")
#                 st.write("---")

#         st.subheader("Sentiment Analysis Visualization")
#         generate_word_cloud(sentiment_data)
\

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

# Function to analyze and categorize comments based on sentiment
def analyze_and_categorize_comments(comments):
    categorized_comments = {"Positive": [], "Neutral": [], "Negative": []}

    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        if polarity > 0:
            categorized_comments["Positive"].append((comment, polarity, subjectivity))
        elif polarity == 0:
            categorized_comments["Neutral"].append((comment, polarity, subjectivity))
        else:
            categorized_comments["Negative"].append((comment, polarity, subjectivity))

    return categorized_comments

# Function to generate a word cloud from comments
def generate_word_cloud(comments):
    if not comments:
        st.warning("No comments found for the given video.")
        return

    all_comments = ' '.join(comments)

    # Generate WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)

    # Display WordCloud using Matplotlib
    st.image(wordcloud.to_image(), use_column_width=True)

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
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Analyze Sentiment"):
        comments = get_video_comments(video_id)
        st.subheader("Sentiment Analysis")
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

        # Display buttons to show Positive, Negative, and Neutral comments
        show_positive = st.button("Show Positive Comments")
        show_negative = st.button("Show Negative Comments")
        show_neutral = st.button("Show Neutral Comments")

        if show_positive:
            st.subheader("Positive Comments")
            for comment in categorized_comments["Positive"]:
                st.write(comment[0])

        if show_negative:
            st.subheader("Negative Comments")
            for comment in categorized_comments["Negative"]:
                st.write(comment[0])

        if show_neutral:
            st.subheader("Neutral Comments")
            for comment in categorized_comments["Neutral"]:
                st.write(comment[0])

if task == "Generate Word Cloud":
    video_id = st.sidebar.text_input("Enter Video ID")

    if st.sidebar.button("Generate Word Cloud"):
        comments = get_video_comments(video_id)
        st.subheader("Word Cloud")
        generate_word_cloud(comments)

