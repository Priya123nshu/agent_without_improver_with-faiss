import os
import json
import time
from typing import Dict, Any, Optional


class WriterAgent:
    """
    Writer Agent (Autonomous Code Generator)
    ----------------------------------------
    - Consumes a structured plan produced by the ReaderAgent
    - Generates runnable, modular code files for each component
    - Supports LangGraph, CrewAI, AutoGen, and LlamaIndex frameworks
    - Automatically builds an orchestrator (main.py)
    - Optionally saves files to disk
    """

    def __init__(self, llm_client=None, base_output_dir: str = "./generated_code", auto_save: bool = True):
        """
        Args:
            llm_client: LLM instance with .invoke(prompt). If None, a mock generator is used.
            base_output_dir: directory for saving generated files.
            auto_save: whether to automatically save generated files to disk.
        """
        self.llm = llm_client or self._mock_llm()
        self.base_output_dir = base_output_dir
        self.auto_save = auto_save

        os.makedirs(self.base_output_dir, exist_ok=True)

    def _mock_llm(self):
        """Fallback LLM that returns placeholder code for offline testing."""
        class MockLLM:
            def invoke(self, prompt):
                return f"# Mock code generated for: {prompt[:60]}...\nprint('Simulated component behavior')"

        print("Using MockLLM (offline mode)")
        return MockLLM()

    def _build_code_prompt(self, component_name: str, details: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """
        Construct a detailed prompt for generating actual component code.
        The prompt instructs the LLM how to implement the requested component.
        """
        framework = plan.get("framework", "LangGraph")
        language = plan.get("language", "python")
        embedding_model = plan.get("embedding_model", "None")
        llm_model = plan.get("llm", "Unknown")

        return f"""
You are the Writer Agent, a senior {language} developer and AI systems engineer.

Implement the following software component as part of a larger autonomous system.

Component information:
- Name: {component_name}
- Description: {details.get("description", "N/A")}
- Inputs: {details.get("inputs", [])}
- Outputs: {details.get("outputs", [])}
- Dependencies: {details.get("dependencies", [])}

System context:
- Framework: {framework}
- LLM Model: {llm_model}
- Embedding Model: {embedding_model}

Instructions:
1. Write clean, executable, modular {language} code.
2. Include meaningful class or function definitions.
3. Add docstrings and type hints for public methods/functions.
4. Handle dependency imports gracefully.
5. If using LangGraph, define the component as a node function/class.
6. The code must be runnable and relevant to the component description.
7. Return only code, no explanations or markdown.

Return valid {language} source code only.
""".strip()

    def _generate_component_code(self, component_name: str, details: Dict[str, Any], plan: Dict[str, Any]) -> str:
        """
        Use the LLM to generate the actual code implementation for one component.
        """
        prompt = self._build_code_prompt(component_name, details, plan)
        response = self.llm.invoke(prompt)
        content = getattr(response, "content", None) or getattr(response, "text", None) or str(response)
        return content.strip()

    def _generate_main_script(self, plan: Dict[str, Any]) -> str:
        """
        Create the main orchestrator script depending on the selected framework.
        This generates a simple entrypoint that wires components together.
        """
        framework = plan.get("framework", "").lower()
        components = list(plan.get("components", {}).keys())

        if not components:
            return "# No components defined in plan.\n"

        if framework == "langgraph":
            lines = [
                "# Auto-generated LangGraph Orchestrator",
                "from langgraph.graph import StateGraph, END",
                "from typing import Dict, Any",
                "",
                "graph = StateGraph()"
            ]
            for comp in components:
                safe_name = comp.lower()
                lines.append(f"from {safe_name} import {comp}")
                lines.append(f'graph.add_node("{comp}", {comp})')

            for i in range(len(components) - 1):
                lines.append(f'graph.add_edge("{components[i]}", "{components[i+1]}")')

            lines.append(f'graph.set_entry_point("{components[0]}")')
            lines.append(f'graph.add_edge("{components[-1]}", END)')
            lines.append("")
            lines.append("if __name__ == '__main__':")
            lines.append("    result = graph.run({'input': 'start'})")
            lines.append("    print(result)")
            return "\n".join(lines)

        # Fallback orchestrator for other frameworks
        return f"# Orchestrator for {framework}\n# TODO: Implement orchestration logic here.\n"

    def write_system_code(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code for all components and optionally save to disk.
        Returns a dictionary with file contents and status.
        """
        if "components" not in plan:
            raise ValueError("Plan missing 'components' key.")

        generated_files = {}
        print("Starting system code generation.")

        # Iterate through each component and generate code
        for comp_name, details in plan["components"].items():
            print(f"Generating component: {comp_name}")
            code = self._generate_component_code(comp_name, details, plan)
            filename = f"{comp_name.lower()}.py"
            filepath = os.path.join(self.base_output_dir, filename)

            generated_files[filename] = code

            if self.auto_save:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"Saved {filename}")

        # Generate orchestrator script
        print("Generating main orchestrator script.")
        main_code = self._generate_main_script(plan)
        generated_files["main.py"] = main_code

        if self.auto_save:
            with open(os.path.join(self.base_output_dir, "main.py"), "w", encoding="utf-8") as f:
                f.write(main_code)
            print("Saved main.py")

        print("Code generation complete.")
        return {"status": "success", "files": [{"name": k, "content": v} for k, v in generated_files.items()]}
