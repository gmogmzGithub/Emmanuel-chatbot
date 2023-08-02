# Standard library imports
import logging
import os
import pickle
import tempfile

# Third-party library imports
from dotenv import find_dotenv, load_dotenv

# Langchain imports
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS


load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        self.createEmbeddingsDir()

    def createEmbeddingsDir(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)
        logger.info("Embeddings directory created.")

    def storeDocEmbeds(self, file, original_filename):
        """
        Stores document embeddings using Langchain and FAISS
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        def get_file_extension(uploaded_file):
            file_extension = os.path.splitext(uploaded_file)[1].lower()
            return file_extension

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )

        file_extension = get_file_extension(original_filename)

        if file_extension == ".csv":
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ',', })
            data = loader.load()
            logger.debug("CSV len(data)", len(data))
            logger.debug(f"CSV file loaded: {original_filename}")

        elif file_extension == ".pdf":
            loader = PyPDFLoader(file_path=tmp_file_path)
            data = loader.load_and_split(text_splitter)
            logger.debug("PDF len(data)", len(data))
            logger.debug(f"PDF file loaded: {original_filename}")

        elif file_extension == ".txt":
            loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
            data = loader.load_and_split(text_splitter)
            logger.debug(f"TXT file loaded: {original_filename}")

        embeddings = OpenAIEmbeddings()

        vectors = FAISS.from_documents(data, embeddings)
        logger.info(f"Vectors for {original_filename} created.")
        os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)
        logger.info(f"Vectors for {original_filename} stored in pickle file.")

    def storeVideoEmbeds(self, chunks, original_filename):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )

        # Convert chunks into a single string if it is a list
        text_data = chunks[0] if isinstance(chunks, list) and len(chunks) == 1 else " ".join(chunks)

        # Create a temporary file to store the text data
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
            temp_file.write(text_data)
            temp_file_path = temp_file.name

        loader = TextLoader(file_path=temp_file_path, encoding="utf-8")
        data = loader.load_and_split(text_splitter)

        embeddings = OpenAIEmbeddings()

        vectors = FAISS.from_documents(data, embeddings)
        logger.info(f"Vectors for {original_filename} created.")
        os.remove(temp_file_path)

        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)
        logger.info(f"Vectors for {original_filename} stored in pickle file.")

    def getDocEmbeds(self, file, original_filename):
        """
        Retrieves document embeddings
        """
        if not os.path.isfile(f"{self.PATH}/{original_filename}.pkl"):
            self.storeDocEmbeds(file, original_filename)

        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "rb") as f:
            vectors = pickle.load(f)

        logger.info(f"Vectors for {original_filename} retrieved.")
        return vectors

    def getVideoEmbeds(self, chunks, original_filename):
        """
        Retrieves document embeddings
        """
        if not os.path.isfile(f"{self.PATH}/{original_filename}.pkl"):
            self.storeVideoEmbeds(chunks, original_filename)

        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "rb") as f:
            vectors = pickle.load(f)

        logger.info(f"Vectors for {original_filename} retrieved.")
        return vectors
