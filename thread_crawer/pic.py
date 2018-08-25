# encoding:utf-8
import wx
from configs import par_url, strip


class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "信息框",
                          size=(300, 200))

        panel = wx.Panel(self, -1)

        word_label = wx.StaticText(panel, -1, "word:")
        self.word_text = wx.TextCtrl(panel, -1, "",
                                    size=(175, -1))

        self.word_text.SetInsertionPoint(0)

        depth_label = wx.StaticText(panel, -1, "depth:")
        self.depth_text = wx.TextCtrl(panel, -1, "", size=(175, -1))

        max_thread_label = wx.StaticText(panel, -1, "max_thread:")
        self.max_thread_text = wx.TextCtrl(panel, -1, "",size=(175, -1))

        number_label = wx.StaticText(panel, -1, "number:")
        self.number_text = wx.TextCtrl(panel, -1, '', size=(175, -1))

        self.button = wx.Button(panel, -1, "开始", pos=(80, 130))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()

        add_list = [word_label, self.word_text, depth_label,
                    self.depth_text, max_thread_label, self.max_thread_text,
                    number_label, self.number_text]

        sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        sizer.AddMany(add_list)
        panel.SetSizer(sizer)

    def OnClick(self, event):
        self.button.SetLabel("已开始")
        par_url['word'] = self.word_text.GetValue()
        strip['com_url']['depth'] = self.depth_text.GetValue()
        strip['com_url']['max_thread'] = self.max_thread_text.GetValue()
        strip['number'] = self.number_text.GetValue()
        self.Close(True)


class MyApp(wx.App):
    def OnInit(self):
        frame = TextFrame()
        frame.Show(True)
        return True  #如果没有返回值，结果一闪而过，不能驻留窗口


def win():
    app = MyApp()
    app.MainLoop()

