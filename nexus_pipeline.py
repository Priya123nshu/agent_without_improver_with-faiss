# nexus_pipeline.py
# Project Nexus Orchestrator Pipeline
# -----------------------------------
# Connects all modules into one sequential flow:
# RAGManager -> DynamicPromptNode -> LLMValidator -> ReaderAgent -> WriterAgent

import os
import json
import sys
from typing import Optional

from rag_manager import RAGManager
from dynamic_node_prompt import DynamicPromptNode
from llm_validator import LLMValidator
from reader_agent import ReaderAgent
from writer_agent import WriterAgent
from langchain_openai import AzureChatOpenAI


def make_llm_client() -> AzureChatOpenAI:
    """
    Initialize AzureChatOpenAI using environment variables.
    Adjust this function if you switch to another LLM.
    """
    return AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.7
    )


def run_pipeline(user_query: str, rag_persist_dir: str = "./rag_memory", code_output_dir: str = "./generated_code"):
    """
    Main orchestrator pipeline for the Nexus System.

    Steps:
        1. Initialize dependencies (LLM, RAG, Validator, Reader, Writer).
        2. Generate enhanced prompt dynamically using RAG memory.
        3. Validate the enhanced prompt.
        4. Generate system architecture plan with ReaderAgent.
        5. Validate the plan structure.
        6. Generate component code and orchestrator using WriterAgent.
    """

    # Initialize Azure LLM
    llm_client = make_llm_client()

    # Initialize RAG Manager and Dynamic Prompt Creator
    rag = RAGManager(persist_dir=rag_persist_dir)
    dp_node = DynamicPromptNode(rag)

    # Validator, Reader, and Writer
    validator = LLMValidator(llm_client)
    reader = ReaderAgent(llm_client=llm_client, validator=validator)
    writer = WriterAgent(llm_client=llm_client, base_output_dir=code_output_dir, auto_save=True)

    # Step 1: Generate enhanced prompt
    print("Generating enhanced prompt from stored corrective memory.")
    enhanced_prompt = dp_node.generate_prompt(user_query, k=3)
    print("Enhanced prompt generated successfully.\n")

    # Step 2: Validate the enhanced prompt
    print("Validating enhanced prompt for structure and instruction fidelity.")
    prompt_validation = validator.validate_response(
        response_text=enhanced_prompt,
        instruction=user_query,
        require_json=False,
        run_llm_check=True
    )
    print("Prompt validation report:")
    print(json.dumps(prompt_validation, indent=2))

    if prompt_validation.get("status") == "fail":
        print("Prompt validation failed. Exiting pipeline.")
        return {
            "success": False,
            "stage": "prompt_validation",
            "report": prompt_validation
        }

    # Step 3: Use ReaderAgent to generate plan
    print("\nRequesting ReaderAgent to create system plan.")
    plan_result = reader.plan_from_prompt(enhanced_prompt, instruction=user_query)

    if not plan_result.get("success"):
        print("ReaderAgent failed to produce a valid plan.")
        return {
            "success": False,
            "stage": "reader_planning",
            "error": plan_result.get("error"),
            "attempts": plan_result.get("attempts"),
            "validation_report": plan_result.get("validation_report")
        }

    plan = plan_result["plan"]
    print("\nSystem plan created successfully. Proceeding with plan validation.")

    # Step 4: Validate plan schema and logical structure
    plan_text = json.dumps(plan)
    plan_validation = validator.validate_response(
        response_text=plan_text,
        expected_schema={
            "type": "object",
            "properties": {
                "framework": {"type": "string"},
                "language": {"type": "string"},
                "llm": {"type": "string"},
                "embedding_model": {"type": "string"},
                "components": {"type": ["object", "array"]},
                "termination_policy": {"type": "object"},
                "files": {"type": ["array", "null"]}
            },
            "required": ["framework", "language", "llm", "components"]
        },
        instruction="Validate system plan for schema compliance.",
        require_json=True,
        run_llm_check=True
    )
    print("Plan validation report:")
    print(json.dumps(plan_validation, indent=2))

    if plan_validation.get("status") == "fail":
        print("Plan validation failed. Exiting pipeline.")
        return {
            "success": False,
            "stage": "plan_validation",
            "report": plan_validation
        }

    # Step 5: Normalize components if they are in list format
    if isinstance(plan.get("components"), list):
        normalized = {}
        for item in plan["components"]:
            if isinstance(item, dict) and "name" in item:
                name = item["name"]
                normalized[name] = {k: v for k, v in item.items() if k != "name"}
        plan["components"] = normalized

    # Step 6: Generate actual system code using WriterAgent
    print("\nInvoking WriterAgent for code generation.")
    try:
        write_result = writer.write_system_code(plan)
    except Exception as e:
        print("WriterAgent encountered an error during code generation.")
        print("Error details:", str(e))
        return {
            "success": False,
            "stage": "code_generation",
            "error": str(e)
        }

    # Summarize generated files
    print("Code generation completed successfully.")
    file_summaries = []
    for f in write_result.get("files", []):
        name = f.get("name")
        content = f.get("content", "")
        file_summaries.append({"name": name, "size": len(content)})

    result_summary = {
        "success": True,
        "stage": "done",
        "user_query": user_query,
        "plan": plan,
        "plan_validation": plan_validation,
        "generated_files": file_summaries,
        "output_dir": os.path.abspath(code_output_dir)
    }

    print("\nPipeline executed successfully.")
    return result_summary


def main(argv: Optional[list] = None):
    """
    Entry point for standalone execution.

    Example:
        python nexus_pipeline.py "Create me a weather app in LangGraph"
    """
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("No user query provided.")
        print('Usage: python nexus_pipeline.py "Create me a weather app in LangGraph"')
        return

    user_query = argv[0]
    summary = run_pipeline(user_query)

    print("\nFinal Pipeline Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
