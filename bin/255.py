# coding=gbk

import to_raster
import os
#from matplotlib import pyplot as plt
import numpy as np
import log_process
import time


this_root = os.getcwd()+'\\..\\'

fdir = this_root+'MRT_resample\\'
save_dir = this_root+'MRT_resample_trans\\'
flist = os.listdir(fdir)



time_init = time.time()
flag = 0
for f in flist:
    time_start = time.time()
    #print(f)
    array, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(fdir+f)
    new = array/255.
    # plt.imshow(new)
    # plt.colorbar()
    # plt.show()
    newRasterfn = save_dir+f
    to_raster.array2raster(newRasterfn,originX,originY,pixelWidth,pixelHeight,new)
    time_end = time.time()
    log_process.process_bar(flag,len(flist),time_init,time_start,time_end,f)
    flag+=1