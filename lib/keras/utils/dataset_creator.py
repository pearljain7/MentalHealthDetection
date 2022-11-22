# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=g-classes-have-attributes
"""Input dataset creator for `model.fit`."""

import tensorflow.compat.v2 as tf
from tensorflow.python.util.tf_export import keras_export


@keras_export('keras.utils.experimental.DatasetCreator', v1=[])
class DatasetCreator(object):
  """Object that returns a `tf.data.Dataset` upon invoking.

  `tf.keras.utils.experimental.DatasetCreator` is designated as a supported type
  for `x`, or the input, in `tf.keras.Model.fit`. Pass an instance of this class
  to `fit` when using a callable (with a `input_context` argument) that returns
  a `tf.data.Dataset`.

  ```python
  model = tf.keras.Sequential([tf.keras.layers.Dense(10)])
  model.compile(tf.keras.optimizers.SGD(), loss="mse")

  def dataset_fn(input_context):
    global_batch_size = 64
    batch_size = input_context.get_per_replica_batch_size(global_batch_size)
    dataset = tf.data.Dataset.from_tensors(([1.], [1.])).repeat()
    dataset = dataset.shard(
        input_context.num_input_pipelines, input_context.input_pipeline_id)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(2)
    return dataset

  model.fit(DatasetCreator(dataset_fn), epochs=10, steps_per_epoch=10)
  ```

  `Model.fit` usage with `DatasetCreator` is intended to work across all
  `tf.distribute.Strategy`s, as long as `Strategy.scope` is used at model
  creation:

  ```python
  strategy = tf.distribute.experimental.ParameterServerStrategy(
      cluster_resolver)
  with strategy.scope():
    model = tf.keras.Sequential([tf.keras.layers.Dense(10)])
  model.compile(tf.keras.optimizers.SGD(), loss="mse")
  ...
  ```

  Note: When using `DatasetCreator`, `steps_per_epoch` argument in `Model.fit`
  must be provided as the cardinality of such input cannot be inferred.

  Args:
    dataset_fn: A callable that takes a single argument of type
      `tf.distribute.InputContext`, which is used for batch size calculation and
      cross-worker input pipeline sharding (if neither is needed, the
      `InputContext` parameter can be ignored in the `dataset_fn`), and returns
      a `tf.data.Dataset`.
  """

  def __init__(self, dataset_fn):
    if not callable(dataset_fn):
      raise TypeError('`dataset_fn` for `DatasetCreator` must be a `callable`.')
    self.dataset_fn = dataset_fn

  def __call__(self, *args, **kwargs):
    # When a `DatasetCreator` is invoked, it forwards args/kwargs straight to
    # the callable.
    dataset = self.dataset_fn(*args, **kwargs)
    if not isinstance(dataset, tf.data.Dataset):
      raise TypeError('The `callable` provided to `DatasetCreator` must return '
                      'a Dataset.')
    return dataset