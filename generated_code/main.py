# Auto-generated LangGraph Orchestrator
from langgraph.graph import StateGraph, END
from typing import Dict, Any

graph = StateGraph()
from conversationalcontextmanager import ConversationalContextManager
graph.add_node("ConversationalContextManager", ConversationalContextManager)
from dialoguesynthesizer import DialogueSynthesizer
graph.add_node("DialogueSynthesizer", DialogueSynthesizer)
from emotionaltoneanalyzer import EmotionalToneAnalyzer
graph.add_node("EmotionalToneAnalyzer", EmotionalToneAnalyzer)
from responserefiner import ResponseRefiner
graph.add_node("ResponseRefiner", ResponseRefiner)
from conversationlogger import ConversationLogger
graph.add_node("ConversationLogger", ConversationLogger)
graph.add_edge("ConversationalContextManager", "DialogueSynthesizer")
graph.add_edge("DialogueSynthesizer", "EmotionalToneAnalyzer")
graph.add_edge("EmotionalToneAnalyzer", "ResponseRefiner")
graph.add_edge("ResponseRefiner", "ConversationLogger")
graph.set_entry_point("ConversationalContextManager")
graph.add_edge("ConversationLogger", END)

if __name__ == '__main__':
    result = graph.run({'input': 'start'})
    print(result)