#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from pytube import YouTube

# Function to fetch YouTube video details
def get_video_details(youtube_url):
    try:
        # Parse the YouTube URL to extract video ID
        parsed_url = urlparse(youtube_url)
        query_parameters = parse_qs(parsed_url.query)
        video_id = query_parameters.get("v", [None])[0]

        if video_id:
            # Fetch the video details using pytube
            yt = YouTube(youtube_url)
            thumbnail_image = yt.thumbnail_url
            video_title = yt.title
            return video_id, video_title, thumbnail_image
        else:
            return None, None, None
    except Exception as e:
        return None, None, None

# Function to fetch video transcript
def get_video_transcript(video_id):
    try:
        # Fetch the video transcript using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(item["text"] for item in transcript)
        return transcript_text
    except Exception as e:
        return ""

# Set the page title and layout
st.set_page_config(page_title='YouTube Bot Assistant', layout='wide')

# Set the background color to turquoise
st.markdown("""
<style>
.stApp {
    background-color: #40E0D0;
}
</style>
""", unsafe_allow_html=True)

# Display the header
st.title("YouTube Bot Assistant")

# Input field for YouTube video URL in the main window
youtube_url = st.text_input("Enter the YouTube Video URL:")

# Placeholder for video details
video_id = None
video_title = None
thumbnail_image = None

# Display video details in the left-hand sidebar if URL is provided
if youtube_url:
    video_id, video_title, thumbnail_image = get_video_details(youtube_url)

# Display the YouTube video and title in the left-hand sidebar
if video_id:
    st.sidebar.header("YouTube Video")
    st.sidebar.video(f"https://www.youtube.com/watch?v={video_id}")
    st.sidebar.markdown(f"<h3 style='font-weight: bold; font-size: larger;'>{video_title}</h3>", unsafe_allow_html=True)
    #st.sidebar.subheader("Video Title:")
    #st.sidebar.write(video_title)

# Input field for user prompt in the main window
prompt = st.text_area("Enter the prompt:")

# API request button in the main window
if st.button("Submit"):
    if video_id:
        # Fetch the video transcript
        transcript_text = get_video_transcript(video_id)

    # Define the API endpoint URL
    url = "https://api-bcbe5a.stack.tryrelevance.com/latest/studios/e73273d3-ef52-4a68-beed-6e29a10b8f2f/trigger_limited"

    # Define the headers with the Content-Type
    headers = {
        "Content-Type": "application/json"
    }

    # Define the request payload with user inputs and the derived transcript
    payload = {
        "params": {
            "transcript": transcript_text if video_id else "",
            "prompt": prompt
        },
        "project": "1f236b8ce381-4d68-898d-298413845b84"
    }

    # Display a loading message while processing
    with st.spinner("Genie Work is in Progress .. !"):
        # Make the POST request to the API
        response = requests.post(url, headers=headers, data=json.dumps(payload))

     # Hide the spinner once processing is done
    st.spinner(False)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        # Print the response data for debugging
        print("Response Data:", response_data)

        # Access the relevant data from the response
        answer = response_data.get("output", {}).get("answer")
        # Display the AI response
        st.write("AI Response:", answer)
    else:
        st.write("Error - HTTP Status Code:", response.status_code)

