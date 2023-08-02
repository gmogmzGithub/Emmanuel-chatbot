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


class Sidebar:
    MODEL_OPTIONS = ["gpt-3.5-turbo"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        logger.info('About section accessed')
        about = st.sidebar.expander("🧠 About Emma ")
        sections = [
            "#### Meet Emma, your personal AI chatbot here to make your data more accessible and understandable. 📄",
            "#### Emma uses advanced AI technology to chat with you in a natural, intuitive way about the content of "
            "your documents and videos. 🌐",
            "#### Emma is brought to life thanks to the power of Langchain, OpenAI, and Streamlit. Together, "
            "they make Emma your go-to tool for engaging with your digital world. ⚡",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            logger.info('Reset chat button clicked')
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox(label="Model", options=self.MODEL_OPTIONS)
        logger.debug(f'Model selected: {model}')
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        logger.debug(f'Temperature set: {temperature}')
        st.session_state["temperature"] = temperature

    def show_options(self):
        with st.sidebar.expander("You can reset the conversation here", expanded=False):
            logger.info('Options section accessed')
            self.reset_chat_button()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)
