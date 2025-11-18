import json
from typing import Dict, Any, Optional, List
from jsonschema import validate as jsonschema_validate, ValidationError as JSONSchemaValidationError

SENSITIVE_KEYWORDS = [
    "hack", "exploit", "bypass", "malware", "injection",
    "attack", "phishing", "illegal", "bomb", "terror", "kill"
]

class LLMValidator:
    def __init__(self, llm_client, max_length: int = 2500):
        self.llm = llm_client
        self.max_length = max_length

    def _try_json(self, text: str) -> Optional[Any]:
        try:
            return json.loads(text)
        except Exception:
            return None

    def _validate_schema(self, data: Any, schema: Dict) -> Optional[str]:
        try:
            jsonschema_validate(instance=data, schema=schema)
            return None
        except JSONSchemaValidationError as e:
            return str(e)

    def _scan_safety(self, text: str) -> List[str]:
        issues = []
        lower = text.lower()
        for word in SENSITIVE_KEYWORDS:
            if word in lower:
                issues.append(word)
        return issues

    def validate_response(
        self,
        response_text: str,
        *,
        expected_schema: Optional[Dict] = None,
        instruction: Optional[str] = None,
        require_json: bool = False,
        run_llm_check: bool = True
    ) -> Dict[str, Any]:

        report = {
            "status": "pass",
            "scores": {"format": 1.0, "instruction_fidelity": 1.0, "safety": 1.0},
            "issues": [],
            "suggestions": [],
            "parsed": None,
            "llm_feedback": None
        }

        if len(response_text) > self.max_length:
            report["issues"].append(f"Response too long ({len(response_text)} chars)")
            report["scores"]["format"] -= 0.3
            report["status"] = "warn"

        if response_text.strip().endswith("..."):
            report["issues"].append("Possible truncation detected")
            report["scores"]["format"] -= 0.2

        parsed = None
        if require_json or expected_schema:
            parsed = self._try_json(response_text)
            if not parsed:
                report["issues"].append("Not valid JSON")
                report["scores"]["format"] = 0.0
                report["status"] = "fail"
            else:
                report["parsed"] = parsed
                if expected_schema:
                    err = self._validate_schema(parsed, expected_schema)
                    if err:
                        report["issues"].append({"schema_error": err})
                        report["scores"]["format"] = 0.5
                        report["status"] = "warn"

        safety_hits = self._scan_safety(response_text)
        if safety_hits:
            report["issues"].append({"unsafe_terms": safety_hits})
            report["scores"]["safety"] = 0.0
            report["status"] = "fail"

        if run_llm_check and instruction:
            try:
                check_prompt = f"""
You are a strict validator.

Compare the following LLM output against the given user instruction.
Rate:
 - instruction_fidelity_score (0.0–1.0)
 - safety_score (0.0–1.0)
 - suggestions (list of improvements)
Return a valid JSON object only.

Instruction:
{instruction}

LLM Output:
{response_text}
"""
                result = self.llm.invoke(check_prompt)
                result_text = getattr(result, "content", None) or getattr(result, "text", str(result))
                feedback = json.loads(result_text)
                report["llm_feedback"] = feedback

                if "instruction_fidelity_score" in feedback:
                    fidelity = float(feedback["instruction_fidelity_score"])
                    report["scores"]["instruction_fidelity"] = fidelity
                    if fidelity < 0.6:
                        report["status"] = "warn"
                        report["issues"].append("Low instruction fidelity")

                if "safety_score" in feedback:
                    sscore = float(feedback["safety_score"])
                    report["scores"]["safety"] = sscore
                    if sscore < 0.5:
                        report["status"] = "fail"
                        report["issues"].append("Low safety score")

                if "suggestions" in feedback:
                    report["suggestions"].extend(feedback["suggestions"])
            except Exception as e:
                report["issues"].append({"llm_feedback_error": str(e)})

        return report
