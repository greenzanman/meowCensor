"""
data structures, 
- ensures the TranscriberAgent, CensorAgent, and AudioSurgeonAgent all communicate good.
"""

from pydantic import BaseModel
from typing import List

class Word(BaseModel):
    """Represents a single word with its timestamp."""
    word: str
    start_time: float
    end_time: float

class Transcript(BaseModel):
    """Represents the full transcript as a list of words."""
    words: List[Word]