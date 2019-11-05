'''
@Description: main program
@Version: 1.1.0.20191029
@Author: Alexandra Garton, Connor Worthington, Jichen Zhao, Niran Prajapati, and William Staff
@Date: 2019-10-22 15:22:59
@Last Editors: Jichen Zhao
@LastEditTime: 2019-10-29 15:48:27
'''
from newsapi import NewsApiClient
from monkeylearn import MonkeyLearn

from keywordExtractor import ExtractKeywords


newsApi = NewsApiClient(api_key = '3bd762aea6134796b564d8e18df60cf8') # handle authentication with a News API key (registered using zjcarvin@outlook.com)
mlApi = MonkeyLearn('e4aabc61a7a365fdf7bda3ab14c7be6c5007d930') # handle authentication with a MonkeyLearn API key (registered using tomzjc@qq.com)

keywordList = ExtractKeywords(newsApi, mlApi, 'gb')
print(keywordList)