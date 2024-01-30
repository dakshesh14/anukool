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

# local imports
from helper import load_environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "docs")


def create_vector_database():
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

    model_name = os.environ.get("MODEL_NAME", "openai-gpt")

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
        chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_documents(loaded_documents)

    # loading the embeddings
    if model_name == "openai-gpt":
        embeddings = OpenAIEmbeddings()
    else:
        # TODO: get device from env or programmatically
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
        )

    # creating the vector store
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("db")

    print("Vector database created successfully!")


if __name__ == "__main__":
    load_environment()
    create_vector_database()
