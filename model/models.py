from langchain.chat_models import init_chat_model
from config import GEMINI_MODEL,MODEL_PROVIDER
from dotenv import load_dotenv

#load env variabless
load_dotenv()

def get_chat_model():
    """Build the Gemini chat model used by all agents."""
    gemini_model=init_chat_model(model=GEMINI_MODEL,model_provider=MODEL_PROVIDER,max_retries=3,timeout=30)
    return gemini_model