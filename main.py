import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openrouter import ChatOpenRouter
from langchain_tavily import TavilySearch
from pydantic import SecretStr

load_dotenv()

open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY","")
tavily_api_Key = os.getenv("TAVILY_API_KEY","")


@tool
def triple(x: int) -> int:
    """Returns the triple of a number."""
    return x * 3

tools = [
    TavilySearch(
        tavilyApiKey=tavily_api_Key,
        maxResults=1,
    ),
    triple
]

llm = ChatOpenRouter(
    api_key=SecretStr(open_router_api_key),
    model="liquid/lfm-2.5-24b-a2b",
    temperature=0
).bind_tools(
    tools
)