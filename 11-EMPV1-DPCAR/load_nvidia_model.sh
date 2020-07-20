#!/bin/sh
python load_nvidia_model.py --model_path ./models/nvidia_endtoend_lane_navigation_check.h5 --testset tublist_by_data.csv --ddir ./data
