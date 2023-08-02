# Standard library imports
import logging
import os
import re
import sys
from io import StringIO

# Third-party imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv

# Local module imports
from utils.history import ChatHistory
from utils.layout import Layout
from utils.sidebar import Sidebar
from utils.utils import Utilities


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

# Log the start of the script
logger.info('Documents Script started')


# To be able to update the changes made to utils in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]


# Log the reloading of utils
logger.debug('Reloading utils')

history_module = reload_module('utils.history')
layout_module = reload_module('utils.layout')
utils_module = reload_module('utils.utils')
sidebar_module = reload_module('utils.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="Your Friendly Chat-Bot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

# Log the instantiation of the main components
logger.debug('Main components instantiated')

layout.show_header("PDF, TXT, CSV")

user_api_key = utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    uploaded_file = utils.handle_upload(["pdf", "txt", "csv"])

    if uploaded_file:
        # Log the uploaded file
        logger.debug(f'Uploaded file: {uploaded_file}')

        # Configure the sidebar
        sidebar.show_options()
        sidebar.about()

        # Initialize chat history
        history = ChatHistory()

        # Log the initialization of chat history
        logger.debug('Chat history initialized')

        try:
            chatbot = utils.setup_chatbot(
                uploaded_file, st.session_state["model"], st.session_state["temperature"]
            )

            # Log the setup of the chatbot
            logger.debug('Chatbot setup completed')

            st.session_state["chatbot"] = chatbot

            if st.session_state["ready"]:
                # Log the readiness of the session
                logger.debug('Session is ready')

                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                with prompt_container:
                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()

                    # Log the user input
                    logger.debug(f'User input: {user_input}')

                    # Initialize the chat history
                    history.initialize(uploaded_file)

                    # Reset the chat history if button clicked
                    if st.session_state["reset_chat"]:
                        history.reset(uploaded_file)

                    if is_ready:
                        # Update the chat history and display the chat messages
                        history.append("user", user_input)

                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()

                        output = st.session_state["chatbot"].conversational_chat(user_input)

                        sys.stdout = old_stdout

                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        thoughts = captured_output.getvalue()
                        cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            # Log any exceptions that occurred
            logger.error(f'Error occurred: {str(e)}', exc_info=True)
            st.error(
                f"Error: We're having trouble reading the file you uploaded. {str(e)} Please ensure the file "
                f"meets the following criteria:\n\n "
                "- It is not password protected or encrypted.\n" 
                "- The text in the file can be highlighted and copied (this often isn't the case if the file was "
                "scanned).\n "
                "- It is not primarily composed of images.\n\n"
                "Please try uploading another file.")

# Log the end of the script
logger.info('Documents Script ended')
