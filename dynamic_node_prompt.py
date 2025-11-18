import json
from typing import Dict, List

class DynamicPromptNode:
    """Dynamic Prompt Creator"""

    def __init__(self, rag_manager):
        self.rag = rag_manager

    def generate_prompt(self, user_query: str, k: int = 3) -> str:
        contexts = self.rag.fetch_context(user_query, k=k)

        if not contexts:
            return f"""
[User Objective]
{user_query}

[Instruction]
Design and write the complete agent architecture, using any suitable framework.
Explain your reasoning and structure the components (Reader, Writer, Improver, etc.)
clearly so they can work autonomously.
""".strip()

        context_blocks = []
        for i, ctx in enumerate(contexts, 1):
            try:
                data = json.loads(ctx["text"])
                sys = data.get("system_context", {})
                beh = data.get("behavioral_insights", {})
                corr = data.get("corrective_knowledge", {})

                block = f"""
[Memory Block {i}]
System Context:
  - Preferred LLM: {sys.get('preferred_llm', 'N/A')}
  - Embedding Model: {sys.get('preferred_embedding_model', 'N/A')}
  - Active Tools: {sys.get('active_tools', 'N/A')}

Behavioral Insights:
  - Style Preference: {beh.get('user_style_preference', 'N/A')}
  - Framework Preference: {beh.get('code_framework_preference', 'N/A')}
  - Common Errors: {beh.get('common_errors', 'N/A')}
  - Fix Patterns: {beh.get('fix_patterns', 'N/A')}

Corrective Knowledge:
  - Insight Summary: {corr.get('insight_summary', 'N/A')}
  - Recommendations: {corr.get('recommendations', 'N/A')}
  - Relevant Tags: {corr.get('relevance_tags', 'N/A')}
"""
                context_blocks.append(block.strip())
            except Exception:
                context_blocks.append(f"[Unparsed Memory Block] {ctx['text'][:500]}")

        merged_context = "\n\n".join(context_blocks)

        return f"""
[Dynamic Context Retrieved from Corrective Memory]
{merged_context}

[User Objective]
{user_query}

[Instruction]
Using the above context and memory, design the complete autonomous agent code pipeline:
  1. Select framework (LangGraph, LlamaIndex, or CrewAI) based on relevance.
  2. Decide the programming language and embedding models automatically.
  3. Define Reader, Writer, Validator, and Improver nodes and their interactions.
  4. Generate base code structure for the requested app.
  5. Include modularity, validation flow, and error handling.

Ensure your reasoning aligns with user’s historical preferences, 
framework usage patterns, and corrective insights.
""".strip()
