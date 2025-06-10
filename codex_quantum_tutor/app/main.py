from fastapi import FastAPI, HTTPException
 kczlam-codex/crear-proyecto-python-con-fastapi-y-codex
from fastapi.middleware.cors import CORSMiddleware

main
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

openai.api_key = api_key

app = FastAPI(title="Codex Quantum Tutor")

 kczlam-codex/crear-proyecto-python-con-fastapi-y-codex
# Allow requests from any origin so the HTML file can be opened locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

 main
class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(data: Prompt):
    try:
        # Try GPT-4 via chat completion
        try:
            chat_resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": data.prompt}],
                max_tokens=400,
                temperature=0.3,
            )
            text = chat_resp.choices[0].message.content
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=data.prompt,
                max_tokens=400,
                temperature=0.3,
            )
            text = resp.choices[0].text
        return {"code": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
