# Overview
This repo contains a collection of tools for collecting, cleaning, and analyzing data to be consumed by the Stump web app.

# API Clients
## News Api
  - [Documentation](https://newsapi.org/docs)
  - Demo: executed in python shell from `/src/stump_data_pipeline`
  ```python
  from api_clients import NewsAPIClient
  client = NewsAPIClient(<your-api-key>)
  sources = client.get_sources()
  sources_dict = sources.to_json()
  response = client.get_everything()
  articles_list = response.to_json()['articles']
  ```
