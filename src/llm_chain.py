from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from src.config import settings
from src.tools import all_tools
from src.prompts.prompt_loader import load_prompt

llm = ChatGoogleGenerativeAI(
    model=settings.model_name,
    api_key=settings.gemini_api_key,
)

agent = create_agent(
    model=llm,
    tools=all_tools,
)

system_message = SystemMessage(load_prompt("system"))
