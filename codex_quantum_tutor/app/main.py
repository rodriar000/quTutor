from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
import openai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

openai.api_key = api_key

app = FastAPI(title="Codex Quantum Tutor")

# Allow requests from any origin so the HTML file can be opened locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LEVEL_MSG = {
    "beginner": "Responde con explicaciones sencillas y paso a paso.",
    "intermediate": "Asume conocimientos básicos de computación cuántica.",
    "advanced": "Utiliza terminología técnica y da detalles avanzados.",
}

class Prompt(BaseModel):
    prompt: str
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

@app.post("/generate")
async def generate_code(data: Prompt):
    try:
        instruction = LEVEL_MSG.get(data.level, "")
        # Try GPT-4 via chat completion
        try:
            chat_resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": data.prompt},
                ],
                max_tokens=400,
                temperature=0.3,
            )
            text = chat_resp.choices[0].message.content
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=f"{instruction}\n{data.prompt}",
                max_tokens=400,
                temperature=0.3,
            )
            text = resp.choices[0].text
        return {"code": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
