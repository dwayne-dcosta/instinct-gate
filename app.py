# app.py - Streamlit User Interface Dashboard
import streamlit as st
from router_agent import evaluate_and_route

# Import decoupled modular tracking, governance, and optimization systems
from telemetry_logger import log_telemetry_metrics
from budget_guard import is_budget_exceeded
from cache_manager import get_cached_route, set_cached_route

# 1. Configure an eye-friendly, wide page state layout.
st.set_page_config(
    page_title="AMD Hybrid Router Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Render a clean header title block.
st.title("Enterprise Token-Efficient Routing Hub")
st.markdown("Track 1 Optimization Panel - Deployed on AMD Developer Cloud Architecture")
st.write("----")

# 3. Construct the primary input payload area.
st.subheader("Data Processing Unit")
user_query = st.text_area(
    label="Enter your prompt, code snippet, or dataset task payload below:",
    placeholder="Type or paste text here...",
    height=150
)

# 4. Trigger the analytical computation pipeline on button click.
if st.button("Analyze & Route Payload", type="primary"):
    if not user_query.strip():
        st.warning("Please input a text payload before running the router analysis.")
    else:
        # Pass the UI text box entry straight into your verified routing engine.
        verdict = evaluate_and_route(user_query)

        st.write("----")
        st.subheader("Real-Time Diagnostic Verdict")

        # 5. Create clean visual columns to organize your data cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Assigned Processing Node", value=verdict["route"].upper())
        with col2:
            st.metric(label="Calculated Token Length", value=f"{verdict['tokens']} Tokens")
        with col3:
            st.metric(label="Simulated Run Cost", value=f"${verdict['estimated_cost']:.5f}")
        
        # 6. Render the algorithmic reasoning explanation log inside a soft text box
        st.info(f" **Routing Logic Decision Log:** {verdict['reasoning']}")

# ========================================================================
# 7. AUTOMATED GRADING BOT ENTRYPOINT (Dual-Input, Multi-Task Compliance)
# ========================================================================
if __name__ == "__main__":
    import sys
    import json
    import os
    import traceback

    # Define absolute pathing matrix targeting requested root paths
    absolute_input_file = os.path.abspath("/input/tasks.json")
    absolute_output_dir = os.path.abspath("/output")
    absolute_output_file = os.path.join(absolute_output_dir, "results.json")

    results_payload = []
    tasks_list = []

    # 1. Check if the Budget Guard circuit breaker has been tripped up front
    budget_tripped = is_budget_exceeded(max_hourly_budget=0.005)

    # Strategy A: Check if the evaluator mounted a JSON tasks file
    if os.path.exists(absolute_input_file):
        try:
            with open(absolute_input_file, "r") as f:
                task_data = json.load(f)
            
            if isinstance(task_data, dict):
                tasks_list = [task_data]
            elif isinstance(task_data, list):
                tasks_list = task_data
        except Exception as file_error:
            print(f"Error parsing tasks.json: {str(file_error)}", file=sys.stderr)

    # Strategy B: Fallback to command-line arguments for local development
    if not tasks_list and len(sys.argv) > 1:
        tasks_list = [{
            "task_id": "T01",
            "prompt": " ".join(sys.argv[1:])
        }]

    # Strategy C: Master safety fallback item if no inputs exist anywhere
    if not tasks_list:
        tasks_list = [{
            "task_id": "T01",
            "prompt": "Default fallback validation prompt execution."
        }]

    # ========================================================================
    # CORE TRACK PROCESSING & TELEMETRY LOGGING MATRIX
    # ========================================================================
    for task in tasks_list:
        if isinstance(task, dict):
            current_task_id = task.get("task_id") or task.get("id") or "T01"
            bot_prompt = task.get("prompt") or task.get("task") or task.get("input") or ""
            
            # ⚡ CHECK PRE-ROUTING LOOKUP CACHE FIRST FOR SUB-MILLISECOND SPEED
            cached_verdict = get_cached_route(bot_prompt)
            
            if cached_verdict:
                verdict = cached_verdict
            # If cache misses, fall back to our safety cost governance gates
            elif budget_tripped:
                verdict = {
                    "route": "LOCAL_CHEAP",
                    "tokens": 7,
                    "estimated_cost": 0.0,
                    "reasoning": "Budget Guard Active: Bypassed cloud to protect cost parameters."
                }
            else:
                try:
                    # Execute your core analytical routing pipeline
                    verdict = evaluate_and_route(bot_prompt)
                    
                    # ⚡ CACHE THE NEW SUCCESSFUL VERDICT FOR FUTURE DUPLICATE HITS
                    set_cached_route(bot_prompt, verdict, ttl_minutes=10)
                    
                except Exception as eval_error:
                    verdict = {
                        "route": "LOCAL_CHEAP",
                        "tokens": 7,
                        "estimated_cost": 0.0,
                        "reasoning": f"Engine execution fallback: {str(eval_error)}"
                    }

            # Print metrics out cleanly to standard output streams
            print(f"{verdict['route'].upper()}", flush=True)
            
            # Construct compliant schema dictionary layout
            task_output = {
                "task_id": str(current_task_id),
                "answer": str(verdict['route'].upper()),
                "route": str(verdict['route'].upper()),
                "tokens": int(verdict['tokens']),
                "estimated_cost": float(verdict['estimated_cost']),
                "reasoning": str(verdict.get('reasoning', 'Processed successfully.'))
            }
            results_payload.append(task_output)
            
            # 🪝 Invoke our decoupled append-only telemetry logging module
            log_telemetry_metrics(current_task_id, bot_prompt, verdict)

    # ========================================================================
    # FILE SERIALIZATION LAYER (Guarantees Physical Data Delivery)
    # ========================================================================
    try:
        os.makedirs(absolute_output_dir, exist_ok=True)
        with open(absolute_output_file, "w") as f:
            json.dump(results_payload, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
    except Exception as io_error:
        print(f"Fatal writing execution restriction: {str(io_error)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
