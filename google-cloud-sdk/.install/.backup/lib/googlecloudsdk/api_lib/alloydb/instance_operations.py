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
"""AlloyDB instance operations API helper."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.alloydb import api_util
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.core import resources


def Await(operation, message, creates_resource=True):
  """Waits for the given google.longrunning.Operation to complete.

  Args:
    operation: The operation to poll.
    message: String to display for default progress_tracker.
    creates_resource: Whether or not the operation creates a resource

  Raises:
    apitools.base.py.HttpError: if the request returns an HTTP error

  Returns:
    The Operation or the Resource the Operation is associated with.
  """
  client = api_util.AlloyDBClient(api_util.API_VERSION_DEFAULT)
  alloydb_client = client.alloydb_client
  if creates_resource:
    poller = waiter.CloudOperationPoller(
        alloydb_client.projects_locations_clusters_instances,
        alloydb_client.projects_locations_operations)
  else:
    poller = waiter.CloudOperationPollerNoResources(
        alloydb_client.projects_locations_operations)
  ref = resources.REGISTRY.ParseRelativeName(
      operation.name,
      collection='alloydbadmin.projects.locations.operations')
  return waiter.WaitFor(poller, ref, message)
