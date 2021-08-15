import mainFunctions
import os
import wx
import wx.lib.agw.multidirdialog as MDD
wildcard = "Python source (*.bmp)|*.bmp|" \
           "Text file (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
wildcard1="Text file (*.txt)|*.txt"
wildcard2="Python source (*.bmp)|*.bmp"
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Huffman image compressor")
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        
        # create the buttons and bindings
        openFileDlgBtn = wx.Button(panel, label="Compress image")
        openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
        
        saveFileDlgBtn = wx.Button(panel, label="Decode image")
        saveFileDlgBtn.Bind(wx.EVT_BUTTON, self.onSaveFile)
        
        # put the buttons in a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(openFileDlgBtn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(saveFileDlgBtn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)
        
 
    #----------------------------------------------------------------------
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose an image",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard2,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            imagePath=paths[0]
        dlg.Destroy()
#----------#
        """
        Create and show the Save FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Save file", 
            defaultDir=self.currentDirectory, 
            defaultFile="codedImage", wildcard=wildcard1, style=wx.FD_SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            filePath = dlg.GetPath()
        dlg.Destroy()
        
        print(imagePath)
        mainFunctions.codeImage(imagePath, filePath)
        print('Image compressed')
    #----------------------------------------------------------------------
    def onSaveFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard1,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            filePath=paths[0]
        dlg.Destroy()
#----------#
        """
        Create and show the Save FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Save image", 
            defaultDir=self.currentDirectory, 
            defaultFile="image", wildcard=wildcard2, style=wx.FD_SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            imagePath = dlg.GetPath()
        dlg.Destroy()
        
        mainFunctions.decodeFile(filePath, imagePath)
        print('Image decompressed')
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()


