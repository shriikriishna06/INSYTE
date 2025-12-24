import json
import re
from typing import Tuple, Dict, Any
def validate_json(output: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Extracts and validates the first JSON object found in the model output.
    This is robust against extra text or markdown.
    """
    if not output:
        return False, {}
    try:
        # Find first JSON block
        match = re.search(r"\{[\s\S]*\}", output)
        if not match:
            return False, {}

        parsed = json.loads(match.group())
        return True, parsed

    except Exception:
        return False, {}
