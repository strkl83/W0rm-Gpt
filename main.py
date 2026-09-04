#!/usr/bin/env python3
"""Safe, small W0rm-GPT command-line client.

The original repository delegated execution to an opaque compiled extension and
included an updater that downloaded and executed remote code. This replacement
keeps the useful chat workflow while making all network behavior explicit:

  - no compiled extension is imported
  - no files are deleted or replaced
  - the only optional network call is an OpenAI-compatible chat completion
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. Be accurate about uncertainty, respect privacy, "
    "and do not help with wrongdoing, credential theft, evasion, or unauthorized access."
)


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    base_url: str
    model: str
    system_prompt: str
    timeout: float = 60.0

    @classmethod
    def from_environment(cls, args: argparse.Namespace) -> "Settings":
        base_url = args.base_url or os.getenv("OPENAI_API_BASE", DEFAULT_BASE_URL)
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=base_url.rstrip("/"),
            model=args.model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
            system_prompt=os.getenv("W0RM_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT),
        )


class ApiError(RuntimeError):
    """A readable error from an OpenAI-compatible API."""


class OpenAICompatibleClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.api_key:
            raise ApiError(
                "OPENAI_API_KEY is not configured. Add it to the environment to "
                "enable live responses."
            )
        self.settings = settings

    def complete(self, prompt: str) -> str:
        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": self.settings.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        }
        request = urllib.request.Request(
            f"{self.settings.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.settings.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ApiError(f"API returned HTTP {exc.code}: {detail[:500]}") from exc
        except urllib.error.URLError as exc:
            raise ApiError(f"Could not reach the API: {exc.reason}") from exc
        except TimeoutError as exc:
            raise ApiError("The API request timed out.") from exc

        try:
            data: dict[str, Any] = json.loads(body)
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ApiError("The API returned an unexpected response shape.") from exc
        if not isinstance(content, str) or not content.strip():
            raise ApiError("The API returned an empty response.")
        return content.strip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A safe command-line client for OpenAI-compatible chat APIs."
    )
    parser.add_argument(
        "--once",
        metavar="PROMPT",
        help="send one prompt and exit",
    )
    parser.add_argument(
        "--model",
        help=f"model name (default: $OPENAI_MODEL or {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--base-url",
        help=f"API base URL (default: $OPENAI_API_BASE or {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="check local configuration without making a network request",
    )
    return parser


def print_health(settings: Settings) -> int:
    print("W0rm-GPT safe build")
    print(f"API base: {settings.base_url}")
    print(f"Model: {settings.model}")
    print(f"API key: {'configured' if settings.api_key else 'not configured'}")
    print("Network call: only made when a prompt is submitted with an API key.")
    return 0


def ask(settings: Settings, prompt: str) -> int:
    if not settings.api_key:
        print(
            "No API key is configured, so no network request was made.\n"
            "Set OPENAI_API_KEY and run the command again.\n"
            f"Prompt received: {prompt}"
        )
        return 2
    try:
        print(OpenAICompatibleClient(settings).complete(prompt))
    except ApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


def interactive(settings: Settings) -> int:
    print("W0rm-GPT safe build — type /help for commands, /exit to quit.")
    if not settings.api_key:
        print("Live responses are disabled until OPENAI_API_KEY is configured.")
    while True:
        try:
            prompt = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not prompt:
            continue
        if prompt in {"/exit", "/quit"}:
            return 0
        if prompt == "/help":
            print("Enter a prompt, /health to inspect configuration, or /exit to quit.")
            continue
        if prompt == "/health":
            print_health(settings)
            continue
        ask(settings, prompt)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.from_environment(args)
    if args.health:
        return print_health(settings)
    if args.once is not None:
        return ask(settings, args.once)
    return interactive(settings)


if __name__ == "__main__":
    raise SystemExit(main())