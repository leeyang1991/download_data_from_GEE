# coding=gbk

import arcpy
from arcpy import env
import log_process
import os
import time

this_root = os.getcwd()+'\\..\\'
log = log_process.Logger('log.log')
arcpy.CheckOutExtension("Spatial")
# log.logger.info('test')

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
        
        
def mosaic(fdir,in_rasters_list,out_dir,out_raster):
    if not os.path.isfile(out_dir+out_raster):
        env.workspace = fdir
        in_rasters = ';'.join(in_rasters_list)
        arcpy.MosaicToNewRaster_management(in_rasters, out_dir,
                                           out_raster,pixel_type="8_BIT_UNSIGNED",
                                           number_of_bands="1")
    else:
        print(out_raster+' is existed')


def do_mosaic(year):
    year = str(year)
    fdir = 'E:\\30m_fvc_annual_unzip\\'+year+'\\'
    flist = os.listdir(fdir)
    out_rasters = []
    for f in flist:
        out_rasters.append('_'.join(f.split('_')[:3]))
    out_raster = list(set(out_rasters))
    out_dir = 'E:\\30m_fvc_annual_unzip\\'+year+'_mosaic\\'
    mk_dir(out_dir)
    time_init = time.time()
    flag = 0
    for i in out_raster:
        log.logger.info(i)
        time_start = time.time()
        in_rasters_list = []
        for f in flist:
            if i in f:
                in_rasters_list.append(f)
        mosaic(fdir,in_rasters_list,out_dir=out_dir,out_raster=i+'.tif')
        time_end = time.time()
        
        log_process.process_bar(flag,len(out_raster),time_init,time_start,time_end,'\n')
        flag +=1
    pass



def max_fvc(rasters,out_max_raster):
    # Raster1 = r'D:\project_fvc\AVHRR_fvc\CDR_1981-07-01_1981-08-01.tif'
    # Raster2 = r'D:\project_fvc\AVHRR_fvc\CDR_1981-11-01_1981-12-01.tif'
    outCellStats = arcpy.sa.CellStatistics(rasters, "MAXIMUM")
    outCellStats.save(out_max_raster)


def max_composite():
    raster_dir = r'E:\190604\006_mosaic_0_100\2005\\'
    out_max_tif = r'E:\190604\006_mosaic_0_100\\2005_max.tif'
    rasters_list = os.listdir(raster_dir)
    rasters = []
    for i in rasters_list:
        if i.endswith('tif'):
            print(i)
            rasters.append(raster_dir + i)
    print('calculating')
    max_fvc(rasters,out_max_tif)


def mosaic_2018():

    fdir = r'E:\before2000\unzip\\'
    flist = os.listdir(fdir)
    out_rasters = []
    for f in flist:
        out_rasters.append('_'.join(f.split('_')[:3]))
    out_raster = list(set(out_rasters))
    out_dir = r'E:\before2000\mosaic\\'
    mk_dir(out_dir)
    time_init = time.time()
    flag = 0
    for i in out_raster:
        log.logger.info(i)
        time_start = time.time()
        in_rasters_list = []
        for f in flist:
            if i in f:
                in_rasters_list.append(f)
        mosaic(fdir,in_rasters_list,out_dir=out_dir,out_raster=i+'.tif')
        time_end = time.time()
        
        log_process.process_bar(flag,len(out_raster),time_init,time_start,time_end,'\n')
        flag +=1
    pass


def main():
    mosaic_2018()


if __name__ == '__main__':
    main()