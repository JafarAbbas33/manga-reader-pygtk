#!/usr/bin/env python3

# ./infinite-image-scroller.py --conf infinite-image-scroller.ini '/home/jafarabbas33/Documents/Mangas/Call of the Night'
# ./infinite-image-scroller.py --conf infinite-image-scroller.ini '/home/jafarabbas33/Documents/Mangas/A Couple of Cuckoos/Chapter 1'

import infinite_image_scroller
from zipfile import ZipFile
import pathlib as pl
import shutil
import os
import re

TEMP_DIR = pl.Path('/tmp/manga_reader')
TEMP_DIR.mkdir(exist_ok=True)

def check_is_manga_ch(path):
    if path.endswith('.cbz') or path.endswith('.zip'):
        return True
    print(path)
    for dname, dirs, files in os.walk(path):
        for fname in files:
            if not (fname.endswith('jpg') or fname.endswith('png') or fname.endswith('jpeg')):
                return False
        if dirs:
            return False
        else:
            return True

def get_operational_ch_dir(path):
    operational_ch_dir = path
    if path.endswith('.cbz') or path.endswith('.zip'):
        with ZipFile(path) as zip:
            # extracting all the files 
            # print('Extracting...') 
            operational_ch_dir = (TEMP_DIR / pl.Path(path).name).as_posix()
            zip.extractall(operational_ch_dir)
    assert ensure_path_is_manga_ch(operational_ch_dir), 'Contains non image files...'
    return operational_ch_dir

def getint(name):
    name = name.split('/')[-1] if '/' in name else name
    t = re.findall(r'(\d+\.\d+|\d+)', name)
    # print(name, t)
    if t:
        return float(t[0])
    else:
        return 0
        
def ensure_path_is_manga_ch(path):
    # if path.endswith('.cbz') or path.endswith('.zip'):
    #     return True
    for dname, dirs, files in os.walk(path):
        if dirs:
            return False
        for fname in files:
            if not (fname.endswith('jpg') or fname.endswith('png') or fname.endswith('jpeg')):
                return False
    return True
    
def ensure_path_is_manga_dir(path):
    ch_dirs = []
    for dname, dirs, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            ch_dirs.append(fpath)
        for fname in dirs:
            fpath = os.path.join(dname, fname)
            ch_dirs.append(fpath)
        break
    for ch_dir in ch_dirs:
        ensure_path_is_manga_ch(ch_dir)

def main():
    # path = '/home/jafarabbas33/Documents/Mangas/Call of the Night'
    # print(path, check_is_manga_ch(path))
    # path = '/home/jafarabbas33/Documents/Mangas/A Couple of Cuckoos/Chapter 1'
    # print(path, check_is_manga_ch(path))
    # path = '/home/jafarabbas33/Documents/Mangas/A Couple of Cuckoos'
    # print(path, check_is_manga_ch(path))
    path = '/home/jafarabbas33/Documents/Mangas/Call of the Night/Night 1.cbz'
    print(path, check_is_manga_ch(path))

    is_manga_ch = check_is_manga_ch(path)
    # If is manga chapter path then run the application and return
    if is_manga_ch:
        operational_ch_dir = get_operational_ch_dir(path)
        infinite_image_scroller.main(passed_path=operational_ch_dir)
        return
    # If is manga chapters directory path then run the application
    ch_dirs = []
    for dname, dirs, files in os.walk(path):
        for fname in files:
            fpath = os.path.join(dname, fname)
            ch_dirs.append(fpath)
        for fname in dirs:
            fpath = os.path.join(dname, fname)
            ch_dirs.append(fpath)
        break
    ch_dirs.sort(key=getint)
    for ch_dir in ch_dirs:
        operational_ch_dir = get_operational_ch_dir(ch_dir)
        infinite_image_scroller.main(passed_path=operational_ch_dir)

if __name__ == '__main__':
    main()
