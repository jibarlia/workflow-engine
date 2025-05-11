import pytest
from app.redis_client import RedisClient
from tests.utils import FakeRedis

@pytest.mark.asyncio
async def test_redis_client_initialization():
    # Test default initialization
    client = RedisClient()
    assert client.client is not None
    assert client.client.connection_pool.connection_kwargs['host'] == 'localhost'
    assert client.client.connection_pool.connection_kwargs['port'] == 6379
    assert client.client.connection_pool.connection_kwargs['db'] == 0

    # Test custom initialization
    client = RedisClient(host='redis.example.com', port=6380, db=1)
    assert client.client.connection_pool.connection_kwargs['host'] == 'redis.example.com'
    assert client.client.connection_pool.connection_kwargs['port'] == 6380
    assert client.client.connection_pool.connection_kwargs['db'] == 1

@pytest.mark.asyncio
async def test_redis_client_get_client():
    client = RedisClient()
    redis_client = client.get_client()
    assert redis_client is not None
    assert redis_client == client.client

@pytest.mark.asyncio
async def test_redis_client_operations():
    # Use FakeRedis for testing operations
    fake_redis = FakeRedis()
    client = RedisClient()
    client.client = fake_redis

    # Test hset operation
    await client.client.hset('test_key', 'field1', 'value1')
    result = await client.client.hgetall('test_key')
    assert result == {'field1': 'value1'}

    # Test hset with mapping
    await client.client.hset('test_key2', mapping={'field1': 'value1', 'field2': 'value2'})
    result = await client.client.hgetall('test_key2')
    assert result == {'field1': 'value1', 'field2': 'value2'} 