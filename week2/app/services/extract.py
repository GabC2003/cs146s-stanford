from ..config import settings

import re
import json
from typing import List
from ollama import chat


BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str) -> List[str]:
    """
    LLM-powered extraction using Ollama and llama3.1:8b.
    Uses structured JSON output to ensure reliable parsing.
    """
    if not text.strip():
        return []

    # Define the expected JSON schema for structured output
    schema = {
        "type": "object",
        "properties": {
            "action_items": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["action_items"]
    }

    try:
        response = chat(
            model=settings.LLM_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a task management assistant. Extract a list of actionable items, tasks, or commitments from the provided text. Return ONLY a JSON object.'
                },
                {
                    'role': 'user',
                    'content': f'Extract action items from this text:\n\n{text}'
                }
            ],
            format=schema  # Enforcement of structured output
        )
        
        # Parse the JSON response
        result = json.loads(response.message.content)
        extracted = result.get("action_items", [])
        
        # Simple cleanup: strip results and remove any empty strings
        return [item.strip() for item in extracted if item.strip()]
        
    except Exception as e:
        print(f"Error during LLM extraction: {e}")
        # Optionally fall back to the heuristic version or return an empty list
        return []
