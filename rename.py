# coding=gbk

import os


def rename(name):
    name = name.replace('1988','1979')
    return name



def main():
    fdir = r'E:\before2000\zip\\'
    flist = os.listdir(fdir)
    for f in flist:
        print(f)
        new_f = rename(f)
        os.rename(fdir+f,fdir+new_f)

if __name__ == '__main__':
    main()