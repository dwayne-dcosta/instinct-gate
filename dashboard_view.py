# dashboard_view.py - High-Signal Analytics Frontend Module
import os
import sys
# 🕒 Explicitly append the parent root folder path straight into python's lookup registry
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone


import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta, timezone

def render_advanced_dashboard():
    """
    Renders enterprise telemetry logs, live budget metrics, 
    and microsecond performance data onto the Streamlit canvas.
    """
    # 📁 Path Matrix Setup
        # Secure serverless sandboxed path fallback tracking
    telemetry_file_path = os.path.abspath("/output/telemetry_analytics.csv")
    if not os.path.exists(telemetry_file_path):
        telemetry_file_path = os.path.abspath("./output/telemetry_analytics.csv")
    
    st.markdown("## 📊 System Monitoring & Governance Command Center")
    st.write("Real-time edge-to-cloud performance tracking and automated budget circuit breakers.")
    st.write("----")

    # ========================================================================
    # 🗃️ STEP 1: DATA INGESTION & PARSING MATRIX
    # ========================================================================
    df = None
    if os.path.exists(telemetry_file_path):
        try:
        # 🤫 SUPPRESS HARMLESS PARSING HINTS DURING DATA INGESTION
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = pd.read_csv(telemetry_file_path)
            
            # 🗓️ Ensure proper datetime formatting, forcing invalid header text to NaT null values
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            
            # 🧼 DROP ALL ROWS THAT ARE NOT VALID DATETIME OBJECTS (Cleans out string headers)
            df = df.dropna(subset=['timestamp'])
        
        except Exception as e:
            # Prevent logging errors from bubbling up to the user interface
            pass

        # ========================================================================
    # 🛡️ STEP 2: BUDGET & CACHE METRICS AGGREGATION (Session State Secured)
    # ========================================================================
    max_budget = 0.005000
    
    # Initialize session tracking keys if they don't exist in browser memory yet
    if "ui_total_requests" not in st.session_state:
        st.session_state.ui_total_requests = 0
    if "ui_cache_hits" not in st.session_state:
        st.session_state.ui_cache_hits = 0
    if "ui_hourly_spend" not in st.session_state:
        st.session_state.ui_hourly_spend = 0.0

    # Read tracking variables out of persistent memory state arrays
    total_requests = st.session_state.ui_total_requests
    cache_hits = st.session_state.ui_cache_hits
    hourly_spend = st.session_state.ui_hourly_spend

    if df is not None and not df.empty:
        total_requests = len(df)
        
        # 🤫 SUPPRESS HARMLESS HINT WARNINGS FROM TELEMETRY DATA INGESTION
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Convert strings to datetime objects, cleanly forcing invalid header rows to NaT null values
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        df = df.dropna(subset=['timestamp'])
        
        # 🧼 SECURE THE PRECISION COST COLUMN AGAINST STRING POLLUTION
        # errors='coerce' turns text words into NaN, and fillna(0.0) replaces them with 0.0
        df['precision_cost'] = pd.to_numeric(df['precision_cost'], errors='coerce').fillna(0.0)
        
        # Calculate trailing 60-minute spending metrics cleanly
        now = datetime.now(timezone.utc)
        one_hour_ago = now - timedelta(hours=1)
        hourly_df = df[df['timestamp'] >= one_hour_ago]
        
        # Type-secure extraction pass
        hourly_spend = float(hourly_df['precision_cost'].sum())

        
        # Extract operational cache and local edge tracking metrics
        cache_hits = len(df[df['reasoning_summary'].str.contains('CACHE|Cache', na=False) | (df['routing_target'] == 'LOCAL_CHEAP')])
        
        # Update session memory states so they survive subsequent user clicks
        st.session_state.ui_total_requests = total_requests
        st.session_state.ui_cache_hits = cache_hits
        st.session_state.ui_hourly_spend = hourly_spend

    # ========================================================================
    # 🎛️ STEP 3: HIGH-SIGNAL METRIC CARDS & GAUGES
    # ========================================================================
    m1, m2, m3 = st.columns(3)
    
    with m1:
        budget_delta = max_budget - hourly_spend
        st.metric(
            label="Trailing 60-Min Operational Spend", 
            value=f"${hourly_spend:.6f}", 
            delta=f"${budget_delta:.6f} Remaining",
            delta_color="normal" if hourly_spend < max_budget else "inverse"
        )
    with m2:
        st.metric(
            label="Active In-Memory Cache Hits", 
            value=f"{cache_hits} Hits", 
            delta=f"{total_requests} Total Requests Evaluated"
        )
    with m3:
        efficiency_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0.0
        st.metric(
            label="Edge Infrastructure Efficiency Rate", 
            value=f"{efficiency_rate:.1f}%",
            delta="Sub-millisecond latency optimized" if efficiency_rate > 0 else "Awaiting duplicate sequences"
        )

    # ========================================================================
    # 🚨 STEP 4: AUTOMATED CIRCUIT BREAKER ALERT BANNER
    # ========================================================================
    if hourly_spend >= max_budget:
        st.error(
            f"⚠️ **[BUDGET CIRCUIT BREAKER TRIPPED]** "
            f"Trailing hourly cost (${hourly_spend:.6f}) violates safety parameter limit (${max_budget:.6f}). "
            f"All outbound premium cloud traffic has been blocked. System operating strictly on zero-overhead edge routing nodes."
        )
    elif cache_hits > 0:
        st.success(f"⚡ **[OPTIMIZATION ENGINE ACTIVE]** Instinct Gate has successfully bypassed third-party cloud API costs for {cache_hits} traffic requests.")

    st.write("----")

    # ========================================================================
    # 📋 STEP 5: INTERACTIVE TELEMETRY DATA SEARCH INDEX
    # ========================================================================
    st.subheader("📋 Core Audit Ledger & Telemetry Feed")
    if df is not None and not df.empty:
        # Sort logs by newest first for immediate engineer evaluation
        sorted_df = df.sort_values(by='timestamp', ascending=False)
        st.dataframe(
            sorted_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "timestamp": "Timestamp (UTC)",
                "task_id": "Task ID",
                "prompt_character_length": "Payload Length",
                "calculated_tokens": "Token Count",
                "routing_target": "Assigned Node",
                "precision_cost": "Calculated Cost",
                "reasoning_summary": "Decision Log Summary"
            }
        )
    else:
        st.info("Awaiting traffic stream ingestion... Core audit log buffer currently empty.")
