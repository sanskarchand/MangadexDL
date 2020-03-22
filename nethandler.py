#!/usr/bin/env python

import requests
import const as c
import os
import time
import json  # should be in parser.py

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

    def downloadChapter(self, path, link, chap_id):
        
        # link -> link to whole chapter
        
        cur_path = os.getcwd()

        if not os.path.exists(path):
            #os.mkdir(path)
            os.makedirs(path, exist_ok=True)

        os.chdir(path)
    
        dat = self.login_session.get(c.N_API_CHAPTER +  chap_id)
        json_dict = json.loads(dat.content)

        
        serv_ = json_dict["server"]
        hash_ = json_dict["hash"]
        page_arr_ = json_dict["page_array"]

        for img_name in page_arr_:
            url = serv_ + hash_ + "/" + img_name
            #print("URL: ", url)
            resp = self.login_session.get(url)

            with open(img_name, "wb") as f:
                f.write(resp.content)

            time.sleep(c.N_WAIT_TIME)


        # reset path at the end
        os.chdir(cur_path)


