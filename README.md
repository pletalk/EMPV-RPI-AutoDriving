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

### 04-DeepPiCar-NVIDIA-AutoLaneFollow-Colab

### 05-EMPV1-AutoLaneFollow-Colab

### 11-EMPV1-DPCAR

### 99-DONKEYCAR_PARTS


# Copyrights 2020

* Donkeycar는 https://github.com/autorope/donkeycar 를 참고하였습니다.
* DeepPiCar는 https://github.com/dctian/DeepPiCar 를 참고하였습니다. 
* EMPV1에서 Donkeycar와 DeepPiCar를 모두 운영하기 위해서 위의 각각의 소스코드를 수정/변경하였습니다. Donkeycar는 Parts부분중에서 acutator, camera, datastore의 모듈의 소스코드를 수정하였습니다. 아울러, Donkeycar의 제어부분 상에서 DeepPiCar이 동작하도록 하기 위해서 DeepPiCar의 OpenCV Lane Follow 부분과 NVIDIA 모델기반의 Lane Follow 부분의 소스코드를 Donkeycar에서 운영되도록 Donkeycar의 drive파트를 변경하였습니다.  
