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

feature/Respuesta-explicativa
Enviar un POST a `/generate` con un JSON que contenga los campos `prompt` y
`level`. El nivel puede ser `beginner`, `intermediate` o `advanced`.

Enviar un POST a `/generate` con un JSON que contenga el campo `prompt`.
 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex
La respuesta incluirá el código generado y una explicación línea por línea.
 main
 main

Ejemplo usando `curl`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @test_prompt.json
```
 feature/Respuesta-explicativa

 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex

 kczlam-codex/crear-proyecto-python-con-fastapi-y-codex
 main

 main
## Interfaz web

Con el backend en marcha puedes abrir `frontend/index.html` en tu navegador.
 j3ihug-codex/crear-proyecto-python-con-fastapi-y-codex
Allí podrás introducir un prompt y ver el código generado junto con su explicación.

Allí podrás introducir un prompt y ver el código generado directamente.
 feature/Respuesta-explicativa

main
main
 main
