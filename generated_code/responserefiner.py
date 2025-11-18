from typing import Dict, Any
from langgraph import NodeFunction
from EmotionalToneAnalyzer import analyze_tone

class ResponseRefiner(NodeFunction):
    def __init__(self) -> None:
        super().__init__()

    def refine_response(self, response: str, tone: str) -> Dict[str, str]:
        """
        Refines the generated response based on the provided tone.

        Args:
            response (str): The original generated response.
            tone (str): The identified tone of the original response.

        Returns:
            Dict[str, str]: A dictionary containing the refined response.
        """
        refined_response = self._refine(response, tone)
        return {'refined_response': refined_response}

    def _refine(self, response: str, tone: str) -> str:
        """
        Performs the actual refinement of the response.

        Args:
            response (str): The original response to refine.
            tone (str): The tone to guide the refinement.

        Returns:
            str: The refined response.
        """
        # Analyze the tone and adjust the response accordingly
        tone_analysis = analyze_tone(tone)
        
        # Refinement logic based on tone analysis
        if tone_analysis['polarity'] == 'negative':
            return self._make_positive(response)
        elif tone_analysis['polarity'] == 'neutral':
            return self._enhance_clarity(response)
        else:
            return response  # Assuming the response is appropriate if positive

    def _make_positive(self, response: str) -> str:
        # Logic to convert negative response to a more positive tone
        return response.replace("not good", "acceptable").replace("bad", "challenging")

    def _enhance_clarity(self, response: str) -> str:
        # Logic to improve clarity of the response
        return response.strip().capitalize() + "."

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        response = inputs.get('response', '')
        tone = inputs.get('tone', '')
        return self.refine_response(response, tone)