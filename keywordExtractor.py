'''
@Description: keyword extractor that can extract keywords from the news content downloaded from each URL
@Version: 3.0.0.20191110
@Author: Jichen Zhao (driver) and Connor Worthington (observer)
@Date: 2019-10-29 14:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-10 02:55:01
'''

from newspaper import Config, Article
from gensim.summarization import keywords

from logTool import Log


def ExtractKeywords(urlList: list) -> list:
    '''
    This function can extract keywords from the news content downloaded from each URL.

    :param urlList: a list of URLs from which the news content will be downloaded for keyword extraction
    :returns: a keyword list whose elements are lists of keywords extracted from each news (no more than 5 words in each list)
    '''
    
    if len(urlList) > 0:
        keywordList = []

        articleConfig = Config()
        articleConfig.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' # avoid Newspaper3k 403 Client Error for some URLs
        
        # loop to get each URL and to extract keywords from the news content downloaded
        for count in range(len(urlList)):
            content = Article(urlList[count].strip(), language = 'en', config = articleConfig)
            content.download()

            try:
                content.parse()
            except Exception as e:
                Log('error', repr(e))
            else:
                try:
                    keywords = keywords(
                        content.text,
                        words = 5, # no more than 5 words in a list of keywords extracted from a piece of news
                        lemmatize = True, # lemmatise words (e.g. ['dances'] instead of ['dancing', 'dance', 'dances'])
                        split = True)
                except Exception as e:
                    Log('error', repr(e))
                else:
                    if len(keywords) > 0:
                        keywordList.append(keywords)

        if len(keywordList) == 0:
            Log('warning', 'The keyword list is empty.')

        return keywordList
    else:
        Log('warning', 'The URL list is empty.')
        return []


# test purposes only
if __name__ == '__main__':
    from pullNews import get_headlines

    urlList = get_headlines('gb')
    print(len(urlList), 'URL(s):\n', urlList)

    keywordList = ExtractKeywords(urlList)
    print(len(keywordList), 'group(s) of keywords:\n', keywordList)