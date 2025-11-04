import redis


def get_all_redis_cache_keys():
    # Connect to your Redis instance (use the same settings as your Django cache)
    r = redis.StrictRedis.from_url('redis://tuto_django_redis:6379/1')  # Update with your actual Redis settings

    # Use SCAN for better performance (vs KEYS, which can block)
    keys = r.scan_iter()  # Iterates over keys in the Redis instance
    return list(keys)  # Convert iterator to a list (or handle as needed)


def delete_cache_by_prefix(prefix):
    # Connect to Redis directly (using the same settings as Django)
    r = redis.StrictRedis.from_url('redis://tuto_django_redis:6379/1')

    # Scan all keys with the specified prefix
    keys = r.scan_iter(match=f"{prefix}*")  # Match keys starting with the prefix

    # Delete each key
    for key in keys:
        r.delete(key)
    print(f"Deleted cache keys with prefix: {prefix}")
