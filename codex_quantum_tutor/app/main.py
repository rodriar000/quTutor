from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
import openai
from dotenv import load_dotenv
import os
import html

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

openai.api_key = api_key

app = FastAPI(title="Codex Quantum Tutor")
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

def sanitize_text(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("<<<<<<<") or stripped.startswith(">>>>>>>"):
            lines.append("# Línea conflictiva filtrada")
        else:
            lines.append(line)
    sanitized = "\n".join(lines)
    sanitized = sanitized.replace("<<<<<", "&lt;&lt;&lt;&lt;&lt;")
    sanitized = sanitized.replace(">>>>>", "&gt;&gt;&gt;&gt;&gt;")
    return sanitized

@app.post("/generate")
async def generate_code(data: Prompt):
    try:
        instruction = LEVEL_MSG.get(data.level, "")
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
            code_text = chat_resp.choices[0].message.content.strip()
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=f"{instruction}\n{data.prompt}",
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
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {e}")

    sanitized_code = html.escape(sanitize_text(code_text))
    sanitized_explanation = html.escape(sanitize_text(explanation_text))
    return {"code": sanitized_code, "explanation": sanitized_explanation}
