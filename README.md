# Generic_RAG

An early-stage FastAPI backend for the ingestion layer of a retrieval-augmented generation (RAG) application.

**Current status:** this repository implements application configuration and upload validation only. It does not yet parse or store documents, create embeddings, retrieve context, or generate answers.

## Implemented

- `GET /api/v1/` returns the configured application name and version.
- `POST /api/v1/data/upload/{project_id}` accepts a multipart file and returns its metadata and a validation result.
- Pydantic settings load the application name, version, allowed MIME types, and file-size limit from `src/.env`.
- The default configuration accepts `text/plain` and `application/pdf` files up to 10 MiB.

The setting is named `FILE_ALLOWED_EXTENSIONS`, but the implementation checks the supplied **MIME type**, not the filename extension or actual file contents.

## Run locally

Run these commands from the repository root. The setup was smoke-tested with Python 3.10; dependencies are currently unpinned.

```bash
git clone https://github.com/moatasem75291/Generic_RAG.git
cd Generic_RAG
python -m venv .venv
source .venv/bin/activate
python -m pip install -r src/requirements.txt
cp src/.env.example src/.env
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` and copy the configuration with `Copy-Item src/.env.example src/.env`.

Keep the working directory at the repository root so the configured `src/.env` path resolves correctly. Keep local settings out of Git.

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Try the API

Check application information:

```bash
curl http://127.0.0.1:8000/api/v1/
```

Create a small text file and submit it for validation:

```bash
printf 'Example document\n' > sample.txt
curl -X POST http://127.0.0.1:8000/api/v1/data/upload/demo \
  -F 'file=@sample.txt;type=text/plain'
```

Expected response:

```json
{
  "project_id": "demo",
  "filename": "sample.txt",
  "content_type": "text/plain",
  "is_valid": true
}
```

The upload endpoint does **not** persist the file. `project_id` is echoed in the response; it does not currently create a project or storage namespace. Invalid MIME types and oversized uploads return HTTP 200 with `is_valid: false`, rather than an HTTP error status.

## Configuration

Edit `src/.env` after copying the example:

| Setting | Purpose | Example value |
| --- | --- | --- |
| `APP_NAME` | Application name | `Generic_RAG` |
| `APP_VERSION` | Application version | `0.1` |
| `FILE_ALLOWED_EXTENSIONS` | JSON list of accepted MIME types | `["text/plain", "application/pdf"]` |
| `MAX_FILE_SIZE_MB` | Maximum size, calculated in 1,024² bytes | `10` |

## Structure

```text
src/
  main.py                       FastAPI app, middleware, router registration
  routes/base.py                Application information endpoint
  routes/data.py                Upload-validation endpoint
  controllers/BaseController.py Shared configuration access
  controllers/DataController.py MIME-type and size checks
  helpers/config.py             Pydantic settings
  .env.example                  Local configuration template
  requirements.txt              Runtime dependencies
```

## Checks and evaluation

A local smoke check of the current code using FastAPI's test client confirmed:

| Input | Observed result |
| --- | --- |
| Application information request | HTTP 200 with configured name and version |
| Small upload declared as `text/plain` | `is_valid: true` |
| Small upload declared as `application/pdf` | `is_valid: true` |
| Upload declared as `image/png` | `is_valid: false` |
| Text upload larger than 10 MiB | `is_valid: false` |

These checks cover the current validation behavior, not document correctness, security under load, or an end-to-end RAG pipeline. No automated test suite or retrieval/answer-quality benchmark is committed in this repository. There are no RAG quality scores to report yet.

For future RAG evaluation, add a versioned question-and-source dataset, test retrieval recall, check answer support against the retrieved passages, and measure latency. Those are proposed next steps, not implemented capabilities.

## Limits and next steps

- File validation trusts client-supplied MIME metadata. A file declared as PDF can pass without being a valid PDF.
- The size check reads the entire file into memory before comparing it with the limit. It is not an ingress memory limit.
- No document parsing, persistence, chunking, embeddings, vector database, retrieval, or LLM integration is implemented.
- There is no authentication, authorization, rate limiting, or per-project isolation.
- CORS is broadly configured. Review it before any deployment beyond local development.
- Dependencies are not locked, and deployment behavior has not been validated.

Use this as a local development scaffold, not a production document service. A sensible next milestone is tested document persistence and parsing, followed by a small retrieval baseline with measured results.
