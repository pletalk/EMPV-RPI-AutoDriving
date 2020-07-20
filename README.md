# EMPV 소개

라즈베리파이기반의 donkeycar + deeppicar 교육 프로그램을 위한 코드 repository로 3DEMP의 EMPV1기반에 Donkeycar와 DeepPicar의 운용을 위한 프로그램들이 포함되어 있습니다.
프로그램 동작을 위해서 아래의 환경이 필요합니다.

- Raspberry Pi 3B+ 이상의 보드
- 광각카메라
- 서보모터와 배터리를 탑재한 RC카 샤시
- 무선통신기능 (WiFi)
- 차량조정을 위한 근거리 통신(IR,Bluetooth등)


# 프로그램 폴더 안내

### 01-Google Colab

주행데이타에 대한 딥러닝 학습을 위해서 [Google Colab](https://colab.research.google.com/)을 사용하는 방법들에 대해서 소개합니다. 예시 및 설명코드는 모두 Google Colab에서 동작하도록 주피터노트북으로 작성되어 있습니다. 해당 디렉토리에는 총 5개의 주피너 노트북이 포함되어 있으며, Google Colab에서 사용가능한 매직(magic) 명령어, 쉘(shell) 명령어, 문서작성을 위한 마크다운(Markdown) 문법, 유틸리티 기능들, 그리고 Colab 환경에서 파이썬을 사용하기 위해 기존에 설치된 패키지들이나 패키지 버전등을 확인하는 방법들에 대해서 주피터 노트북을 실행해보면서 각각의 내용을 배워볼 수 있습니다.


### 02-OpenCV
컴퓨터 비전처리를 위한 파이썬라이브러리인 OpenCV에 대한 주요 내용들과 기능들을 중심으로 본 프로젝트에서 활용되는 내용들을 중심으로 주요 기능들의 실제 사용방법에 대해서 배워보는 주피터 노트북이 포함되어 있습니다. 이와 아울러, 컴퓨터 카메라를 통해 저장된 연속된 이미지들을 병합해서 하나의 영상으로 변환하는 과정에 대한 주피터 노트북도 함께 포함되어 있습니다(주행시 캡쳐된 영상의 동영상 변황에 유용하게 활용가능합니다). 

### 03-Donkeycar-Training-Colab
Donkeycar 드라이버의 주행 행동모방(Behavior Cloning)을 통해 수집된  주행 데이타를 사용해서 딥러닝 기반의 주행모델을 학습하는 주피터 노트북이 폴더 내에 있으며, Donkeycar Simulator(시뮬레이터)상에서의 자율주행을 테스트할 수 있도록 제공되는 학습데이타를 사용해서 주행모델을 학습하는 주피터 노트북도 함께 포함됩니다.

### 04-DeepPiCar-OpenCV-AutoLaneFollow-Colab
DeepPiCar의 컴퓨터비전을 활용한 openCV기반 주행 영상 이미지로부터 주행차선을 인식하고, 이를 통해 차량의 주행각도를 변경하여 자율을 하는 DeepPiCar의 수행 코드를 단계적으로 실행할 수 있는 주피터 노트북이 포함되어 있습니다.

### 05-DeepPiCar-NVIDIA-AutoLaneFollow-Colab
DeepPiCar의 OpenCV기반 자동주행 데이타에 기반하여 NVIDIA사의 CNN기반 딥러닝 주행모델학습의 과정들을 따라서 배워볼 수 있는 주피터노트북이 포함되어 있으며, 이와함께 주행 데이타 이미지에 대한 다양한  변환(transform)과정을 통해  학습데이타를 증강(augment)시켜서 학습량을 증가하여 주행모델을 학습하는 과정에 대한 주피터 노트북도 함께 실행해볼 수 있습니다.

### 06-EMPV1-AutoLaneFollow-Colab
EMPV1의 OpenCV기반 자동주행 데이타에 기반하여 NVIDIA사의 CNN기반 딥러닝 주행모델학습의 과정들을 DeepPiCar의 경우도 동일하게 따라 배워볼 수 있는 주피터노트북이 포함되어 있으며, 이와함께 주행 데이타 이미지에 대한 다양한  변환(transform)과정을 통해  학습데이타를 증강(augment)시켜서 학습량을 증가하여 주행모델을 학습하는 과정에 대한 주피터 노트북도 함께 실행해볼 수 있습니다.

### 11-DONKEYCAR_PARTS
Donkeycar에 기반하여 DeepPiCar의 다양한 기능들 - OpenCV기반 자동 차선 탐지 및 주행, NVIDIA 딥러닝 모델 기반의 End-To-End 자율 주행 - 을 구현하기 위해서 수정된 Donkeycar의 기능 모듈들의 수정된 코드들이 들어있습니다. Donkeycar를 PC/노트북에 설치하고, 이 폴더의 파일들을 donkeycar/donkeycar/parts 디렉토리에 복사합니다(기존 Donkeycar코드를 사용하는 경우, DeepPiCar의 기능들이 동작하지 않습니다).

### 21-EMPV1-DPCAR
EMPV1을 위한 car 프로젝트 폴더로, DeepPiCar에서 지원되는 기능들 - OpenCV기반 자동 차선 탐지 및 주행, NVIDIA 딥러닝 모델 기반의 End-To-End 자율 주행 - 을 python프로그램 기반으로 구동하고, 라즈베리파이 내에서 실행해볼 수 있는 프로그램 코드들을 포함하고 있습니다. 

EMPV1과 관련하여 유용한 utils 폴더, 구동 테스팅을 위한 test_programs 폴더가 있으며, models의 경우 Google Colab에서 학습한 딥러닝 모델을 저장하는데 사용됩니다. 폴더 내에 있는 01~04의 파이썬 프로그램은 각각 아래의 용도를 위해서 사용할 수 있습니다.

* **01_dpcar_drive.py**
  * EMPV1의 카메라가 촬영한 영상이 별도의 윈도우에 표시되며, 라즈베리파이 내의 로컬 웹 서버에 접속해서 EMPV1의 주행을 직접제어할 수 있는 프로그램입니다. 주행 시, 주행 영상은 별도의 디렉토리에 저장됩니다(data/tub_ 폴더에 주행영상과 속도,각도등의 정보가 함께 저장됩니다)
* **02_dpcar_drive_lanefollow.py**
  * DeepPiCar의 openCV기반 주행선 탐지 및 자율주행의 처리과정을 EMPV1을 통해 실행해보는 프로그램입니다. 프로그램 구동 시, EMPV1의 카메라가 촬영한 영상이 표시되는 윈도우를 포함해서 HSV로 변환된 영상, edge탐지 영상 및 탐지된 주행선이 직선으로 표시되는 창까지 4개의 창을 확인할 수 있습니다. 로컬웹서버에 접속해 EMPV1을 직접 주행해보면서 openCV를 통한 주행선 탐지가 제대로 이루어지는지 실시간으로 확인할 수 있습니다.
* **03_dpcar_drive_auto_lanefollow.py**
  
  
* **04_dpcar_nvidia_auto_drive.py**
  
 

위의 프로그램들은 동일한 이름을 가진 bash 파일(확장자 .sh)을 통해 실행가능합니다. Bash 파일을 열어보면, 명령행에 사용가능한 인수들을 확인하실 수 있습니다.


## Copyrights 2020

* Donkeycar는 https://github.com/autorope/donkeycar 를 참고하였습니다.
* DeepPiCar는 https://github.com/dctian/DeepPiCar 를 참고하였습니다. 
* EMPV1에서 Donkeycar와 DeepPiCar를 모두 운영하기 위해서 위의 각각의 소스코드를 수정/변경하였습니다. Donkeycar는 Parts부분중에서 acutator, camera, datastore의 모듈의 소스코드를 수정하였습니다. 아울러, Donkeycar의 제어부분 상에서 DeepPiCar이 동작하도록 하기 위해서 DeepPiCar의 OpenCV Lane Follow 부분과 NVIDIA 모델기반의 Lane Follow 부분의 소스코드를 Donkeycar에서 운영되도록 Donkeycar의 drive파트를 변경하였습니다.  
