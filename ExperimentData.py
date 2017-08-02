#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

import urlparse
import requests

from StringIO import StringIO
from secureconfig import SecureConfigParser


key_env = 'MONTAGE_DATALOADER_INI_KEY'
scfg = SecureConfigParser.from_env(key_env)
scfg.read('./config.ini')

baseURL = 'https://montage-test.bi.vt.edu/'
LOGIN = urlparse.urljoin(baseURL, '/accounts/login/')

#App CSVs
appURL = lambda x: urlparse.urljoin(baseURL,'ExportApp/{}'.format(x))
INSTRUCTIONS_PGG = appURL('instructions_pgg')
ANAGRAMS = appURL('anagrams')
WELCOME = appURL('welcome')
DEMOGRAPHIC_DETAILED = appURL('demographic_detailed')
DEMOGRAPHIC = appURL('demographic')
PUBLIC_GOODS = appURL('public_goods')
INSTRUCTIONS_ANAGRAMS = appURL('instructions_anagrams')
CONCLUSION = appURL('conclusion')
RUSE = appURL('ruse')

#Custom CSVs
TIME_ON_PAGE = urlparse.urljoin(baseURL,'ExportTimeSpent/')
CLICKTRACKING = urlparse.urljoin(baseURL,'/clicktracking_click_export')
ANAGRAMS_NEIGHBORS = urlparse.urljoin(baseURL,'/anagrams_neighbors_export')
ANAGRAMS_USER_LETTER = urlparse.urljoin(baseURL,'/anagrams_userletter_export')
ANAGRAMS_TEAM_WORD = urlparse.urljoin(baseURL,'/anagrams_teamword_export')
ANAGRAMS_LETTER_TRANSACTIONS = urlparse.urljoin(baseURL,'/anagrams_lettertransaction_export')

class Loader():
    
    def __init__(self):
        
        client = requests.session()

        # Retrieve the CSRF token first
        client.get(LOGIN)  # sets cookie
        csrftoken = client.cookies['csrftoken']

        username = scfg.get('credentials', 'username')
        password = scfg.get('credentials', 'password')
        
        login_data = dict(login=username, password=password, csrfmiddlewaretoken=csrftoken, next='/')
        r = client.post(LOGIN, data=login_data, headers=dict(Referer=LOGIN))
        
        self.client = client
        
        return
    
    def parseSession(self,df, session):
        if isinstance(session,str):
            session = [session]
            
        return df
    
    def getDetailedDemographicSurvey(self,session=None):
        data_string = self.client.get(DEMOGRAPHIC_DETAILED).content
        df = pd.read_csv(StringIO(data_string))
        
        if not session:
            return df
        #Session Processing Here
        return df
    
    
    def getDemographicSurvey(self,session=None):
        data_string = self.client.get(DEMOGRAPHIC).content
        df = pd.read_csv(StringIO(data_string))
        
        if not session:
            return df
        #Session Processing Here
        return df
    
    
    def getInstructionsAnagrams(self, session=None):
        data_string = self.client.get(INSTRUCTIONS_ANAGRAMS).content
        df = pd.read_csv(StringIO(data_string))
        
        if not session:
            return df
        #Session Processing Here
        return df

    
    def getAnagramsGame(self,session=None):
        data_string = self.client.get(ANAGRAMS).content
        df = pd.read_csv(StringIO(data_string))
        
        if not session:
            return df
        #Session Processing Here
        return df

    
    def getPublicGoodsGame(self,session=None):
        data_string = self.client.get(PUBLIC_GOODS).content
        df = pd.read_csv(StringIO(data_string))
        
        if not session:
            return df
        #Session Processing Here
        return df
    
    
    def getDifiScores(self,session=None):
        Pgg = self.getPublicGoodsGame()
        Anagrams = self.getAnagramsGame()
        Inst_Anagrams = self.getInstructionsAnagrams()
        
        return
    
    
    def getRuseAnswers(self,session=None):
        return
    
    
    def getLetterTransactions(self,session=None):
        data_string = self.client.get(ANAGRAMS_LETTER_TRANSACTIONS).content
        df = pd.read_csv(StringIO(data_string))
        df.approve_time = pd.to_datetime(df.approve_time, unit = 's')
        df.timestamp = pd.to_datetime(df.timestamp, unit = 's')
        
        if not session:
            return df
        #Session Processing Here
        return df
    
    
    def getTimeOnPage(self,session=None):
        data_string = self.client.get(TIME_ON_PAGE).content
        df = pd.read_csv(StringIO(data_string))
        df.time_stamp = pd.to_datetime(df.time_stamp, unit = 's')
        
        if not session:
            return df
        #Session Processing Here
        return df
        