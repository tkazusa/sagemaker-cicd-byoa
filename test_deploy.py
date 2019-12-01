# -*- coding: utf-8 -*-
import argparse

import sagemaker
from sagemaker.tensorflow.serving import Model

if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='deployment script')
    parser.add_argument('--model_data', type=str)
    parser.add_argument('--role', type=str)
    parser.add_argument('--entry_point', type=str)
    parser.add_argument('--src_dir', type=str)
    parser.add_argument('--framework_version', type=str)
    parser.add_argument('--initial_instance_count', type=int)    
    parser.add_argument('--instance_type', type=str) 

    args = parser.parse_args()

    model_data = args.model_data
    role = args.role
    entry_point = args.entry_point
    src_dir = args.src_dir
    framework_version = args.framework_version
    initial_instance_count = args.initial_instance_count
    instance_type = args.instance_type
    
    cifar10_estimator = Model(model_data=model_data,
                              role=role,
                              entry_point=entry_point,
                              source_dir=src_dir,
                              framework_version=framework_version)

    cifar10_predictor = cifar10_estimator.deploy(initial_instance_count=initial_instance_count,
                             instance_type=instance_type)
    
    
    sagemaker_session = sagemaker.Session()
    sagemaker.Session().delete_endpoint(cifar10_predictor.endpoint)
    
    