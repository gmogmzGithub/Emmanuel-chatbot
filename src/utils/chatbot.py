# Standard library imports
import logging
import os

# Third-party library imports
import streamlit as st
from dotenv import find_dotenv, load_dotenv
import langchain  # fix Error: module 'langchain' has no attribute 'verbose'

# Langchain imports
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback


langchain.verbose = False
load_dotenv(find_dotenv())
logging_level = os.getenv('LOGGING_LEVEL') or 'INFO'

# Configure logging with module name and filename
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Chatbot:

    def __init__(self, model_name, temperature, vectors, mode):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors
        self.mode = mode
        self.qa_template = self.get_qa_template()
        self.QA_PROMPT = PromptTemplate(template=self.qa_template, input_variables=["context", "question"])
        logger.info(f'Chatbot initialized with model: {model_name}, temperature: {temperature}')

    def get_qa_template(self):
        if self.mode == "DOCUMENTS":
            logger.debug("Using the 'DOCUMENTS' template prompt")
            return """
                You are a helpful AI assistant named Emma or Emmanuel. The user gives you a file its content is represented by 
                the following pieces of context, use them to answer the question at the end.
                If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
                If the question is not related to the context, politely respond that you are tuned to only answer questions that 
                are related to the context.
                Use as much detail as possible when responding.

                context: {context}
                =========
                question: {question}
                ======
                """
        else:
            logger.debug("Using the 'YOUTUBE' template prompt")
            return """
                You are a helpful AI assistant named Emma or Emmanuel. The user provides you with a YouTube 
                video that has been translated into text, and you will use this text to answer the question at the end. 
                If you don't know the answer, simply say that you don't know, and do NOT attempt to make up an answer. 
                If the question is unrelated to the context of the provided video, respond politely that you are only 
                equipped to answer questions related to the given context. Please provide as much detail as possible in 
                your response. 

                context: {context}
                =========
                question: {question}
                ======
                """

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        logger.debug(f'Starting conversational chat with query: {query}')
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()

        chain = ConversationalRetrievalChain.from_llm(llm=llm,
                                                      retriever=retriever, verbose=True, return_source_documents=True,
                                                      max_tokens_limit=4097,
                                                      combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        # count_tokens_chain(chain, chain_input)
        logger.debug(f'Chatbot response: {result["answer"]}')
        return result["answer"]


def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result
