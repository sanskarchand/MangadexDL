#!/usr/bin/env python
import wx
import const as c
import nethandler as nh
import parser as par

class MyFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):

        super(MyFrame, self).__init__(*args, **kwargs)
        
        self.net_handler = nh.NetHandler()

        self.panel  = wx.Panel(self)
        self.status_text = "<Status:Okay>"
        
        '''
        self.st = wx.StaticText(self.panel, label="Hello wx")
        font = self.st.GetFont()
        font.PointSize += 10
        self.st.SetFont(font.Bold())
        '''
        
        # sizer to manage child widgets' layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.Add(self.st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        self.panel.SetSizer(self.sizer)

        # input field for manga link
        self.manga_link_field = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, size=(c.FIELD_WIDTH, -1))
        self.manga_link_field.SetFocus()
        self.manga_link_field.Bind(wx.EVT_TEXT_ENTER, self.onLinkEntered)
        self.sizer.Add(self.manga_link_field, 0, wx.ALL, 24)
        
        #self.panel.SetSizer


        self.makeMenuBar()
        #self.makeStatusBar()
        self.CreateStatusBar()
        #self.SetStatusText(self.status_text)
        self.updateStatusText()

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
        
        # assume this is a link
        text = self.manga_link_field.GetValue()
        
        self.updateStatusText("Downloading URL content")

        page_data = self.net_handler.getURLContent(text)

        with open("temp.html", "w") as f:
            f.write(page_data)

        p = par.MangaParser(c.P_TYPE_TITLE_PAGE, page_data)
    
        self.updateStatusText("Parsing URL content")

        p.parse()

        self.updateStatusText("Finished Parsing")



if __name__ == '__main__':

    app = wx.App()
    frame = MyFrame(None, title="HW 2")
    frame.Show()
    app.MainLoop()
