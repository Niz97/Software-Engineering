'''
@Description: keyword extractor that can extract keywords from the news content downloaded from each URL
@Version: 2.7.2.20191109
@Author: Jichen Zhao (driver) and Connor Worthington (observer)
@Date: 2019-10-29 14:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-09 06:50:02
'''

from newspaper import Config, Article
import nltk

from logTool import Log


def ExtractKeywords(urlList: list) -> list:
    '''
    This function can extract keywords from the news content downloaded from each URL.

    :param urlList: a list of URLs containing the news content for keyword extraction
    :returns: a list of all keywords extracted
    '''
    
    if len(urlList) > 0:
        keywordList = []

        articleConfig = Config()
        articleConfig.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' # avoid Newspaper3k 403 Client Error for some URLs
        nltk.download('punkt') # the package punkt is required by the following function nlp()
        
        # loop to get a list of all keywords
        for count in range(len(urlList)):
            content = Article(urlList[count].strip(), language = 'en', config = articleConfig)
            content.download()

            try:
                content.parse()
            except Exception as e:
                Log('error', repr(e))
            else:
                content.nlp()
                keywordList.append(content.keywords) # TODO: the order of keywords always changes, too many

        # true if Newspaper3k fails to parse any news content downloaded
        if len(keywordList) == 0:
            Log('warning', 'It seems that Newspaper3k fails to parse any news content downloaded.')

        return keywordList
    else:
        Log('warning', 'The URL list is empty.')
        return []


# test purposes only
if __name__ == '__main__':
    from pullNews import get_headlines

    urlList = get_headlines('gb')
    keywordList = ExtractKeywords(urlList)
    
    print(len(urlList), 'URL(s):\n', urlList)
    print(len(keywordList), 'group(s) of keywords:\n', keywordList)