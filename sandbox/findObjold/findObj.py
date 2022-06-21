from cgitb import text
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import tkinter.font as tkFont
import os

class tk_objDetection:
  def __init__(self, root):
    #key class variables for gui
    self.beginTag   = False;
    self.workingDir = None;
    self.videoRpo   = None;
    self.objTag     = None;
    self.outAmd     = None;
    self.radioOpt   = tk.StringVar();
    self.radioOpt.set('n')
    self.sroot      = root

    #setting title
    root.title("Object detection tool")
    #setting window size
    width  = 550
    height = 310
    screenwidth  = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)


    #----------------- labels
    label_title=tk.Label(root)
    label_title["anchor"] = tk.CENTER
    ft = tkFont.Font(family='Calibri',size=18,weight='bold')
    label_title["font"] = ft
    label_title["fg"] = "#333333"
    label_title["text"] = "Object Tagging Toolbox"
    label_title.place(x=80,y=20,width=400,height=25)

    label_workingDir = tk.Label(root)
    label_workingDir["anchor"]  = tk.E
    ft = tkFont.Font(family='Calibri',size=14)
    label_workingDir["font"]    = ft
    label_workingDir["fg"]      = "#333333"
    label_workingDir["text"]    = "Working directory [d]"
    label_workingDir.place(x=10,y=80,width=170,height=25)

    label_videoRpo = tk.Label(root)
    label_videoRpo["anchor"]  = tk.E
    ft = tkFont.Font(family='Calibri',size=14)
    label_videoRpo["font"]    = ft
    label_videoRpo["fg"]      = "#333333"
    label_videoRpo["text"]    = "Video repository [f]"
    label_videoRpo.place(x=10,y=120,width=170,height=25)

    label_objTag = tk.Label(root)
    label_objTag["anchor"]  = tk.E
    ft = tkFont.Font(family='Calibri',size=14)
    label_objTag["font"]    = ft
    label_objTag["fg"]      = "#333333"
    label_objTag["text"]    = "Object tag [s]"
    label_objTag.place(x=10,y=160,width=170,height=25)

    label_outAmd = tk.Label(root)
    label_outAmd["anchor"]  = tk.E
    ft = tkFont.Font(family='Calibri',size=14)
    label_outAmd["font"]    = ft
    label_outAmd["fg"]      = "#333333"
    label_outAmd["text"]    = "Output/amend [f]"
    label_outAmd.place(x=10,y=200,width=170,height=25)

    #----------------- Entries
    self.entry_workingDir=tk.Entry(root)
    self.entry_workingDir["bd"]      = "1px"
    self.entry_workingDir["cursor"]  = "shuttle"
    ft = tkFont.Font(family='Calibri',size=10)
    self.entry_workingDir["font"]    = ft
    self.entry_workingDir["fg"]      = "#9c8553"
    self.entry_workingDir["justify"] = "left"
    self.entry_workingDir["text"]    = ""
    self.entry_workingDir["exportselection"] = 0
    self.entry_workingDir.place(x=190,y=80,width=300,height=25)

    self.entry_videoRpo=tk.Entry(root)
    self.entry_videoRpo["bd"]      = "1px"
    self.entry_videoRpo["cursor"]  = "shuttle"
    ft = tkFont.Font(family='Calibri',size=10)
    self.entry_videoRpo["font"]    = ft
    self.entry_videoRpo["fg"]      = "#9c8553"
    self.entry_videoRpo["justify"] = "left"
    self.entry_videoRpo["text"]    = ""
    self.entry_videoRpo.place(x=190,y=120,width=300,height=25)

    self.entry_objTag=tk.Entry(root)
    self.entry_objTag["bd"]      = "1px"
    self.entry_objTag["cursor"]  = "shuttle"
    ft = tkFont.Font(family='Calibri',size=10)
    self.entry_objTag["font"]    = ft
    self.entry_objTag["fg"]      = "#9c8553"
    self.entry_objTag["justify"] = "left"
    self.entry_objTag["text"]    = ""
    self.entry_objTag.place(x=190,y=160,width=300,height=25)

    self.entry_outAmd=tk.Entry(root)
    self.entry_outAmd["bd"]      = "1px"
    self.entry_outAmd["cursor"]  = "shuttle"
    ft = tkFont.Font(family='Calibri',size=10)
    self.entry_outAmd["font"]    = ft
    self.entry_outAmd["fg"]      = "#9c8553"
    self.entry_outAmd["justify"] = "left"
    self.entry_outAmd["text"]    = ""
    self.entry_outAmd.place(x=190,y=200,width=300,height=25)
    self.entry_outAmd['state']   = 'disabled';

    #----------------- Buttons
    bttn_workingDir=tk.Button(root) #working dir
    bttn_workingDir["bg"]   = "#733c61"
    bttn_workingDir["activebackground"] = "#48263d"
    bttn_workingDir["text"] = ""
    bttn_workingDir.place(x=500,y=80,width=25,height=25)
    bttn_workingDir["command"] = self.bttn_workingDir_command

    bttn_videoRpo=tk.Button(root) #Video Repo
    bttn_videoRpo["bg"]   = "#733c61"
    bttn_videoRpo["activebackground"] = "#48263d"
    bttn_videoRpo["text"] = ""
    bttn_videoRpo.place(x=500,y=120,width=25,height=25)
    bttn_videoRpo["command"] = self.bttn_videoRpo_command

    self.bttn_outAmd=tk.Button(root) #Project to ammend
    self.bttn_outAmd["bg"]   = "#6f676c"
    self.bttn_outAmd["activebackground"] = "#48263d"
    self.bttn_outAmd["text"] = ""
    self.bttn_outAmd.place(x=500,y=200,width=25,height=25)
    self.bttn_outAmd["command"] = self.bttn_outAmd_command
    self.bttn_outAmd['state']   = 'disabled';

    bttn_help=tk.Button(root) #help button
    bttn_help["bg"] = "#00babd"
    bttn_help["borderwidth"] = "1px"
    bttn_help["bitmap"] = "question"
    bttn_help["text"]   = ""
    bttn_help.place(x=500,y=250,width=30,height=30)
    bttn_help["command"] = self.bttn_help_command

    #----------------- Radio Bttn
    self.radio_newEnt=tk.Radiobutton(root)
    self.radio_newEnt.place(x=10,y=160,width=25,height=30)
    self.radio_newEnt["variable"] = self.radioOpt
    self.radio_newEnt["value"] = 'n'
    self.radio_newEnt["command"] = self.radio_newEnt_command

    self.radio_amdEnt=tk.Radiobutton(root)
    self.radio_amdEnt.place(x=10,y=200,width=25,height=30)
    self.radio_amdEnt["variable"] = self.radioOpt
    self.radio_amdEnt["value"] = 'a'
    self.radio_amdEnt["command"] = self.radio_amdEnt_command

    #----------------- Begin tagg button
    bttn_beginTag=tk.Button(root)
    bttn_beginTag["activeforeground"] = "#733c69"
    bttn_beginTag["bg"] = "#ccd3dd"
    bttn_beginTag["borderwidth"] = "1.5px"
    ft = tkFont.Font(family='Calibri',size=14)
    bttn_beginTag["font"]    = ft
    bttn_beginTag["fg"]      = "#9e528f"
    bttn_beginTag["justify"] = "center"
    bttn_beginTag["text"]    = "Begin tagging"
    bttn_beginTag["relief"]  = "raised"
    bttn_beginTag.place(x=180,y=250,width=190,height=40)
    bttn_beginTag["command"] = self.bttn_beginTag_command


  #============== CALLOUT FUNCTIONS
  #select a workign directory
  def bttn_workingDir_command(self):
    tmp = fd.askdirectory()
    if tmp != '' and os.path.isdir(tmp):
      self.entry_workingDir.delete(0,tk.END)
      self.entry_workingDir.insert(0,os.path.normpath(tmp))
      self.entry_workingDir.xview_scroll(len(tmp)-51, tk.UNITS)
    elif not os.path.isdir(tmp):
      messagebox.showerror('Oh no!', 'The directory you selected does not exist!')

  
  #select a file that contains locations to video repos
  def bttn_videoRpo_command(self):
    tmp = fd.askopenfile().name
    if tmp != '' and os.path.isfile(tmp):
      self.entry_videoRpo.delete(0,tk.END)
      self.entry_videoRpo.insert(0,tmp)
      self.entry_videoRpo.xview_scroll(len(tmp)-51, tk.UNITS)
    elif not os.path.isfile(tmp):
      messagebox.showerror('Oh no!', 'The file you selected does not exist!')


  #if ammending, then select file
  def bttn_outAmd_command(self):
    tmp = fd.askopenfile().name
    if tmp != '' and os.path.isfile(tmp):
      self.entry_outAmd.delete(0,tk.END)
      self.entry_outAmd.insert(0,tmp)
      self.entry_outAmd.xview_scroll(len(tmp)-51, tk.UNITS)
    elif not os.path.isfile(tmp):
      messagebox.showerror('Oh no!', 'The file you selected does not exist!')


  def radio_newEnt_command(self):
    self.entry_outAmd['state'] = 'disabled';
    self.bttn_outAmd['state']  = 'disabled';
    self.bttn_outAmd["bg"]     = "#6f676c"
    self.entry_objTag['state'] = 'normal';


  def radio_amdEnt_command(self):
    self.entry_outAmd['state'] = 'normal';
    self.bttn_outAmd['state']  = 'normal';
    self.bttn_outAmd["bg"]     = "#733c61"
    self.entry_objTag['state'] = 'disabled';

  def bttn_help_command(self):
    messagebox.showinfo('Help!', 'learn how to use this at github.com/alberto-bortoni/biolocomotion-haar')


  #ensure that all entries are good then close app
  def bttn_beginTag_command(self):
    ver_workingDir = False
    ver_videoRepo  = False
    ver_objTag     = False
    ver_outAmd     = False

    #verify that entries are valid
    if os.path.isdir(self.entry_workingDir.get()):
      ver_workingDir = True
    
    if os.path.isfile(self.entry_videoRpo.get()):
      ver_videoRepo = True

    if self.radioOpt.get() == 'n':
      ver_outAmd = True
      if self.entry_objTag.get().isidentifier():
        ver_objTag = True
    else:
      ver_objTag = True
      if os.path.isfile(self.entry_outAmd.get()):
        ver_outAmd = True
    
    #ensure that all are valid
    if not (ver_workingDir and ver_videoRepo and ver_objTag and ver_outAmd):
      tmsg = ("Validity of each entry\n"
              "\n"
              "Working Directory: " + str(ver_workingDir) + "\n"
              "Video Repository:  " + str(ver_videoRepo) + "\n"
              "Object Tag:        " + str(ver_objTag) + "\n"
              "File to ammend:    " + str(ver_outAmd) + "\n"
              "\n"
              "Change entries before proceeding\n") 
      messagebox.showinfo('Entries not vallid', tmsg)
      return
    
    #if all entries are valid
    else:
      #get the values to be used later
      self.workingDir = os.path.normpath(self.entry_workingDir.get())
      self.videoRpo   = os.path.normpath(self.entry_videoRpo.get())
      self.objTag   = self.entry_objTag.get()
      self.outAmd   = os.path.normpath(self.entry_outAmd.get())
      self.beginTag = True

      tmsg = ('All looks good!\n' 'Now the tagging window will open.\n' 'Some files may be created.\n')
      messagebox.showinfo('READY!', tmsg)
      self.sroot.destroy()
      return


#=========================
if __name__ == "__main__":
  root = tk.Tk()
  app  = tk_objDetection(root)
  root.mainloop()

  
