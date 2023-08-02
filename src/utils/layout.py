# Standard library imports
import logging
import os

# Third-party library imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Layout:

    def show_header(self, types_files):
        """
        Displays the header of the app
        """
        logger.debug(f'Displaying header for file types: {types_files}')
        st.markdown(
            f"""
            <h1 style='text-align: center;'> Ask Emma about your {types_files} files ! 😁</h1> <p>Getting started is 
            as easy as dropping your file into the box on your left. Emma will then be all set to chat with you about 
            your document, revealing insights and information in a snap!</p> """,
            unsafe_allow_html=True,
        )

    def show_api_key_missing(self):
        """
        Displays a message if the user has not entered an API key
        """
        logger.warning('API key is missing')
        st.markdown(
            """
            <div style='text-align: center;'>
                <h4>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a>
                 to start chatting</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def prompt_form(self):
        """
        Displays the prompt form
        """
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="Ask me anything about the document...",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input
            if is_ready:
                logger.debug(f'User input: {user_input}')
        return is_ready, user_input
