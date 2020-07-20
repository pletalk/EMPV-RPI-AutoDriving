#!/usr/bin/env python3

'''
$tub2list_by_data.py 

data 디렉토리 아래의 tub 디렉토리들 전체에 대해서 학습을 위한 하나의 목록파일을 생성하는 프로그램
@2020-07-14 / @ignitespark

'''

import os,sys,json,argparse
import time
import csv
import pprint

from docopt import docopt
import numpy as np


#
# cmdargs_parsing : 명령형의 인수를 파싱하는 함수
#
def cmdargs_parsing(parser):
        parser.add_argument('--ddir', required=True, help='data directory')
        parser.add_argument('--o',required=False, default="./tublist_by_data.csv", 
                                help='data directory아래의 tub 디렉토리 내의 주행데이타에 대한 전체 목록 파일(저장파일)')

        args = parser.parse_args()

        return args


#
# get_file_path
#
def get_file_path(dir_path, file_name, file_ext='jpg'):
        file_path = os.path.join(dir_path,file_name,file_ext)
        if os.path.exists(file_path) != True :
                raise Exception("File(%s)가 존재하지 않습니다"% (file_path))

        return file_path

#
# make_output_dir : tub의 목록파일을 만들 디렉토리 생성
#
def make_output_dir(dir_path):
        if (os.path.exists(dir_path)):
                print("%s 디렉토리가 이미 존재합니다" % dir_path)
        else:
                os.makedirs(dir_path)


#
# parse_tublist
#
def parse_tublist(json_file_path):
        if(os.path.exists(json_file_path) != True):
                raise Exception("File(%s)가 존재하지 않습니다"% (json_file_path))

        config = dict()
        with open(json_file_path) as f:
                config = json.load(f)

        return config


#
# get_seqno_from_filename
#
def get_seqno_from_filename(flist):
        seqno = []
        for x in flist:
                aa = x.split("_")
                seqno.append(int(aa[0]))
        
        return seqno


#
# 이미지프레임에 대응되는 녹화기록정보 파일 로딩하기
#
def load_record_json(json_file_path):
        if(os.path.exists(json_file_path) != True):
                raise Exception("Record JSON(%s)가 존재하지 않습니다"% (json_file_path))

        record = dict()
        with open(json_file_path) as f:
                record = json.load(f)

        #pp.pprint(record)

        return record


#
# make_tubdir_to_list 변환 함수
#

def make_tubdir_to_list(tub_base_dir, tub_dir, sfile, tub_target_seqno):
        tub_target_dir = os.path.join(tub_base_dir, tub_dir)
        print("tub_target_dir=>",tub_target_dir)

        if(os.path.exists(tub_target_dir) != True):
                raise Exception("tub dir(%s)가 존재하지 않습니다"% (tub_target_dir))

        xjpgfiles = [x for x in os.listdir(tub_target_dir) if x.endswith(".jpg")]
        print(len(xjpgfiles))
        jpgfiles = [x for x in xjpgfiles if not x.startswith("._")]
        nfiles = len(jpgfiles)

        if nfiles == 0:
                print("[NOTICE] 해당 tubdir에는 jpg파일이없습니다(%s)" % tub_dir)
        else:
            print(">>> 해당tubdir에는 %d개의 jpg파일이 있습니다" % nfiles)

            seqno = get_seqno_from_filename(jpgfiles)
            sorted_index = np.argsort(seqno)

            writer = csv.writer(sfile)
            if tub_target_seqno == 0:
                colnames = ['cam/image_array', 'user/angle', 'user/throttle', 'user/mode', 'milliseconds']
                writer.writerow(colnames)

            for i in range(nfiles):
                cpos = sorted_index[i]
                #print("%s -> %s -> %s" %(cpos,seqno[cpos],jpgfiles[cpos]))
                record_file_path = os.path.join(tub_target_dir,"record_%d.json" % (seqno[cpos]))
                print(record_file_path)

                record = load_record_json(record_file_path)
                record_row = [ val for key,val in record.items()]                       
                record_row[0] = os.path.join(tub_dir,record_row[0])
                writer.writerow(record_row)


#
# data directory 아래의 tub directory이름 구하기
#
def get_tubdirs_list(data_dir):
    tubdirs = [x for x in os.listdir(data_dir)]
    return tubdirs

#
# main program
#
if __name__ == '__main__':

    pp = pprint.PrettyPrinter(indent=4)

    parser = argparse.ArgumentParser()
    args = cmdargs_parsing(parser)
    pp.pprint(args)

    # data directory아래의 tub dirs들의 목록을 가져옵니다
    xtubdirs = get_tubdirs_list(args.ddir)
    tubdirs = [x for x in xtubdirs if not x.startswith('._')]
    print(tubdirs)

    # 하나의 목록파일(저장)
    sfile = open(args.o, 'w', newline='') 

    for seqno,tubdir in enumerate(tubdirs):
        tub_full_path = os.path.join(args.ddir, tubdir)
        print("seqno->",seqno,",tub_full_path->",tub_full_path)
        
        make_tubdir_to_list(args.ddir, tubdir, sfile, seqno)

    sfile.close()

