#!/usr/bin/env python

import wx
import const as c
import nethandler as nh
import parser as par
import util

class MyFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):

        super(MyFrame, self).__init__(*args, **kwargs)

        # basic config
        self.lang = "1"     #  English
        self.status_text = "Initializing"
        
        self.net_handler = nh.NetHandler()
        
        self.panel_main = wx.Panel(self)
        self.panel_top = wx.Panel(self.panel_main)
        self.panel_bottom  = wx.Panel(self.panel_main)

        self.panel_top_left = wx.Panel(self.panel_top)
        self.panel_top_right = wx.Panel(self.panel_top)
        self.panel_bottom_left = wx.Panel(self.panel_bottom)
        self.panel_bottom_right = wx.Panel(self.panel_bottom)

        
        
        # sizer to manage child widgets' layout
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_top = wx.BoxSizer(wx.HORIZONTAL) 
        self.sizer_top_left = wx.BoxSizer(wx.VERTICAL)
        self.sizer_top_right = wx.BoxSizer(wx.VERTICAL)
        self.sizer_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_bottom_left = wx.BoxSizer(wx.VERTICAL)
        self.sizer_bottom_right = wx.BoxSizer(wx.VERTICAL)

        self.sizer_main.Add(self.panel_top)
        self.sizer_main.Add(self.panel_bottom)
        self.sizer_top.Add(self.panel_top_left, proportion=1, flag=wx.ALIGN_LEFT)
        self.sizer_top.AddSpacer(12)
        self.sizer_top.Add(self.panel_top_right, proportion=1, flag=wx.ALIGN_RIGHT)

        self.sizer_bottom.Add(self.panel_bottom_left, proportion=1, flag=wx.ALIGN_LEFT)
        self.sizer_top.AddSpacer(8)
        self.sizer_bottom.Add(self.panel_bottom_right, proportion=1, flag=wx.ALIGN_RIGHT)


        #self.panel_top.SetSizer(self.sizer_top)
        #self.panel_bottom.SetSizer(self.sizer_bottom)


        #--- MANGA LINK INPUT WIDGETS BEGIN---
        self.manga_link_text = wx.StaticText(self.panel_top_left, label="Manga: ")

        self.manga_link_field = wx.TextCtrl(self.panel_top_left, style=wx.TE_PROCESS_ENTER, size=(c.FIELD_WIDTH, -1))
        self.manga_link_field.SetFocus()
        self.manga_link_field.Bind(wx.EVT_TEXT_ENTER, self.onLinkEntered)

        self.manga_link_button = wx.Button(self.panel_top_left, label="Get Chapters")
        self.manga_link_button.Bind(wx.EVT_BUTTON, self.onLinkEntered)

    
        self.sizer_top_left.Add(self.manga_link_text, wx.ALL, border=2)
        self.sizer_top_left.Add(self.manga_link_field, wx.ALL, border=2)
        self.sizer_top_left.Add(self.manga_link_button, wx.ALL, border=2)
        #--- MANGA LINK INPUT WIDGETS END---

        #--- LANGUAGE SELECT WIDGETS BEGIN---
        self.lang_select_text  = wx.StaticText(self.panel_top_right, label="Lang: ")
        
        self.lang_select_field = wx.TextCtrl(self.panel_top_right, style=wx.TE_PROCESS_ENTER, size=(c.FIELD_WIDTH_2, -1))

        self.lang_select_button = wx.Button(self.panel_top_right, label="Set Language")
        self.lang_select_button.Bind(wx.EVT_BUTTON, self.onLangSet)
        

        self.sizer_top_right.Add(self.lang_select_text, wx.ALL)
        self.sizer_top_right.Add(self.lang_select_field, wx.ALL)
        self.sizer_top_right.Add(self.lang_select_button, wx.ALL)
        #--- LANGUAGE SELECT WIDGETS END---

        self.chapter_clist_box = wx.CheckListBox(self.panel_bottom_left)
        self.sizer_bottom_left.Add(self.chapter_clist_box, wx.ALL|wx.EXPAND)   # window, proportion, flag, border

        

        self.makeMenuBar()
        #self.makeStatusBar()
        self.CreateStatusBar()
        #self.SetStatusText(self.status_text)
        self.updateStatusText()

        #self.handleLogin()
        
        self.panel_main.SetSizer(self.sizer_main)
        self.panel_top_left.SetSizer(self.sizer_top_left)
        self.panel_top_right.SetSizer(self.sizer_top_right)
        self.panel_top.SetSizer(self.sizer_top)
        self.panel_bottom_left.SetSizer(self.sizer_bottom_left)
        self.panel_bottom_right.SetSizer(self.sizer_bottom_right)
        self.panel_bottom.SetSizer(self.sizer_bottom)

    

    def prepareForLaunch(self):
        self.handleLogin()


    def handleLogin(self):
        self.net_handler.setUserCredentials(c.N_UNAME, c.N_PASSWD) 
        self.updateStatusText("Logging in as " + c.N_UNAME)
        self.net_handler.userLogin()
        self.updateStatusText("Attempting to set modal" + c.N_UNAME)
        self.net_handler.adjustModal()
        self.updateStatusText("Updated Modal. Ready for download")

    def makeStatusBar(self):
        
        self.status_bar = self.CreateStatusBar(1)
        self.status_bar.SetStatusText(self.status_text)

    def makeMenuBar(self):

        self.file_menu = wx.Menu()
        self.help_menu = wx.Menu()
        self.menu_bar = wx.MenuBar()


        # "\t..." syntax defines accelerator key
        
        item1 = self.file_menu.Append(-1, "&Hello...\tCtrl-H",
                "[HINT]")
        self.file_menu.AppendSeparator()

        item_exit = self.file_menu.Append(wx.ID_EXIT)

        item_about = self.help_menu.Append(wx.ID_ABOUT)
            
        self.menu_bar.Append(self.file_menu, "&File")
        self.menu_bar.Append(self.help_menu, "&Help")

        self.SetMenuBar(self.menu_bar)

        # associate handler functions for menu items

        self.Bind(wx.EVT_MENU, self.onHello, item1)
        self.Bind(wx.EVT_MENU, self.onExit, item_exit)
        self.Bind(wx.EVT_MENU, self.onAbout, item_about)
    
    def updateStatusText(self, text=None):
        if text is not None:
            self.status_text = text
        self.SetStatusText(self.status_text)

    def onExit(self, event):
        self.Close(True)

    def onHello(self, event):
        wx.MessageBox("[PLACEHOLDER]")

    def onAbout(self, event):
        wx.MessageBox("Sample", "About HW 2", wx.OK|wx.ICON_INFORMATION)
    
    def onLinkEntered(self, event):
        
        text = self.manga_link_field.GetValue()

        if not text:
            return
        
        self.updateStatusText("Downloading URL content")

        page_data = self.net_handler.getURLContent(text)

        with open("temp.html", "w") as f:
            f.write(page_data)

        p = par.MangaParser(c.P_TYPE_TITLE_PAGE, page_data)
    
        self.updateStatusText("Parsing URL content")
        chapter_objects = p.parse()   # list of MDChapter objects
        self.updateStatusText("Finished Parsing")

        
        chapter_map = util.getMapFromMDChapterList(chapter_objects)
        choice_strings = list(chapter_map.keys())[::-1]
        self.chapter_clist_box.InsertItems(choice_strings, 0)

    def onLangSet(self, event):
        val = self.lang_select_field.GetValue()

        if not val:
            return
        self.lang = val



if __name__ == '__main__':

    app = wx.App()
    frame = MyFrame(None, title="Mangadex Downloader")
    frame.Show()
    frame.prepareForLaunch()
    app.MainLoop()
