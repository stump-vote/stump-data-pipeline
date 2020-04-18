from datetime import datetime

from api_clients import NewsAPIClient
from api_clients.news_api_client import FILTER_BY_OPTIONS
from env import env

import pytest


@pytest.fixture(scope="module")
def news_api_client():
    client = NewsAPIClient(api_key=env.NEWS_API_KEY)
    return client


def test_news_api_client_basic_response(news_api_client):
    # the news api client should be able to make a request to
    # the google news apis everything endpoint
    okay_response = news_api_client.get_everything(query="bitcoin").to_json()
    assert okay_response["status"] == "ok"


def test_news_api_client_date_range(news_api_client):

    today = datetime.now().strftime("%Y-%m-%d")
    # it should be possible to specify a date range
    okay_response = news_api_client.get_everything(
        query="trump", date_to=today, date_from=today
    ).to_json()
    assert okay_response["status"] == "ok"
    articles = okay_response["articles"]
    assert all(
        a["published_at"].startswith(today) for a in articles
    ), "article not published today"


def test_news_api_get_sources(news_api_client):

    # it should be possible to see which sources are available
    okay_response = news_api_client.get_sources().to_json()
    assert okay_response["status"] == "ok"
    assert "sources" in okay_response
    assert len(okay_response["sources"]) > 0

    # only english language sources should be returned
    # only sources from the us should be returned
    for source in okay_response["sources"]:
        assert source["language"] == "en"
        assert source["country"] == "us"


# it should be possible to limit the result to specific sources
def test_filter_by_source(news_api_client):
    response = news_api_client.get_everything(
        query="python", sources=["techcrunch"],
    ).to_json()
    assert response["status"] == "ok"
    articles = response["articles"]
    for article in articles:
        source = article["source"]
        assert source["id"] == "techcrunch"
    # the client will fail before making a request if more than 20 sources
    # are requested


def test_filter_by_source_value_error(news_api_client):
    with pytest.raises(ValueError) as e:
        response = news_api_client.get_everything(
            query="covid-19", sources=[f"source-{i}" for i in range(21)]
        )
        assert str(e) == "Too many sources specified. Use a max of 20."
    # it should be possible to limit the number of results returned


def test_limit_page_size(news_api_client):
    response = news_api_client.get_everything(query="bitcoin", page_size=5).to_json()
    articles = response["articles"]
    assert len(articles) == 5

    # it should be possible to query the full article content


@pytest.mark.skip(
    reason="news content abbreviated, so it might not contain the exact query"
)
def test_query_article_content(news_api_client):
    response = news_api_client.get_everything(query="bitcoin", page_size=5).to_json()
    articles = response["articles"]
    for article in articles:
        assert (
            "bitcoin" in article["title"].lower()
            or "bitcoin" in article["content"].lower()
        )
    # it should also be possible to just query the article's title

    # we can query for specific domains


def test_filter_by_domain(news_api_client):
    response = news_api_client.get_everything(
        query="trump", page_size=5, domains=["wsj.com"]
    ).to_json()
    articles = response["articles"]
    assert response["status"] == "ok"
    for article in articles:
        url = article["url"]
        assert "wsj.com" in url

    # we can also exclude domains


def test_exclude_domain(news_api_client):
    response = news_api_client.get_everything(
        query="trump", page_size=5, domains=["wsj.com"], exclude_domains=["axios.com"]
    ).to_json()
    articles = response["articles"]
    assert response["status"] == "ok"
    for article in articles:
        url = article["url"]
        assert "wsj.com" in url


# we can sort the results by relevancy, popularity, and date published
@pytest.mark.parametrize(
    "sort_by_option", (("popularity",), ("relevancy",), ("publishedAt",),)
)
def test_sort_by(news_api_client, sort_by_option):
    response = news_api_client.get_everything(
        query="trump", page_size=5, sort_by=sort_by_option
    ).to_json()
    assert response["status"] == "ok"

@pytest.mark.parametrize('expected_error, expected_msg, kwargs', (
    (
        ValueError,
        f'Invalid choice for filter_by parameter. Use one of {",".join(list(FILTER_BY_OPTIONS))}',
        {
            'filter_by': 'unknown',
        },
    ),
))
def test_get_everything_errors(news_api_client, expected_error, expected_msg, kwargs):
    with pytest.raises(expected_error) as excinfo:
        news_api_client.get_everything(**kwargs)
    assert str(excinfo.value) == expected_msg

