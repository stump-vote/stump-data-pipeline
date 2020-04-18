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


@pytest.mark.parametrize(
    "endpoint,query,date_from,date_to,sort_by,expected",
    (
        (
            "everything",
            "trump",
            None,
            None,
            None,
            f"http://newsapi.org/v2/everything?apiKey={NEWS_API_KEY}&q=trump",
        ),
    ),
)
def test_make_url(
    news_api_client, endpoint, query, date_from, date_to, sort_by, expected
):
    url = news_api_client._make_url(endpoint, query, date_from, date_to, sort_by)
    assert url == expected
