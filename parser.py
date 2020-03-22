#!/usr/bin/env python

import bs4
import const as c

class MDChapter:

    def __init__(self, m_lang, m_id, m_vol, m_chap, m_title):
        self.lang = m_lang
        self.id = m_id 
        self.vol = m_vol
        self.chap = m_chap
        self.title = m_title

    def getFullTitle(self):
        return "Vol {} Chap {} - {}".format(self.vol, self.chap, self.title)

    def getChapterLink(self):
        return c.N_ROOT_URL + "chapter/" + str(self.id)

        
class MangaParser:

    def __init__(self, m_type, m_source):
        self.type = m_type
        self.source = m_source
        self.soup = bs4.BeautifulSoup(self.source, "html.parser")

    def parse(self):

        if self.type == c.P_TYPE_TITLE_PAGE:
            return self.parseTitlePage()

    def parseTitlePage(self):
        
        chapter_divs = self.soup.select(".chapter-row")
        chapter_objs = []
        
        for div in chapter_divs:
            if "data-title" not in div.attrs:
                continue
            
            chap_obj = MDChapter( div["data-lang"], div["data-id"], div["data-volume"], div["data-chapter"], div["data-title"])
            chapter_objs.append(chap_obj)
            print("Vol {} Ch {} - {}".format(div["data-volume"], div["data-chapter"],div["data-title"]))

        return chapter_objs
            
        
        '''
        return 
        for child in self.soup.find_all('div'):
            if 'class' in child.attrs:
                print(child["class"])
            #if child.attrs.has_key('class'):
                if "chapter-row" in child['class']:
                    print(child["data-title"])
        '''
