import threading
import multiprocessing
import tk_objTag
import biolocomotion


def dostuff():
  wd = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest'
  repo = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\videoRepo.txt'
  out = 'C:\\Users\\alberto-bortoni\\Desktop\\haartest\\tags\\testbat.txt'

  a =multiprocessing.Process(target=count)
  a.start()
  a.terminate()

  print(a.is_alive()) 


  # t1=multiprocessing.Process(target=tk_objTag.objTag_main, args=(wd,repo,out),name='obj')
  # t2=multiprocessing.Process(target=biolocomotion.biolocomotion_main,name='main')


  
  # t2.start()
  # t1.start()



  print('after')


def count():
  return 1+1

# ts=threading.Thread(target=tk_objTag.objTag_main, args=(wd,repo,out))
# ts.daemon = True
# ts.start()
if __name__ == '__main__':
  dostuff()
