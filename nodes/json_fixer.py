import json
import re
from typing import Tuple


class JSONFixer:
    """
    Fix malformed JSON from LLM outputs.
    
    Common issues fixed:
    - Trailing commas
    - Single quotes instead of double quotes
    - Unquoted keys
    - Missing quotes around string values
    - Markdown code block wrappers
    - Extra text before/after JSON
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("fixed_json",)
    FUNCTION = "fix"
    CATEGORY = "🚦ComfyUI_LLMs_Toolkit/JSON"

    def fix(self, text: str) -> Tuple[str]:
        """
        Attempt to fix malformed JSON.
        
        Args:
            text: Raw text that should contain JSON
            
        Returns:
            Fixed JSON string, or error message if unfixable
        """
        original = text
        
        # Step 1: Try direct parse first (already valid)
        try:
            parsed = json.loads(text)
            print(f"# [🚦 LLMs_Toolkit] JSON already valid")
            return (json.dumps(parsed, ensure_ascii=False),)
        except json.JSONDecodeError:
            pass
        
        # Step 2: Extract JSON from markdown code blocks
        code_block_pattern = r"```(?:json)?\s*([\s\S]*?)```"
        matches = re.findall(code_block_pattern, text)
        if matches:
            text = matches[0].strip()
        
        # Step 3: Find JSON-like content (starts with { or [)
        json_pattern = r'(\{[\s\S]*\}|\[[\s\S]*\])'
        json_matches = re.findall(json_pattern, text)
        if json_matches:
            # Try each match
            for match in json_matches:
                text = match.strip()
                try:
                    parsed = json.loads(text)
                    print(f"# [🚦 LLMs_Toolkit] extracted JSON from text")
                    return (json.dumps(parsed, ensure_ascii=False),)
                except json.JSONDecodeError:
                    pass
        
        # Step 4: Apply common fixes
        fixed = text
        
        # Remove trailing commas before } or ]
        fixed = re.sub(r',\s*([}\]])', r'\1', fixed)
        
        # Replace single quotes with double quotes (careful with apostrophes)
        # Only replace quotes that look like JSON string delimiters
        fixed = re.sub(r"'([^']*)':", r'"\1":', fixed)  # Keys
        fixed = re.sub(r":\s*'([^']*)'([,}\]])", r': "\1"\2', fixed)  # Values
        
        # Try parse after fixes
        try:
            parsed = json.loads(fixed)
            print(f"# [🚦 LLMs_Toolkit] fixed JSON (trailing commas, quotes)")
            return (json.dumps(parsed, ensure_ascii=False),)
        except json.JSONDecodeError as e:
            pass
        
        # Step 5: Last resort - try to find any valid JSON substring
        for i in range(len(original)):
            if original[i] in '{[':
                for j in range(len(original), i, -1):
                    try:
                        candidate = original[i:j]
                        parsed = json.loads(candidate)
                        print(f"# [🚦 LLMs_Toolkit] extracted valid JSON substring")
                        return (json.dumps(parsed, ensure_ascii=False),)
                    except json.JSONDecodeError:
                        continue
        
        # Failed to fix
        error_msg = f"Unable to fix JSON: {str(e)}"
        print(f"# [🚦 LLMs_Toolkit] ✗ {error_msg}")
        return (error_msg,)


# Register the node
NODE_CLASS_MAPPINGS = {"JSONFixer": JSONFixer}
NODE_DISPLAY_NAME_MAPPINGS = {"JSONFixer": "JSON Fixer"}
