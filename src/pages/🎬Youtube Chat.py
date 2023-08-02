# Standard library imports
import logging
import os
import re

# Third-party imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Langchain imports
from langchain.chains import AnalyzeDocumentChain, ConversationalRetrievalChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter

# Local module imports
from utils.embedder import Embedder
from utils.layout import Layout
from utils.sidebar import Sidebar
from utils.utils import Utilities
from streamlit_chat import message


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

# Log the start of the script
logger.info('YouTube Script started')

st.set_page_config(layout="wide", page_icon="💬", page_title="Your Friendly Chat-Bot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

st.markdown(
    f"""
    <h1 style='text-align: center;'> Ask Emma to summarize youtube video 🎬! </h1>
    """,
    unsafe_allow_html=True,
)

user_api_key = utils.load_api_key()

sidebar.about()
chunks = []

st.session_state["model"] = "gpt-3.5-turbo"
st.session_state["temperature"] = 0.0

if not user_api_key:
    layout.show_api_key_missing()

else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    script_docs = []

    def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match:
            video_id = match.group()
        else:
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match:
                video_id = match.group()
        return video_id


    video_url = st.text_input(placeholder="Enter Youtube Video URL", label_visibility="hidden", label=" ")
    if video_url:
        video_id = get_youtube_id(video_url)

        if video_id != "":
            # Log the video ID
            logger.debug(f'Video ID: {video_id}')

            t = YouTubeTranscriptApi.get_transcript(video_id, languages=(
            'en', 'fr', 'es', 'zh-cn', 'hi', 'ar', 'bn', 'ru', 'pt', 'sw'))
            finalString = ""
            for item in t:
                text = item['text']
                finalString += text + " "

            text_splitter = CharacterTextSplitter()
            chunks = text_splitter.split_text(finalString)

            summary_chain = load_summarize_chain(OpenAI(temperature=0),
                                                 chain_type="map_reduce", verbose=False)

            summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)

            answer = summarize_document_chain.run(chunks)

            st.subheader(answer)

if video_url:
    video_id = get_youtube_id(video_url)

    if video_id != "":
        # Define the iframe code with the desired width, height, and autoplay enabled
        iframe_code = f"""
        <div style="text-align: center;">
            <iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}?autoplay=1" 
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; 
                picture-in-picture" allowfullscreen></iframe> </div> """

        # Embed the iframe code using Streamlit's Markdown component
        st.markdown(iframe_code, unsafe_allow_html=True)
        embeds = Embedder()
        vectors = embeds.getVideoEmbeds(chunks, video_id)  # You may need to adjust this method for chunks

        chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(temperature=0.0,
                                                                     model_name='gpt-3.5-turbo',
                                                                     openai_api_key=user_api_key),
                                                      retriever=vectors.as_retriever(),
                                                      verbose=False)  # Add this line

        def conversational_chat(query):

            result = chain({"question": query, "chat_history": st.session_state['history']})
            st.session_state['history'].append((query, result["answer"]))

            return result["answer"]


        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello ! Ask me anything about the video 🤗"]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! 👋"]

        # container for the chat history
        response_container = st.container()
        # container for the user's text input
        container = st.container()

        with container:
            with st.form(key='my_form', clear_on_submit=True):
                user_input = st.text_input("Chat:", placeholder="Talk about your csv data here (:", key='input')
                submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                output = conversational_chat(user_input)

                st.session_state['past'].append(user_input)
                st.session_state['generated'].append(output)

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="fun-emoji")
                    message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")

# Log the end of the script
logger.info('YouTube Script ended')
