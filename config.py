# config.py - Centralized Configuration for the Generalist LLM Endpoints.
import os

# 1. API Configuration Object
# This dictionary dynamically binds endpoints and runtime tokens injected by the evaluation harness.
MODELS = {
    "local_cheap": {
        # Points to your local machine serving framework or your raw AMD Cloud pod vLLM instance.
        "url": os.getenv("AMD_LOCAL_API_URL", "http://localhost:8000/v1"),
        "key": "fake-local-key",
        "name": "meta-llama/Llama-3-8B-Instruct"
    },
    "remote_premium": {
        # CRITICAL UPDATE: Points directly to the automated grading engine's injected base routing url.
        "url": os.getenv("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1"),
        # CRITICAL UPDATE: Pulls the official system key at runtime without hardcoding sensitive strings.
        "key": os.getenv("FIREWORKS_API_KEY", ""),
        # UPDATE: Dynamically reads the official leaderboard model choice, defaulting to the optimal Qwen layer.
        "name": os.getenv("FIREWORKS_MODEL_NAME", "accounts/fireworks/models/qwen2p5-coder-32b-instruct")
    }
}

# 2. Dynamic Array Mapping for the Disclosed Track 1 Models List
# This list extracts the permitted model string array dynamically from the testing VM if provided.
ALLOWED_MODELS_STR = os.getenv("ALLOWED_MODELS", "")
ALLOWED_MODELS = ALLOWED_MODELS_STR.split(",") if ALLOWED_MODELS_STR else [
    "minimax-m3",
    "kimi-k2p7-code",
    "gemma-4-31b-it",
    "gemma-4-26b-a4b-it",
    "gemma-4-31b-it-nvfp4"
]

# 3. Thresholds constraints for Track 1 Router Logic.
# If a prompt exceeds these metrics, it triggers specific conditional actions.
TOKEN_LIMIT_LOCAL = 150 # Max context token ceiling before routing to Fireworks AI.
MOCK_BUDGET_LIMIT = 106.00 # UPDATE: Upgraded to track your full enterprise credit monopoly safety envelope.
