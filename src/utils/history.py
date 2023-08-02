# Standard library imports
import logging
import os

# Third-party library imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from streamlit_chat import message


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class ChatHistory:

    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history
        logger.debug('Chat history initialized')

    def default_greeting(self):
        return "Hey Emma ! 👋"

    def default_prompt(self, topic):
        return f"Hello ! Ask me anything about {topic} 🤗"

    def initialize_user_history(self):
        st.session_state["user"] = [self.default_greeting()]

    def initialize_assistant_history(self, uploaded_file):
        st.session_state["assistant"] = [self.default_prompt(uploaded_file.name)]

    def initialize(self, uploaded_file):
        if "assistant" not in st.session_state:
            self.initialize_assistant_history(uploaded_file)
        if "user" not in st.session_state:
            self.initialize_user_history()

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        self.initialize_user_history()
        self.initialize_assistant_history(uploaded_file)
        st.session_state["reset_chat"] = False
        logger.info('Chat history reset')


    def append(self, mode, message):
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    logger.debug('st.session_state["user"][i]: %s', st.session_state["user"][i])
                    message(
                        st.session_state["user"][i],
                        is_user=True,
                        key=f"history_{i}_user",
                        avatar_style="fun-emoji",
                    )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="bottts")

    def load(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()
                logger.info('Chat history loaded from file')

    def save(self):
        with open(self.history_file, "w") as f:
            f.write("\n".join(self.history))
        logger.info('Chat history saved to file')
