from dataclasses import dataclass, asdict
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

    def to_json(self):
        return asdict(self)


@dataclass
class NewsApiOkayResponse:
    status: str
    total_results: int
    articles: List[NewsApiArticle]

    def to_json(self):
        return {
            'status': self.status,
            'total_results': self.total_results,
            'articles': [a.to_json() for a in self.articles],
        }

@dataclass
class NewsApiErrorResponse:
    status: str
    code: str
    message: str

    def to_json(self):
        return asdict(self)

@dataclass
class NewsApiSource:
    id: str
    name: str
    description: str
    url: str
    category: str
    language: str
    country: str

    def to_json(self):
        return asdict(self)


@dataclass
class NewsApiSourcesOkayResponse:
    status: str
    sources: List[NewsApiSource]

    def to_json(self):
        return {
            'status': self.status,
            'sources': [s.to_json() for s in self.sources],
            }


NewsApiResponse = Union[NewsApiOkayResponse, NewsApiErrorResponse]
