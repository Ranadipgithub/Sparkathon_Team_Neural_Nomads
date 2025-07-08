import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

# Load the .env file where your GROQ API key and base URL are stored
load_dotenv()

# Create the LLM client using Groq
llm = ChatOpenAI(
    model="llama3-70b-8192",
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),    # your Groq API key
    temperature=0.7
)
response = llm.predict("Suggest 3 useful Python projects for a college student.")
print(response)
