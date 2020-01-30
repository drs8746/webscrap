import os
import shutil
import requests
import bs4
import pandas as pd
from zipfile import ZipFile
from pathlib import Path


def download_csvfile(url_bis, dn_folder='downloads', numcsv=5):
    cont_bis = requests.get(url_bis)
    soup = bs4.BeautifulSoup(cont_bis.content, "lxml")
    htm_li_filelist = soup.find(id='cmsContent').find('ul').find('li')
    
    if not os.path.isdir(dn_folder):
      os.mkdir(dn_folder)
    
    num_files = 0
    lst_files = list()
    for i, x in enumerate(soup.find(id='cmsContent').find('ul').findAll('li')):
        if i < 3: continue # skip first 3 files(LBS, CBS, DEBT_SEC) because it is big
        url_zipfile = r'https://www.bis.org' + x.find('a')['href']
        zip_content = requests.get(url_zipfile)
        with open(os.path.join(dn_folder,url_zipfile.split(r'/')[-1]), 'wb') as fout:
            fout.write(zip_content.content)
            print('Downloaded: {0}'.format(url_zipfile))
            num_files = num_files + 1
            lst_files.append(url_zipfile.split(r'/')[-1])
        if num_files == numcsv: # maximum download files
            break

    return lst_files


def unzip_csvfile(lst_files,dn_folder='downloads'):
    lst_unzip_folder = list()
    for csvfile in lst_files:
        csvfile = os.path.join(dn_folder, csvfile)
        csvfile_unzip = csvfile + 'unzipped'
        if os.path.exists(csvfile):
            #If the folder is exist, it removes forcefully
            if os.path.isdir(csvfile_unzip):
                shutil.rmtree(csvfile_unzip)
            else:
                os.mkdir(csvfile_unzip)
            with ZipFile(csvfile, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall(csvfile_unzip)
                lst_unzip_folder.append(csvfile_unzip)
                print('Extracted: {0}'.format(csvfile_unzip))

    return lst_unzip_folder


def count_row_columns_csvfile(lst_unzip_folder):
    for unzip_folder in lst_unzip_folder:
        for csvfile in os.listdir(unzip_folder):
            csvfile2 = os.path.join(unzip_folder, csvfile)
            df = pd.read_csv(csvfile2)
            print('# row and columns of {0}: {1}'.format(csvfile, df.shape))


def main():
    url_bis = r'https://www.bis.org/statistics/full_data_sets.htm'

    #STEP1: download csv files
    lst_files = download_csvfile(url_bis, 'downloads', 2)

    #STEP2: unzip csv files
    lst_unzip_folder = unzip_csvfile(lst_files)

    #STEP3: count number of row and columns of csv files
    count_row_columns_csvfile(lst_unzip_folder)

if __name__ == '__main__':
    main()