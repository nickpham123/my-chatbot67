import os
from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

# Local imports
from backend.core.system_prompt import system_prompt, rewrite_prompt

app = Flask(
    __name__,
    template_folder="../../frontend/templates",
    static_folder="../../frontend/static"
)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# --- Components initialized lazily ---
retriever = None
answer_chain = None
rewrite_llm = None

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", rewrite_prompt),
    ("human", "{input}")
])


def init_components():
    """Initialize retriever, answer chain, and rewrite LLM."""
    global retriever, answer_chain, rewrite_llm

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docsearch = PineconeVectorStore.from_existing_index(index_name="my-chatbot67", embedding=embedding)
    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

    # Use the same model for rewriting (lightweight call)
    rewrite_llm = chat_model

    answer_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    answer_chain = create_stuff_documents_chain(chat_model, answer_prompt)


def rewrite_query(original_query: str) -> str:
    """Use Gemini to rewrite the user's question into a better search query."""
    # Skip rewriting for short, clear queries
    if len(original_query.split()) <= 5:
        print(f"[Query Rewrite] Skipped (short query): '{original_query}'")
        return original_query

    result = rewrite_llm.invoke(REWRITE_PROMPT.format_messages(input=original_query))
    rewritten = result.content.strip()
    print(f"[Query Rewrite] '{original_query}' -> '{rewritten}'")
    return rewritten


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/ask", methods=["GET", "POST"])
def chat():
    global retriever, answer_chain, rewrite_llm
    if retriever is None:
        init_components()

    original_msg = request.json["message"]

    # Step 1: Rewrite the query for better retrieval
    search_query = rewrite_query(original_msg)

    # Step 2: Retrieve documents using the rewritten query
    docs = retriever.invoke(search_query)

    # Log retrieved documents for debugging
    print(f"\n[Retrieved {len(docs)} documents]")
    for i, doc in enumerate(docs):
        preview = doc.page_content[:150].replace('\n', ' ')
        print(f"  Doc {i+1}: {preview}...")

    # Step 3: Generate answer using the ORIGINAL question + retrieved docs
    response = answer_chain.invoke({"input": original_msg, "context": docs})

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
