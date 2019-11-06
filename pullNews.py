# figure out how to request an article and its headline
# method to be used in keywordExtractor
# should pull headlines 
# get URL of where the headlines exist

# Pair programming Authors: 
# Driver: Niran Prajapati
# Observer: Alexandra Garton


def get_headlines(countryCode, lang):

  l = lang

  try:
  	# get top headlines from "source"
  	top_headlines = newsapi.get_top_headlines(country = countryCode, language = l)
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

# print(get_headlines('gb', 'en'))