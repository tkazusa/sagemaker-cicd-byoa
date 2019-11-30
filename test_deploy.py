# -*- coding: utf-8 -*-
import argparse
from sagemaker.tensorflow import TensorFlowModel

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='training script')
    parser.add_argument('--model_path', type=str)
    parser.add_argument('--instance_type', type=str)
    

    args = parser.parse_args()

    model_data = args.model_path
    instance_type = args.instance_type
    
    
    cifar10_estimator = TensorFlowModel(model_data=model_data)

    cifar10_estimator.deploy(initial_instance_count=1,
                             instance_type=instane_type)