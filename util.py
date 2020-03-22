#!/usr/bin/env python

import parser as par
import const as c


def getTitleFromURL(url):
    # e.g. url = https://mangadex.org/title/10285/hyouryuu-net-cafe
    if url[-1] == "/":
        url = url[:-1]

    url = url[::-1]
    ind = url.index("/")
    url = url[:ind]

    return url[::-1]

def getMapFromMDChapterList(liste):

    dicto = {}

    for md_chap in liste:
        #dicto[md_chap.getFullTitle()] = md_chap.getChapterLink()
        dicto[md_chap.getFullTitle()] = md_chap

    return dicto


def getNumPagesChapterNav(href_string):
    
    # NOTABENE: shoulda used regex. eh, fuck it
    
    print("util:getNumPagesChapterNav: input => ", href_string)
    rev = href_string[::-1]
    rev = rev[1:] 
    ind = rev.index("/")
    rev = rev[:ind]
    
    # get original num string
    rev = rev[::-1]
    return int(rev)


def filterChaptersByLand(md_chap_list, lang):

    li = [ chap for chap in md_chap_list if chap.lang == lang ]
    return li
