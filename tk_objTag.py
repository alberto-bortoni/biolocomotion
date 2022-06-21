import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import glob
import random
from PIL import Image, ImageTk
import math
import numpy as np
import csv
import shutil
from pathlib import Path
import time


class tk_objDetectionImg(tk.Toplevel):
  def __init__(self, root, workingDir, videoRepo, outFile):
    #---------------- class variables
    self.sroot      = root
    self.frsize_w   = 1480
    self.frsize_h   = 800
    self.frorig_x   = 10
    self.frorig_y   = 65
    self.ratio      = None
    self.dispw      = None
    self.disph      = None
    self.workingDir = workingDir
    self.videoRepo  = videoRepo
    self.outFile    = outFile
    self.videoList  = None
    self.outList    = None
    self.currImg    = None
    self.currImgNam = None
    self.markerSize = 16
    self.imgTagPtr  = None
    self.marker_xx  = None
    self.marker_yy  = None

    #---------------- setting base geometry
    root.title("Object tagging toolbox")
    width=1500
    height=900
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    #----------------- event bindings
    root.bind('s', self.key_prev)
    root.bind('d', self.key_next)
    root.bind('q', self.key_skip)
    root.bind("<Button-1>", self.left_click)

    #----------------- labels
    titleStyle = ttk.Style()
    titleStyle.configure('titleStyle.TLabel', font=('Calibri',20,'bold'))

    label_title = ttk.Label(root,text='Object Tagging Toolbox',style='titleStyle.TLabel', anchor=tk.CENTER)
    label_title.place(x=550,y=20,width=400,height=35)

    smallLabelStyle = ttk.Style()
    smallLabelStyle.configure('smallLabelStyle.TLabel', font=('Calibri',10))

    self.label_imgName=ttk.Label(root, text='image name', justify=tk.RIGHT, style='smallLabelStyle.TLabel')
    self.label_imgName.place(x=690,y=875,width=800,height=20)

    self.label_imgNum=ttk.Label(root, text='', justify=tk.LEFT, style='smallLabelStyle.TLabel')
    self.label_imgNum.place(x=20,y=875,width=50,height=20)

    
    #----------------- Buttons
    bttnStyle = ttk.Style()
    bttnStyle.configure('bttn.TButton', background='#3f333b', foreground='#3f333b', font=('Calibri',13))
    bttnStyle.map('bttn.TButton', background=[('active', '#48263d')])

    bttn_prev=ttk.Button(root, text='Previous (s)', style='bttn.TButton',command=self.bttn_prev_command)
    bttn_prev.place(x=10,y=20,width=130,height=35)

    bttn_next=ttk.Button(root, text='Next (d)', style='bttn.TButton',command=self.bttn_next_command)
    bttn_next.place(x=160,y=20,width=130,height=35)

    bttn_skip=ttk.Button(root, text='Skip/Delete (q)', style='bttn.TButton',command=self.bttn_skip_command)
    bttn_skip.place(x=310,y=20,width=130,height=35)

    bttn_quit=ttk.Button(root, text='Save and Quit', style='bttn.TButton',command=self.bttn_quit_command)
    bttn_quit.place(x=1360,y=20,width=130,height=35)

    #----------------- Image and crossmark
    self.label_img=tk.Label(root, justify=tk.CENTER)
    self.label_img.place(x=self.frorig_x,y=self.frorig_y,width=self.frsize_w,height=self.frsize_h)

    self.label_dot=tk.Label(root, bg='#e65e5e', justify=tk.CENTER, text='', state='disabled')
    self.label_dot.place(x=100,y=100,width=self.markerSize,height=self.markerSize)
    
    #load data in app
    self.loadProject()


  #-----------------------------------------------------------
  #============================================ INIT FUNCTIONS
  #___________________________________________________________
  def loadProject(self):
    random.seed()
    try:
      #--------------- Video Repo
      #TODO -- only works for videos exported as images
      #first open file
      tlist = None
      with open(os.path.normpath(self.videoRepo), 'r') as f:
        tlist = f.readlines()
        f.close()
      
      #now find number of frames and make list
      tlist = list(map(self.formatEntries, tlist))

      self.videoList = []
      for xx in tlist:
        self.videoList.extend(glob.glob(xx))


      #---------------- Output list
      self.outList = {}
      if os.path.isfile(self.outFile):
        with open(os.path.normpath(self.outFile), 'r') as f:
          rawFile = f.readlines()
          f.close()
        
        for entry in rawFile:
          tmp = entry.rstrip('\n').split(',')
          if tmp[1] == '':
            self.outList[tmp[0]] = (None, None, False)
          else:
            self.outList[tmp[0]] = (int(tmp[1]), int(tmp[2]), bool(tmp[3]))
    except:
      messagebox.showerror('Oh NO!', 'there was an error reading the files')
      self.sroot.destroy()

    #remove videos already categorixed from the repo
    for entry in self.outList.keys():
      self.videoList.pop(self.videoList.index(entry))
    
    #increase the indiex so user an browse back and forth over entries
    self.imgTagPtr = len(self.outList)-1
    
    # after reading from file, create a copy in the backup directory 
    #TODO -- check that backup dir exists
    tpath = Path(self.outFile)
    backFile = self.workingDir+'\\backup\\tags\\'+tpath.stem+'_'+str(math.floor(time.time()))+str(tpath.suffix)
    shutil.copyfile(self.outFile, backFile)

    #--------------- LoadImage
    self.bttn_next_command()


  #-----------------------------------------------------------
  #========================================= PROCESS FUNCTIONS
  #___________________________________________________________
  def getPrevImgIdx(self):
    tmp = list(self.outList.keys())
    
    self.marker_xx = self.outList[tmp[self.imgTagPtr]][0]
    self.marker_yy = self.outList[tmp[self.imgTagPtr]][1]
    self.label_imgName.config(text = tmp[self.imgTagPtr])
    self.label_imgNum.config(text=str(self.imgTagPtr+1) + ' / ' + str(len(self.outList)))
    self.loadImage(tmp[self.imgTagPtr], self.outList[tmp[self.imgTagPtr]][2])

  #___________________________________________________________
  def getNextImgIdx(self):
    tmp = list(self.outList.keys())

    #if showing a new image
    if len(tmp) < self.imgTagPtr+1 or len(tmp) == 0: 
      #ensure that there is more to go, otherwise exit
      if len(self.videoList) == 0:
        messagebox.showinfo('!dne ehT', 'It seems like all the images in the video repo file have been tagged. Manually save and exit to quit')
        return

      #get an unsued index first
      idx = random.randint(0,len(self.videoList)-1)

      self.marker_xx = None
      self.marker_yy = None
      self.label_imgName.config(text = self.videoList[idx])
      self.label_imgNum.config(text=str(self.imgTagPtr+1) + ' / ' + str(len(self.outList)))
      self.loadImage(self.videoList[idx], False)
    
    #if showing a previously seen image ahead if index pointer
    else:
      self.marker_xx = self.outList[tmp[self.imgTagPtr]][0]
      self.marker_yy = self.outList[tmp[self.imgTagPtr]][1]
      self.label_imgName.config(text = tmp[self.imgTagPtr])
      self.label_imgNum.config(text=str(self.imgTagPtr+1) + ' / ' + str(len(self.outList)))
      self.loadImage(tmp[self.imgTagPtr], self.outList[tmp[self.imgTagPtr]][2])
    
  #___________________________________________________________
  def loadImage(self, key, mark):
    #get image and resize
    imgraw = Image.open(key)
    imgw   = imgraw.size[0]
    imgh   = imgraw.size[1]

    if self.frsize_w/imgw < self.frsize_h/imgh:
      self.ratio = self.frsize_w/imgw
      self.dispw = self.frsize_w
      self.disph = math.floor(self.ratio*imgh)
    else:
      self.ratio = self.frsize_h/imgh
      self.dispw = math.floor(self.ratio*imgw)
      self.disph = self.frsize_h

    #convert to numpy array and display
    #TODO -- this seems to be necesary because either tkinter is no good with tiffs or bit depth is odd
    #TODO -- hardcoding when it imports it as 16 bit format with 8 bit shift
    #TODO -- a msg will ensure the user knows this ahrdcoding is no good
    
    img_arr = np.array(imgraw)
    if img_arr.dtype is np.dtype('uint16'):
      divisor = 8
    elif img_arr.dtype is np.dtype('uint8'):
      divisor = 1
    else:
      messagebox.showerror('Oh NO!', 'Hardcode error: the bit depth of this immage is not uint16 but: '+ str(img_arr.dtype))
      return
    
    img_arr = img_arr/(2**divisor)
    img_arr = img_arr.astype(np.uint8)
    img_cov = Image.fromarray(img_arr)
    img_cov = img_cov.resize((self.dispw, self.disph))
    self.currImg    = ImageTk.PhotoImage(img_cov)
    self.currImgNam = str(key)

    imgraw.close()

    #add image and remove marker
    if mark:
      txx = self.frorig_x + math.floor((self.frsize_w - self.dispw)/2) + self.outList[key][0] - self.markerSize/2
      tyy = self.frorig_y + math.floor((self.frsize_h - self.disph)/2) + self.outList[key][1] - self.markerSize/2
      self.label_dot.place(x=txx,y=tyy,width=self.markerSize,height=self.markerSize)
    else:
      self.label_dot.place_forget()

    
    self.label_img.config(image=self.currImg)


  #-----------------------------------------------------------
  #========================================= BINDING FUNCTIONS
  #___________________________________________________________
  def bttn_prev_command(self):
    if self.imgTagPtr > 0:
      self.imgTagPtr = self.imgTagPtr - 1
      self.getPrevImgIdx()
    
  #___________________________________________________________
  def bttn_next_command(self):
    #if new image is being tagged
    if self.marker_xx is not None:
      self.outList[self.currImgNam] = (self.marker_xx, self.marker_yy, True)

      if self.currImgNam in self.videoList and self.currImg in self.outList: 
        self.videoList.pop(self.videoList.index(self.currImgNam))
      
    #if it is at the end of the list
    if len(self.outList)>=self.imgTagPtr+1:
      self.imgTagPtr = self.imgTagPtr + 1


    self.getNextImgIdx()

  #___________________________________________________________
  def bttn_skip_command(self):
    self.outList[self.currImgNam] = (None, None, False)

    if self.currImgNam in self.videoList:
      self.videoList.pop(self.videoList.index(self.currImgNam))

    self.imgTagPtr = self.imgTagPtr + 1
    self.getNextImgIdx()

  #___________________________________________________________
  def key_prev(self,event):
    self.bttn_prev_command()

  #___________________________________________________________
  def key_next(self,event):
    self.bttn_next_command()

  #___________________________________________________________
  def key_skip(self,event):
    self.bttn_skip_command()

  #___________________________________________________________
  def left_click(self,event):
    if str(event.widget)[1:] == str(self.label_img.winfo_name()):
      xx = event.x - math.floor((self.frsize_w - self.dispw)/2)
      yy = event.y - math.floor((self.frsize_h - self.disph)/2)

      if xx >= 0 and xx <= self.dispw and yy >= 0 and yy <= self.disph:
        self.marker_xx = xx
        self.marker_yy = yy
        self.label_dot.place(x=(event.x+self.frorig_x-self.markerSize/2),y=(event.y+self.frorig_y-self.markerSize/2),width=self.markerSize,height=self.markerSize)

  #___________________________________________________________
  def bttn_quit_command(self):
    try:
      tlist = list(map(self.formatlist, self.outList))

      with open(self.outFile, 'w',  newline='') as f:
          writer = csv.writer(f)
          writer.writerows(tlist)
          f.close()

      messagebox.showinfo('Oh NO!', 'New tags appended succesfuly! closing app now =)')
      self.sroot.destroy()
    except:
      messagebox.showerror('Oh NO!', 'there was an error saving the files!! closing and loosing new tags.... =(')
      self.sroot.destroy()


  #-----------------------------------------------------------
  #============================================= MAP FUNCTIONS
  #___________________________________________________________
  def formatEntries(self, xx):
    return os.path.normpath(xx.rstrip('\n') + '\\*.tif')
  
  #___________________________________________________________
  def formatlist(self, xx):
    return [xx, self.outList[xx][0], self.outList[xx][1], self.outList[xx][2]]

  #___________________________________________________________
  def parseFile(self, xx):
    return [xx, self.outList[xx][0], self.outList[xx][1], self.outList[xx][2]]


#-------------------------------------------------------------
#=============================================== MAP FUNCTIONS
#_____________________________________________________________
def objTag_main(workingDir, videoRepo, outAmd):
    objTag_root = tk.Tk()
    app  = tk_objDetectionImg(objTag_root, workingDir, videoRepo, outAmd)
    objTag_root.mainloop()

#_____________________________________________________________
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Object tagging toolbox')
    parser.add_argument('--wd', metavar='path', required=True,
                        help='the path the working directory')
    parser.add_argument('--repo', metavar='path', required=True,
                        help='The path to the video repository file')
    parser.add_argument('--out', metavar='path', required=True,
                        help='Output/ammend file')
    args = parser.parse_args()
    objTag_main(workingDir=args.wd, videoRepo=args.repo, outAmd=args.out)

    # wd = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest'
    # repo = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\videoRepo.txt'
    # out = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\tags\\testbat.txt'
    # objTag_main(workingDir=wd, videoRepo=repo, outAmd=out)
