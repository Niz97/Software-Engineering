'''
@Description: function that extracts keywords from top headlines in the specified country
@Version: 2.0.1.20191105
@Author: Jichen Zhao
@Date: 2019-10-29 14:22:59
@Last Editors: Jichen
@LastEditTime: 2019-11-05 15:55:26
'''
from newspaper import Article


def ExtractKeywords(newsApi, mlApi, countryCode):
    '''
    (TODO:) If the keyword list returned is an empty list, there may be an error or no top headlines got from News API.
    '''
    
    try:
        '''
        get the query result of top headlines in the specified country;
        for more information about the top headline endpoint, please refer to: https://newsapi.org/docs/endpoints/top-headlines
        '''
        topH = newsApi.get_top_headlines(country = countryCode, language = 'en')
    except Exception as e:
        #TODO: consider error logs
        return []
    else:
        if (topH['totalResults'] > 0):
            newsList = topH['articles'] # the value paired with the key "articles" is a list of top headlines got from News API
            contentList = []

            '''
            loop to get a list of all top headline content;
            generally, the value paired with the key "totalResults" is NOT equivalent to the length of the list of top headlines got from News API because not all available top headlines are returned from the server
            '''
            for count in range(len(newsList) - 1):
                news = newsList[count] # each entry of the list is a dictionary of the info of 1 top headline

                content = Article(news['url'], language = 'en')
                content.download()
                content.parse()
                contentList.append(content.text)

            try:
                '''
                get the keyword extraction report after analysing all top headline content;
                the value "ex_YCya9nrn" indicates that the module used is Keyword Extractor;
                for more information about MonkeyLearn's Extractor API, please refer to: https://monkeylearn.com/api/v3/#extractor-api
                '''
                kExtraction = mlApi.extractors.extract('ex_YCya9nrn', contentList)
            except Exception as e:
                #TODO: consider error logs
                return []
            else:
                keywordList = []

                # loop to get a list of all keywords
                for count in range(len(kExtraction.body) - 1):
                    kExResult = kExtraction.body[count] # get the keyword extraction result of the specified top headline content

                    if (kExResult['error'] == False):
                        keywords = []

                        for keywordInfo in kExResult['extractions']:
                            keywords.append(keywordInfo['parsed_value'])

                        keywordList.append(keywords)
                    #else: # TODO: what should be printed if some extract keywords successfully...
                        #print('Error! Failed to extract keywords.\n', kExResult['error_detail'])
                
                return keywordList   
        else:
            #TODO: consider logs
            return []