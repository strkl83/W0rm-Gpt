# W0rm-GPT safe build

This is a clean, runnable replacement for the original wrapper in the
`W0rm-Gpt` repository.

## What changed

- Removed the dependency on the opaque `main.cpython-311.so` module.
- Removed the download-and-execute updater behavior.
- Added a small CLI with explicit configuration and error handling.
- Added support for OpenAI and OpenAI-compatible chat-completion APIs.
- Added local health checks and tests that do not make network requests.

The program never executes downloaded code and never deletes or replaces local
files.

## Run

Use the project **Run** button, or start it from the Shell:

```bash
python3 main.py --health
python3 main.py
```

To enable live responses, set an API key in the environment. The key is not
stored by this project:

```bash
export OPENAI_API_KEY="your-key"
python3 main.py --once "Explain what this project does."
```

OpenRouter is the default provider. To use another OpenAI-compatible provider:

```bash
export OPENAI_API_BASE="https://provider.example/v1"
export OPENAI_MODEL="provider-model"
python3 main.py
```

## Verify

```bash
python3 -m unittest -v
```

No API key is needed for the health check or tests.