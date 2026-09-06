import threading 


class URLStorage:
    def __init__(self):
        self.urls={}
        self._lock=threading.RLock()
        
        def save(self, record):
            with self._lock:
                self.urls[record.short_code]=record

        def get(self, short_code):
            with self._lock:
                return self.urls.get(short_code)
            
        def exists(self, short_code):
            with self._lock:
                return short_code in self._urls

        def delete(self, short_code):
            with self._lock:
                self.urls.pop(short_code)

        def count(self):
            with self._lock:
                return len(self._urls)