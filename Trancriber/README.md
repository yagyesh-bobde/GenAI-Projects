# YouTube Transcript to Detailed Notes Converter

## Overview

This Streamlit app leverages the power of AI to automate the process of generating detailed notes from YouTube video transcripts. The Gemini Pro model is employed for advanced note generation, making it suitable for various subjects, including Physics, Chemistry, Mathematics, or Data Science & Statistics.

## How It Works

1. **Input YouTube Link:** Provide the link of the YouTube video you want to transcribe.
2. **Select Video Language:** Choose the language of the video transcript.
3. **Set Maximum Summary Length:** Adjust the maximum length of the generated summary in words.
4. **Click "Get Detailed Notes":** Witness the AI-powered Gemini Pro model generate detailed notes based on the video transcript!

## Technologies Used

- [Streamlit](https://www.streamlit.io/): Streamlit is used for creating a user-friendly web application interface.
- [Google Generative AI](https://cloud.google.com/ai): The Gemini Pro model is employed for advanced text generation.
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcription-api): Extracts video transcripts from YouTube.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your Google API key: `GOOGLE_API_KEY=your_api_key`
3. Run the app: `streamlit run app.py`

## Sample Usage

1. Input: Paste the YouTube video link.
2. Select: Choose the video language and set the maximum summary length.
3. Generate: Click the "Get Detailed Notes" button to generate notes.
