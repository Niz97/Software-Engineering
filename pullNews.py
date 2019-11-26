# figure out how to request an article and its headline
# method to be used in keywordExtractor
# should pull headlines 
# get URL of where the headlines exist

# Pair programming Authors: 
# Driver: Niran Prajapati
# Observer: Alexandra Garton

from newsapi import NewsApiClient

from logTool import Log


def get_headlines(source):
  
  newsApi = NewsApiClient(api_key = '3bd762aea6134796b564d8e18df60cf8') # handle authentication with a News API key (registered using zjcarvin@outlook.com)
  titles = []
  urls = []

  try:
  	# get top headlines from "source"
  	top_headlines = newsApi.get_top_headlines(sources = source, language = 'en')
  except Exception as e:
  	Log('error', repr(e))
  else:
  	num_articles = len(top_headlines['articles'])

  	if (num_articles > 0):
  		# get and append all article URL's
  		for i in range(num_articles):
  			titles.append(top_headlines['articles'][i]['title'])
  			urls.append(top_headlines['articles'][i]['url'])
  	else:
  		Log('warning', 'The top headline list is empty.')
  
  return titles, urls

############ END OF FEATURE ############ 

# test purposes only
if __name__ == '__main__':
	print(get_headlines('bbc-news'))