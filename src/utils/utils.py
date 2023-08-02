# Standard library imports
import logging
import os

# Third-party library imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv

# Local module imports
from utils.chatbot import Chatbot
from utils.embedder import Embedder


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Utilities:
    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or
        from the user's input and returns it
        """
        api_key = st.session_state.get("api_key")

        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            logger.debug("API key loaded from .env")
            # st.sidebar.success("API key loaded from .env", icon="🚀")
        elif api_key is not None:
            user_api_key = api_key
            logger.debug("API key loaded from previous input")
            # st.sidebar.success("API key loaded from previous input", icon="🚀")
        else:
            user_api_key = st.sidebar.text_input(
                label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
            )
            if user_api_key:
                st.session_state.api_key = user_api_key
                logger.debug("API key loaded from user input")

        return user_api_key

    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """
        logger.info("About to upload the file")
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file:
            logger.info(f"File {uploaded_file.name} uploaded")
        else:
            logger.warning("File upload failed")
        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # Get the document embeddings for the uploaded file
            try:
                vectors = embeds.getDocEmbeds(file, uploaded_file.name)
            except Exception as e:
                logger.error(e)
                raise
            logger.debug("Embeddings for uploaded file obtained")

            # Create a Chatbot instance with the specified model and temperature
            chatbot = Chatbot(model, temperature, vectors, "DOCUMENTS")
            logger.debug("Chatbot setup complete")
        st.session_state["ready"] = True

        return chatbot
