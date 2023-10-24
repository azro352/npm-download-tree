from functools import lru_cache

from requests import Session
from requests.adapters import HTTPAdapter, Retry


class CachedSession(Session):
    @lru_cache(2048)
    def get(self, url, **kwargs):
        return super().get(url, **kwargs)


session = CachedSession()

retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))
