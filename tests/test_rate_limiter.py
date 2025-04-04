import pytest
from unittest.mock import MagicMock
from src.middleware.rate_limiter import RateLimiter
from src.config import config
from unittest.mock import ANY

@pytest.fixture
def mock_redis():
    """Mock do Redis client"""
    mock = MagicMock()
    call_count = {}

    def mock_incr(key):
        """Simula um contador do Redis"""
        if key not in call_count:
            call_count[key] = 0
        call_count[key] += 1
        return call_count[key]

    mock.incr.side_effect = mock_incr
    return mock

@pytest.fixture
def rate_limiter(mock_redis):
    """Instancia RateLimiter com mock do Redis"""
    return RateLimiter(mock_redis)

def test_allow_first_request(rate_limiter, mock_redis):
    """Deve permitir a primeira requisição e armazenar no Redis"""
    mock_redis.incr.return_value = 1

    assert rate_limiter.allow_request("user_123") is True
    mock_redis.expire.assert_called_once_with(ANY, config.TIME_SECONDS)

def test_allow_multiple_requests_within_limit(rate_limiter, mock_redis):
    """Deve permitir requisições dentro do limite"""
    for _ in range(config.MAX_REQUESTS_PER_MINUTE - 1):
        assert rate_limiter.allow_request("user_123") is True
    
    assert mock_redis.incr.call_count == config.MAX_REQUESTS_PER_MINUTE - 1

def test_block_excess_requests(rate_limiter):
    """Deve bloquear requisições acima do limite"""
    for _ in range(config.MAX_REQUESTS_PER_MINUTE):
        assert rate_limiter.allow_request("user_123") is True

    # A próxima requisição deve ser bloqueada, por atingir o limite
    assert rate_limiter.allow_request("user_123") is False
