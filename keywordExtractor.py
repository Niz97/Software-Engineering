'''
@Description: function that extracts keywords from top headlines in the specified country
@Version: 1.0.1.20191026
@Author: Jichen Zhao
@Date: 2019-10-22 15:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-10-26 15:39:11
'''

from newspaper import Article
import nltk


def ExtractKeywords(newsApi, countryCode):
    '''
    If the keyword list returned is an empty list, there may be an error or no top headlines got from News API.
    '''

    try:
        '''
        get the query result of top headlines in the specified country;
        for more information about the top headline endpoint, please refer to: https://newsapi.org/docs/endpoints/top-headlines
        '''
        topH = newsApi.get_top_headlines(country = countryCode, language = 'en')
    except Exception as e:
        return []
    else:
        totalCount = topH['totalResults']

    if (totalCount > 0):
        newsList = topH['articles'] # the value paired with the key "articles" is a list of top headlines got from News API
        keywordList = []

        nltk.download('punkt') # this file is required by the following function nlp()
        
        '''
        loop to get a list of all keywords;
        generally, the value paired with the key "totalResults" is NOT equivalent to the length of the list of top headlines got from News API because not all available top headlines are returned from the server
        '''
        for count in range(len(newsList) - 1):
            news = newsList[count] # each entry of the list is a dictionary of the info of 1 top headline
            
            content = Article(news['url'], language = 'en')
            content.download()
            content.parse()
            content.nlp()
            keywordList.append(content.keywords)

        return keywordList
    else:
        return []