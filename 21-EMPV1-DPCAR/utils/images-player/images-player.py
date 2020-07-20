#!/usr/bin/env python3

'''
$images_player.py 

주행영상의 개별 이미지(혹은 저장된 주행영상의 개별 이미지들)들을 저장한
이미지 디렉토리로부터 이미지를 읽어서 동영상처럼 뷰잉하는 프로그램 
@2020-07-06 / @ignitespark


Usage:
- 이미지를 보여주는 창이 표시되면, esc를 눌러서 한 프레임씩 이동시키면서
  이미지의 변화를 볼 수 있습니다.
- 이이지 표시창을 사라지게 하려면, 이미지 창이 선택된 상황에서 q를 누르면
  이미지 창이 사라집니다.
- 이미지 창표시를 위해서 GUI환경에서 프로그램을 수행합니다.
  (명령행에서 수행하면, GTK오류가 발생됩니다)
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

		return jpgfiles, sorted_index


#
# play_images
#

def play_images(images_list):
	nsize = len(images_list)

	window_name = "Racing Windows"	
	for i in range(nsize):
		image = load_bgr_image(images_list[i])
		cv2.imshow(window_name, image)

		if cv2.waitKey(0) & 0xFF == ord('q'):
            		break

	cv2.destroyAllWindows()

#
# main program
#
if __name__ == '__main__':

	pp = pprint.PrettyPrinter(indent=4)
	parser = argparse.ArgumentParser()
	args = cmdargs_parsing(parser)
	print(args)

	jpgfiles,sorted_index = ordering_filenames(args.tub_basedir,args.tub)

	# tub디렉토리 아래의 .jpg파일들을 순차번호대로 파일명 리스트를 생성
	images_path_list=[]
	for i in range(len(jpgfiles)):
		cpos = sorted_index[i]
		image_file_path = os.path.join(args.tub_basedir,args.tub,jpgfiles[cpos])
		#print("image_file_path=%s" % image_file_path)
		images_path_list.append(image_file_path)
	#pp.pprint(images_path_list)

	play_images(images_path_list)

