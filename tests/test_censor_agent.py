import unittest

# two lines to help Python find the parent directory's modules
import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fix for asyncio errors on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from data_models import Transcript, Word
from agents.censor_agent import find_swear_words


class TestCensorAgent(unittest.TestCase):
    """
    Unit tests for the CensorAgent's find_swear_words function.
    """

    def test_profanity_present(self):
        """
        Test Case 1: Verifies that the agent correctly identifies and returns profane words.
        """
        print("\n--- Running Test Case 1: Profanity Present ---")
        # Create a sample transcript containing known curse words
        transcript_with_profanity = Transcript(words=[
            Word(word="This", start_time=0.1, end_time=0.4),
            Word(word="is", start_time=0.5, end_time=0.7),
            Word(word="a", start_time=0.8, end_time=0.9),
            Word(word="bitch", start_time=1.0, end_time=1.5),
            Word(word="sentence", start_time=1.6, end_time=2.2),
            Word(word="with", start_time=2.3, end_time=2.6),
            Word(word="fuck", start_time=2.7, end_time=3.1),
            Word(word="in", start_time=3.2, end_time=3.4),
            Word(word="it", start_time=3.5, end_time=3.6)
        ])
        
        # Call the function to find swear words
        identified_words = find_swear_words(transcript_with_profanity)
        
        # Define the expected output
        expected_words = [
            Word(word="bitch", start_time=1.0, end_time=1.5),
            Word(word="fuck", start_time=2.7, end_time=3.1)
        ]
        
        print(f"Input Transcript: {transcript_with_profanity.model_dump_json(indent=2)}")
        print(f"Agent Output: {[word.model_dump() for word in identified_words]}")
        print(f"Expected Output: {[word.model_dump() for word in expected_words]}")
        
        # Assert that the identified words match the expected words
        self.assertIsInstance(identified_words, list)
        self.assertEqual(len(identified_words), 2)
        # Convert to dicts for easier comparison, as Pydantic models are objects
        self.assertEqual([word.model_dump() for word in identified_words], [word.model_dump() for word in expected_words])
        print("--- Test Case 1: Passed ---")


    def test_no_profanity(self):
        """
        Test Case 2: Verifies that the agent returns an empty list for a clean transcript.
        """
        print("\n--- Running Test Case 2: No Profanity ---")
        # Create a sample transcript with clean language
        transcript_clean = Transcript(words=[
            Word(word="This", start_time=0.1, end_time=0.4),
            Word(word="is", start_time=0.5, end_time=0.7),
            Word(word="a", start_time=0.8, end_time=0.9),
            Word(word="perfectly", start_time=1.0, end_time=1.5),
            Word(word="normal", start_time=1.6, end_time=2.2),
            Word(word="sentence", start_time=2.3, end_time=2.9)
        ])

        # Call the function
        identified_words = find_swear_words(transcript_clean)

        print(f"Input Transcript: {transcript_clean.model_dump_json(indent=2)}")
        print(f"Agent Output: {identified_words}")
        print("Expected Output: []")

        # Assert that the function returns an empty list
        self.assertIsInstance(identified_words, list)
        self.assertEqual(len(identified_words), 0)
        print("--- Test Case 2: Passed ---")

    def test_edge_case_similar_words(self):
        """
        Test Case 3: Verifies that the agent does not flag words that only sound like profanity.
        """
        print("\n--- Running Test Case 3: Edge Cases ---")
        # Create a transcript with words that are not profanity but could be tricky
        transcript_edge_case = Transcript(words=[
            Word(word="The", start_time=0.1, end_time=0.3),
            Word(word="ship", start_time=0.4, end_time=0.8),
            Word(word="sailed", start_time=0.9, end_time=1.4),
            Word(word="to", start_time=1.5, end_time=1.6),
            Word(word="the", start_time=1.7, end_time=1.8),
            Word(word="dam", start_time=1.9, end_time=2.3)
        ])

        # Call the function
        identified_words = find_swear_words(transcript_edge_case)

        print(f"Input Transcript: {transcript_edge_case.model_dump_json(indent=2)}")
        print(f"Agent Output: {identified_words}")
        print("Expected Output: []")
        
        # Assert that the function returns an empty list
        self.assertIsInstance(identified_words, list)
        self.assertEqual(len(identified_words), 0)
        print("--- Test Case 3: Passed ---")


if __name__ == '__main__':
    unittest.main()