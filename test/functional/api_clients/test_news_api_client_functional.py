from api_clients import NewsAPIClient
import env

import pytest


@pytest.fixture(scope='module')
def news_api_client():
    client = NewsAPIClient(api_key=env.news_api_key)
    return client


def test_news_api_client(news_api_client):
    pass
    # the news api client should be able to make a request to
    # the google news apis everything endpoint

    # it should be possible to specify a date range

    # it should be possible to limit the result to specific sources

    # it should be possible to limit the number of results returned

    # it should be possible to query the full article content

    # it should also be possible to just query the article's title

    # we can query for specific domains

    # we can also exclude domains

    # we can sort the results by relevancy, popularity, and date published
