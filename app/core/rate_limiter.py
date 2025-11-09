from datetime import datetime, timedelta, timezone
from collections import defaultdict
from fastapi import HTTPException, status

from app.core.config import settings


class RateLimiter:
    def __init__(self, limit: int = settings.RATE_LIMIT_PER_MINUTE, window_seconds: int = 60):
        self.limit = limit
        self.window = timedelta(seconds=window_seconds)
        self._requests = defaultdict(list)

    def __clean_request_list(self, client_id:str)->None:
        now=datetime.now(timezone.utc)
        self._requests[client_id] = [
            request_time for request_time in self._requests[client_id] if (now - request_time).total_seconds() < self.window.total_seconds()
        ]

        if not self._requests[client_id]:
            del self._requests[client_id]

    def __check_limit(self,client_id:str)->bool:
        now=datetime.now(timezone.utc)
        self.__clean_request_list(client_id)
        if len(self._requests.get(client_id, [])) >= self.limit:
            return False
        self._requests[client_id].append(now)
        return True

    def check_rate_limit(self, client_id: str)->None:
        if not self.__check_limit(client_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {self.limit} requests per {int(self.window.total_seconds())} seconds.",
                headers={"Retry-After": str(int(self.window.total_seconds()))}
            )