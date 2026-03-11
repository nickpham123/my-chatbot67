from flask import Flask, render_template, request, jsonify
from helper import download_hugging_face_embedding
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from prompt import *
import os

app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

embedding = download_hugging_face_embedding()

index_name = "my-chatbot67"

docsearch = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3} )
chatModel = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["GET", "POST"])
def chat():
    msg = request.json["message"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Retrieved chunks:")
    for doc in response.get("context", []):
        print("---", doc.page_content[:200])
    print("Response: ", response["answer"])
    return jsonify({"response": response["answer"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug= True)