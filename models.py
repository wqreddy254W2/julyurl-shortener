from dataclasses import dataclass
from datetime import datetime

@dataclass
class URLRecord:
    short_code:str
    original_url:str
    created_at:datetime
    expires_at:datetime