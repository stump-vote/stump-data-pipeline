import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from dataclasses import asdict
from datetime import datetime
import math

from api_clients.news_api_client import NewsAPIClient
from models.news_api_article import NewsApiArticle, NewsApiErrorResponse, NewsApiOkayResponse, NewsApiResponse
from mongo_client import connect_to_mongo

PAGE_SIZE = 5
MAX_PAGES_PER_QUERY = 2

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
MONGO_USER = os.environ.get('MONGO_USER', 'stump')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'stump')
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27018))
MONGO_DB = os.environ.get('MONGO_DB', 'test_two')

QUERIES = [
    'Abortion',
    'Budget',
    'Campaign Finance', 
    'Defense',
    'Economy',
    'Education',
    'Energy',
    'Environment',
    'Guns',
    'Healthcare',
    'Immigration',
    'National Security',
    'Trade',
]

def fetch_news_api_data(queries=QUERIES, news_api_key=NEWS_API_KEY, mongo_user=MONGO_USER, mongo_password=MONGO_PASSWORD,
                        mongo_host=MONGO_HOST, mongo_port=MONGO_PORT, mongo_db=MONGO_DB):
    api_client = NewsAPIClient(news_api_key)
    mongo_client = connect_to_mongo(mongo_user, mongo_password, mongo_host, mongo_port)

    db = mongo_client[mongo_db]
    for query in queries:
        collection = db[query]
        today = datetime.now().strftime('%Y-%m-%d')
        response = api_client.get_everything(query, date_from=today,
                                                date_to=today,
                                                page_size=PAGE_SIZE, page=1)
        n_pages = min(MAX_PAGES_PER_QUERY, int(math.ceil(response.total_results / PAGE_SIZE)))
        for page in range(1, n_pages+1):
            if page > 1:
                response = api_client.get_everything(query, date_from=today,
                                                    date_to=today,
                                                    page_size=PAGE_SIZE, page=page)
            articles = [asdict(article) for article in response.articles]
            collection.insert_many(articles)


if __name__ == '__main__':

    fetch_news_api_data()
