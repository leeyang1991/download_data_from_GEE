# coding=gbk
import ee
import time
# from matplotlib import pyplot as plt
from osgeo import ogr
import os
import requests
import sys
import log_process as logger
import zipfile



this_root = os.getcwd()+'\\..\\'
log = logger.Logger('l.log', level='info')

def mk_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


# def get_download_url(datatype = "LANDSAT/LC08/C01/T1_32DAY_NDVI",
#                      start = '2000-01-01',
#                      end = '2000-02-01',
#                      region='[[117, 47], [119, 47], [119, 45], [117, 45]]',
#                      ):
#
#     dataset = ee.ImageCollection(datatype).filterDate(start, end)
#     image1 = dataset.max()
#     fvc = image1.divide(0.8).rename('FVC')
#     path = fvc.getDownloadUrl({
#         'scale': 30,
#         'crs': 'EPSG:4326',
#         'region': region
#                                 })
#
#     return path



def get_download_url(datatype = "LANDSAT/LC08/C01/T1_32DAY_NDVI",
                     start = '2000-01-01',
                     end = '2000-02-01',
                     region='[[117, 47], [119, 47], [119, 45], [117, 45]]',
                     ):

    dataset = ee.ImageCollection(datatype).filterDate(start, end)
    ndvi = dataset.select('NDVI')
    image1 = ndvi.max()
    fvc = image1.divide(8000).rename('FVC')
    path = fvc.getDownloadUrl({
        'scale': 30,
        'crs': 'EPSG:4326',
        'region': region
                                })

    return path


def gen_polygons():
    shapefile = this_root + 'shp\\fishnet.shp'
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(shapefile, 0)
    layer = dataSource.GetLayer()
    all_polygons = []
    for feature in layer:
        geom = feature.GetGeometryRef()
        g = geom.GetEnvelope()
        # print(type(g))
        # [[117, 47], [119, 47], [119, 45], [117, 45]]
        # print(g)
        region = [
            [g[0],g[2]],
            [g[1],g[2]],
            [g[1],g[3]],
            [g[0],g[3]]
                  ]
        # print(str(region))
        all_polygons.append(str(region))
    return all_polygons


# def gen_urls():
#
#     # os.makedirs(this_root + 'url\\')
#     start = time.time()
#     log.logger.info('Initializing auth...')
#     ee.Initialize()
#     end = time.time()
#     log.logger.info('Account initialized '+'time %0.2f' % (end - start)+' s')
#
#     # time_start = time.time()
#     polygon_list = gen_polygons()
#     date_list = gen_landsat_8_date()
#
#     dataset = "LANDSAT/LT05/C01/T1_32DAY_NDVI"
#     flag = 0
#     download_dir = this_root + 'download_data\\'
#     mk_dir(download_dir)
#
#     for i in range(len(date_list)):
#         if i == len(date_list)-1:
#             break
#         start = date_list[i]
#         end = date_list[i+1]
#
#         for j in range(len(polygon_list)):
#             data = dataset.split('/')[1]
#             file_name = data + '_' + start + '_' + end + '_' + '%02d' % (j + 1) + '.zip'
#             path = download_dir + file_name
#             if os.path.isfile(path):
#                 log.logger.info(path+' is already existed')
#                 continue
#             flag += 1
#             url = get_download_url(dataset,start,end,polygon_list[j])
#
#             download_data(url,path)



def download_data(url,file_name):


    path = file_name
    if not os.path.isfile(path):
        # success = 0
        attempt = 0
        while 1:
            try:
                with open(path, "wb") as f:
                    log.logger.info("\nDownloading %s" % file_name)
                    response = requests.get(url, stream=True)
                    total_length = 100.*1024.*1024.

                    if total_length is None:  # no content length header
                        f.write(response.content)
                    else:
                        dl = 0
                        total_length = int(total_length)
                        for data in response.iter_content(chunk_size=1024):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                            sys.stdout.flush()
                success = 1
            except Exception as e:
                attempt += 1
                time.sleep(1)
                log.logger.info(e)
                log.logger.info('try '+str(attempt))
                success = 0
            if success == 1:
                break
            if attempt > 10:
                log.logger.info(str(attempt)+' try')
                break
    else:
        log.logger.info(path+' is already existed')

def check(path):
    ZipFile = zipfile.ZipFile
    BadZipfile = zipfile.BadZipfile
    try:
        with ZipFile(path) as zf:
            pass

    except BadZipfile:
        # print path
        return 1
    pass


def main():
    print('initializing GEE')
    ee.Initialize()
    print('done')
    product_dic = {
        # 'LC08':"LANDSAT/LC08/C01/T1_32DAY_NDVI",
        # 'LE07':'LANDSAT/LE07/C01/T1_32DAY_NDVI',
        # 'LT05':"LANDSAT/LT05/C01/T1_32DAY_NDVI",
        '006':"MODIS/006/MOD13Q1"
    }
    fdir = this_root+'download_data\\'
    re_download_dir = this_root+'re_download_data\\'
    mk_dir(re_download_dir)
    poligon_list = gen_polygons()
    polygon_dic = {}
    for i in range(len(poligon_list)):
        polygon_dic['%02d'%(i+1)] = poligon_list[i]
    flist = os.listdir(fdir)
    #
    time_init = time.time()
    flag = 0
    invalid_list = []
    for f in flist:
        start = time.time()
        if check(fdir+f):
            invalid_list.append(f)
        end = time.time()
        logger.process_bar(flag,len(flist),time_init,start,end,'checked')
        flag += 1

    time_init = time.time()
    flag = 0
    for f in invalid_list:
        start = time.time()
        # print(f)
        fsplit = f.split('_')
        product = fsplit[0]
        dataset = product_dic[product]
        date_start = str(fsplit[1])
        date_end = str(fsplit[2])
        num = str(fsplit[3].split('.')[0])
        region = polygon_dic[num]
        # print(dataset)
        # print(date_start)
        # print(date_end)
        # print(num)
        # print(region)
        #
        url = get_download_url(dataset,date_start,date_end,region)
        file_name = '_'.join([product,date_start,date_end,num])+'.zip'
        # print(file_name)
        download_data(url,re_download_dir+file_name)
        end = time.time()
        logger.process_bar(flag,len(invalid_list),time_init,start,end,str(flag+1)+'/'+str(len(invalid_list))+'\n')
        flag+=1


if __name__ == '__main__':
    main()