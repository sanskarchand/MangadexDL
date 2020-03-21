#!/usr/bin/env python

import bs4
import const as c

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
        
        for div in chapter_divs:
            if "data-title" not in div.attrs:
                continue
            
            print("Vol {} Ch {} - {}".format(div["data-volume"], div["data-chapter"],div["data-title"]))
        
        '''
        return 
        for child in self.soup.find_all('div'):
            if 'class' in child.attrs:
                print(child["class"])
            #if child.attrs.has_key('class'):
                if "chapter-row" in child['class']:
                    print(child["data-title"])
        '''
