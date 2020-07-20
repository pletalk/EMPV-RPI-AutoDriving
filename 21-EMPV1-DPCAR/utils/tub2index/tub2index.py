#!/usr/bin/env python3

'''
$tub2index.py 

동키카의 Tub디렉토리전체를 하나의 목록파일로 변환하는 프로그램
@2020-07-06 / @ignitespark

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
	parser.add_argument('--tub', required=True, help='tub 디렉토리 명을 담은 파일명(확장자.json)')
	parser.add_argument('--odir',required=False, default="./tublist", 
				help='tub 디렉토리별로 이미지파일명,속도,방향의 정보저장 색인파일 저장 디렉토리')

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

def make_tubdir_to_list(tub_base_dir, tub_dir, out_dir): 
	tub_target_dir = os.path.join(tub_base_dir, tub_dir)
	print("tub_target_dir=>",tub_target_dir)

	if(os.path.exists(tub_target_dir) != True):
		raise Exception("tub dir(%s)가 존재하지 않습니다"% (tub_target_dir))

	jpgfiles = [x for x in os.listdir(tub_target_dir) if x.endswith(".jpg")]
	nfiles = len(jpgfiles)

	if nfiles == 0:
		print("[NOTICE] 해당 tubdir에는 jpg파일이없습니다(%s)" % tub_dir)
	else:
		print(">>> 해당tubdir에는 %d개의 jpg파일이 있습니다" % nfiles)

		seqno = get_seqno_from_filename(jpgfiles)
		sorted_index = np.argsort(seqno)

		save_file_path = os.path.join(out_dir,"%s.csv"%tub_dir)
		colnames = ['cam/image_array', 'user/angle', 'user/throttle', 'user/mode', 'milliseconds']
	
		with open(save_file_path, 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(colnames)

			for i in range(nfiles):
				cpos = sorted_index[i]
				#print("%s -> %s -> %s" %(cpos,seqno[cpos],jpgfiles[cpos]))
				record_file_path = os.path.join(tub_base_dir,tub_dir,"record_%d.json" % (seqno[cpos]))
				#print(record_file_path)

				record = load_record_json(record_file_path)
				record_row = [ val for key,val in record.items()]			
				#record_row[0] = os.path.join(tub_dir,record_row[0])
				writer.writerow(record_row)
#
# main program
#
if __name__ == '__main__':

	pp = pprint.PrettyPrinter(indent=4)

	parser = argparse.ArgumentParser()
	args = cmdargs_parsing(parser)
	pp.pprint(args)

	make_output_dir(args.odir)
	tub_config = parse_tublist(args.tub)
	pp.pprint(tub_config)

	tub_base_dir = tub_config['basedir']
	for i in range(len(tub_config['tubdir'])):
		tub_dir = tub_config['tubdir'][i]
		make_tubdir_to_list(tub_base_dir, tub_dir, args.odir)
