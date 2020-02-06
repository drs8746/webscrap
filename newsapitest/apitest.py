from newsapi import NewsApiClient


def retrieve_news(api_key, query, language='en'):
  # Init
  newsapi = NewsApiClient(api_key=api_key)

  # /v2/top-headlines
  top_headlines = newsapi.get_top_headlines(q=query,language=language)

  return top_headlines

def main():
    api_key = r''
    query ='bitcoin'
    #STEP1: retrieve news using query and language parameters 
    news = retrieve_news(api_key, query)
    print(news)

if __name__ == '__main__':
    main()