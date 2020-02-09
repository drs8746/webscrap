import sys
import configparser
from newsapi import NewsApiClient


class NewsorgApiError(Exception):
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload

    def __str__(self):
        return str(self.message)


def retrieve_news_head(api_key, query, language='en'):

    try:
        # Init
        newsapi = NewsApiClient(api_key=api_key)
        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(q=query, language=language)
    except:
        raise NewsorgApiError("API request is invalid")

    return top_headlines


def retrieve_news_everything(api_key, query, langauge='en'):
    try:
        # Init
        newsapi = NewsApiClient(api_key=api_key)
        # /v2/top-headlines
        res_everything = newsapi.get_everything(q=query, language=language)
    except:
        raise NewsorgApiError("API request is invalid")


def main(query):

    config = configparser.ConfigParser()
    config.read('./news_org.config')
    api_key = config.get('news_org', 'api_key')

    # STEP1: retrieve news using query and language parameters
    news = retrieve_news(api_key, query)
    print(news)


if __name__ == '__main__':
    query = sys.argv[1]
    main(query)
