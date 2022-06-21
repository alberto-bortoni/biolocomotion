import tkinter as tk
import tkinter.font as tkFont
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


class tk_objDetectionImg:
  def __init__(self, root, workingDir, videoRepo, outFile):
    #key class variables for gui
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
    labelFgCol      = '#333333'

    #setting app objects
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
    label_title=tk.Label(root)
    label_title['anchor'] = tk.CENTER
    ft = tkFont.Font(family='Calibri',size=20,weight='bold')
    label_title['font'] = ft
    label_title['fg']   = labelFgCol
    label_title['text'] = "Object Tagging Toolbox"
    label_title.place(x=550,y=20,width=400,height=35)

    self.label_imgName=tk.Label(root)
    ft = tkFont.Font(family='Calibri',size=10)
    self.label_imgName['font'] = ft
    self.label_imgName['fg']   = labelFgCol
    self.label_imgName['justify'] = tk.RIGHT
    self.label_imgName['text'] = "image name"
    self.label_imgName.place(x=690,y=875,width=800,height=20)

    self.label_imgNum=tk.Label(root)
    ft = tkFont.Font(family='Calibri',size=10)
    self.label_imgNum['font'] = ft
    self.label_imgNum['fg']   = labelFgCol
    self.label_imgNum['justify'] = tk.LEFT
    self.label_imgNum['text'] = ""
    self.label_imgNum.place(x=20,y=875,width=50,height=20)

    #----------------- Buttons
    bttn_prev=tk.Button(root)
    bttn_prev['bg'] = "#cccccc"
    bttn_prev['activeforeground'] = "#733c69"
    bttn_prev['activebackground'] = "#979797"
    ft = tkFont.Font(family='Calibri',size=12,weight='bold')
    bttn_prev['font'] = ft
    bttn_prev['fg']   = "#000000"
    bttn_prev['justify'] = "center"
    bttn_prev['text'] = "Previous (s)"
    bttn_prev.place(x=10,y=20,width=130,height=35)
    bttn_prev['command'] = self.bttn_prev_command

    bttn_next=tk.Button(root)
    bttn_next['bg'] = "#cccccc"
    bttn_next['activeforeground'] = "#733c69"
    bttn_next['activebackground'] = "#979797"
    ft = tkFont.Font(family='Calibri',size=12,weight='bold')
    bttn_next['font'] = ft
    bttn_next['fg']   = "#000000"
    bttn_next['justify'] = "center"
    bttn_next['text'] = "Next (d)"
    bttn_next.place(x=160,y=20,width=130,height=35)
    bttn_next['command'] = self.bttn_next_command

    bttn_skip=tk.Button(root)
    bttn_skip['bg'] = "#cccccc"
    bttn_skip['activeforeground'] = "#733c69"
    bttn_skip['activebackground'] = "#979797"
    ft = tkFont.Font(family='Calibri',size=12,weight='bold')
    bttn_skip['font'] = ft
    bttn_skip['fg'] = "#000000"
    bttn_skip['justify'] = "center"
    bttn_skip['text'] = "Skip/Delete (q)"
    bttn_skip.place(x=310,y=20,width=130,height=35)
    bttn_skip['command'] = self.bttn_skip_command

    bttn_quit=tk.Button(root)
    bttn_quit['bg'] = "#cccccc"
    bttn_quit['activeforeground'] = "#733c69"
    bttn_quit['activebackground'] = "#979797"
    ft = tkFont.Font(family='Calibri',size=12,weight='bold')
    bttn_quit['font'] = ft
    bttn_quit['fg'] = "#000000"
    bttn_quit['justify'] = "center"
    bttn_quit['text'] = "Save and Quit"
    bttn_quit.place(x=1360,y=20,width=130,height=35)
    bttn_quit['command'] = self.bttn_quit_command

    #----------------- Image and crossmark
    self.label_img=tk.Label(root)
    self.label_img['justify'] = "center"
    self.label_img.place(x=self.frorig_x,y=self.frorig_y,width=self.frsize_w,height=self.frsize_h)

    self.label_dot=tk.Label(root)
    self.label_dot['bg'] = "#e65e5e"
    self.label_dot['justify'] = tk.CENTER
    self.label_dot['text'] = ""
    self.label_dot['state']   = 'disabled';
    self.label_dot.place(x=100,y=100,width=self.markerSize,height=self.markerSize)
    
    #load data in app
    self.loadProject()


  #-----------------------------------------------------------
  #============================================ INIT FUNCTIONS
  #________________________________
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
    tpath = Path(outFile)
    backFile = self.workingDir+'\\backup\\objTags\\'+tpath.stem+'_'+str(math.floor(time.time()))+str(tpath.suffix)
    shutil.copyfile(outFile, backFile)

    #--------------- LoadImage
    self.bttn_next_command()



  #-----------------------------------------------------------
  #========================================= PROCESS FUNCTIONS
  #________________________________
  def getPrevImgIdx(self):
    tmp = list(self.outList.keys())
    
    self.marker_xx = self.outList[tmp[self.imgTagPtr]][0]
    self.marker_yy = self.outList[tmp[self.imgTagPtr]][1]
    self.label_imgName['text'] = tmp[self.imgTagPtr]
    self.label_imgNum['text']  = str(self.imgTagPtr+1) + ' / ' + str(len(self.outList))
    self.loadImage(tmp[self.imgTagPtr], self.outList[tmp[self.imgTagPtr]][2])


  #________________________________
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
      self.label_imgName['text'] = self.videoList[idx]
      self.label_imgNum['text']  = str(self.imgTagPtr+1) + ' / ' + str(len(self.outList))
      self.loadImage(self.videoList[idx], False)
    
    #if showing a previously seen image ahead if index pointer
    else:
      self.marker_xx = self.outList[tmp[self.imgTagPtr]][0]
      self.marker_yy = self.outList[tmp[self.imgTagPtr]][1]
      self.label_imgName['text'] = tmp[self.imgTagPtr]
      self.label_imgNum['text']  = str(self.imgTagPtr+1) + ' / ' + str(len(self.outList))
      self.loadImage(tmp[self.imgTagPtr], self.outList[tmp[self.imgTagPtr]][2])
  
  
  #________________________________
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

    self.label_img['image'] = self.currImg
  


  #-----------------------------------------------------------
  #========================================= BINDING FUNCTIONS
  #________________________________
  def bttn_prev_command(self):
    if self.imgTagPtr > 0:
      self.imgTagPtr = self.imgTagPtr - 1
      self.getPrevImgIdx()
    

  #________________________________
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


  #________________________________
  def bttn_skip_command(self):
    self.outList[self.currImgNam] = (None, None, False)

    if self.currImgNam in self.videoList:
      self.videoList.pop(self.videoList.index(self.currImgNam))

    self.imgTagPtr = self.imgTagPtr + 1
    self.getNextImgIdx()


  #________________________________
  def key_prev(self,event):
    self.bttn_prev_command()


  #________________________________
  def key_next(self,event):
    self.bttn_next_command()


  #________________________________
  def key_skip(self,event):
    self.bttn_skip_command()


  #________________________________
  def left_click(self,event):
    if str(event.widget)[1:] == str(self.label_img.winfo_name()):
      xx = event.x - math.floor((self.frsize_w - self.dispw)/2)
      yy = event.y - math.floor((self.frsize_h - self.disph)/2)

      if xx >= 0 and xx <= self.dispw and yy >= 0 and yy <= self.disph:
        self.marker_xx = xx
        self.marker_yy = yy
        self.label_dot.place(x=(event.x+self.frorig_x-self.markerSize/2),y=(event.y+self.frorig_y-self.markerSize/2),width=self.markerSize,height=self.markerSize)


  #________________________________
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
  #________________________________
  def formatEntries(self, xx):
    return os.path.normpath(xx.rstrip('\n') + '\\*.tif')
  
  #________________________________
  def formatlist(self, xx):
    return [xx, self.outList[xx][0], self.outList[xx][1], self.outList[xx][2]]

  #________________________________
  def parseFile(self, xx):
    return [xx, self.outList[xx][0], self.outList[xx][1], self.outList[xx][2]]



def objTag_main(workingDir, videoRepo, outAmd):
    root = tk.Tk()
    app  = tk_objDetectionImg(root, workingDir, videoRepo, outAmd)
    root.mainloop()


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

















# import tkinter as tk
# root = tk.Tk()

# def motion(event):
#     x, y = event.x, event.y
#     print('{}, {}'.format(x, y))

# root.bind('<Motion>', motion)
# root.mainloop()

# #https://www.youtube.com/watch?v=pcmd-kNQpx4