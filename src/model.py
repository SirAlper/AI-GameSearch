from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import MODEL_NAME, TEMPERATURE
from src.tools import ALL_TOOLS

_base_model = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE,


)

model_with_tools = _base_model.bind_tools(ALL_TOOLS)