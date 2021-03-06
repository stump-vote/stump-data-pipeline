import json
from typing import List, Optional, Union, Iterable

from models.news_api_article import (
    NewsApiArticle,
    NewsApiResponse,
    NewsApiErrorResponse,
    NewsApiOkayResponse,
    NewsApiSourcesOkayResponse,
    NewsApiSource,
)
from util.dictionary import convert_keys_from_camel_to_snake

import requests


FILTER_BY_OPTIONS = frozenset({"relevancy", "popularity", "publishedAt"})


class NewsAPIClient:

    BASE_URL = "http://newsapi.org/v2"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __repr__(self) -> str:
        return "NewsAPIClient()"

    def _make_url(
        self,
        endpoint: str,
        query: str = None,
        date_from: str = None,
        date_to: str = None,
        sort_by: str = None,
        page_size: int = 100,
        page: int = 1,
        title_query: str = None,
        sources: Iterable = None,
        domains: Iterable = None,
        exclude_domains: Iterable = None,
        filter_by: str = None,
    ) -> str:
        if endpoint[0] == "/":
            endpoint = endpoint[1:]
        endpoint_url = f"{self.BASE_URL}/{endpoint}"
        query_params = {
            "q": query,
            "apiKey": self.api_key,
            "pageSize": page_size,
            "page": page,
        }
        if date_from is not None:
            query_params["from"] = date_from
        if date_to is not None:
            query_params["to"] = date_to
        if sort_by is not None:
            query_params["sortBy"] = sort_by
        if sources is not None:
            query_params["sources"] = ",".join(str(source) for source in sources)
        if title_query is not None:
            query_params["qInTitle"] = title_query
        if domains is not None:
            query_params["domains"] = ",".join([str(domain) for domain in domains])
        if exclude_domains is not None:
            query_params["excludeDomains"] = ",".join(
                [str(domain) for domain in exclude_domains]
            )
        if filter_by is not None:
            query_params["filterBy"] = filter_by
        query_string_args = sorted([f"{k}={v}" for k, v in query_params.items()])
        query_string = "&".join(query_string_args)

        return f"{endpoint_url}?{query_string}"

    def _make_get_request(self, url: str) -> requests.Response:
        return requests.get(url)

    def _parse_response(self, response: requests.Response) -> NewsApiResponse:
        data = json.loads(response.text)
        data = convert_keys_from_camel_to_snake(data)

        if data["status"] != "ok":
            return NewsApiErrorResponse(**data)

        data["articles"] = [NewsApiArticle(**article) for article in data["articles"]]
        return NewsApiOkayResponse(**data)

    def get_everything(
        self,
        query: str = None,
        date_from: str = None,
        date_to: str = None,
        sort_by: str = None,
        page_size: int = 100,
        page: int = 1,
        title_query: str = None,
        sources: Iterable = None,
        domains: Iterable = None,
        exclude_domains: Iterable = None,
        filter_by: str = None,
    ) -> NewsApiResponse:
        if filter_by is not None and filter_by not in FILTER_BY_OPTIONS:
            raise ValueError(
                f'Invalid choice for filter_by parameter. Use one of {",".join(list(FILTER_BY_OPTIONS))}'
            )
        if sources is not None and len(sources) > 20:
            raise ValueError("Too many sources specified. Use a max of 20.")
        url = self._make_url(
            "everything",
            query,
            date_from,
            date_to,
            sort_by,
            page_size,
            page,
            title_query,
            sources,
            domains,
            exclude_domains,
            filter_by,
        )
        response = self._make_get_request(url)
        return self._parse_response(response)

    def get_sources(self) -> Union[NewsApiSourcesOkayResponse, NewsApiErrorResponse]:
        url = self.BASE_URL + "/sources"
        params = {"apiKey": self.api_key, "language": "en", "country": "us"}
        query_str = "&".join([f"{k}={v}" for k, v in params.items()])
        res = self._make_get_request(f"{url}?{query_str}")
        data = json.loads(res.text)
        if data["status"] != "ok":
            return NewsApiErrorResponse(**data)
        data = convert_keys_from_camel_to_snake(data)
        data["sources"] = [NewsApiSource(**source) for source in data["sources"]]
        return NewsApiSourcesOkayResponse(**data)
