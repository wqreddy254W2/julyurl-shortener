import threading
import time

class Cache:
    def __init__(self,ttl=300):
        self.data={}
        self.ttl=ttl
        self._lock=threading.RLock()
        
    def set(self, key, value):
        with self._lock:
            expires_at=time.time()+self._ttl
        self.data[key]=(value, time.time()+self.ttl)
        
    def get(self,key):
        with self._lock:
         item = self._data.get(key)
        
        if item is None:
           return None

        value, expires_at=item
        
        if time.time()>=expires_at:
            del self.data[key]
            return None
        
        return value
    
        def delete(self, key):
            with self._lock:
                self.data.pop(key, None)
      
        def clear(self):
            with self._lock:
             self.data.clear()