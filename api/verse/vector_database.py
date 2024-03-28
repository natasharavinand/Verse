import os
import shutil

from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def create_document_chunks():
    """
    create_document_chunks iterates through the processed data directory and uses the cleaned .txt files
    (that represent lecture transcripts) and turns them into langchain Documents that langchain's RecursiveCharacterTextSplitter can
    recognize. This text splitter recursively creates chunks with different parameters (ex. chunk size, overlap).

    Args:
    None

    Returns:
    chunks (List[Document]): This is a list of Documents that represent chunks from text.

    Raises:
    None

    """

    processed_data_path = os.path.join(BASEDIR, "data/processed")

    loader = DirectoryLoader(processed_data_path, glob="*.txt", recursive=True)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


def create_chromaDB(chunks):
    """
    create_chromaDB uses chunks created with langchain's RecursiveCharacterTextSplitter and split_documents and creates a
    new ChromaDB. This ChromaDB can be used as a vector database with Retrieval Augmented Generation and stores vector embeddings.

    Args:
    chunks (List[Documents]): This is a list of Documents that represent chunks from text.

    Returns:
    None

    Raises:
    None

    """
    chroma_path = os.path.join(BASEDIR, "chroma")

    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

    chromaDB = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(model="text-embedding-3-large"),
        collection_name="transcripts",
        persist_directory=chroma_path,
    )

    chromaDB.persist()


def generate_vector_db_from_processed_data():
    """
    generate_vector_db_from_processed_data executes the pipeline to create a Chroma vector database from the
    Retrieval-Augmented-Generation/data/processed directory.

    Args:
    None

    Returns:
    None

    Raises:
    None

    """

    chunks = create_document_chunks()
    create_chromaDB(chunks)


if __name__ == "__main__":
    generate_vector_db_from_processed_data()