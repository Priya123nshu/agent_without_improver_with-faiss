from typing import List, Dict, Any
import json

class UserFeedbackCollector:
    """Collects feedback from users to improve future code generation."""

    def __init__(self) -> None:
        """Initialize the UserFeedbackCollector."""
        self.feedback_data: List[Dict[str, Any]] = []

    def collect_feedback(self, user_feedback: str) -> None:
        """Collect user feedback and store it in the feedback data list.

        Args:
            user_feedback (str): Feedback provided by the user.
        """
        feedback_entry = {"feedback": user_feedback}
        self.feedback_data.append(feedback_entry)

    def get_feedback_data(self) -> List[Dict[str, Any]]:
        """Retrieve all collected feedback data.

        Returns:
            List[Dict[str, Any]]: A list of feedback entries.
        """
        return self.feedback_data

    def save_feedback_to_file(self, file_path: str) -> None:
        """Save the collected feedback data to a JSON file.

        Args:
            file_path (str): The path to the file where feedback data will be saved.
        """
        with open(file_path, 'w') as file:
            json.dump(self.feedback_data, file, indent=4)

# Example usage of UserFeedbackCollector
if __name__ == "__main__":
    collector = UserFeedbackCollector()
    collector.collect_feedback("The code is very intuitive and easy to follow.")
    collector.collect_feedback("I would like more examples in the documentation.")
    
    print(collector.get_feedback_data())
    collector.save_feedback_to_file('feedback.json')