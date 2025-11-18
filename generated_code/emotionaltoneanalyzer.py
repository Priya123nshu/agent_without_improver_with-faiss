from typing import Dict, Any
import openai

class EmotionalToneAnalyzer:
    def __init__(self, api_key: str) -> None:
        """
        Initializes the EmotionalToneAnalyzer with the provided OpenAI API key.

        :param api_key: Your OpenAI API key for accessing the language model.
        """
        openai.api_key = api_key

    def analyze_tone(self, user_input: str) -> Dict[str, str]:
        """
        Analyzes the emotional tone of the user's input.

        :param user_input: The string input from the user to analyze.
        :return: A dictionary containing the detected emotional tone.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"Analyze the emotional tone of the following input: '{user_input}'"}
            ]
        )
        
        tone = response['choices'][0]['message']['content'].strip()
        return {'tone': tone}

# Example of how to use the EmotionalToneAnalyzer
if __name__ == "__main__":
    analyzer = EmotionalToneAnalyzer(api_key="YOUR_OPENAI_API_KEY")
    user_input = "I'm feeling really happy today!"
    tone_output = analyzer.analyze_tone(user_input)
    print(tone_output)