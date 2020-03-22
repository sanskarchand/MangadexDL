#!/usr/bin/env python

import bs4
import const as c
import util

class MDChapter:

    def __init__(self, m_lang, m_id, m_vol, m_chap, m_title):
        self.lang = m_lang
        self.id = m_id 
        self.vol = m_vol
        self.chap = m_chap
        self.title = m_title

    def getChapterFolderName(self):
        # NOTABENE: should this behavior be defined here? ( alt: util )
        _str_ch = ""
        if self.vol != "":
            _str_ch += "Vol_" + self.vol
        if self.chap != "":
            _str_ch += "Ch_" + self.chap

        _str_ch += "_" + self.title

        annoying_marks = ["'", ":"]
        
        for mark in annoying_marks:
            _str_ch = _str_ch.replace(mark, "--")

        
        return _str_ch

    def getFullTitle(self):
        return "Vol {} Chap {} - {}".format(self.vol, self.chap, self.title)

    def getChapterLink(self):
        return c.N_ROOT_URL + "chapter/" + str(self.id)

        
class MangaParser:

    def __init__(self, m_type, m_source, nh=None):
        self.type = m_type
        self.source = m_source
        self.soup = bs4.BeautifulSoup(self.source, "html.parser")
        self.net_handler = nh

    def setNetHandler(self, nh):
        self.net_handler = nh

    def parse(self):

        if self.type == c.P_TYPE_TITLE_PAGE:
            return self.parseTitlePage()
        
        elif self.type == c.P_TYPE_NAV_PAGE:
            return self.parseNavPage()

    def parseTitlePage(self):
        
        #chapter_divs = self.soup.select(".chapter-row")
        chapter_page_links = self.soup.select(".page-link")

        # find the last page no. for the chapter list navigator
        index = -1
        for idx, each in enumerate(chapter_page_links):

            ch_list = each.findAll("span")
            if ch_list:
                span = ch_list[0]
                if span["title"] == "Jump to last page":
                    index = idx
                    break
        
        if index == -1:
            last_page_num = 1
        else:
            last_page_num = util.getNumPagesChapterNav(chapter_page_links[index]["href"])

        return last_page_num

        #print("No. of chapter navigation pages = ", last_page_num)


    def parseNavPage(self):

        #new_soup = bs4.BeautifulSoup(raw_page, "html.parser")
        chapter_divs = self.soup.select(".chapter-row")

        chapter_objs = []
        
        for div in chapter_divs:
            if "data-title" not in div.attrs:
                continue
            
            chap_obj = MDChapter( div["data-lang"], div["data-id"], div["data-volume"], div["data-chapter"], div["data-title"])
            chapter_objs.append(chap_obj)

        return chapter_objs
