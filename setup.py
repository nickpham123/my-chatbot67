from setuptools import find_packages, setup

setup(
    name="my_chatbot67",
    version="0.1.0",
    author="Nick Pham",
    author_email="chihungpham123@gmail.com",
    packages=find_packages(),
    install_requires=[
        flask==3.1.1
        python-dotenv==1.1.0
        gunicorn==23.0.0
        langchain==0.3.28
        langchain-openai==0.3.24
        langchain-community==0.3.31
        langchain-pinecone==0.2.8
        pinecone-client==5.0.1
        sentence-transformers==3.3.1
        supabase==2.11.0
        pytest==8.3.4
        pytest-cov==6.0.0
        pypdf==5.6.1
        tiktoken==0.8.0
    ]
)