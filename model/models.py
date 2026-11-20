from langchain.chat_models import init_chat_model
from config import GEMINI_MODEL,MODEL_PROVIDER
from dotenv import load_dotenv

#load env variabless
load_dotenv()

def get_chat_model():
    """Returns gemini chat model"""
    gemini_model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER)
    return gemini_model