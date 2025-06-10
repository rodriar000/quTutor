# Codex Quantum Tutor

API sencilla basada en FastAPI que usa OpenAI Codex o GPT-4 para generar código a partir de prompts.

## Instalación

```bash
pip install -r requirements.txt
```

Crea un archivo `.env` con tu clave de OpenAI:

```
OPENAI_API_KEY=tu_clave
```

## Uso

Inicia la aplicación con:

```bash
uvicorn app.main:app --reload
```

Envía un POST a `/generate` con un JSON que contenga los campos `prompt` y `level`.
El nivel puede ser `beginner`, `intermediate` o `advanced`.
La respuesta incluirá el código generado y una explicación línea por línea.

Ejemplo usando `curl`:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @test_prompt.json
```

## Interfaz web

Con el backend en marcha puedes abrir `frontend/index.html` en tu navegador.
Allí podrás introducir un prompt y ver el código generado junto con su explicación.

## Sanitización automática

Sanitización de símbolos conflictivos activada automáticamente para evitar errores de visualización o conflictos de merge.
