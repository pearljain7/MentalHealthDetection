# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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

"""Task iterator for copy functionality."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os

from googlecloudsdk.command_lib.storage import errors
from googlecloudsdk.command_lib.storage import plurality_checkable_iterator
from googlecloudsdk.command_lib.storage import progress_callbacks
from googlecloudsdk.command_lib.storage import storage_url
from googlecloudsdk.command_lib.storage import wildcard_iterator
from googlecloudsdk.command_lib.storage.resources import resource_reference
from googlecloudsdk.command_lib.storage.tasks.cp import copy_task_factory
from googlecloudsdk.core import log


class CopyTaskIterator:
  """Iterates over each expanded source and creates an appropriate copy task."""

  def __init__(self,
               source_name_iterator,
               destination_string,
               custom_md5_digest=None,
               task_status_queue=None):
    """Initializes a CopyTaskIterator instance.

    Args:
      source_name_iterator (name_expansion.NameExpansionIterator):
        yields resource_reference.Resource objects with expanded source URLs.
      destination_string (str): The copy destination path or url.
      custom_md5_digest (str|None): User-added MD5 hash output to send to server
        for validating a single resource upload.
      task_status_queue (multiprocessing.Queue|None): Used for estimating total
        workload from this iterator.
    """
    self._source_name_iterator = (
        plurality_checkable_iterator.PluralityCheckableIterator(
            source_name_iterator))
    self._multiple_sources = self._source_name_iterator.is_plural()
    self._destination_string = destination_string
    self._custom_md5_digest = custom_md5_digest
    self._task_status_queue = task_status_queue

    self._total_file_count = 0
    self._total_size = 0

    if self._multiple_sources and self._custom_md5_digest:
      raise ValueError('Received multiple objects to upload, but only one'
                       'custom MD5 digest is allowed.')

  def _update_workload_estimation(self, resource):
    """Updates total_file_count and total_size.

    Args:
      resource (resource_reference.Resource): Any type of resource. Parse to
        help estimate total workload.
    """
    if self._total_file_count == -1 or self._total_size == -1:
      # -1 is signal that data is corrupt and not worth tracking.
      return
    try:
      if resource.is_container():
        return
      if isinstance(resource, resource_reference.FileObjectResource):
        size = os.path.getsize(resource.storage_url.object_name)
      elif (isinstance(resource, resource_reference.ObjectResource) and
            resource.size is not None):
        size = resource.size
      else:
        raise errors.ValueCannotBeDeterminedError
    except (OSError, errors.ValueCannotBeDeterminedError):
      log.error('Could not get size of resource {}.'.format(resource))
      self._total_file_count = -1
      self._total_size = -1
    else:
      self._total_file_count += 1
      self._total_size += size

  def __iter__(self):
    raw_destination = self._get_raw_destination()
    for source in self._source_name_iterator:

      if (isinstance(source.resource, resource_reference.ObjectResource) and
          isinstance(raw_destination.storage_url, storage_url.FileUrl) and
          source.resource.storage_url.object_name.endswith(
              raw_destination.storage_url.delimiter)):
        log.debug('Skipping the object {} since its name ends with a file '
                  'system delimiter.'.format(
                      source.resource.storage_url.versionless_url_string))
        continue

      destination_resource = self._get_copy_destination(raw_destination, source)

      if source.original_url.generation:
        source_url_string = source.resource.storage_url.url_string
      else:
        source_url_string = source.resource.storage_url.versionless_url_string

      if self._custom_md5_digest:
        source.resource.md5_hash = self._custom_md5_digest

      log.status.Print('Copying {} to {}'.format(
          source_url_string,
          destination_resource.storage_url.versionless_url_string))
      if self._task_status_queue:
        self._update_workload_estimation(source.resource)

      yield copy_task_factory.get_copy_task(source.resource,
                                            destination_resource)

    if (self._task_status_queue and
        (self._total_file_count > 0 or self._total_size > 0)):
      # Show fraction of total copies completed now that we know totals.
      progress_callbacks.workload_estimator_callback(
          self._task_status_queue,
          item_count=self._total_file_count,
          size=self._total_size)

  def _get_raw_destination(self):
    """Converts self._destination_string to a destination resource.

    Returns:
      A resource_reference.Resource. Note that this resource may not be a valid
      copy destination if it is a BucketResource, PrefixResource,
      FileDirectoryResource or UnknownResource.

    Raises:
      ValueError if the destination url is a cloud provider or if it specifies
      a version.
    """
    destination_url = storage_url.storage_url_from_string(
        self._destination_string)

    if isinstance(destination_url, storage_url.CloudUrl):
      if destination_url.is_provider():
        raise ValueError(
            'The cp command does not support provider-only destination URLs.')
      elif destination_url.generation is not None:
        raise ValueError(
            'The destination argument of the cp command cannot be a '
            'version-specific URL ({}).'
            .format(self._destination_string))

    raw_destination = self._expand_destination_wildcards()
    if raw_destination:
      return raw_destination
    return resource_reference.UnknownResource(destination_url)

  def _expand_destination_wildcards(self):
    """Expands destination wildcards.

    Ensures that only one resource matches the wildcard expanded string. Much
    like the unix cp command, the storage surface only supports copy operations
    to one user-specified destination.

    Returns:
      A resource_reference.Resource, or None if no matching resource is found.

    Raises:
      ValueError if more than one resource is matched, or the source contained
      an unescaped wildcard and no resources were matched.
    """
    destination_iterator = (
        plurality_checkable_iterator.PluralityCheckableIterator(
            wildcard_iterator.get_wildcard_iterator(self._destination_string)))

    contains_unexpanded_wildcard = (
        destination_iterator.is_empty() and
        wildcard_iterator.contains_wildcard(self._destination_string))

    if destination_iterator.is_plural() or contains_unexpanded_wildcard:
      raise ValueError('Destination ({}) must match exactly one URL'.format(
          self._destination_string))

    if not destination_iterator.is_empty():
      return next(destination_iterator)

  def _get_copy_destination(self, raw_destination, source):
    """Returns the final destination StorageUrl instance."""
    completion_is_necessary = (
        self._destination_is_container(raw_destination) or
        self._multiple_sources or
        source.resource.storage_url != source.expanded_url  # Recursion case.
    )

    if completion_is_necessary:
      return self._complete_destination(raw_destination, source)
    else:
      return raw_destination

  def _destination_is_container(self, destination):
    try:
      return destination.is_container()
    except errors.ValueCannotBeDeterminedError:
      # Some resource classes are not clearly containers. In these cases we need
      # to use the storage_url attribute to infer how to treat them.
      destination_url = destination.storage_url
      return (
          destination_url.url_string.endswith(destination_url.delimiter) or (
              isinstance(destination_url, storage_url.CloudUrl) and
              destination_url.is_bucket()))

  def _complete_destination(self, destination_container, source):
    """Gets a valid copy destination incorporating part of the source's name.

    When given a source file or object and a destination resource that should
    be treated as a container, this function uses the last part of the source's
    name to get an object or file resource representing the copy destination.

    For example: given a source `dir/file` and a destination `gs://bucket/`, the
    destination returned is a resource representing `gs://bucket/file`.

    Args:
      destination_container (resource_reference.Resource): The destination
        container.
      source (NameExpansionResult): Represents the source resource and the
        expanded parent url in case of recursion.

    Returns:
      The completed destination, a resource_reference.Resource.
    """
    destination_url = destination_container.storage_url
    source_url = source.resource.storage_url
    if source_url != source.expanded_url:
      # In case of recursion, the expanded_url can be the expanded wildcard URL
      # representing the container, and the source url can be the file/object.
      destination_suffix = self._get_destination_suffix_for_recursion(
          destination_container, source)
    else:
      # Schema might give us incorrect suffix for Windows.
      # TODO(b/169093672) This will not be required if we get rid of file://
      schemaless_url = source_url.versionless_url_string.rpartition(
          source_url.scheme.value + '://')[2]

      destination_suffix = schemaless_url.rpartition(source_url.delimiter)[2]

    new_destination_url = destination_url.join(destination_suffix)
    return resource_reference.UnknownResource(new_destination_url)

  def _get_destination_suffix_for_recursion(self, destination_container,
                                            source):
    """Returns the suffix required to complete the destination URL.

    Let's assume the following:
      User command => cp -r */base_dir gs://dest/existing_prefix
      source.resource.storage_url => a/base_dir/c/d.txt
      source.expanded_url => a/base_dir
      destination_container.storage_url => gs://dest/existing_prefix

    If the destination container exists, the entire directory gets copied:
    Result => gs://dest/existing_prefix/base_dir/c/d.txt

    On the other hand, if the destination container does not exist, the
    top-level dir does not get copied over.
    Result => gs://dest/existing_prefix/c/d.txt

    Args:
      destination_container (resource_reference.Resource): The destination
        container.
      source (NameExpansionResult): Represents the source resource and the
        expanded parent url in case of recursion.

    Returns:
      (str) The suffix to be appended to the destination container.
    """
    source_prefix_to_ignore = storage_url.rstrip_one_delimiter(
        source.expanded_url.versionless_url_string,
        source.expanded_url.delimiter)
    if (not isinstance(destination_container,
                       resource_reference.UnknownResource) and
        destination_container.is_container()):
      # Destination container exists. This means we need to preserve the
      # top-level source directory.
      # Remove the leaf name so that it gets added to the destination.
      source_prefix_to_ignore = source_prefix_to_ignore.rpartition(
          source.expanded_url.delimiter)[0]
      if not source_prefix_to_ignore:
        # In case of Windows, the source URL might not contain any Windows
        # delimiter if it was a single directory (e.g file://dir) and
        # source_prefix_to_ignore will be empty. Set it to <scheme>://.
        # TODO(b/169093672) This will not be required if we get rid of file://
        source_prefix_to_ignore = source.expanded_url.scheme.value + '://'

    full_source_url = source.resource.storage_url.versionless_url_string
    suffix_for_destination = full_source_url.split(source_prefix_to_ignore)[1]

    # Windows uses \ as a delimiter. Force the suffix to use the same
    # delimiter used by the destination container.
    source_delimiter = source.resource.storage_url.delimiter
    destination_delimiter = destination_container.storage_url.delimiter
    if source_delimiter != destination_delimiter:
      return suffix_for_destination.replace(source_delimiter,
                                            destination_delimiter)
    return suffix_for_destination
