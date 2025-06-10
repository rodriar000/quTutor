from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Allow requests from any origin so the HTML file can be opened locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_code(data: Prompt):
    try:
        try:
            chat_resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": data.prompt}],
                max_tokens=400,
                temperature=0.3,
            )
            code_text = chat_resp.choices[0].message.content.strip()
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=data.prompt,
                max_tokens=400,
                temperature=0.3,
            )
            code_text = resp.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {e}")

    explanation_prompt = (
        "Explica línea por línea el siguiente código en lenguaje natural, "
        "como si enseñaras a un estudiante de computación cuántica:\n\n"
        f"```python\n{code_text}\n```"
    )

    try:
        try:
            chat_resp = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": explanation_prompt}],
                max_tokens=400,
                temperature=0.3,
            )
            explanation_text = chat_resp.choices[0].message.content.strip()
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=explanation_prompt,
                max_tokens=400,
                temperature=0.3,
            )
            explanation_text = resp.choices[0].text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating explanation: {e}"
        )

    return {"code": code_text, "explanation": explanation_text}
