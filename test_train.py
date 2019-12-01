# -*- coding: utf-8 -*-
import argparse

from sagemaker.tensorflow import TensorFlow

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='training script')
    parser.add_argument('--entry_point', type=str)
    parser.add_argument('--src_dir', type=str)
    parser.add_argument('--role', type=str)
    parser.add_argument('--input_s3', type=str)
    parser.add_argument('--output_s3', type=str)
    parser.add_argument('--repo', type=str)
    parser.add_argument('--version', type=str)

    args = parser.parse_args()

    entry_point = args.entry_point
    src_dir = args.src_dir
    dataset_location = args.input_s3
    model_dir = args.output_s3
    repo = args.repo
    version = args.version
    code_url = repo + '/tree/' + version
    role = args.role

    cifar10_estimator = TensorFlow(base_job_name='cifar10',
                                   entry_point=entry_point,
                                   source_dir=src_dir,
                                   role=role,
                                   framework_version='1.12.0',
                                   py_version='py3',
                                   hyperparameters={'epochs': 1},
                                   train_instance_count=1,
                                   train_instance_type='ml.p2.xlarge',
                                   model_dir=model_dir,
                                   output_path=model_dir,
                                   metric_definitions=[
                                       {'Name': 'accuracy',
                                        'Regex': 'accuracy = ([0-9\\.]+)'}
                                   ],
                                   tags=[
                                       {'Key': 'code_url', 'Value': code_url},
                                       {'Key': 'training_task','Value': 'cifar10-keras'},
                                   ])

    cifar10_estimator.fit({'train': '{}/train'.format(dataset_location),
                           'validation': '{}/validation'.format(dataset_location),
                           'eval': '{}/eval'.format(dataset_location)})