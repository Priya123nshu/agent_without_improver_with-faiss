from datetime import datetime
from typing import Dict, Any

class ConversationLogger:
    def __init__(self) -> None:
        """Initialize the ConversationLogger instance."""
        self.logs: List[Dict[str, Any]] = []

    def log_conversation(self, user_input: str, response: str, tone: str) -> Dict[str, Any]:
        """
        Log a conversation entry.

        Args:
            user_input (str): The input provided by the user.
            response (str): The system's response to the user input.
            tone (str): The tone of the response.

        Returns:
            Dict[str, Any]: A dictionary containing the log entry.
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'response': response,
            'tone': tone
        }
        self.logs.append(log_entry)
        return log_entry

def conversation_logger_node(user_input: str, response: str, tone: str) -> Dict[str, Any]:
    """
    Node function for logging conversations in LangGraph.

    Args:
        user_input (str): The input provided by the user.
        response (str): The system's response to the user input.
        tone (str): The tone of the response.

    Returns:
        Dict[str, Any]: A dictionary containing the log entry.
    """
    logger = ConversationLogger()
    return logger.log_conversation(user_input, response, tone)