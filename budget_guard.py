import csv
from datetime import datetime, timedelta
import os
import sys

def is_budget_exceeded(max_hourly_budget=0.005):
    """
    Parses the telemetry CSV file, aggregates precision costs incurred over 
    the trailing 60 minutes, and checks if it violates the safety budget cap.
    """
    telemetry_file_path = os.path.abspath("/output/telemetry_analytics.csv")
    
    # Safety pass: if no telemetry file exists yet, budget cannot be spent
    if not os.path.exists(telemetry_file_path):
        return False
        
    running_cost_total = 0.0
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    
    try:
        with open(telemetry_file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Parse ISO 8601 string back to datetime object
                    timestamp_str = row.get("timestamp", "").replace("Z", "")
                    row_time = datetime.fromisoformat(timestamp_str)
                    
                    # If transaction falls inside our trailing 60-minute window, accumulate cost
                    if row_time >= one_hour_ago:
                        running_cost_total += float(row.get("precision_cost", 0.0))
                except (ValueError, TypeError):
                    continue # Skip malformed row fragments safely
                    
        # Check if current consumption breaks the circuit breaker
        if running_cost_total >= float(max_hourly_budget):
            print(f"⚠️ [BUDGET GUARD TRIP] Trailing hourly cost (${running_cost_total:.6f}) exceeds limit (${max_hourly_budget}).", file=sys.stderr)
            return True
            
    except Exception as budget_error:
        print(f"Budget guard telemetry check warning: {str(budget_error)}", file=sys.stderr)
        
    return False
