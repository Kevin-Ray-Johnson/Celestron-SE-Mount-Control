# -*- coding: utf-8 -*-
"""
Paddle.py

This is the GUI interface to Mount.py.

"""

import wx
import winsound
import Mount
#import DummyMount

class MyFancyTextBox(wx.Panel):
    """  Displays a message with a formatted numerical value.  """
    def __init__(self, parent, ID, label, message, value, initStr='000'):
        wx.Panel.__init__(self, parent, ID)
        self.text = message + initStr        
        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.myText = wx.StaticText(self, wx.ID_ANY, self.text, style=wx.ALIGN_RIGHT)
        # Set colors and font
        self.myText.SetForegroundColour("black")
        self.myText.SetFont(wx.Font(40, wx.MODERN, wx.NORMAL, wx.BOLD))
        sizer.Add(self.myText, 0, wx.ALL, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        
    def UpdateText(self, message, value, frmt='%(#1)i'):
        newText = message + frmt%{'#1':value}
        self.myText.SetLabel(newText)
        
    def UpdateForegroundColor(self, color):
        self.myText.SetForegroundColour(color)

class MyFrame(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(500,500))            
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Variable used across all parts of this module.
        self.mnt = Mount.Mount()
        #self.mnt = DummyMount.Mount()
        self.maxRate = self.mnt.MaxSlewingRate
        self.rate = 8
        [self.azmInit, self.altInit] = self.mnt.GetAzmAlt()
        self.azmVal = self.azmInit
        self.altVal = self.altInit
        self.keyDown = False
        
        # The top part of the GUI where the azimuth and altitude angles are displayed.
        self.AzmAltBox = wx.GridSizer(1,2,1,1)
        self.AzmDisplay = MyFancyTextBox(self, -1, 'AZM:', '', str(self.azmVal))
        self.AltDisplay = MyFancyTextBox(self, -1, 'ALT:', '', str(self.altVal))
        self.AzmAltBox.AddMany([(self.AzmDisplay,1,wx.EXPAND), (self.AltDisplay,1,wx.EXPAND)])
        sizer.Add(self.AzmAltBox, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 4)
        self.AzmDisplay.UpdateText('', self.azmVal, '%(#1)1.2f')
        self.AltDisplay.UpdateText('', self.altVal, '%(#1)1.2f')
        
        # The "control pad" part of the GUI where the direction buttons are layed out.
        gs = wx.GridSizer(3,3,1,1)
        
        upButton = wx.Button(self, 1, 'Up')
        upButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        upButton.Bind(wx.EVT_KEY_UP, self.OnKeyRelease)
        
        leftButton = wx.Button(self, 2, 'Left')
        leftButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        leftButton.Bind(wx.EVT_KEY_UP, self.OnKeyRelease)
        
        stopButton = wx.Button(self, 0, 'Stop')
        stopButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        stopButton.Bind(wx.EVT_KEY_UP, self.OnKeyRelease)
        
        rightButton = wx.Button(self, 3, 'Right')
        rightButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        rightButton.Bind(wx.EVT_KEY_UP, self.OnKeyRelease)
        
        downButton = wx.Button(self, 4, 'Down')
        downButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        downButton.Bind(wx.EVT_KEY_UP, self.OnKeyRelease)
        
        gs.AddMany([(wx.StaticText(self, -1, ''), 0, wx.EXPAND),
                        (upButton, 1, wx.EXPAND),
                        (wx.StaticText(self, -1, ''), 0, wx.EXPAND),
                        (leftButton, 2, wx.EXPAND),
                        (stopButton, 0, wx.EXPAND),
                        (rightButton, 3, wx.EXPAND),
                        (wx.StaticText(self, -1, ''), 0, wx.EXPAND),
                        (downButton, 4, wx.EXPAND),
                        (wx.StaticText(self, -1, ''), 0, wx.EXPAND) ])
        sizer.Add(gs, 1, wx.EXPAND | wx.TOP | wx.BOTTOM)
        # Disable the GUI buttons for directional control
        # The button are NOT "push-to-go/release-to-stop".
        #wx.EVT_BUTTON(self, 1, self.OnUp)
        #wx.EVT_BUTTON(self, 2, self.OnLeft)
        #wx.EVT_BUTTON(self, 0, self.OnStop)
        #wx.EVT_BUTTON(self, 3, self.OnRight)
        #wx.EVT_BUTTON(self, 4, self.OnDown)
        
        # The rate selector across the bottom of the GUI.
        self.RateBox = wx.GridSizer(1,1,1,1)
        self.RateDisplay = MyFancyTextBox(self, -1, 'Mount Slew Rate:', 'Rate: ', str(self.rate))
        self.RateBox.AddMany([(self.RateDisplay, 1,wx.EXPAND)])
        sizer.Add(self.RateBox, 0, wx.EXPAND, 4)
        self.RateDisplay.UpdateText('Rate: ', self.rate, '%(#1)i')
        
        self.SetSizer(sizer)
        self.Center()

    def UpdateDisplay(self):
        [self.azmVal, self.altVal] = self.mnt.GetAzmAlt()
        
        if 295 < self.azmVal or self.azmVal < 45.0: 
            self.AzmDisplay.UpdateForegroundColor('black')
        else:
            self.AzmDisplay.UpdateForegroundColor('red')
            winsound.MessageBeep()

        if 330 < self.altVal or self.altVal < 30:
            self.AltDisplay.UpdateForegroundColor('black')
        else:
            self.AltDisplay.UpdateForegroundColor('red')
            winsound.MessageBeep()
        
        self.AzmDisplay.UpdateText('', self.azmVal, '%(#1)1.2f')
        self.AltDisplay.UpdateText('', self.altVal, '%(#1)1.2f')
    
    def OnStop(self, event):
        print 'STOP'
        self.mnt.SlewAzm(0)
        self.mnt.SlewAlt(0)
        self.UpdateDisplay()
        
    def OnUpPress(self, event):
        print 'UP Pressed'
        self.mnt.SlewAlt(self.rate)
        self.UpdateDisplay()

    def OnUpRelease(self, event):
        print 'UP Released'
        self.mnt.SlewAlt(0)
        self.UpdateDisplay()

    def OnLeftPress(self, event):
        print 'LEFT Pressed'
        self.mnt.SlewAzm(-self.rate)
        self.UpdateDisplay()

    def OnLeftRelease(self, event):
        print 'LEFT Released'
        self.mnt.SlewAzm(0)
        self.UpdateDisplay()

    def OnRightPress(self, event):
        print 'RIGHT Pressed'
        self.mnt.SlewAzm(self.rate)
        self.UpdateDisplay()

    def OnRightRelease(self, event):
        print 'RIGHT Released'
        self.mnt.SlewAzm(0)
        self.UpdateDisplay()
        
    def OnDownPress(self, event):
        print 'DOWN Pressed'
        self.mnt.SlewAlt(-self.rate)
        self.UpdateDisplay()

    def OnDownRelease(self, event):
        print 'Down Released'
        self.mnt.SlewAlt(0)
        self.UpdateDisplay()
    
    def OnKeyPress(self, event):
        keycode = event.GetKeyCode()
        # Turns the numbers keys from 1-9 into rate set keys. 
        if 49 <= keycode <= 57:
            self.rate = keycode - 48
            self.RateDisplay.UpdateText('Rate: ', self.rate)
        # Bind the arrow keys.
        if keycode == wx.WXK_UP:
            self.OnUpPress(self)
        elif keycode == wx.WXK_LEFT or keycode == 306:
            self.OnLeftPress(self)
        elif keycode == wx.WXK_RIGHT or keycode == 90:
            self.OnRightPress(self)
        elif keycode == wx.WXK_DOWN:
            self.OnDownPress(self)
        # Make all other keys stop the mount.
        else:
            self.OnStop(self)

    def OnKeyRelease(self, event):
        keycode = event.GetKeyCode()
        # Bind the arrow keys.
        if keycode == wx.WXK_UP:
            self.OnUpRelease(self)
        elif keycode == wx.WXK_LEFT or keycode == 306:
            self.OnLeftRelease(self)
        elif keycode == wx.WXK_RIGHT or keycode == 90:
            self.OnRightRelease(self)
        elif keycode == wx.WXK_DOWN:
            self.OnDownRelease(self)
        # Make all other keys stop the mount.
        else:
            self.OnStop(self)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Paddle')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()