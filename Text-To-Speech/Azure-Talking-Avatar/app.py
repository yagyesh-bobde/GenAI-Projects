import streamlit as st
import requests
import json
from urllib.parse import unquote
import time
import logging
from dotenv import load_dotenv
import os
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
logger = logging.getLogger(__name__)

load_dotenv()
SUBSCRIPTION_KEY = os.getenv('SUBSCRIPTION_KEY')
SERVICE_REGION = os.getenv('SERVICE_REGION')
SERVICE_HOST = os.getenv('SERVICE_HOST')

st.set_page_config(page_title="Talking Avatar", page_icon="🗣️",initial_sidebar_state="auto",layout='centered')
NAME = "Text-to-Speech"
DESCRIPTION = "Using Azure AI Services"

lang_voices = {
    'Arabic': ['ar-SA', 'ar-SA-ZariyahNeural'],
    'Bahasa Indonesian': ['id-ID', 'id-ID-GadisNeural'],
    'Bengali': ['bn-IN', 'bn-IN-TanishaaNeural'],
    'Chinese Mandarin': ['zh-CN', 'zh-CN-XiaoxiaoNeural'],
    'Dutch': ['nl-NL', 'nl-NL-FennaNeural'],
    'English': ['en-US', 'en-US-AvaNeural'],
    'French': ['fr-FR', 'fr-FR-DeniseNeural'],
    'German': ['de-DE', 'de-DE-KatjaNeural'],
    'Hindi': ['hi-IN', 'hi-IN-SwaraNeural'],
    'Italian': ['it-IT', 'it-IT-ElsaNeural'],
    'Japanese': ['ja-JP', 'ja-JP-NanamiNeural'],
    'Korean': ['ko-KR', 'ko-KR-SunHiNeural'],
    'Russian': ['ru-RU', 'ru-RU-SvetlanaNeural'],
    'Spanish': ['es-ES', 'es-ES-ElviraNeural'],
    'Telugu': ['te-IN', 'te-IN-ShrutiNeural']
}

with st.sidebar:
    lang=st.selectbox('Choose the language',list(lang_voices.keys()), index=5) 
    style=st.selectbox('Avatar Style',["Casual-Sitting","Graceful-Sitting","Technical-Sitting","Graceful-Standing","Technical-Standing"],index=1)
    style=style.lower()
    voice=lang_voices[lang][1]
    st.markdown("[Source Code](https://github.com/Sgvkamalakar/Azure-Talking-Avatar)")
    st.markdown("[Explore my Codes](https://github.com/sgvkamalakar)")
    st.markdown("[Connect with me on LinkedIn](https://www.linkedin.com/in/sgvkamlakar)")
    

def submit_synthesis(text):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Content-Type':'application/json'
    }
    payload = {
        'displayName': NAME,
        'description': DESCRIPTION,
        "textType": "PlainText",
        'synthesisConfig': {
            "voice": voice,
        },
        'customVoices': {},
        "inputs": [
            {
                "text": text,
            },
        ],
        "properties": {
            "customized": False,
            "talkingAvatarCharacter": "lisa",
            "talkingAvatarStyle": style,
            "videoFormat": "webm",
            "videoCodec": "vp9",
            "subtitleType": "soft_embedded",
            "backgroundColor": "transparent",
        }
    }

    response = requests.post(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        logger.info('Batch avatar synthesis job submitted successfully')
        logger.info(f'Job ID: {response.json()["id"]}')
        return response.json()["id"]
    else:
        logger.error(f'Failed to submit batch avatar synthesis job: {response.text}')


def get_synthesis(job_id):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar/{job_id}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.debug('Get batch synthesis job successfully')
        logger.debug(response.json())
        if response.json()['status'] == 'Succeeded':
            logger.info(f'Batch synthesis job succeeded, download URL: {response.json()["outputs"]["result"]}')
            video_url = f'{response.json()["outputs"]["result"]}'
            decoded_url = unquote(video_url)
            st.video(decoded_url)
        

        return response.json()['status']
    else:
        logger.error(f'Failed to get batch synthesis job: {response.text}')

def list_synthesis_jobs(skip: int = 0, top: int = 100):
    url = f'https://{SERVICE_REGION}.{SERVICE_HOST}/api/texttospeech/3.1-preview1/batchsynthesis/talkingavatar?skip={skip}&top={top}'
    header = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    response = requests.get(url, headers=header)
    if response.status_code < 400:
        logger.info(f'List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        logger.info(response.json())
    else:
        logger.error(f'Failed to list batch synthesis jobs: {response.text}')


def main():
    st.title("Azure Text-to-Talking Avatar")
    # st.info()
    text_input = st.text_area(f'Type text in {lang}')
    submit_button = st.button("Submit Job")
    if submit_button:
        with st.spinner("Processing..."):
            job_id = submit_synthesis(text_input)
            if job_id is not None:
                while True:
                    status = get_synthesis(job_id)
                    if status == 'Succeeded':
                        st.success('Batch avatar synthesis job succeeded ✅')
                        break
                    elif status == 'Failed':
                        st.error('Batch avatar synthesis job failed ❌')
                        break
                    else:
                        time.sleep(5)  

footer = """<style>
a:link , a:visited{
    color: #00aadd;
    background-color: transparent;
}

a:hover, a:active {
    color: blue;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color:#0e1117;
    color: white;
    text-align: center;
    padding: 10px;  /* Added padding for better appearance */
}

.footer p {
    margin-bottom: 5px;  /* Adjusted margin for better spacing */
}

.footer a {
    text-decoration: none;
}
.red-heart {
    color: red;  /* Set the color of the heart emoji to red */
}
.footer a:hover {
    text-decoration: underline;
}
</style>
<div class="footer">
    <p>Developed with <span class="red-heart">❤</span> using <a href="https://speech.microsoft.com/" target="_blank">Azure Speech Services</a>  by <a href="https://www.linkedin.com/in/sgvkamalakar" target="_blank">Kamalakar</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

