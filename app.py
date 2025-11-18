# app.py
import streamlit as st
import json
import traceback
from nexus_pipeline import run_pipeline

st.set_page_config(page_title="Project Nexus - Agentic System Builder", layout="wide")

st.title("🧩 Project Nexus: Agentic System Orchestrator")
st.write("This interface connects your RAG, prompt engine, validator, reader, and writer agents.")

# Input box
user_query = st.text_input("Enter your system request:", placeholder="Example: Create me a weather app in LangGraph")

# Optional advanced settings
with st.expander("Advanced Settings"):
    rag_dir = st.text_input("RAG Memory Directory", "./rag_memory")
    output_dir = st.text_input("Code Output Directory", "./generated_code")

# Run button
if st.button("Run Nexus Pipeline"):
    if not user_query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Running Nexus pipeline..."):
            try:
                result = run_pipeline(user_query, rag_persist_dir=rag_dir, code_output_dir=output_dir)
                st.success("Pipeline completed successfully!")

                # Display the summary cleanly
                st.subheader("Pipeline Summary")
                st.json(result)

                # Show enhanced prompt (if available)
                if "plan" in result:
                    st.subheader("Generated Plan")
                    st.code(json.dumps(result["plan"], indent=2), language="json")

                # Show generated files if available
                if "generated_files" in result:
                    st.subheader("Generated Code Files")
                    for file_info in result["generated_files"]:
                        name = file_info["name"]
                        size = file_info["size"]
                        st.write(f"**{name}**  — {size} characters")
                        if size < 15000:
                            with open(f"{output_dir}/{name}", "r", encoding="utf-8") as f:
                                code_content = f.read()
                            st.code(code_content, language="python")

            except Exception as e:
                st.error("An error occurred during pipeline execution.")
                st.text(traceback.format_exc())








#chainlit





# import chainlit as cl
# import traceback
# from rag_manager import RAGManager

# # Try to import your main pipeline (LangGraph or other)
# try:
#     from nexus_pipeline import run_pipeline
# except Exception as e:
#     print(f"⚠️ Could not import NexusPipeline: {e}")
#     NexusPipeline = None


# @cl.on_chat_start
# async def start():
#     """Initialize the RAG and pipeline when a new chat starts."""
#     rag = RAGManager()
#     pipeline = NexusPipeline() if NexusPipeline else None

#     cl.user_session.set("rag", rag)
#     cl.user_session.set("pipeline", pipeline)

#     await cl.Message(
#         content="🤖 **Nexus Agentic System** ready! Type your request below."
#     ).send()


# @cl.on_message
# async def main(message: cl.Message):
#     """Main entry point for handling user messages."""
#     user_query = message.content
#     rag: RAGManager = cl.user_session.get("rag")
#     pipeline = cl.user_session.get("pipeline")

#     try:
#         # Step 1️⃣ – Retrieve context using your RAG memory
#         contexts = rag.fetch_context(user_query, k=3)

#         if contexts:
#             top_contexts = "\n\n".join(
#                 [f"• {c['text'][:250]}..." for c in contexts[:2]]
#             )
#             await cl.Message(
#                 content=f"📚 **Top memory matches:**\n{top_contexts}"
#             ).send()
#         else:
#             await cl.Message(content="⚙️ No relevant memory found.").send()

#         # Step 2️⃣ – Pass user input and context into your Nexus pipeline
#         if pipeline:
#             try:
#                 result = None
#                 if hasattr(pipeline, "run"):
#                     result = pipeline.run(user_query, contexts)
#                 elif hasattr(pipeline, "invoke"):
#                     result = pipeline.invoke({"input": user_query, "context": contexts})
#                 elif hasattr(pipeline, "process"):
#                     result = pipeline.process(user_query)
#                 else:
#                     raise AttributeError("No run/invoke/process method found in pipeline.")

#                 # If result is dict, extract text-like field
#                 if isinstance(result, dict):
#                     for key in ("output", "response", "result", "text"):
#                         if key in result:
#                             result = result[key]
#                             break

#                 await cl.Message(content=f"🧠 {result}").send()

#             except Exception as e:
#                 await cl.Message(
#                     content=f"❌ Pipeline error:\n```\n{traceback.format_exc()}\n```"
#                 ).send()
#         else:
#             await cl.Message(content="⚠️ Pipeline not initialized.").send()

#     except Exception as e:
#         await cl.Message(
#             content=f"❌ Error in processing message:\n```\n{traceback.format_exc()}\n```"
#         ).send()
