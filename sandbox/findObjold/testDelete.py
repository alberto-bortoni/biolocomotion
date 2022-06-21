import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import cv2
import numpy as np
import math

root = tk.Tk()
root.geometry('1480x800')

# photo = Image.open('C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam1\\TS5-544-Cam1_2021-07-02_000108\\0000120.tif')


# # Make into Numpy array and normalise
# na   = np.array(photo)
# if na.dtype == np.dtype('uint16'):
#   print('hello')
# else:
#   print('no')

# na   = na/(2**8)
# na   = na.astype(np.uint8)
# photo1 = Image.fromarray(na)
# photo2 = photo1.resize((1000,800))
# photo3 = ImageTk.PhotoImage(photo2)
# photo.close()


# photo = Image.open('C:\\Users\\alberto-bortoni\\Desktop\\haartest\\test.png')
# img_dis = ImageTk.PhotoImage(photo)
# label = tk.Label(root, image=img_dis, width=1480, height=800)

photo = Image.open('C:\\Users\\alberto-bortoni\\Desktop\\haartest\\test.png')
img_dis = ImageTk.PhotoImage(photo)
# label = tk.Label(root, image=img_dis, width=1480, height=800)
# label.place(x=10,y=65)
label_img=tk.Label(root)
ft = tkFont.Font(family='Calibri',size=10)
label_img["font"] = ft
label_img["fg"] = "#333333"
label_img["justify"] = "center"
label_img["text"] = "image"
label_img["image"] = img_dis
label_img.place(x=10,y=65,width=1480,height=800)


#label = tk.Label(root, image=photo3, width=1480, height=800)
#label.pack()
photo.close()

root.mainloop()