import subprocess
import os
import wx
import commands

class LabelViewerPanel(wx.Panel):
    '''Class to create panel on the frame'''
    
    def __init__(self, parent, image, name, panel_size):
        wx.Panel.__init__(self, parent, size=panel_size)
        self.frame = parent
        self.name = name
        self.Bind(wx.EVT_CHAR, self.on_keypress)
        self.cursor = wx.StockCursor(wx.CURSOR_BLANK)
        self.BackgroundColour = wx.BLACK
        self.widgets = []
        self.image = image
        
        # Uncomment the following line on wxpython 2.x
        # self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.draw_image)
        
                
    def hide_cursor(self):
        for widget in self.widgets:
            widget.SetCursor(self.cursor)

    def on_keypress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.frame.close()

    def draw_image(self, event):
        """ Draws the image to the panel's background. """
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Bitmap(self.image)
        dc.DrawBitmap(image, 0, 0)
        self.SetFocus()

    def switch_panel(self, event):
        self.frame.switch_panel(self.name, event.GetEventObject().GetName())
    
    def add_button(self, image_path, img_name, position):
        image_path = './images/buttons/' + image_path
        bmp = wx.Bitmap(image_path, wx.BITMAP_TYPE_PNG)
        widget = wx.StaticBitmap(self, name=img_name, pos=position, bitmap=bmp)
        widget.Bind(wx.EVT_LEFT_DOWN, self.switch_panel)
        self.widgets.append(widget)
        
class MainPanel(LabelViewerPanel):
    '''   Main home screen. '''
    def __init__(self, parent, image, name, panel_size):
        LabelViewerPanel.__init__(self, parent, image, name, panel_size)
        self.add_button('AnimalMotifs1.png', 'AnimalMotifs', (831, 256))
        self.add_button('AnimalMotifs2.png', 'AnimalMotifs', (152, 44))
        self.add_button('Beadwork1.png', 'Beadwork', (362, 556))
        self.add_button('Beadwork2.png', 'Beadwork', (367,37))
        self.add_button('CarvedStoneMauls.png', 'CarvedStoneMauls', (849, 565))
        self.add_button('CarvedStoneNetWeight.png', 'CarvedStoneNetWeight', (1060, 636))
        self.add_button('CollectingRoots1.png', 'CollectingRoots', (591,408))
        self.add_button('CollectingRoots2.png', 'CollectingRoots', (1321,52))
        self.add_button('DecorativeStoneBone1.png', 'DecorativeStoneBoneCarvings', (1173,490))
        self.add_button('DecorativeStoneBone2.png', 'DecorativeStoneBoneCarvings', (1337,643))
        self.add_button('DecorativeStoneBone3.png', 'DecorativeStoneBoneCarvings', (1058,552))
        self.add_button('DiamondShapedFace.png', 'DiamondShapedFace', (1061,315))
        self.add_button('Games1.png', 'Games', (167,690))
        self.add_button('Games2.png', 'Games', (283,705))
        self.add_button('Hats1.png', 'Hats', (593,69))
        self.add_button('Hats2.png', 'Hats', (654,231))
        self.add_button('Hats3.png', 'Hats', (813,35))
        self.add_button('Horses1.png', 'Horses', (122,503))
        self.add_button('Horses2.png', 'Horses', (155,274))
        self.add_button('SheepHornBowl.png', 'SheepHornBowl', (1072,54))
        self.add_button('StoneCarvings1.png', 'StoneCarvings', (1350,533))
        self.add_button('StoneCarvings2.png', 'StoneCarvings', (1162,619))
        self.add_button('StoneDuck.png', 'StoneDuck', (836,426))
        self.add_button('StoneLamp1.png', 'StoneLamps', (1243,580))
        self.add_button('StoneLamp2.png', 'StoneLamps', (1082,733))
        self.add_button('WhaleboneFishClub.png', 'WhaleboneFishClub', (589,689))
        self.hide_cursor()
        self.SetFocus()

class LabelPanel(LabelViewerPanel):
    '''Add Buttons on other screen except Main'''
    def __init__(self, parent, background, name, panel_size):
        LabelViewerPanel.__init__(self, parent, background, name, panel_size)
        self.add_button('home.png', 'main', (22, 800))
        self.hide_cursor()
        
            
class MainFrame(wx.Frame):
    """    Create Background Frame and create panels for each page   """

    def __init__(self, parent, image_size):
        wx.Frame.__init__(self, parent, wx.ID_ANY, size=image_size)
        self.size = image_size
        self.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
        self.panels = []
        self.panel_dict = {}

        main_panel = MainPanel(self, './images/pages/HomePage.png', 'main', image_size)
        self.panel_dict['main'] = main_panel

        self.add_panel('AnimalMotifs')
        self.add_panel('Beadwork')
        self.add_panel('CarvedStoneMauls')
        self.add_panel('CarvedStoneNetWeight')
        self.add_panel('CollectingRoots')
        self.add_panel('DecorativeStoneBoneCarvings')
        self.add_panel('DiamondShapedFace')
        self.add_panel('Games')
        self.add_panel('Hats')
        self.add_panel('Horses')
        self.add_panel('SheepHornBowl')
        self.add_panel('StoneCarvings')
        self.add_panel('StoneDuck')
        self.add_panel('StoneLamps')
        self.add_panel('WhaleboneFishClub')

        # Timer to switch back to main shelf
        self.timeout = 600000  # 10 min
        self.timeout_timer = wx.Timer(self, wx.ID_ANY)
        self.start_timeout_timer()

    def add_panel(self, name):
        bg = './images/pages/'+ name +'.png'
        panel = LabelPanel(self, bg, name, self.size)
        panel.Hide()
        self.panel_dict[name] = panel
        
    def switch_panel(self, src_id, dest_id):
        print src_id +'->'+ dest_id
        self.panel_dict[src_id].Hide()
        self.panel_dict[dest_id].Show()
        self.panel_dict[dest_id].SetFocus()
        self.current_panel = dest_id
        self.Layout()
        self.restart_timeout_timer()

    def start_timeout_timer(self):
        self.Bind(wx.EVT_TIMER, self.switch_on_timeout, self.timeout_timer)
        self.timeout_timer.Start(self.timeout)

    def restart_timeout_timer(self):
        self.timeout_timer.Stop()
        self.start_timeout_timer()

    def switch_on_timeout(self, event):
        self.switch_panel(self.current_panel, 'main')
        self.restart_timeout_timer()

    def close(self):
        self.Destroy()


        
if __name__ == '__main__':
    app = wx.App(False)
    MainFrame(None, (1900, 900))
    app.MainLoop()

