import json
from typing import Any

def to_json(obj: Any) -> str:
    return json.dumps(obj)

def from_json(s: str) -> Any:
    return json.loads(s)
