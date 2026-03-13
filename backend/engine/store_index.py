from dotenv import load_dotenv
import os
import time
import torch
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from backend.utils.helper import load_pdf_files, filter_to_minimal_docs, text_split



load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_files(data="data/")
minimal_docs = filter_to_minimal_docs(extracted_data)
texts_chunk = text_split(minimal_docs)

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
)

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "my-chatbot67"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,  # all-MiniLM-L6-v2 dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Set this to the batch number you want to resume from (1-indexed)
start_batch = 1  # Change this if resuming after an error

batch_size = 50
start_index = (start_batch - 1) * batch_size

docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)

for i in range(start_index, len(texts_chunk), batch_size):
    batch = texts_chunk[i:i + batch_size]
    docsearch.add_documents(batch)
    print(f"Embedded batch {i // batch_size + 1} ({len(batch)} docs)")

print("Done! All documents embedded.")