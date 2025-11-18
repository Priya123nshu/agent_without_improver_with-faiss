from typing import List, Dict, Any
import openai
from sentence_transformers import SentenceTransformer

class SpecificationAnalyzer:
    def __init__(self, llm_model: str, embedding_model: str):
        """
        Initializes the SpecificationAnalyzer with the specified models.

        Args:
            llm_model (str): The model name for the language model (e.g., GPT-4).
            embedding_model (str): The model name for the sentence embedding model.
        """
        self.llm_model = llm_model
        self.embedding_model = SentenceTransformer(embedding_model)

    def analyze_specification(self, user_specification: str) -> Dict[str, List[str]]:
        """
        Analyzes the user specification to extract functional requirements and constraints.

        Args:
            user_specification (str): The user specification text to analyze.

        Returns:
            Dict[str, List[str]]: A dictionary containing functional requirements and constraints.
        """
        functional_requirements = self.extract_functional_requirements(user_specification)
        constraints = self.extract_constraints(user_specification)
        return {
            'functional_requirements': functional_requirements,
            'constraints': constraints
        }

    def extract_functional_requirements(self, user_specification: str) -> List[str]:
        """
        Extracts functional requirements from the user specification.

        Args:
            user_specification (str): The user specification text.

        Returns:
            List[str]: A list of functional requirements.
        """
        response = openai.ChatCompletion.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": f"Extract functional requirements from the following specification: {user_specification}"}]
        )
        return response['choices'][0]['message']['content'].split('\n')

    def extract_constraints(self, user_specification: str) -> List[str]:
        """
        Extracts constraints from the user specification.

        Args:
            user_specification (str): The user specification text.

        Returns:
            List[str]: A list of constraints.
        """
        response = openai.ChatCompletion.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": f"Extract constraints from the following specification: {user_specification}"}]
        )
        return response['choices'][0]['message']['content'].split('\n') 

# Example usage (This should be outside of the class definition):
# analyzer = SpecificationAnalyzer(llm_model='gpt-4', embedding_model='all-MiniLM-L6-v2')
# result = analyzer.analyze_specification("User wants a system that can process payments securely and must comply with PCI DSS.")
# print(result)