# coding=gbk

import zipfile
import os
import shutil
import sys
import log_process as logger

this_root = 'E:\\'
def mk_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def unzip(zip,move_dst_folder):
    mk_dir(move_dst_folder)
    path_to_zip_file = zip
    tif_name = zip.split('\\')[-1].split('.')[0]
    # print(tif_name)
    # exit()
    # move_dst_folder = this_root+'tif\\'
    if not os.path.isfile(move_dst_folder+tif_name+'.tif'):
        directory_to_extract_to = this_root+'temp\\'
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()

        file_list = os.listdir(directory_to_extract_to)
        for i in file_list:
            if i.endswith('.tif'):
                shutil.move(directory_to_extract_to+'\\'+i,move_dst_folder+tif_name+'.tif')
    else:
        print(move_dst_folder+tif_name+'.tif is existed')


def check_zip(path):
    ZipFile = zipfile.ZipFile
    BadZipfile = zipfile.BadZipfile
    try:
        with ZipFile(path) as zf:
            pass

    except BadZipfile:
        print path + " Does not work"
        os.remove(path)
    pass

def do_unzpi(year):
    year = str(year)
    import time
    fdir = this_root+'30m_fvc_annual\\'+year+'\\'
    flist = os.listdir(fdir)
    P = logger.process_bar
    dest_folder = this_root+'30m_fvc_annual_unzip\\'+year+'\\'
    mk_dir(dest_folder)
    time_init = time.time()
    for f in range(len(flist)):
        start = time.time()
        fzip = fdir+flist[f]
        # print(fzip)
        unzip(fzip,dest_folder)
        end = time.time()
        P(f,len(flist),time_init,start,end,year)


def do_unzpi1():
    import time
    fdir = 'E:\\before2000\\zip\\'
    flist = os.listdir(fdir)
    P = logger.process_bar
    dest_folder = 'E:\\before2000\\unzip\\'
    mk_dir(dest_folder)
    time_init = time.time()
    for f in range(len(flist)):
        start = time.time()
        fzip = fdir+flist[f]
        # print(fzip)
        if os.path.isfile(dest_folder+fzip.split('\\')[-1].split('.')[0]):
            print(fzip+'is existed')
            continue
        try:
            unzip(fzip,dest_folder)
        except Exception as e:
            print e
        #check_zip(fzip)
        end = time.time()
        P(f,len(flist),time_init,start,end)


def main():
    for y in [1978,1985,1995,2005,2018]:
        do_unzpi(y)

    pass


if __name__ == '__main__':
    do_unzpi1()


