import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import multiprocessing
import tk_objTag
import errno

#TODO -- add all self. variables and methods to header
class biolocomotion:
  def __init__(self, root):
    #---------------- base variables
    self.workingDir = None;

    #objTag
    self.objTag_beginTag = False;
    self.objTag_videoRpo = None;
    self.objTag_objTag   = None;
    self.objTag_outAmd   = None;
    self.objTag_radioOpt = tk.StringVar();

    #---------------- child processes
    self.objTag_proc = multiprocessing.Process()

    #---------------- setting base geometry
    root.title('Biolocomotion Haar Cascade')
    width  = 800
    height = 310
    screenwidth  = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    #---------------- Create frames
    #general grid layout
    root.columnconfigure(0,weight=1)
    root.columnconfigure(1,weight=15)
    root.rowconfigure(0,weight=1)
    root.rowconfigure(1,weight=6)
    
    #---------------- title and help button
    titleStyle = ttk.Style()
    titleStyle.configure('main_titleStyle.TLabel', font=('Calibri',18,'bold'))
    label_title = ttk.Label(root,text='Biolocomotion Haar Cascade Trainer',style='main_titleStyle.TLabel')
    label_title.grid(row=0,column=0,columnspan=2)

    tmp = Image.open(os.path.join(os.getcwd(),'res\\buttons\\question.png'))
    self.img_cov  = tmp.resize((20, 20))
    self.helpIcon = ImageTk.PhotoImage(self.img_cov)
    bttn_help=ttk.Button(root, image=self.helpIcon, command=self.bttn_help_command,) #help button
    bttn_help.place(x=760,y=10)

    #---------------- make all frames
    self.mainCtl   = ttk.Frame(root,width=200,height=310)
    self.mainCtl.grid(row=1,column=0,padx=10,pady=10,ipadx=0,ipady=0, sticky=tk.EW+tk.NS)

    self.baseFr  = ttk.Frame(root,width=500,height=310)
    self.baseFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

    self.objTagFr  = ttk.Frame(root,width=500,height=310)
    self.objTagFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)
    
    self.objCropFr = ttk.Frame(root,width=500,height=310)
    self.objCropFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)
    
    self.trainHcFr = ttk.Frame(root,width=500,height=310)
    self.trainHcFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

    #---------------- hide frames
    self.baseFr.grid_forget()
    self.objTagFr.grid_forget()
    self.objCropFr.grid_forget()
    self.trainHcFr.grid_forget()

    #---------------- Create content on all containers
    self.createMainGui(self.mainCtl)
    self.createBaseFrame(self.baseFr)
    self.createObjTagFrame(self.objTagFr)
    self.createObjCropFrame(self.objCropFr)
    self.createHaarFrame(self.trainHcFr)

    #---------------- enable base container
    self.bttn_base_cmd()


  #-----------------------------------------------------------
  #=============================================== INIT FRAMES
  #___________________________________________________________
  def createMainGui(self, container):
    container.grid_columnconfigure(0, weight=1)

    bttnStyle = ttk.Style()
    bttnStyle.configure('main_bttn.TButton', font=('Calibri',12))

    self.main_bttn2 = ttk.Style()
    self.changePathBttnColor('r')

    bttn_base = ttk.Button(container,text='Set path',width=20, style='main_bttn2.TButton', command=self.bttn_base_cmd)
    bttn_base.grid(row=0,column=0,pady=5, sticky=tk.EW)

    bttn_objTag = ttk.Button(container, text='Tag objects',width=20, style='main_bttn.TButton', command=self.bttn_tag_cmd)
    bttn_objTag.grid(row=1,column=0,pady=5, sticky=tk.EW)

    bttn_objCrop = ttk.Button(container, text='Center/Crop objects ',width=20, style='main_bttn.TButton', command=self.bttn_crop_cmd)
    bttn_objCrop.grid(row=2,column=0,pady=5, sticky=tk.EW)

    bttn_trainHaar = ttk.Button(container, text='Train Haar Cascade',width=20, style='main_bttn.TButton', command=self.bttn_train_cmd)
    bttn_trainHaar.grid(row=3,column=0,pady=5, sticky=tk.EW)

  #___________________________________________________________
  def changePathBttnColor(self, rg):
    if rg == 'g':
      self.main_bttn2.configure('main_bttn2.TButton', background='#488740', foreground='#488740', font=('Calibri',12))
      self.main_bttn2.map('main_bttn2.TButton', background=[('active', '#315c2c')])
    else:
      self.main_bttn2.configure('main_bttn2.TButton', background='#874040', foreground='#874040', font=('Calibri',12))
      self.main_bttn2.map('main_bttn2.TButton', background=[('active', '#5c2c2c')])
  
  #___________________________________________________________
  def createBaseFrame(self, container):
    entryBackCol    = '#9c8553'

    #----------------- grid layout
    container.grid_columnconfigure(0, weight=2)
    container.grid_columnconfigure(1, weight=4)
    container.grid_columnconfigure(2, weight=1)

    #----------------- labels
    labelStyle = ttk.Style()
    labelStyle.configure('labelStyle_base.TLabel', font=('Calibri',14))

    label_workingDir=ttk.Label(container, text='Working directory [d]', style='labelStyle_base.TLabel', justify='right')
    label_workingDir.grid(row=2,column=1,padx=2,pady=40,columnspan=1,sticky=tk.E)

    #----------------- Entries
    entryStyle = ttk.Style()
    entryStyle.configure('entryStyle_base.TEntry', font=('Calibri',11), foreground=entryBackCol)

    self.base_entry_workingDir=ttk.Entry(container, cursor='shuttle', width=50, style='entryStyle_base.TEntry', justify='left')
    self.base_entry_workingDir.grid(row=2,column=2,padx=2,pady=2,columnspan=1,sticky=tk.EW)

    #----------------- Buttons
    bttnStyle = ttk.Style()
    bttnStyle.configure('bttnStyle_base.TButton', background='#733c61', foreground='#733c61', font=('Calibri',10))
    bttnStyle.map('bttnStyle_base.TButton', background=[('active', '#48263d')])

    bttn_workingDir=ttk.Button(container, text='', width=4, style='bttnStyle_base.TButton', command=self.base_bttn_workingDir_cmd)
    bttn_workingDir.grid(row=2,column=3,padx=2,pady=2,columnspan=1,sticky=tk.EW)

  #___________________________________________________________
  def createObjTagFrame(self, container):
    #key class variables for gui
    self.objTag_radioOpt.set('n')
    entryBackCol    = '#9c8553'

    #----------------- grid layout
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=3)
    container.grid_columnconfigure(2, weight=4)
    container.grid_columnconfigure(3, weight=1)
    
    #----------------- labels
    titleStyle = ttk.Style()
    titleStyle.configure('titleStyle_objTag.TLabel', font=('Calibri',16))

    label_title=ttk.Label(container, text='Object Tagging Toolbox', style='titleStyle_objTag.TLabel', justify='center')
    label_title.grid(row=0,column=0,columnspan=4)

    label_space1=ttk.Label(container, text='', style='titleStyle_objTag.TLabel', justify='center')
    label_space1.grid(row=1,column=0,columnspan=4,sticky=tk.EW)

    labelStyle = ttk.Style()
    labelStyle.configure('labelStyle_objTag.TLabel', font=('Calibri',14))

    label_videoRpo=ttk.Label(container, text='Video repository [f]', style='labelStyle_objTag.TLabel', justify='right')
    label_videoRpo.grid(row=2,column=1,padx=2,pady=5,columnspan=1,sticky=tk.E)

    label_objTag=ttk.Label(container, text='Object tag [str]', style='labelStyle_objTag.TLabel', justify='right')
    label_objTag.grid(row=3,column=1,padx=2,pady=5,columnspan=1,sticky=tk.E)

    label_outAmd=ttk.Label(container, text='Output/amend [f]', style='labelStyle_objTag.TLabel', justify='right')
    label_outAmd.grid(row=4,column=1,padx=2,pady=5,columnspan=1,sticky=tk.E)

    #----------------- Entries
    entryStyle = ttk.Style()
    entryStyle.configure('entryStyle_objTag.TEntry', font=('Calibri',11), foreground=entryBackCol)

    self.objTag_entry_videoRpo=ttk.Entry(container, cursor='shuttle', width=50 ,style='entryStyle_objTag.TEntry', justify='left')
    self.objTag_entry_videoRpo.grid(row=2,column=2,padx=2,pady=5,columnspan=1,sticky=tk.EW)

    self.objTag_entry_objTag=ttk.Entry(container, cursor='shuttle', width=50 ,style='entryStyle_objTag.TEntry', justify='left', state='normal')
    self.objTag_entry_objTag.grid(row=3,column=2,padx=2,pady=5,columnspan=1,sticky=tk.EW)

    self.objTag_entry_outAmd=ttk.Entry(container, cursor='shuttle', width=50 ,style='entryStyle_objTag.TEntry', justify='left', state='disabled')
    self.objTag_entry_outAmd.grid(row=4,column=2,padx=2,pady=5,columnspan=1,sticky=tk.EW)

    #----------------- Buttons
    bttnStyle = ttk.Style()
    bttnStyle.configure('bttnStyle_objTag.TButton', background='#733c61', foreground='#733c61', font=('Calibri',10))
    bttnStyle.map('bttnStyle_objTag.TButton', background=[('active', '#48263d')])

    bttn_videoRpo=ttk.Button(container, text='', width=4, style='bttnStyle_objTag.TButton', command=self.objTag_bttn_videoRpo_command)
    bttn_videoRpo.grid(row=2,column=3,padx=2,pady=5,columnspan=1,sticky=tk.EW)

    self.objTag_bttn_outAmd=ttk.Button(container, text='', width=4, style='bttnStyle_objTag.TButton', command=self.objTag_bttn_outAmd_command)
    self.objTag_bttn_outAmd.grid(row=4,column=3,padx=5,pady=2,columnspan=1,sticky=tk.EW)

    #----------------- Radio Bttn
    self.objTag_radio_newEnt=ttk.Radiobutton(container, variable=self.objTag_radioOpt, value='n', command=self.objTag_rNewEnt_command)
    self.objTag_radio_newEnt.grid(row=3,column=0,padx=5,pady=5)

    self.objTag_radio_amdEnt=ttk.Radiobutton(container, variable=self.objTag_radioOpt, value='a', command=self.objTag_rAmdEnt_command)
    self.objTag_radio_amdEnt.grid(row=4,column=0,padx=5,pady=5)


    # #----------------- Begin tagg button
    bttnStyle2 = ttk.Style()
    bttnStyle2.configure('bttnStyle2_objTag.TButton', background='#733c61', foreground='#733c61', font=('Calibri',14))
    bttnStyle2.map('bttnStyle2_objTag.TButton', background=[('active', '#48263d')])
    
    objTag_bttn_beginTag=ttk.Button(container, text='Begin tagging', width=20, style='bttnStyle2_objTag.TButton', command=self.objTag_bttn_beginTag_command)
    objTag_bttn_beginTag.grid(row=6,column=1, columnspan=2, pady=20)
    
  #___________________________________________________________
  def createObjCropFrame(self, container):
    print('er')

  #___________________________________________________________
  def createHaarFrame(self, container):
    print('here')


  #-----------------------------------------------------------
  #====================================== MAIN BUTTON CALLOUTS
  #___________________________________________________________
  def bttn_base_cmd(self):
    self.baseFr.grid_forget()
    self.objTagFr.grid_forget()
    self.objCropFr.grid_forget()
    self.trainHcFr.grid_forget()

    self.baseFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

  #___________________________________________________________
  def bttn_tag_cmd(self):
    self.baseFr.grid_forget()
    self.objTagFr.grid_forget()
    self.objCropFr.grid_forget()
    self.trainHcFr.grid_forget()
    
    self.objTagFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

  #___________________________________________________________
  def bttn_crop_cmd(self):
    self.baseFr.grid_forget()
    self.objTagFr.grid_forget()
    self.objCropFr.grid_forget()
    self.trainHcFr.grid_forget()
    
    self.objCropFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

  #___________________________________________________________
  def bttn_train_cmd(self):
    self.baseFr.grid_forget()
    self.objTagFr.grid_forget()
    self.objCropFr.grid_forget()
    self.trainHcFr.grid_forget()
    
    self.trainHcFr.grid(row=1,column=1,padx=10,pady=10,ipadx=10,ipady=10, sticky=tk.EW+tk.NS)

  #-----------------------------------------------------------
  #============================================ BASE FUNCTIONS
  #___________________________________________________________
  def base_bttn_workingDir_cmd(self):
    tmp = fd.askdirectory()
    if tmp != '' and os.path.isdir(tmp):
      self.base_entry_workingDir.delete(0,tk.END)
      self.base_entry_workingDir.insert(0,os.path.normpath(tmp))
      self.base_entry_workingDir.xview_scroll(len(tmp)-51, tk.UNITS)
      self.workingDir = os.path.normpath(tmp)
      self.changePathBttnColor('g')
    elif not os.path.isdir(tmp):
      self.changePathBttnColor('r')
      messagebox.showerror('Oh no!', 'The directory you selected does not exist!')

  #___________________________________________________________
  def bttn_help_command(self):
    messagebox.showinfo('Help!', 'learn how to use this at github.com/alberto-bortoni/biolocomotion-haar')

  #-----------------------------------------------------------
  #================================== OBJECT TAGGING FUNCTIONS
  #___________________________________________________________
  def objTag_bttn_videoRpo_command(self):
    tmp = fd.askopenfile().name
    if tmp != '' and os.path.isfile(tmp):
      self.objTag_entry_videoRpo.delete(0,tk.END)
      self.objTag_entry_videoRpo.insert(0,tmp)
      self.objTag_entry_videoRpo.xview_scroll(len(tmp)-51, tk.UNITS)
    elif not os.path.isfile(tmp):
      messagebox.showerror('Oh no!', 'The file you selected does not exist!')

  #___________________________________________________________
  def objTag_bttn_outAmd_command(self):
    tmp = fd.askopenfile().name
    if tmp != '' and os.path.isfile(tmp):
      self.objTag_entry_outAmd.delete(0,tk.END)
      self.objTag_entry_outAmd.insert(0,tmp)
      self.objTag_entry_outAmd.xview_scroll(len(tmp)-51, tk.UNITS)
    elif not os.path.isfile(tmp):
      messagebox.showerror('Oh no!', 'The file you selected does not exist!')

  #___________________________________________________________
  def objTag_rNewEnt_command(self):
    self.objTag_entry_outAmd['state'] = 'disabled';
    self.objTag_bttn_outAmd['state']  = 'disabled';
    self.objTag_entry_objTag['state'] = 'normal';

  #___________________________________________________________
  def objTag_rAmdEnt_command(self):
    self.objTag_entry_outAmd['state'] = 'normal';
    self.objTag_bttn_outAmd['state']  = 'normal';
    self.objTag_entry_objTag['state'] = 'disabled';

  #___________________________________________________________
  def objTag_bttn_beginTag_command(self):
    ver_workingDir = False
    ver_videoRepo  = False
    ver_objTag     = False
    ver_outAmd     = False

    #verify that entries are valid
    if os.path.isdir(self.base_entry_workingDir.get()):
      ver_workingDir = True
    
    if os.path.isfile(self.objTag_entry_videoRpo.get()):
      ver_videoRepo = True

    if self.objTag_radioOpt.get() == 'n':
      ver_outAmd = True
      if self.objTag_entry_objTag.get().isidentifier():
        ver_objTag = True
    else:
      ver_objTag = True
      if os.path.isfile(self.objTag_entry_outAmd.get()):
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
      self.workingDir = os.path.normpath(self.base_entry_workingDir.get())
      self.objTag_videoRpo = os.path.normpath(self.objTag_entry_videoRpo.get())
      self.objTag_objTag   = self.objTag_entry_objTag.get()
      self.objTag_outAmd   = os.path.normpath(self.objTag_entry_outAmd.get())
      self.objTag_beginTag = True

      #if it is a new tag, then create a file to dump tags
      if self.objTag_radioOpt.get() == 'n':
        try:
          os.makedirs(os.path.join(self.workingDir,'backup','tags'), exist_ok=True)
          os.makedirs(os.path.join(self.workingDir,'tags'), exist_ok=True)
          self.objTag_outAmd = os.path.normpath(os.path.join(self.workingDir, 'tags', (self.objTag_objTag+'.txt')))
          with open(self.objTag_outAmd, 'x') as f:
            f.close()
        except OSError as exc:
          if exc.errno != errno.EEXIST:
              raise
          pass

      #exit and create instance of video tagging tool
      if not self.objTag_proc.is_alive():
        tmsg = ('All looks good!\n' 'Now the tagging window will open.\n' 'Some files may be created.\n')
        messagebox.showinfo('READY!', tmsg)

        self.objTag_proc = multiprocessing.Process(target=tk_objTag.objTag_main, args=(self.workingDir,self.objTag_videoRpo,self.objTag_outAmd))
        self.objTag_proc.start()
      
      return


  #-----------------------------------------------------------
  #================================= OBJECT CROPPING FUNCTIONS



#-------------------------------------------------------------
#===================================== HAAR TRAINING FUNCTIONS
#_____________________________________________________________
def biolocomotion_main():
  biolocomotionRoot = tk.Tk()
  app  = biolocomotion(biolocomotionRoot)
  biolocomotionRoot.mainloop()

#_____________________________________________________________
if __name__ == "__main__":
  biolocomotion_main()

  
