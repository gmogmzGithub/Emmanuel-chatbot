import streamlit as st
import os
import logging

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)

# Log the start of the script
logger.info('Emma Script Started')

# Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Your Friendly Chat-Bot 🤖")

# Log the configuration setup
logger.debug('Streamlit page configuration set')


def delete_pkl_files():
    # Log the start of the deletion process
    logger.debug(f'Starting deletion of .pkl files in embeddings')

    # Iterate through the files in the specified directory
    for filename in os.listdir("./embeddings"):
        if filename.endswith(".pkl"):
            # Construct the full path to the file
            file_path = os.path.join("./embeddings", filename)

            try:
                # Delete the file
                os.remove(file_path)
                # Log successful deletion
                logger.debug(f'{file_path} deleted successfully')
            except Exception as e:
                # Log any errors that occur during deletion
                logger.error(f'Error deleting {file_path}: {str(e)}')

    # Log the end of the deletion process
    logger.debug(f'Finished deletion of .pkl files in /embeddings')


delete_pkl_files()

# Contact
with st.sidebar.expander("📬 Contact"):
    st.write("**Mail** : guillermogomezmora@gmail.com")
    st.write("**LinkedIn** : linkedin.com/in/gmogmz/")
    st.write("**Created by Guillermo Gomez**")

# Log the contact info setup
logger.debug('Contact info set')

# Title
st.markdown(
    """
    <h2 style='text-align: center;'>Emma: Your Personal Document and Video Interpreter! 🤖</h1>
    """,
    unsafe_allow_html=True, )

st.markdown("---")

video_id = 'u3ybWiEUaUU'
youtube_url = f'https://www.youtube.com/embed/{video_id}?loop=1&playlist={video_id}&autoplay=1'
iframe_code = f'<div style="text-align:center;"><iframe width="560" height="315" src="{youtube_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
st.markdown(iframe_code, unsafe_allow_html=True)

# Description
# Description
st.markdown(
    """ 
    <div style="text-align:center; padding: 20px;">
        <h3>Are you in search of a smarter way to interact with your documents?</h3>
        <p>You've come to the right place.</p>
        <p>Emma is your go-to chatbot for making sense of documents and videos. Upload a PDF, TXT, or CSV file and let Emma chat with you about its content. Need precise information from tabular data? Emma's got you covered.</p>
        <p>Want a quick summary of a YouTube video? Emma can do that too.</p>
        <p>Best of all, Emma is free to use, thanks to our select advertisers.</p>
        <h4>Ready to get started? Watch our quick tutorial video above and let Emma simplify your digital world.</h4>
    </div>
    <ul style="padding-left:10%; padding-right:10%;">
        <li><strong>Document Chatbot:</strong> Have a PDF, TXT, or CSV file you want to discuss? Emma-Chat is here to help. She'll pick out the most useful parts of your document and chat with you about them. It's like having a conversation with your data!</li>
        <li><strong>Excel Chatbot:</strong> Need to dive deep into a CSV file? Emma-Sheet is your go-to. She'll process your entire file, providing precise information and even creating graphs to help you visualize your data.</li>
        <li><strong>Youtube Chatbot:</strong> Want a quick summary of a YouTube video? Emma-Youtube has got you covered. She'll provide you with a concise summary, saving you time and effort.</li>
    </ul>
    """,
    unsafe_allow_html=True)
st.markdown("---")

# Emma's Pages
st.subheader("What can Emma do for you? 🤖")
st.write("""
- **Document Chat bot**: Have a PDF, TXT, or CSV file you want to discuss? Emma-Chat is here to help. She'll pick out the most useful parts of your document and chat with you about them. It's like having a conversation with your data!
- **Excel Chat bot**: Need to dive deep into a CSV file? Emma-Sheet is your go-to. She'll process your entire file, providing precise information and even creating graphs to help you visualize your data.
- **Youtube Chat bot**: Want a quick summary of a YouTube video? Emma-Youtube has got you covered. She'll provide you with a concise summary, saving you time and effort.
""")
st.markdown("---")

# Log the pages setup
logger.debug('Pages setup complete')

st.markdown("---")

# Log the end of the script
logger.info('Emma script ended')
