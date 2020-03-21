#!/usr/bin/env python

import requests
import const as c

class NetHandler:
    
    def __init__(self):
        self.uname = None
        self.passwd = None
        self.login_session = None

    def setUserCredentials(self, uname, passwd):
        self.uname = uname
        self.passwd = passwd

    def userLogin(self):

        self.login_session = requests.Session()
        
        auth_dict = { "login_username": self.uname, 
                    "login_password": self.passwd }

        resp = self.login_session.post( c.N_LOGIN_URL, auth_dict )
        print("Login resp code: ", resp.status_code)


    def getURLContent(self, url):

        response = self.login_session.get(url)
        return response.text
