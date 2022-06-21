import csv
import os
from pathlib import Path
import time
import math

# def formatlist(xx):
#   return [xx, dic[xx][0], dic[xx][1], dic[xx][2]]


# dic = {'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam1\\TS5-544-Cam1_2021-07-02_000107\\0000238.tif': (545, 325, True), 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam3\\IL5-534-Cam3_2021-07-02_000108\\0000441.tif': (528, 394, True), 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam3\\IL5-534-Cam3_2021-07-02_000108\\0000319.tif': (215, 345, True), 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam1\\TS5-544-Cam1_2021-07-02_000107\\0000083.tif': (648, 352, True), 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam3\\IL5-534-Cam3_2021-07-02_000108\\0000094.tif': (599, 242, True), 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\vids\\cam2\\IL5-519-Cam2_2021-07-02_000108\\0000289.tif': (260, 120, True)}


# tlist = list(map(formatlist, dic))

# with open("file.txt", "w",  newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(tlist)

outFile = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\batObj.txt'

# outList = {}
# with open(os.path.normpath(outFile), 'r') as f:
#   rawFile = f.readlines()
#   f.close()

# for entry in rawFile:
#   tmp = entry.rstrip('\n').split(',')
#   outList[tmp[0]] = (tmp[1], tmp[2], tmp[3])

# keys = list(outList.keys())
# print(keys[0])


p = Path(outFile)
print(str(p.parent)+'\\backup\\objTags\\'+p.stem+'_'+str(math.floor(time.time()))+str(p.suffix))