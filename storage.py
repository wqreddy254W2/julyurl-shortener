class URLStorage:
    def __init__(self):
        self.urls={}
        
        def save(self, record):
            self.urls[record.short_code]=record
            def get(self, short_code):
                return self.urls.get(short_code)
            def delete(self, short_code):
                self.urls.pop(short_code)
                def exists(self, short_code):
                    return short_code in self.urls