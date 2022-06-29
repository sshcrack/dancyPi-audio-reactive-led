from typing import Any, Optional

required_parsable = ["min", "max", "type", "sug_min", "sug_max"]


class VerifierResult:
    error: Optional[str]
    result: Any
