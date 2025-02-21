import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("Error: API key is missing. Please check your .env file.")
    exit()

groq_model = ChatGroq(model="llama3-8b-8192", temperature=0.4, groq_api_key=GROQ_API_KEY)
