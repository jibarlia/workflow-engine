def pytest_configure(config):
    config.addinivalue_line(
        "markers", "asyncio: mark test to be run with asyncio"
    )