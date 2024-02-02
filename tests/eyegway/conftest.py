import pytest
import redis.asyncio as aioredis


@pytest.fixture
def redis_test_mock_async() -> aioredis.Redis:
    import fakeredis

    return fakeredis.FakeAsyncRedis()
