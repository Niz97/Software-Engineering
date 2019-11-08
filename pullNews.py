# figure out how to request an article and its headline
# method to be used in keywordExtractor
# should pull headlines 
# get URL of where the headlines exist

# Pair programming Authors: 
# Driver: Niran Prajapati
# Observer: Alexandra Garton

from newsapi import NewsApiClient


def get_headlines(countryCode):

  newsApi = NewsApiClient(api_key = '3bd762aea6134796b564d8e18df60cf8') # handle authentication with a News API key (registered using zjcarvin@outlook.com)

  try:
  	# get top headlines from "source"
  	top_headlines = newsApi.get_top_headlines(country = countryCode, language = 'en')
  except Exception as e:
  	return []
  else:
  	num_articles = len(top_headlines['articles'])

  	if (num_articles > 0):
  		headlines = []
  		# get and append all article URL's
  		for i in range(num_articles):
  			headlines.append(top_headlines['articles'][i]['url'])

  		return headlines
  	else:
  		return []

############ END OF FEATURE ############ 

# test purposes only
if __name__ == '__main__':
	print(get_headlines('gb'))