import numpy as np
from typing import List, Dict, Any, Tuple
from CodeValidator import CodeValidator

class UserFeedbackIntegrator:
    """
    A class to collect user feedback on generated code and adjust future outputs accordingly.
    
    Attributes:
        validation_results (List[Dict[str, Any]]): Results from the code validation process.
        user_feedback (List[Dict[str, Any]]): Feedback provided by users regarding the generated code.
        adjusted_criteria (Dict[str, Any]): Criteria adjusted based on the validation results and user feedback.
    """

    def __init__(self) -> None:
        self.validation_results = []
        self.user_feedback = []
        self.adjusted_criteria = {}

    def collect_feedback(self, validation_results: List[Dict[str, Any]], user_feedback: List[Dict[str, Any]]) -> None:
        """
        Collects validation results and user feedback.

        Args:
            validation_results (List[Dict[str, Any]]): Results from the code validation process.
            user_feedback (List[Dict[str, Any]]): Feedback provided by users regarding the generated code.
        """
        self.validation_results = validation_results
        self.user_feedback = user_feedback

    def adjust_criteria(self) -> Dict[str, Any]:
        """
        Adjusts criteria for future code generation based on validation results and user feedback.

        Returns:
            Dict[str, Any]: Adjusted criteria for code generation.
        """
        # Example logic for adjusting criteria
        if not self.validation_results or not self.user_feedback:
            return self.adjusted_criteria
        
        # Analyze validation results
        validation_scores = [result.get('score', 0) for result in self.validation_results]
        average_validation_score = np.mean(validation_scores)

        # Analyze user feedback
        feedback_scores = [feedback.get('score', 0) for feedback in self.user_feedback]
        average_feedback_score = np.mean(feedback_scores)

        # Adjust criteria based on both scores
        self.adjusted_criteria = {
            'validation_threshold': average_validation_score - 0.1,
            'feedback_threshold': average_feedback_score + 0.1,
            'improvement_suggestions': self.generate_improvement_suggestions()
        }

        return self.adjusted_criteria

    def generate_improvement_suggestions(self) -> List[str]:
        """
        Generates suggestions for improving code generation based on user feedback.

        Returns:
            List[str]: A list of improvement suggestions.
        """
        suggestions = []
        for feedback in self.user_feedback:
            if feedback.get('suggestion'):
                suggestions.append(feedback['suggestion'])
        return suggestions

# Example usage
if __name__ == "__main__":
    feedback_integrator = UserFeedbackIntegrator()
    validation_results_example = [{'score': 0.8}, {'score': 0.9}]
    user_feedback_example = [{'score': 0.7, 'suggestion': 'Add more comments.'}, {'score': 0.6, 'suggestion': 'Improve variable names.'}]
    
    feedback_integrator.collect_feedback(validation_results_example, user_feedback_example)
    adjusted_criteria = feedback_integrator.adjust_criteria()
    print(adjusted_criteria)