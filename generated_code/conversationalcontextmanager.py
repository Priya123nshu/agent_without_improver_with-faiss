from langgraph import Node

class ConversationalContextManager(Node):
    def __init__(self):
        super().__init__()

    def update_context(self, user_input: str, previous_context: str) -> str:
        """
        Updates the conversation context based on the user input and previous context.

        Args:
            user_input (str): The input string from the user.
            previous_context (str): The previous context of the conversation.

        Returns:
            str: The updated context string.
        """
        # Combine previous context with user input for continuity
        updated_context = f"{previous_context} {user_input}".strip()
        
        # Here, you may implement additional logic for context management,
        # such as summarizing or filtering irrelevant information based on rules.
        
        return updated_context

    def run(self, inputs: dict) -> dict:
        """
        Run the context manager with the provided inputs.

        Args:
            inputs (dict): A dictionary containing 'user_input' and 'previous_context'.

        Returns:
            dict: A dictionary with the updated context.
        """
        user_input = inputs.get('user_input', '')
        previous_context = inputs.get('previous_context', '')
        
        updated_context = self.update_context(user_input, previous_context)
        
        return {'updated_context': updated_context}