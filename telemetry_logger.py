import csv
from datetime import datetime
import os
import sys

def log_telemetry_metrics(task_id, prompt, verdict):
    """
    Appends a structured transaction row to a local CSV database file.
    Captures operational timestamps, token weights, destinations, and precise costs.
    """
    # Ensure our data persists on the mounted /output directory layer
    telemetry_dir = os.path.abspath("/output")
    telemetry_file_path = os.path.join(telemetry_dir, "telemetry_analytics.csv")
    
    # Establish explicit column layout matrix matching enterprise schema
    fieldnames = [
        "timestamp", 
        "task_id", 
        "prompt_character_length", 
        "calculated_tokens", 
        "routing_target", 
        "precision_cost", 
        "reasoning_summary"
    ]
    
    # Check if the file needs initialization headers dropped in
    file_exists = os.path.exists(telemetry_file_path)
    
    try:
        os.makedirs(telemetry_dir, exist_ok=True)
        
        # Open resource file context handling locking and append flags
        with open(telemetry_file_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            # Construct row data block ensuring precise type constraints
            writer.writerow({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "task_id": str(task_id),
                "prompt_character_length": len(str(prompt)),
                "calculated_tokens": int(verdict.get("tokens", 0)),
                "routing_target": str(verdict.get("route", "UNKNOWN")).upper(),
                "precision_cost": float(verdict.get("estimated_cost", 0.0)),
                "reasoning_summary": str(verdict.get("reasoning", "")).replace("\n", " ")
            })
            
            # Flush internal cache layers to push data physical layer instantly
            csvfile.flush()
            os.fsync(csvfile.fileno())
            
    except Exception as log_error:
        # Prevent telemetry file write errors from ever crashing the core engine
        print(f"Telemetry tracking bypass warning: {str(log_error)}", file=sys.stderr)
