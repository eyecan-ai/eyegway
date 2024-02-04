import pytest
import redis.asyncio as aioredis
import redis


@pytest.fixture
def redis_test_mock_async() -> aioredis.Redis:
    import fakeredis

    return fakeredis.FakeAsyncRedis()


@pytest.fixture
def redis_test_mock_sync() -> redis.Redis:
    import fakeredis

    return fakeredis.FakeRedis()
