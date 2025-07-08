from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.6))  # default if missing
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))
# "deepseek-r1-distill-llama-70b"



from flask import Blueprint

voiceBlueprint = Blueprint('voiceBlueprint', __name__)

from VoiceAssistance import routes

