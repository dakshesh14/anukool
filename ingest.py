"""
This file contains the code for ingesting data from the data source. 
"""

import os

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings

# env variables
from constants import OPENAI_API_KEY, USE_OPENAI


def create_vector_database(device="cpu"):
    """
    Create the vector database from the documents in the docs folder
    and save it in the db folder.
    """

    # take confirmation if there's some already in db folder
    if os.path.exists("db"):
        confirmation = input(
            "Do you want to overwrite the existing database? (y/n): "
        ).lower()

        if confirmation == "n":
            print("Aborting...")
            return

    pdf_loader = DirectoryLoader(
        "docs/",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    text_loader = DirectoryLoader(
        "docs/",
        glob="**/*.txt",
        loader_cls=TextLoader,
    )

    all_loaders = [pdf_loader, text_loader]

    # loading the documents from all the loaders
    loaded_documents = []
    for loader in all_loaders:
        loaded_documents.extend(loader.load())

    # splitting the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=24, length_function=len
    )
    chunks = text_splitter.split_documents(loaded_documents)

    # loading the embeddings
    if USE_OPENAI:
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    else:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": device},
        )

    # creating the vector store
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("db")

    print("Vector database created successfully!")


def get_vector_database(device="cpu"):
    """
    Get the vector database from the db folder.
    """

    if USE_OPENAI:
        embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    else:
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": device},
        )

    return FAISS.load_local("db", embedding)


if __name__ == "__main__":
    create_vector_database()
