from langgraph import Node
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import openai
import re

class CodeQualityEvaluator(Node):
    def __init__(self, model_name: str = "text-davinci-003") -> None:
        super().__init__()
        self.model_name = model_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def evaluate_quality(self, java_code_snippet: str) -> Dict[str, Any]:
        """
        Evaluates the quality of the given Java code snippet based on best practices.

        Args:
            java_code_snippet (str): A snippet of Java code to evaluate.

        Returns:
            Dict[str, Any]: A dictionary containing quality metrics.
        """
        quality_metrics = {
            'syntax_errors': self.check_syntax(java_code_snippet),
            'best_practices_score': self.evaluate_best_practices(java_code_snippet),
            'complexity_score': self.calculate_complexity(java_code_snippet),
        }
        return quality_metrics

    def check_syntax(self, java_code: str) -> List[str]:
        """
        Checks for syntax errors in the Java code snippet.

        Args:
            java_code (str): The Java code snippet to check.

        Returns:
            List[str]: A list of syntax error messages, if any.
        """
        # Placeholder for syntax checking logic; would typically involve a parser
        errors = []
        if not java_code.strip().endswith(';'):
            errors.append("Missing semicolon at the end of the statement.")
        return errors

    def evaluate_best_practices(self, java_code: str) -> float:
        """
        Evaluates the Java code against best practices.

        Args:
            java_code (str): The Java code snippet to evaluate.

        Returns:
            float: A score representing adherence to best practices (0 to 100).
        """
        prompt = f"Evaluate the following Java code for best practices: {java_code}"
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        score = float(response['choices'][0]['message']['content'].strip())
        return score

    def calculate_complexity(self, java_code: str) -> float:
        """
        Calculates the cyclomatic complexity of the Java code.

        Args:
            java_code (str): The Java code snippet to analyze.

        Returns:
            float: A complexity score.
        """
        # Simple complexity estimation based on the number of control flow statements
        complexity_indicators = re.findall(r'\b(if|for|while|case|catch)\b', java_code)
        return len(complexity_indicators) + 1  # +1 for the default path

    def run(self, java_code_snippet: str) -> Dict[str, Any]:
        """
        Executes the quality evaluation process.

        Args:
            java_code_snippet (str): A snippet of Java code to evaluate.

        Returns:
            Dict[str, Any]: The evaluated quality metrics.
        """
        return self.evaluate_quality(java_code_snippet)