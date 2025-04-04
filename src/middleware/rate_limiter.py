from fastapi import Request, HTTPException
from src.databases.redis import redis_client
import time
from src.config import config

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    def allow_request(self, identifier: str) -> bool:
        """ Verifica se o identificador pode realizar novas requisições com base no limite e tempo de expiração.
            :param identifier: Representa o user_id, esta sendo usando o primeiro ip da lista de "X-Forwarded-For"

            :return: retorna um boolean, True para permitido e False caso exceda o limite.
        """
        now = int(time.time())
        key = f"rate_limit:{identifier}:{now // config.TIME_SECONDS}"
        
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, config.TIME_SECONDS)

        # Vou deixar aqui para caso queira acompanhar a contagem de requests pelo console
        print('ip:', identifier, 'count:', count)
        return count <= config.MAX_REQUESTS_PER_MINUTE

limiter = RateLimiter(redis_client)

def rate_limit_dependency(request: Request):
    forward_for = request.headers.get("X-Forwarded-For")
    client_ip = forward_for.split(",")[0] if forward_for else request.client.host
    if not limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")