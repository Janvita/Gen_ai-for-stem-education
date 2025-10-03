"""
llm.py

This module defines a FastAPI router for interacting with a Large Language Model (LLM) 
using the Groq API. 

Key functionalities:
- Accept user-provided text.
- Query an LLM (LLaMA-3.1-8b-instant) via Groq.
- Return a simplified explanation of the input text in less than 100 words.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client with API key
client = Groq(api_key=api_key)

# Initialize FastAPI router for LLM endpoints
router = APIRouter()


class LLMRequest(BaseModel):
    """
    Request model for generating simplified information from text.

    Fields:
        - content (str): The raw text content provided by the user.
    """
    content: str


def generate_info_from_llm(text: str) -> str:
    """
    Sends the given text to the Groq LLM (LLaMA-3.1-8b-instant) and requests a 
    simplified explanation.

    Steps:
    1. Create a chat completion request with the model.
    2. Prompt the LLM to explain the input text in simple terms (under 100 words).
    3. Extract and return the model's response as a string.

    Args:
        text (str): The text to be explained.

    Returns:
        str: Simplified explanation of the input text.
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Explain in simple terms the meaning of the content {text} in less than 100 words"
            }
        ]
    )
    return completion.choices[0].message.content.strip()


@router.post("/generate_info")
async def generate_info_endpoint(request: LLMRequest):
    """
    FastAPI endpoint to generate simplified information from user text.

    Steps:
    1. Accept a POST request with JSON containing `content`.
    2. Pass the content to the `generate_info_from_llm` function.
    3. Return the simplified explanation in JSON format.
    """
    try:
        info = generate_info_from_llm(request.content)
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
