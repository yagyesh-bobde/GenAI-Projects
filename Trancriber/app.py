import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the summarization model
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video, providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url, language="en"):
    try:
        # Extract video ID from the YouTube URL
        video_id = youtube_video_url.split("=")[1]
        
        # Get transcript text using YouTubeTranscriptApi
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Concatenate the transcript text
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to generate content using the Gemini Pro model
def generate_gemini_content(transcript_text, prompt):
    # Create a GenerativeModel object with the Gemini Pro model
    model = genai.GenerativeModel("gemini-pro")
    
    # Generate content using the provided prompt and transcript text
    response = model.generate_content(prompt + transcript_text)
    
    return response.text

# Streamlit app title
st.title("YouTube Transcript to Detailed Notes Converter")

# Input for YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Dropdown for selecting video language
language = st.selectbox("Select Video Language:", ["en", "es", "fr", "de", "it", "ja", "ko", "pt", "ru", "zh-CN"])

# Number input for setting maximum summary length
max_summary_length = st.number_input("Maximum Summary Length (words):", min_value=50, max_value=500, value=250)

# Display YouTube video thumbnail if the link is valid
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.warning("Invalid YouTube URL. Please enter a valid URL.")

# Button to trigger the note generation process
if st.button("Get Detailed Notes"):
    try:
        # Extract transcript details from the YouTube video
        transcript_text = extract_transcript_details(youtube_link, language)
    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        st.stop()

    if transcript_text:
        # Display the original transcript
        st.markdown("## Original Transcript:")
        st.write(transcript_text)

        # Generate and display detailed notes using the Gemini Pro model
        summary = generate_gemini_content(transcript_text, prompt)
        truncated_summary = ' '.join(summary.split()[:max_summary_length])
        
        st.markdown("## Detailed Notes:")
        st.write(truncated_summary)