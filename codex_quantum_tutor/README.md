# Codex Quantum Tutor

API sencilla basada en FastAPI que usa OpenAI Codex o GPT-4 para generar código a partir de prompts.

## Instalación

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` con tu clave de OpenAI:

```
OPENAI_API_KEY=tu_clave
```

## Uso

Iniciar la aplicación con:

```bash
uvicorn app.main:app --reload
```

Enviar un POST a `/generate` con un JSON que contenga el campo `prompt`.

Ejemplo usando `curl`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @test_prompt.json
```
