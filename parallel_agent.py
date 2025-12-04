import os
from dotenv import load_dotenv
import asyncio
import google
import warnings
import logging

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from abstract_agent import AbstractAgent

from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

console = Console()

warnings.simplefilter("ignore")
logging.basicConfig(level=logging.CRITICAL)

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError('API key was not found')
print('API key loaded')


retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)