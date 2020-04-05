from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Union


@dataclass
class NewsApiArticle:
    source: Dict[str, str]
    author: str
    title: str
    description: str
    url: str
    url_to_image: str
    published_at: str
    content: str


@dataclass
class NewsApiOkayResponse:
    status: str
    total_results: int
    articles: List[NewsApiArticle]


@dataclass
class NewsApiErrorResponse:
    status: str
    code: str
    message: str


NewsApiResponse = Union[NewsApiOkayResponse, NewsApiErrorResponse]
