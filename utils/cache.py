import time
from threading import Lock


class RateLimitedCache:
    def __init__(self, max_calls_per_minute=30):
        self.cache = {}
        self.timestamps = []
        self.max_calls = max_calls_per_minute
        self.lock = Lock()

    def get_data(self, key, fetch_func):
        """
        Returns cached data if available and fresh; otherwise,
        calls the provided function to fetch data and caches it.
        """
        with self.lock:
            now = time.time()
            # Remove timestamps older than 60 seconds
            self.timestamps = [t for t in self.timestamps if now - t < 60]

            if len(self.timestamps) >= self.max_calls:
                sleep_time = 60 - (now - self.timestamps[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)

            self.timestamps.append(now)

            # Use cached data if it's less than an hour old
            if key in self.cache:
                cache_age = now - self.cache[key]["timestamp"]
                if cache_age < 3600:
                    return self.cache[key]["data"]

            # Otherwise, fetch new data, cache it, and return it
            data = fetch_func()
            self.cache[key] = {"data": data, "timestamp": now}
            return data
