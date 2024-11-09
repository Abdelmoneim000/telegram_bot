import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("API_TOKEN")

if not api_token:
    raise ValueError("Missing API_TOKEN")
