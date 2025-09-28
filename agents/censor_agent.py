import json
import asyncio
import os
from typing import List

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService

from data_models import Transcript, Word

# --- API Key ---
os.environ["GEMINI_API_KEY"] = "AIzaSyDDgzNb_dHv3J-d7eIIA8sqIsVNWFZm5lg"

# Censor Agent Prompt
CENSOR_AGENT_INSTRUCTION = """
You are a precise and automated content moderation agent. Your task is to identify profane words from a structured transcript and return ONLY the identified words in the same structured format.

The user will provide a JSON string representing a transcript. This string is an array of objects, where each object has "word", "start_time", and "end_time" keys.

Your sole responsibility is to analyze the "word" fields and identify common English curse words, slurs, or severe profanity.

Your output MUST be a valid JSON array containing the word objects for ONLY the profane words you identify. If no profane words are found, you MUST return an empty JSON array: `[]`.

Do not include any explanations, apologies, or any text whatsoever outside of the final JSON array.

Never wrap your response in markdown code fences.

Example Input:
[{"word": "Well", "start_time": 0.2, "end_time": 0.5}, {"word": "fuck", "start_time": 0.6, "end_time": 1.1}, {"word": "that", "start_time": 1.2, "end_time": 1.5}, {"word": "is", "start_time": 1.5, "end_time": 1.7}, {"word": "one", "start_time": 1.8, "end_time": 2.1}, {"word": "shitty", "start_time": 2.2, "end_time": 2.9}, {"word": "sentence", "start_time": 3.0, "end_time": 3.6}]

Example Output:
[{"word": "fuck", "start_time": 0.6, "end_time": 1.1}, {"word": "shitty", "start_time": 2.2, "end_time": 2.9}]
"""

# Define a agent to find curse words
censor_agent = LlmAgent(
    name="CensorAgent",
    model="gemini-2.0-flash",
    instruction=CENSOR_AGENT_INSTRUCTION,
)


def find_swear_words(transcript: Transcript) -> List[Word]:
    """
    Identifies swear words in a transcript using the CensorAgent.

    This function encapsulates the logic for running the agent, including
    serializing the input, invoking the agent via the ADK Runner, and
    deserializing the output.

    Args:
        transcript: A Transcript object containing a list of words.

    Returns:
        A list of Word objects corresponding to the identified swear words.
        Returns an empty list if no swear words are found or if an error occurs.
    """
    transcript_json = transcript.model_dump_json()

    async def _run_agent_async(transcript_data: str) -> str:
        """Helper to run the agent asynchronously."""

        # Create the session service that will store our conversation sessions
        session_service = InMemorySessionService()

        # EXPLICITLY CREATE THE SESSION BEFORE USING IT
        session = await session_service.create_session(user_id="censor_user", app_name="CensorApp")
        runner = Runner(
            app_name="CensorApp",
            agent=censor_agent,
            session_service=session_service
        )
        # This gets the whole stream of events / updates from the agent
        events = runner.run_async(
            user_id="censor_user",
            session_id=session.id,
            new_message=types.Content(parts=[types.Part(text=transcript_data)])
        )
        # This loop watches the stream for each new update as it arrives.
        async for event in events:
            if event.is_final_response():
                # Grab the final response text when it's ready
                return event.content.parts[0].text.strip()
        return "[]"  # Return empty JSON array if no response

    try:
        # Run the async helper in a synchronous context
        response_json = asyncio.run(_run_agent_async(transcript_json))

        # The agent is instructed to never use markdown, but just in case, strip code fences
        if response_json.startswith("```json"):
            response_json = response_json.strip("```json\n").strip("```")
        
        # The response should be a clean JSON string
        swear_words_data = json.loads(response_json)
        
        # Parse the list of dictionaries into a list of Word objects
        identified_words = [Word(**word_data) for word_data in swear_words_data]
        return identified_words

    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the CensorAgent's response. Response was: {response_json}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

