import threading
import time

class RateLimiter:
    def __init__(self, limit=70, window=70):
        self.limit=limit
        self.window_seconds=window_seconds
        self.request={}
        self._lock=theading.RLock()
        def allow(self, client):
            now=time.time()
            timestamps=self.requests.get(client,[])
            timestamps=[
                timestamp
                for timestamp in timestamps
                if now-timestamp<self.window
            ]
            
            if len(timestamps)>=self.limit:
                self.requests[client]=timestamps
                return False
            
            timestamps.append(now)
            self.requests[client]=timestamps
            
            return True