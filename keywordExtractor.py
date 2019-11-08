'''
@Description: keyword extractor that extracts keywords from the news content downloaded from each URL
@Version: 2.5.0.20191108
@Author: Jichen Zhao (driver) and Connor Worthington (observer)
@Date: 2019-10-29 14:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-08 15:44:55
'''

from newspaper import Config, Article
import nltk


def ExtractKeywords(urlList):
    '''
    (TODO:) If the keyword list returned is an empty list, there may be an error or no top headlines got from News API.
    '''
    
    if len(urlList) > 0:
        keywordList = []

        articleConfig = Config()
        articleConfig.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' # avoid Newspaper3k 403 Client Error for some URLs
        nltk.download('punkt') # TODO: only needs once, this file is required by the following function nlp()
        
        # loop to get a list of all keywords
        for count in range(len(urlList) - 1):
            content = Article(urlList[count].strip(), language = 'en', config = articleConfig)
            content.download()

            try:
                content.parse()
            except Exception as e:
                # TODO: consider error logs
                print('URL error')
            else:
                content.nlp()
                keywordList.append(content.keywords) # TODO: the order of keywords always changes, too many

        # true if Newspaper3k fails to parse the news content downloaded from all URLs
        if len(keywordList) == 0:
            # TODO: consider logs
            print('Keyword extraction failure')

        return keywordList
    else:
        # TODO: consider logs
        return []