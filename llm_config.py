# src/llm_config.py

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Claude 3 via OpenRouter（你也可以换成 gpt-4 等）
shared_llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0.7
)