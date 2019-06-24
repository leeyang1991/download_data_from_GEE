# coding=gbk

import to_raster
import os
from matplotlib import pyplot as plt
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
    # print(f)
    # exit()
    file_name = (fdir+f).decode('gbk').encode('utf-8')
    array, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(file_name)

    new_array = []
    flag1 = 0
    for i in array:
        flag1 += 1
        # print flag1,'/',len(array)
        temp = []
        for j in i:
            if j < -999:
                val = 255
            elif -999 < j < 0:
                val = 0
            elif 0 <= j <=1:
                val = int(j*100)
            elif j > 1:
                val = 100
            else:
                val = 255
            temp.append(val)
            # print val
        new_array.append(temp)
    # new_array = np.array(new_array,dtype=int)

    new_array = np.array(new_array,dtype=int)
    # print 'ploting'
    # plt.imshow(new_array)
    # plt.colorbar()
    # print 'done'
    # plt.show()
    # exit()
    # print 'saving'
    newRasterfn = (save_dir+f).decode('gbk').encode('utf-8')
    to_raster.array2raster(newRasterfn,originX,originY,pixelWidth,pixelHeight,new_array)
    time_end = time.time()
    log_process.process_bar(flag,len(flist),time_init,time_start,time_end,f)
    flag+=1
