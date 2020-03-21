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

    def adjustModal(self):
        # do this after login
        
        # the corresponding js sends this as a formdata object
        # (site uses ajax and jquery)
        
        header = {'x-requested-with': 'XMLHttpRequest'}

        payload = { "theme_id": "1",
                "default_lang_ids":"0",
                "display_lang_id":"1",
                "hentai_mode":"1"
        }

        resp = self.login_session.post( c.N_CHANGE_URL, headers=header, data=payload)
        print("Modal response code:", resp.status_code)
        
        with open("modal_response", "w") as f:
            f.write(resp.text)

    def getURLContent(self, url):

        response = self.login_session.get(url)
        return response.text
