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

class RefinementAgent(AbstractAgent):

    def __init__(self):
        super().__init__()

        self.initial_writer_agent = Agent(
            name="InitialWriterAgent",
            model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
            instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
            Output only the story text, with no introduction or explanation.""",
            output_key="current_story",  # Stores the first draft in the state.
        )

        self.critic_agent = Agent(
            name="CriticAgent",
            model=Gemini(model="gemini-2.5-flash-lite",retry_options=retry_config),
            instruction="""You are a constructive story critic. Review the story provided below.
            Story: {current_story}
            
            Evaluate the story's plot, characters, and pacing.
            - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
            - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
            output_key="critique",  # Stores the feedback in the state.
        )

        self.refinement_agent = Agent(
            
        )



