import os
import time

from docopt import docopt
import numpy as np
import argparse

import donkeycar as dk
import pprint
import json

from tensorflow import keras

#import parts
from donkeycar.parts.transform import Lambda, TriggeredCallback, DelayedTrigger
from donkeycar.parts.datastore import TubHandler
from donkeycar.parts.controller import LocalWebController, \
    JoystickController, WebFpv
from donkeycar.parts.throttle_filter import ThrottleFilter
from donkeycar.parts.behavior import BehaviorPart
from donkeycar.parts.file_watcher import FileWatcher
from donkeycar.parts.launch import AiLaunch
from donkeycar.utils import *
#from donkeycar.pars.keras import KerasPilot
#from donkeycar.parts.keras import KerasLinear,KerasIMU
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import cv2


class LoadTestSet(object):
    def __init__(self,set_filename=None):
        self.set_filename = set_filename
        self.base_df = None

    def load_testset(self):
        if not os.path.exists(self.set_filename) :
            raise Exception(f"file {self.set_filename} 이 존재하지 않습니다")
        
        self.raw_df = pd.read_csv(self.set_filename)
        print("raw_df.shape=",self.raw_df.shape)

    def drop_cols(self):
        self.base_df = self.raw_df.drop(['user/mode','milliseconds','user/throttle'],axis=1)
        print("base_df.shape=", self.base_df.shape)

    def nrows(self):
        return self.base_df.shape[0]

    def get_colnames(self):
        if not (self.base_df is None):
            return self.base_df.columns
        else:
            raise Exception("데이타가 로드되지 않았습니다")

    def get_col_by_name(self, colname):
        return np.ravel(self.base_df[colname]) 
    
    def get_obs_by_rowidx(self,index):
        if not (self.base_df is None) :
            tmp_row = self.base_df.loc[index,:]
            print("index=",index)
            print("ttype=",type(tmp_row))
            print(np.asarray(tmp_row))

            return self.base_df.loc[index,:]
        else:
            raise Exception("데이타가 로드되지 않았습니다")

#
# image 변환
#

def load_image(data_dir,image_path):
    image_file_path = os.path.join(data_dir,image_path)
    #print("image_file_path->",image_file_path)

    image = cv2.imread(image_file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]  
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (200,66)) 
    image = image / 255 
    return image

def  convert_image_to_nvidia(data_dir, filepath_list):
    merge_list = []
    for fname in filepath_list:
        # 원래 이미지를 로딩
        trgb_image = load_image(data_dir,fname)

        # 전처리를 수행
        prep_trgb_image = img_preprocess(trgb_image)
        merge_list.append(prep_trgb_image)
    return np.array(merge_list)



#
# 각도를 제어변수로, 제어변수를 각도로
#

def control_to_degree(ctl): 
    degree = ctl * 40 + 90
    return degree

def degree_to_control(drg):
    ctl = (drg - 90) * (1/40)
    return ctl

#
# 테스트 결과출력
#

def summary_prediction(Y_true, Y_pred):

    mse = mean_squared_error(Y_true, Y_pred)
    r_squared = r2_score(Y_true, Y_pred)

    print(f'mse       = {mse:.2}')
    print(f'r_squared = {r_squared:.2%}')
    print()


def predict_by_model(mdl, X):
    y_pred = mdl.predict(X) 
    return y_pred


def predict_and_summarize(X, Y):
    model_file_name = f'{model_output_dir}/{trained_model_file}'
    model = load_model(model_file_name)
    Y_pred = model.predict(X)
    summarize_prediction(Y, Y_pred)
    return Y_pred


#
# model의 구조 출력
#

def print_model(mdl):
    to_json = mdl.to_json()
    pp = pprint.PrettyPrinter()
    pp.pprint(json.loads(to_json))

#
# drive 메인함수
#

def drive(cfg,model_path=None,X=None,y=None):
    model_type = cfg.DEFAULT_MODEL_TYPE

    def load_model(model_path):
        start = time.time()
        print('loading model', model_path)
        mdl = keras.models.load_model(model_path)
        print('finished loading in %s sec.' % (str(time.time() - start)) )
        return mdl

    if model_path:
        #When we have a model, first create an appropriate Keras part

        if '.h5' in model_path or '.uff' in model_path or 'tflite' in model_path or '.pkl' in model_path:
            #when we have a .h5 extension
            #load everything from the model file
            kl = load_model(model_path)
            #print("--------> moadl_model=>",model_path)

            print(kl.summary())
            #print_model(kl)

            print("Predictions.....")
            pred_y = predict_by_model(kl,X)
            print("pred_y---->")
            print(pred_y)
            y2 = list(map(control_to_degree,y))
            summary_prediction(y2, pred_y)
            result_df = pd.DataFrame()
            result_df['y_true']=y2
            result_df['y_pred']=pred_y

            # 최종결과를 저장
            result_df.to_csv('./predict_result.csv',index=False)

        '''
        #this part will signal visual LED, if connected
        V.add(FileWatcher(model_path, verbose=True), outputs=['modelfile/modified'])

        #these parts will reload the model file, but only when ai is running so we don't interrupt user driving
        V.add(FileWatcher(model_path), outputs=['modelfile/dirty'], run_condition="ai_running")
        V.add(DelayedTrigger(100), inputs=['modelfile/dirty'], outputs=['modelfile/reload'], run_condition="ai_running")
        V.add(TriggeredCallback(model_path, model_reload_cb), inputs=["modelfile/reload"], run_condition="ai_running")

        outputs=['pilot/angle', 'pilot/throttle']

        if cfg.TRAIN_LOCALIZER:
            outputs.append("pilot/loc")

        V.add(kl, inputs=inputs,
            outputs=outputs,
            run_condition='run_pilot')
        '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path',help='.h5 nvidia model path')
    parser.add_argument('--myconfig', default='myconfig.py', help='configuration file')
    parser.add_argument('--testset', help='test dataset')
    parser.add_argument('--ddir', help='data dir(tub_ directory contains)')
    args = parser.parse_args()

    print(args)

    cfg = dk.load_config(myconfig=args.myconfig)
    lts = LoadTestSet(args.testset)
    lts.load_testset()
    lts.drop_cols()
    print("nrows=", lts.nrows())
    print(lts.get_obs_by_rowidx(0))

    # test데이타를 읽어들여서 X,y로 나누기 
    images_list = lts.get_col_by_name('cam/image_array')
    y = lts.get_col_by_name('user/angle')

    print("images_list.shape=",images_list.shape)
    print("y.shape=",y.shape)
    print(y)

    X = convert_image_to_nvidia(args.ddir,images_list)
    print("X.shape=",X.shape)

    drive(cfg,model_path=args.model_path,X=X,y=y)
