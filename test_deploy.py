# -*- coding: utf-8 -*-
import argparse

from sagemaker.tensorflow import TensorFlowModel

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='training script')
    parser.add_argument('--model_data', type=str)
    parser.add_argument('--instance_type', type=str)
    

    args = parser.parse_args()

    model_data = args.model_path
    role = args.role
    entry_point = args.entry_point
    framework_version = args.framework_version
    initial_instance_count = args.initial_instance_count
    instance_type = args.instance_type
    
    
    cifar10_estimator = Model(model_data=model_data,
                          role=role,
                          entry_point=entry_point,
                          framework_version=framework_version)

    cifar10_estimator.deploy(initial_instance_count=initial_instance_count,
                             instance_type=instane_type)