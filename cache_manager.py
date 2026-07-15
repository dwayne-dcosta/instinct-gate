import sys
from datetime import datetime, timedelta

# Global in-memory cache storage dictionary
# Format: { "clean_prompt_string": {"verdict": {...}, "expires_at": datetime} }
_routing_cache = {}

def get_cached_route(prompt):
    """
    Checks if an incoming prompt string exists in the cache matrix and is still valid.
    Returns the verdict dictionary if it hits, or None if it misses or expired.
    """
    global _routing_cache
    
    if not prompt:
        return None
        
    clean_prompt = str(prompt).strip()
    
    if clean_prompt in _routing_cache:
        cache_entry = _routing_cache[clean_prompt]
        
        # Check if the cache lifetime is still valid
        if datetime.utcnow() < cache_entry["expires_at"]:
            print(f"⚡ [CACHE HIT] Serving sub-millisecond optimized route for: '{clean_prompt[:30]}...'", file=sys.stderr)
            return cache_entry["verdict"]
        else:
            # Evict expired entry cleanly from RAM memory
            del _routing_cache[clean_prompt]
            
    return None

def set_cached_route(prompt, verdict, ttl_minutes=10):
    """
    Locks a successful prompt routing verdict into system RAM memory with a Time-To-Live expiration window.
    """
    global _routing_cache
    
    if not prompt or not verdict:
        return
        
    clean_prompt = str(prompt).strip()
    expiration_time = datetime.utcnow() + timedelta(minutes=int(ttl_minutes))
    
    _routing_cache[clean_prompt] = {
        "verdict": verdict,
        "expires_at": expiration_time
    }
