# sagemaker-cicd-byoa

## データ準備
```
!aws s3 cp --recursive s3://floor28/data/cifar10 ./data
```

```
import os
import numpy as np
import boto3
import sagemaker
from sagemaker import get_execution_role

sagemaker_session = sagemaker.Session()
bucket = 'sagemaker-cicd'

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket)
bucket.create()

dataset_location = sagemaker_session.upload_data(path='data', bucket=bucket, key_prefix='data/DEMO-cifar10')
```
