import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # or GROQ_API_KEY

# Hosts
JSEARCH_API_HOST = "jsearch.p.rapidapi.com"