#!/usr/bin/env python3

'''
$image2video.py 

이미지 디렉토리로부터 동영상 만들기(avi파일)
@2020-07-06 / @ignitespark

'''

import os,sys,json,argparse
import time
import pprint
import cv2

from docopt import docopt
import numpy as np


#
# cmdargs_parsing : 명령형의 인수를 파싱하는 함수
#
def cmdargs_parsing(parser):
	parser.add_argument('--tub', required=True, help='tub 디렉토리 명')
	parser.add_argument('--tub_basedir', required=True, default="./data", help='tub 디렉토리가 저장된 기본 디렉토리')
	parser.add_argument('--odir',required=False, default="./tubvideo", 
				help='tub 디렉토리의 이미지를 영상으로 변환하여 저장하는 디렉토리')

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
# get_seqno_from_filename
#
def get_seqno_from_filename(flist):
	seqno = []
	for x in flist:
		aa = x.split("_")
		seqno.append(int(aa[0]))
	
	return seqno


#
# load_rgb_image
#
def load_rgb_image(file_path):
	img_frame = cv2.imread(file_path)
	# BGR -> RGB
	rgb_img_frame = cv2.cvtColor(img_frame, cv2.COLOR_BGR2RGB)

	return rgb_img_frame

#
# load_bgr_image
#
def load_bgr_image(file_path):
	img_frame = cv2.imread(file_path)

	return img_frame

#
# make_images_to_video
#
def make_images_to_video(images_path_list,video_file_name,vid_fps=24):
	bgr_image = load_bgr_image(images_path_list[0])
	height, width,_ = bgr_image.shape

	print(bgr_image.shape)
	codec = cv2.VideoWriter_fourcc(*'XVID')

	#fourcc = cv2.cv.CV_FOURCC(*'XVID')
	#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

	vid_size = (width,height)
	vid_writer = cv2.VideoWriter(video_file_name, codec, vid_fps, vid_size) 

	print(video_file_name)
	ncounts = len(images_path_list)
	print(ncounts)
	for i in range(ncounts):
		bgr_image = load_bgr_image(images_path_list[i])
		print(images_path_list[i])
		vid_writer.write(bgr_image)         
	vid_writer.release()


#
# make_tubdir_to_list 변환 함수
#

def ordering_filenames(tub_basedir,tub_dir): 

	tub_target_dir = os.path.join(tub_basedir, tub_dir)
	print(tub_target_dir)
	if(os.path.exists(tub_target_dir) != True):
		raise Exception("tub dir(%s)가 존재하지 않습니다"% (tub_target_dir))

	jpgfiles = [x for x in os.listdir(tub_target_dir) if x.endswith(".jpg")]
	nfiles = len(jpgfiles)

	if nfiles == 0:
		raise Exception("[NOTICE] 해당 tubdir에는 jpg파일이없습니다(%s)" % tub_dir)
	else:
		print(">>> 해당tubdir에는 %d개의 jpg파일이 있습니다" % nfiles)

		seqno = get_seqno_from_filename(jpgfiles)
		sorted_index = np.argsort(seqno)

		'''
		for i in range(nfiles):
			cpos = sorted_index[i]
			print("%s -> %s -> %s" %(cpos,seqno[cpos],jpgfiles[cpos]))	
		'''

		return jpgfiles, sorted_index


#
# main program
#
if __name__ == '__main__':

	pp = pprint.PrettyPrinter(indent=4)
	parser = argparse.ArgumentParser()
	args = cmdargs_parsing(parser)
	print(args)

	make_output_dir(args.odir)
	jpgfiles,sorted_index = ordering_filenames(args.tub_basedir,args.tub)

	# tub디렉토리 아래의 .jpg파일들을 순차번호대로 파일명 리스트를 생성
	images_path_list=[]
	for i in range(len(jpgfiles)):
		cpos = sorted_index[i]
		image_file_path = os.path.join(args.tub_basedir,args.tub,jpgfiles[cpos])
		#print("image_file_path=%s" % image_file_path)
		images_path_list.append(image_file_path)
	#pp.pprint(images_path_list)

	# video파일 생성하기
	save_file_path = "%s.avi" % args.tub
	video_file_name = os.path.join(args.odir,save_file_path)
	print(video_file_name)
	make_images_to_video(images_path_list,video_file_name,vid_fps=10)

