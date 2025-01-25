from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()
import os
from loguru import logger
from langchain_text_splitters import MarkdownHeaderTextSplitter
from typing import Literal

DB_PATH = "../chroma_db"
def get_retriever(collection_name, md_path=None):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    if len(vectorstore.get()['ids']) == 0:
        logger.info("Creating database")
        with open(md_path, "r") as f:
            text = f.read()
        headers = [
            ('#', "Book"),
            ('##', 'Part'),
            ('###', 'Title'),
            ('####', 'Chapter'),
            ('#####', 'Section')
        ]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers,
                                            strip_headers=False,)
        md_splits = splitter.split_text(text)


        vectorstore = Chroma.from_documents(
            documents=md_splits,
            collection_name=collection_name,
            embedding=embeddings,
            persist_directory=DB_PATH
        )


    retriever = vectorstore.as_retriever()
    return retriever  




def get_llm(model="gpt-4o"): # TODO: rm this (for testing purposes)
    if model == "gpt-4o":
        return ChatOpenAI(model=model)
    else:
        return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        )