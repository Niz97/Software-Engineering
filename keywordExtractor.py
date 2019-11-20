'''
@Description: keyword extractor that can extract keywords from the news content downloaded from each URL
@Version: 3.7.0.20191118
@Author: Jichen Zhao (driver) and Alexandra Garton (observer)
@Date: 2019-10-29 14:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-11-20 15:34:25
'''

import threading

from newspaper import Config, Article
from gensim.summarization import keywords

from logTool import Log


class KeywordExtractor():
    def __init__(self):
        self.keywordList = []
        self.articleConfig = Config()
        self.articleConfig.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' # avoid Newspaper3k 403 Client Error for some URLs


    def ExtractKeywords(self, urlList: list) -> list:
        '''
        Extract keywords from the news content downloaded from each URL.

        :param urlList: a list of URLs from which the news content will be downloaded for keyword extraction
        :returns: a keyword list whose elements are lists of keywords extracted from each news (generally no more than 5 words in each list)
        '''


        def ThreadTask(self, url: str):
            '''
            The thread allocated should extract keywords from the news content downloaded from a given URL.

            :param url: a given URL from which the news content will be downloaded for keyword extraction
            '''

            content = Article(url, language = 'en', config = self.articleConfig)
            content.download()

            try:
                content.parse()
            except Exception as e:
                Log('error', repr(e))
            else:
                try:
                    keywordList_element = keywords(
                        content.text,
                        words = 5, # no more than 5 words in a list of keywords extracted from a piece of news
                        lemmatize = True, # lemmatise words (e.g. ['dances'] instead of ['dancing', 'dance', 'dances'])
                        split = True)
                except IndexError as e:
                    '''
                    the exception IndexError is raised due to a bug in the package gensim;
                    for more info, please refer to: https://github.com/RaRe-Technologies/gensim/issues/2598
                    '''
                    Log('error', repr(e) + ' (The exception is raised due to a bug in the package gensim. It should be successfully handled by the app.)')
                    keywordList_element = keywords(
                        content.text,
                        lemmatize = True, # lemmatise words (e.g. ['dances'] instead of ['dancing', 'dance', 'dances'])
                        split = True)
                        
                if len(keywordList_element) > 0:
                    self.keywordList.append(keywordList_element)
                else:
                    Log('warning', 'The list of keywords extracted from a piece of news is empty. Related URL: ' + url)
        

        if len(urlList) > 0:
            threadList = []
            
            # loop to start a thread for each URL to try to extract keywords quickly
            for count in range(len(urlList)): # range: [0, len(urlList))
                url = urlList[count].strip()

                newThread = threading.Thread(target = ThreadTask, args = (self, url,)) # extract keywords from the news content downloaded from a URL
                threadList.append(newThread)
                newThread.start()
            
            for thread in threadList:
                thread.join()

            if len(self.keywordList) == 0:
                Log('warning', 'The keyword list is empty.')
        else:
            Log('warning', 'The URL list is empty.')
        
        return self.keywordList


# test purposes only
if __name__ == '__main__':
    from pullNews import get_headlines

    for source in ['bbc-news', 'the-wall-street-journal', 'google-news']:
        print(source)

        urlList = get_headlines('bbc-news')[1]
        print(len(urlList), 'URL(s):\n', urlList)

        extractor = KeywordExtractor()
        keywordList = extractor.ExtractKeywords(urlList)
        print(len(keywordList), 'list(s) of keywords:\n', keywordList)