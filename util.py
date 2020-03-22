#!/usr/bin/env python

import parser as par
import const as c


def getMapFromMDChapterList(liste):

    dicto = {}

    for md_chap in liste:
        dicto[md_chap.getFullTitle()] = md_chap.getChapterLink()

    return dicto

