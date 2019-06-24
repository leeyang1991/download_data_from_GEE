# coding=gbk

import to_raster
import os
#from matplotlib import pyplot as plt
import numpy as np
import log_process
import time



this_root = os.getcwd()+'\\..\\'

fdir = r'F:\FVC内蒙古植被覆盖数据\1km月值_1978_1985_1995_2005_2018\\'
save_dir = r'F:\FVC内蒙古植被覆盖数据\1km_monthly\\'
flist = os.listdir(fdir)



time_init = time.time()
flag = 0
for f in flist:
    time_start = time.time()
    if not f.endswith('.tif'):
        continue
    print(f)
    exit()
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
