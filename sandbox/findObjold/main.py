import tkinter as tk
import findObj
import imageMark
import os

root = tk.Tk()
app  = findObj.tk_objDetection(root)
root.mainloop()


print('')
print('APP OUT:')
print(app.beginTag)
print(app.workingDir)
print(app.videoRpo)
print(app.objTag)
print(app.outAmd)



# workingDir = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest'
# videoRepo  = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\videoRepo.txt'
# outFile    = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\batObj.txt'

# root = tk.Tk()
# app  = imageMark.tk_objDetectionImg(root, workingDir, videoRepo, outFile)\p\men-s-design-by-humans-cat-cat-cat-by-radiomode-t-shirt\-\A-82811126
# root.mainloop()


#create backup directory
    # if self.projType == 'n':
    #   if os.path.exists(os.path.normpath(self.workingDir + '\\' + self.objTag + '.txt')):
    #     messagebox.showerror('Oh NO!', 'The output file seems to exist' + self.objTag + '.txt')
    #     return
    #   tfile = open(os.path.normpath(self.workingDir + '\\' + self.objTag + '.txt'), 'w+')
    #   tfile.close()

