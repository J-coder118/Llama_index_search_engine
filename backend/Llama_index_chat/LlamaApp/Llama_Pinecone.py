#########################  1
from pathlib import Path
from llama_index.storage.storage_context import StorageContext
from llama_index import download_loader
import pinecone
from llama_index.indices.composability.graph import ComposableGraph
from urllib.request import urlopen
import openai
from pathlib import Path
from llama_index import download_loader
from llama_index import (
    VectorStoreIndex,
    GPTSimpleKeywordTableIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
)
from llama_index.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.vector_stores import PineconeVectorStore
from llama_index import (
    StorageContext,
    ServiceContext,
    GPTVectorStoreIndex,
    LLMPredictor,
    PromptHelper,
    SimpleDirectoryReader,
    load_index_from_storage,
)
from langchain.llms.openai import OpenAIChat
import pinecone
from llama_index.node_parser import SimpleNodeParser
from langchain.chat_models import ChatOpenAI
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.indices.composability.graph import ComposableGraph

import json
from .models import Pinecone_indice


openai.api_key = "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"
index_name = "nalc20192023a"

pinecone.init(api_key="a79d363d-0ad1-4b22-a6f4-eacaa0d3a66e", environment="gcp-starter")

index = None
stored_docs = {}
docstore = SimpleDocumentStore.from_persist_dir(persist_dir=f"index_PDF.json")
index_store = SimpleIndexStore.from_persist_dir(persist_dir=f"index_PDF.json")
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])

PDFReader = download_loader("PDFReader")
loader = PDFReader()


def initialize_index(namespace):
    print("start to initialize index")
    """Create a new global index, or load one from the pre-set path."""
    global index, stored_docs, docstore, index_store

    llm_predictor = LLMPredictor(
        # llm=OpenAIChat(temperature=0, model_name="gpt-4")
        llm=OpenAIChat(
            temperature=0,
            model_name="gpt-3.5-turbo",
            openai_api_key="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",
            streaming=True,
        )
    )

    service_context = ServiceContext.from_defaults(
        chunk_size_limit=512,
        llm_predictor=llm_predictor,
        callback_manager=callback_manager,
    )

    vector_store = PineconeVectorStore(
        index_name=index_name,
        environment="gcp-starter",
        metadata_filters=str(namespace),
        api_key="a79d363d-0ad1-4b22-a6f4-eacaa0d3a66e",
    )
    
    storage_context = StorageContext.from_defaults(
        docstore=docstore, index_store=index_store, vector_store=vector_store
    )
    index = VectorStoreIndex.from_documents(
        [], storage_context=storage_context, service_context=service_context
    )
    print("index initialized")


def uploading_to_pinecone(PDF_file_path, pdf_name):
    global index, stored_docs, docstore  # , index_store
    initialize_index(pdf_name)
    document = loader.load_data(file=PDF_file_path)[0]

    # create parser and parse document into nodes
    parser = SimpleNodeParser.from_defaults()
    nodes = parser.get_nodes_from_documents([document])
    docstore.add_documents(nodes)
    print("documentkdkdkdkdk")

    if pdf_name is not None:
        document_data = document.to_dict()
        document_data["pdf_name"] = pdf_name
    print("before insert...")
    index.insert(document)

    stored_docs[document_data["pdf_name"]] = document.text[0:200]

    pineconeDB = Pinecone_indice()
    pineconeDB.path = PDF_file_path
    pineconeDB.pinecone_title = pdf_name
    pineconeDB.save()
    return


def get_DocumentList():
    """Get the list of currently stored documents."""
    global stored_docs
    documents_list = []
    for pdf_name, pdf_text in stored_docs.items():
        documents_list.append({"id": pdf_name, "text": pdf_text})
    return documents_list


def chat(query_text, query_pdf_name):
    global index, stored_docs, docstore, index_store

    initialize_index(query_pdf_name)

    response = index.as_query_engine().query(query_text)
    return response
