# coding=gbk

import to_raster
import os
#from matplotlib import pyplot as plt
import numpy as np
import datetime

this_root = os.getcwd()+'\\..\\'



def mean_1km():
    fdir = r'E:\1km_fvc_monthly\glass\\'
    out_dir = r'E:\1km_fvc_annual\glass\\'
    flist = os.listdir(fdir)

    one_year = {}
    for y in range(2000,2017):
        one_year[str(y)] = []
    for f in flist:

        year = f.split('_')[1].split('-')[0]
        for y in range(2000,2017):
            if year == str(y):
                one_year[year].append(f)

    for y in one_year:
        print(y)
        array_sum = 0.
        flag = 0.
        for mon in one_year[y]:
            array, originX, originY, pixelWidth, pixelHeight = to_raster.raster2array(fdir+mon)
            # array = np.ma.masked_where(array == 255, array)
            # plt.imshow(array, 'jet')
            # plt.colorbar()
            # plt.show()
            array_sum += array
            flag += 1.
        array_mean = array_sum/flag
        # array_mean = np.ma.masked_where(array_mean>254,array_mean)
        newRasterfn = out_dir+y+'.tif'
        longitude_start=originX
        latitude_start=originY
        pixelWidth=pixelWidth
        pixelHeight=pixelHeight
        array=array_mean
        to_raster.array2raster(newRasterfn,longitude_start,latitude_start,pixelWidth,pixelHeight,array)
        # plt.imshow(array_mean,'jet')
        # plt.colorbar()
        # plt.show()
        # exit()


def change_time_GLASS():

    fdir = r'E:\new\MRT_resample_trans\\'
    flist = os.listdir(fdir)
    for f in flist:
        f_split = f.split('.')
        year = int(float(f_split[0].split('_')[0]))
        day = int(float(f_split[0].split('_')[1]))
        init_time = datetime.datetime(year,1,1)
        time_delta1 = datetime.timedelta(day)
        time_delta2 = datetime.timedelta(day+30)
        date_start = init_time+time_delta1
        date_end = init_time+time_delta2
        # print(date_start.year,date_start.month)
        # print(date_end.year,date_end.month)
        # CDR_1981-07-01_1981-08-01.tif
        date_name = 'GLASS_'+\
                    '-'.join([str(date_start.year),'%02d'%date_start.month,'01'])+'_'+\
                    '-'.join([str(date_end.year),'%02d'%date_end.month,'01'])+\
                    '.tif'
        print(f)
        os.rename(fdir+f,fdir+date_name)


def main():
    mean_1km()
    pass


if __name__ == '__main__':
    main()