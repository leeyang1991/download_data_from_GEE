# coding=gbk
import ee
import time
import os
import requests
import sys
import logger
log = logger.Logger('log.txt', level='info')

def get_download_url(datatype = "LANDSAT/LT05/C01/T1_SR",
                     start = '2000-01-01',
                     end = '2001-02-01',
                     region='[[115, 39.38], [117.89, 39.38], [117.89, 41.5], [115, 41.5]]',
                     ):

    # bands = ['B3', 'B2', 'B1']
    geom = ee.Geometry.Point([116.483, 40.423])
    dataset = ee.ImageCollection(datatype).filterDate(start, end).filterBounds(geom).select(['B1', 'B2', 'B3'])
    colList = dataset.toList(1000)

    n = colList.size().getInfo()
    print(n)

    for i in range(n):
        img = ee.Image(colList.get(i))
        id = img.id().getInfo()
        if not '123032' in id:
            continue
        # print(id)
        path = img.getDownloadUrl({
            'scale': 30,
            'crs': 'EPSG:4326',
            'region': region
                                    })

        download_data(path,id)




def download_data(url,file_name):


    path = file_name+'.zip'
    if not os.path.isfile(path):
        # success = 0
        attempt = 0
        while 1:
            try:
                with open(path, "wb") as f:
                    log.logger.info("\nDownloading %s" % file_name)
                    response = requests.get(url, stream=True)
                    total_length = 300.*1024.*1024.

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


def main():
    ee.Initialize()
    get_download_url()

if __name__ == '__main__':
    main()