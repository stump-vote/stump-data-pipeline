import json
import os

from api_clients.news_api_client import NewsAPIClient

import pytest

NEWS_API_KEY = "test_key"
TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


@pytest.fixture(scope="module")
def news_api_client():
    global NEWS_API_KEY
    client = NewsAPIClient(NEWS_API_KEY)
    with open(
        os.path.join(TEST_DATA_DIR, "mock_news_api_client_okay_response.json")
    ) as f:
        client.MOCK_OKAY_RESPONSE = json.loads(f.read())
    with open(
        os.path.join(TEST_DATA_DIR, "mock_news_api_client_error_response.json")
    ) as f:
        client.MOCK_ERROR_RESPONSE = json.loads(f.read())
    return client


# test_make_url
@pytest.mark.parametrize(
    "endpoint, kwargs, expected",
    (
        (
            "everything",
            {
                'page': 1,
                'page_size': 100,
                'query': 'trump',
            },
            f"http://newsapi.org/v2/everything?apiKey={NEWS_API_KEY}&page=1&pageSize=100&q=trump",
        ),
        (
            # test sources parameter
            "everything",
            {
                'page': 1,
                'page_size': 100,
                'query': 'trump',
                'sources': ['cnn', 'techcrunch'],
            },
            f"http://newsapi.org/v2/everything?apiKey={NEWS_API_KEY}&page=1&pageSize=100&q=trump&sources=cnn,techcrunch",

        ),
    ),
)
def test_make_url(
    news_api_client, endpoint, kwargs, expected
):
    url = news_api_client._make_url(endpoint, **kwargs) 
    assert url == expected
