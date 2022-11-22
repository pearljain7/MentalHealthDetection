# -*- coding: utf-8 -*- #
# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utils for components in copy operations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import hashlib
import math
import os

from googlecloudsdk.command_lib.storage import storage_url
from googlecloudsdk.command_lib.storage.resources import resource_reference
from googlecloudsdk.core.util import files
from googlecloudsdk.core.util import scaled_integer


_PARALLEL_UPLOAD_STATIC_SALT = """
PARALLEL_UPLOAD_SALT_TO_PREVENT_COLLISIONS.
The theory is that no user will have prepended this to the front of
one of their object names and then do an MD5 hash of the name, and
then prepended PARALLEL_UPLOAD_TEMP_NAMESPACE to the front of their object
name. Note that there will be no problems with object name length since we
hash the original name.
"""
_PARALLEL_UPLOAD_TEMPORARY_NAMESPACE = (
    '/gcloud/tmp/parallel_composite_uploads/'
    'see_gcloud_storage_cp_help_for_details/')


def _get_temporary_component_name(source_resource, component_id):
  """Gets a temporary object name for a component of source_resource."""
  source_name = source_resource.storage_url.object_name
  salted_name = _PARALLEL_UPLOAD_STATIC_SALT + source_name

  sha1_hash = hashlib.sha1(salted_name.encode('utf-8'))

  return '{}{}_{}'.format(_PARALLEL_UPLOAD_TEMPORARY_NAMESPACE,
                          sha1_hash.hexdigest(), str(component_id))


def create_file_if_needed(source_resource, destination_resource):
  """Creates new file if none exists or one that is too large exists at path.

  Args:
    source_resource (ObjectResource): Contains size metadata for target file.
    destination_resource(FileObjectResource|UnknownResource): Contains path to
      create file at.
  """
  file_path = destination_resource.storage_url.object_name
  if os.path.exists(
      file_path) and os.path.getsize(file_path) <= source_resource.size:
    return

  with files.BinaryFileWriter(
      file_path, create_path=True, mode=files.BinaryFileWriterMode.TRUNCATE):
    # Wipe or create file.
    pass


def get_temporary_component_resource(source_resource, destination_resource,
                                     component_id):
  """Gets a temporary component destination resource for a composite upload.

  Args:
    source_resource (resource_reference.FileObjectResource): The upload source.
    destination_resource (resource_reference.ObjectResource|UnknownResource):
      The upload destination.
    component_id (int): An id that's not shared by any other component in this
      transfer.

  Returns:
    A resource_reference.UnknownResource representing the component's
    destination.
  """
  component_object_name = _get_temporary_component_name(source_resource,
                                                        component_id)

  destination_url = destination_resource.storage_url
  component_url = storage_url.CloudUrl(destination_url.scheme,
                                       destination_url.bucket_name,
                                       component_object_name)

  return resource_reference.UnknownResource(component_url)


def get_component_offsets_and_lengths(file_size, target_component_size,
                                      max_components):
  """Calculates start bytes and sizes for a multi-component copy operation.

  Args:
    file_size (int): Total byte size of file being divided into components.
    target_component_size (int|str): Target size for each component if not total
      components isn't capped by max_components. May be byte count int or size
      string (e.g. "50M").
    max_components (int|None): Limit on allowed components regardless of
      file_size and target_component_size. None indicates no limit.

  Returns:
    List of component offsets and lengths: list[(offset, length)].
    Total component count can be found by taking the length of the list.
  """
  if isinstance(target_component_size, int):
    target_component_size_bytes = target_component_size
  else:
    target_component_size_bytes = scaled_integer.ParseInteger(
        target_component_size)

  target_component_count = min(
      math.ceil(file_size / target_component_size_bytes),
      max_components if max_components is not None else float('inf'))

  component_count = max(target_component_count, 2)
  component_size = math.ceil(file_size / component_count)

  component_offsets_and_lengths = []
  for i in range(component_count):
    offset = i * component_size
    if offset >= file_size:
      break
    length = min(component_size, file_size - offset)
    component_offsets_and_lengths.append((offset, length))

  return component_offsets_and_lengths
