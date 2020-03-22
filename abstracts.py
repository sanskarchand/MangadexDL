#!/usr/bin/env python

import time

class DownloadTask:

    def __init__(self, name, manga_name, md_chap_list=[]):
        
        self.name = name
        self.manga_name = manga_name
        self.time_assigned = time.localtime()
        self.chapters = md_chap_list

    
    def addMdChapters(self, md_chap_list):
        self.chapters.extend(md_chap_list)

    def getChapters(self):
        return self.chapters
    
    def getMangaName(self):
        return self.manga_name
