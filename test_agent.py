import os
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService

# --- API Key ---
# better to set this as an environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyDDgzNb_dHv3J-d7eIIA8sqIsVNWFZm5lg"

# 1. Define a simple agent to find curse words
censor_agent = LlmAgent(
    name="CensorAgent",
    model="gemini-2.0-flash",
    instruction="""You are a censorship agent. The user will provide a sentence.
    Your only job is to identify if the word 'darn' is in the sentence.
    Respond with 'True' if it is, and 'False' if it is not.
    Do not say anything else.""",
)

# 2. Boilerplate to run the agent
async def run_test():
    print("Testing agent...")
    
    # Create the session service that will store our conversation sessions
    session_service = InMemorySessionService()
    
    # EXPLICITLY CREATE THE SESSIONS BEFORE USING THEM
    session_1 = await session_service.create_session(user_id="test_user", app_name="CensorApp")
    session_2 = await session_service.create_session(user_id="test_user", app_name="CensorApp")

    runner = Runner(
        app_name="CensorApp",
        agent=censor_agent,
        session_service=session_service # Pass the service that now holds the sessions
    )
    
    # Test Case 1: Curse word present
    events1 = runner.run_async(
        user_id="test_user",
        session_id=session_1.id, # Use the real ID from the created session
        new_message=types.Content(parts=[types.Part(text="This is a darn sentence.")])
    )
    print("Input: 'This is a bitch sentence.' -> Expected: True")
    async for event in events1:
        if event.is_final_response():
            print(f"Agent Output: {event.content.parts[0].text.strip()}")

    # Test Case 2: No curse word
    events2 = runner.run_async(
        user_id="test_user",
        session_id=session_2.id, # Use the real ID from the created session
        new_message=types.Content(parts=[types.Part(text="This is a clean sentence.")])
    )
    print("\nInput: 'This is a clean sentence.' -> Expected: False")
    async for event in events2:
        if event.is_final_response():
            print(f"Agent Output: {event.content.parts[0].text.strip()}")

# 3. Run the test
if __name__ == "__main__":
    asyncio.run(run_test())
