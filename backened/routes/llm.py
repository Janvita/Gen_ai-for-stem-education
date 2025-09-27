from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

router = APIRouter()

class LLMRequest(BaseModel):
    content: str

def generate_info_from_llm(text: str) -> str:
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
    try:
        info = generate_info_from_llm(request.content)
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
