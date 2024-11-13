import redis
import json

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_message(key, value):
    if not redis_client.exists(key):
        redis_client.set(key, value)
        return True
    return False

def get_cached_data():
    keys = redis_client.keys()
    data = []
    
    for key in keys:
        value = redis_client.get(key)
        if value:
            try:
                data.append(json.loads(value))
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON data for key {key}. Skipping...")
    
    return data