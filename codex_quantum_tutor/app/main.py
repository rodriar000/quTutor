from fastapi import FastAPI, HTTPException
 feature/Respuesta-explicativa
from fastapi.middleware.cors import CORSMiddleware

 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex
from fastapi.middleware.cors import CORSMiddleware

 kczlam-codex/crear-proyecto-python-con-fastapi-y-codex
from fastapi.middleware.cors import CORSMiddleware

main
 main
 main
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

 feature/Respuesta-explicativa

j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex

 kczlam-codex/crear-proyecto-python-con-fastapi-y-codex
 main
 main
# Allow requests from any origin so the HTML file can be opened locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

 feature/Respuesta-explicativa
LEVEL_MSG = {
    "beginner": "Responde con explicaciones sencillas y paso a paso.",
    "intermediate": "Asume conocimientos básicos de computación cuántica.",
    "advanced": "Utiliza terminología técnica y da detalles avanzados.",
}


 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex

 main
  main
 main
class Prompt(BaseModel):
    prompt: str
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

@app.post("/generate")
async def generate_code(data: Prompt):
    try:
 feature/Respuesta-explicativa
        instruction = LEVEL_MSG.get(data.level, "")

 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex

 main
        # Try GPT-4 via chat completion
 main
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
 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex
            code_text = chat_resp.choices[0].message.content.strip()

            text = chat_resp.choices[0].message.content
 main
        except Exception:
            resp = openai.Completion.create(
                model="code-davinci-002",
                prompt=f"{instruction}\n{data.prompt}",
                max_tokens=400,
                temperature=0.3,
            )
 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex
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

            text = resp.choices[0].text
        return {"code": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 main
