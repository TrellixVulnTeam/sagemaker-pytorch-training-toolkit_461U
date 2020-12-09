# Copyright 2017-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

import os

import pytest
from sagemaker.pytorch import PyTorch

from integration import resources_path
from utils.local_mode_utils import assert_files_exist


@pytest.mark.skip_cpu
@pytest.mark.skip_generic
def test_smdataparallel_training(sagemaker_local_session, image_uri, framework_version, tmpdir):
    output_path = 'file://' + str(tmpdir)

    estimator = PyTorch(
        entry_point=os.path.join(resources_path, 'mnist', 'smdataparallel_mnist.py'),
        role='SageMakerRole',
        train_instance_type="local_gpu",
        sagemaker_session=sagemaker_local_session,
        train_instance_count=1,
        image_name=image_uri,
        output_path=output_path,
        framework_version=framework_version,
        hyperparameters={'sagemaker_distributed_dataparallel_enabled': True, "save-model": ""})
    success_files = {
        'model': ['mnist_cnn.pt'],
        'output': ['success'],
    }
    _train_and_assert_success(estimator, str(tmpdir), success_files)


def _train_and_assert_success(estimator, output_path, output_files):
    estimator.fit()
    assert_files_exist(output_path, output_files)