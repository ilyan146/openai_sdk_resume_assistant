from pathlib import Path

import chromadb
import numpy as np
from langchain_community.document_loaders.generic import GenericLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from openai import AzureOpenAI
from PyPDF2 import PdfReader
from tqdm import tqdm

from openai_sdk_resume_assistant.client import AzureAIClient


class VectorDB:
    """Vector database class for creating ChromaDB vector databases using AzureOpenAI embedding models"""

    DEFAULT_DB = "default_vectorstore"

    def __init__(
        self,
        vector_db_name: str = DEFAULT_DB,
        azure_openai_client: AzureAIClient | AzureOpenAI | None = None,
        embedding_model: str = "text-embedding-ada-002",
    ):
        """Initialize the vector database connection with ChromaDB client"""
        self.vector_db_name = vector_db_name
        self.vector_db_path = Path(__file__).parent / vector_db_name
        self.vector_db_client = chromadb.PersistentClient(path=self.vector_db_path)
        logger.info(f"Initialized VectorDB: {self.vector_db_path}")

        self.azure_openai_client = azure_openai_client or AzureAIClient()

        self.embedding_model = embedding_model
        logger.debug(f"Embedding model used: {self.embedding_model}")

    # Viewing existing collections
    @property
    def collection_list(self) -> list[str]:
        """Get list of the existing collection in the vector database"""
        # Get list of existing chroma_client
        existing_collections = [collection.name for collection in self.vector_db_client.list_collections()]
        logger.debug(f"Existing collections: {existing_collections}")

        return existing_collections

    # get a collection or create a new one
    def get_or_create_collection(self, collection_name: str) -> chromadb.Collection:
        """Add a new collection to the vector database or get the existing one with the collection name"""
        if collection_name not in self.collection_list:
            collection = self.vector_db_client.create_collection(name=collection_name)
            logger.info(f"New collection created in the vector database with name: {collection_name}")
            return collection
        else:
            collection = self.vector_db_client.get_collection(name=collection_name)
            logger.info(f"Collection exists with name: {collection_name}, using existing collection")
            return collection

    def _get_embeddings(self, text_input: str) -> np.ndarray:
        """Compute the embedding for the given text using an OpenAI embedding model."""
        response = self.azure_openai_client.embeddings.create(input=text_input, model=self.embedding_model)
        emb = np.array(response.data[0].embedding).astype("float32")
        return emb

    def add_pdf_to_collection(self, directory: Path | str, collection_name: str) -> None:
        """Add PDF documents from a directory to a collection of vector database as vectors of pages"""

        # Exit out if the collection_name already exists
        if collection_name in self.collection_list:
            logger.warning(f"Collection {collection_name} already exists. The new docs will be added to the existing collection.")

        collection = self.get_or_create_collection(collection_name=collection_name)

        if isinstance(directory, str):
            directory = Path(directory)
        logger.debug(f"Processing pdfs from directory: {directory} to collection: {collection.name} ......")

        for pdf_file in directory.glob("*.pdf"):
            logger.debug(f"Processing file: {pdf_file.name}")
            reader = PdfReader(pdf_file)

            snake_file_name = pdf_file.stem.replace(" ", "_").lower()
            ids = []
            metadata = []
            embeddings = []
            documents = []

            for index, page in tqdm(
                enumerate(reader.pages),
                total=len(reader.pages),
                desc=f"Processing file: {pdf_file.name}",
            ):
                text = page.extract_text()
                if text:
                    unique_id = f"{snake_file_name}_page_{index}"
                    ids.append(unique_id)
                    documents.append(text)
                    embeddings.append(self._get_embeddings(text).tolist())
                    metadata.append({"page": index, "source": pdf_file, "file_name": pdf_file.name})

            # Add the pdf data to the collection with embeddings
            # collection = self.get_or_create_collection(collection_name=collection_name)
            collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadata)
            logger.success(f"PDF documents added to the collection: {collection_name} successfully")

    # TODO: Create langchain based text parser from dir
    def add_texts_to_collection(self, directory: Path | str, collection_name: str) -> None:
        """Add text documents from a directory to a collection of vector database as vectors of pages"""
        if isinstance(directory, str):
            directory = Path(directory)
        loader = GenericLoader.from_filesystem(str(directory), glob="**/*.txt")
        documents = loader.load()

        # Instantiate text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
        # Create text chunks
        chunks = text_splitter.split_documents(documents)
        # Loop over the chunks add creat a list of ids, documents, embedding
        ids = []
        metadata = []
        embeddings = []
        documents = []
        collection = self.get_or_create_collection(collection_name=collection_name)
        logger.debug(f"Processing texts from directory: {directory} to collection: {collection_name} ......")
        for index, chunk in tqdm(
            enumerate(chunks),
            total=len(chunks),
            desc=f"Processing text files from dir : {str(directory)}",
        ):
            unique_id = f"{str(directory.stem).replace(' ', '_').lower()}_chunk_{index}"
            ids.append(unique_id)
            documents.append(chunk.page_content)
            embeddings.append(self._get_embeddings(chunk.page_content).tolist())
            metadata.append(
                {
                    "page": index,
                    "source": chunk.metadata.get("source", ""),
                    "file_name": Path(chunk.metadata.get("source", "")).stem,
                }
            )

        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadata)
        logger.success(f"Text documents added to the collection: {collection_name} successfully")

    # Removing collection from the vector database
    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection from the vector database"""
        if collection_name in self.collection_list:
            self.vector_db_client.delete_collection(name=collection_name)
            logger.info(f"Collection {collection_name} deleted from the vector database")
        else:
            logger.warning(f"Collection {collection_name} does not exist in the vector database")


if __name__ == "__main__":
    # Example creating a vector database and adding PDF documents to it
    # COLLECTION_NAME = "ilyan_resume"
    # base_dir = Path(__file__).parent.parent
    # pdf_docs_dir = base_dir / "data"
    # print(f"PDF documents directory: {pdf_docs_dir}")
    #
    # vector_db = VectorDB("resume_vectorstore")  # Using default vector database
    # vector_db.add_pdf_to_collection(directory=pdf_docs_dir, collection_name=COLLECTION_NAME)
    # # Retrieve collection with same name
    # collection = vector_db.get_or_create_collection(collection_name=COLLECTION_NAME)
    # print(f"Retrieved collection: {collection.name}")

    # Adding text document as well to an example collection
    text_docs_dir = Path(__file__).parent.parent / "data"
    print(f"Text documents directory: {text_docs_dir}")

    vector_db_sample = VectorDB("sample_vectorstore")
    vector_db_sample.add_texts_to_collection(directory=text_docs_dir, collection_name="sample_texts")

    # Retrieve collection with same name
    collection = vector_db_sample.get_or_create_collection(collection_name="sample_texts")
    print(f"Retrieved collection: {collection.name}")
