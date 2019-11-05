'''
@Description: main program
@Version: 1.0.0.20191022
@Author: Alexandra Garton, Connor Worthington, Jichen Zhao, Niran Prajapati, and William Staff
@Date: 2019-10-22 15:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-10-22 15:32:49
'''

from newsapi import NewsApiClient

from keywordExtractor import ExtractKeywords


newsApi = NewsApiClient(api_key = '3bd762aea6134796b564d8e18df60cf8') # handle authentication with a News API key (registered using zjcarvin@outlook.com)

keywordList = ExtractKeywords(newsApi, 'gb')
print(keywordList)