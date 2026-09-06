class Statistics:
    def __init__(self):
        self.urls_created=0
        self.redirects=0
        self.cache_hits=0
        self.cache_misses=0
        self.rate_limited=0
        
    def snapshot(self):
        return{
            "urls_created":self.urls_created,
            "redirects":self.redirects,
            "cache_hits":self.cache_hits,
            "cache_misses":self.cache_misses,
            "rate_limited":self.rate_limited,
        }