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
"""Utilities for Eventarc Triggers API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.eventarc import common
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.eventarc import types
from googlecloudsdk.core import exceptions
from googlecloudsdk.core import resources
from googlecloudsdk.core.util import iso_duration
from googlecloudsdk.core.util import times

MAX_ACTIVE_DELAY_MINUTES = 10


class NoFieldsSpecifiedError(exceptions.Error):
  """Error when no fields were specified for a Patch operation."""


class NoRegionSpecifiedError(exceptions.Error):
  """Error when no destination region was specified for a global trigger."""


def CreateTriggersClient(release_track):
  api_version = common.GetApiVersion(release_track)
  if release_track == base.ReleaseTrack.GA:
    return _TriggersClient(api_version)
  else:
    return _TriggersClientBeta(api_version)


def GetTriggerURI(resource):
  trigger = resources.REGISTRY.ParseRelativeName(
      resource.name, collection='eventarc.projects.locations.triggers')
  return trigger.SelfLink()


def TriggerActiveTime(event_type, update_time):
  """Computes the time by which the trigger will become active.

  Args:
    event_type: str, the trigger's event type.
    update_time: str, the time when the trigger was last modified.

  Returns:
    The active time as a string, or None if the trigger is already active.
  """
  if not types.IsAuditLogType(event_type):
    # The delay only applies to Audit Log triggers.
    return None
  update_dt = times.ParseDateTime(update_time)
  delay = iso_duration.Duration(minutes=MAX_ACTIVE_DELAY_MINUTES)
  active_dt = times.GetDateTimePlusDuration(update_dt, delay)
  if times.Now() >= active_dt:
    return None
  return times.FormatDateTime(active_dt, fmt='%H:%M:%S', tzinfo=times.LOCAL)


class _TriggersClient(object):
  """Client for Triggers service in the Eventarc API."""

  def __init__(self, api_version):
    client = apis.GetClientInstance(common.API_NAME, api_version)
    self._messages = client.MESSAGES_MODULE
    self._service = client.projects_locations_triggers
    self._operation_service = client.projects_locations_operations

  def _BuildTriggerMessage(self, trigger_ref, event_filters, service_account,
                           destination_run_service, destination_run_path,
                           destination_run_region, transport_topic_ref):
    """Builds a Trigger message with the given data."""
    filter_messages = [] if event_filters is None else [
        self._messages.EventFilter(attribute=key, value=value)
        for key, value in event_filters.items()
    ]
    transport_topic_name = transport_topic_ref.RelativeName(
        ) if transport_topic_ref else None

    run_message = self._messages.CloudRun(
        service=destination_run_service,
        path=destination_run_path,
        region=destination_run_region)
    destination_message = self._messages.Destination(cloudRun=run_message)
    pubsub = self._messages.Pubsub(topic=transport_topic_name)
    transport = self._messages.Transport(pubsub=pubsub)
    return self._messages.Trigger(
        name=trigger_ref.RelativeName(),
        eventFilters=filter_messages,
        serviceAccount=service_account,
        destination=destination_message,
        transport=transport)

  def BuildUpdateMask(self, event_filters, service_account,
                      destination_run_service, destination_run_path,
                      destination_run_region):
    """Builds an update mask for updating a trigger.

    Args:
      event_filters: bool, whether to update the event filters.
      service_account: bool, whether to update the service account.
      destination_run_service: bool, whether to update the destination service.
      destination_run_path: bool, whether to update the destination path.
      destination_run_region: bool, whether to update the destination region.

    Returns:
      The update mask as a string.

    Raises:
      NoFieldsSpecifiedError: No fields are being updated.
    """
    update_mask = []
    if destination_run_path:
      update_mask.append('destination.cloudRun.path')
    if destination_run_region:
      update_mask.append('destination.cloudRun.region')
    if destination_run_service:
      update_mask.append('destination.cloudRun.service')
    if event_filters:
      update_mask.append('eventFilters')
    if service_account:
      update_mask.append('serviceAccount')
    if not update_mask:
      raise NoFieldsSpecifiedError('Must specify at least one field to update.')
    return ','.join(update_mask)

  def Create(self, trigger_ref, event_filters, service_account,
             destination_run_service, destination_run_path,
             destination_run_region, transport_topic_ref):
    """Creates a new Trigger.

    Args:
      trigger_ref: Resource, the Trigger to create.
      event_filters: dict, the Trigger's event filters.
      service_account: str or None, the Trigger's service account.
      destination_run_service: str, the Trigger's destination Cloud Run service.
      destination_run_path: str or None, the path on the destination service.
      destination_run_region: str or None, the destination service's region.
      transport_topic_ref: Resource or None, the user-provided transport topic.

    Returns:
      A long-running operation for create.

    Raises:
      NoRegionSpecifiedError: Destination region omitted for a global trigger.
    """
    # If no Cloud Run region was provided, use the trigger's location instead.
    if destination_run_region is None:
      destination_run_region = trigger_ref.Parent().Name()
      if destination_run_region == 'global':
        raise NoRegionSpecifiedError(
            'The `--destination-run-region` flag is required when creating a global trigger.'
        )
    trigger_message = self._BuildTriggerMessage(trigger_ref, event_filters,
                                                service_account,
                                                destination_run_service,
                                                destination_run_path,
                                                destination_run_region,
                                                transport_topic_ref)
    create_req = self._messages.EventarcProjectsLocationsTriggersCreateRequest(
        parent=trigger_ref.Parent().RelativeName(),
        trigger=trigger_message,
        triggerId=trigger_ref.Name())
    return self._service.Create(create_req)

  def Delete(self, trigger_ref):
    """Deletes a Trigger.

    Args:
      trigger_ref: Resource, the Trigger to delete.

    Returns:
      A long-running operation for delete.
    """
    delete_req = self._messages.EventarcProjectsLocationsTriggersDeleteRequest(
        name=trigger_ref.RelativeName())
    return self._service.Delete(delete_req)

  def Get(self, trigger_ref):
    """Gets a Trigger.

    Args:
      trigger_ref: Resource, the Trigger to get.

    Returns:
      The Trigger message.
    """
    get_req = self._messages.EventarcProjectsLocationsTriggersGetRequest(
        name=trigger_ref.RelativeName())
    return self._service.Get(get_req)

  def GetEventType(self, trigger_message):
    """Gets the Trigger's event type."""
    return types.EventFiltersMessageToType(trigger_message.eventFilters)

  def List(self, location_ref, limit, page_size):
    """Lists Triggers in a given location.

    Args:
      location_ref: Resource, the location to list Triggers in.
      limit: int or None, the total number of results to return.
      page_size: int, the number of entries in each batch (affects requests
        made, but not the yielded results).

    Returns:
      A generator of Triggers in the location.
    """
    list_req = self._messages.EventarcProjectsLocationsTriggersListRequest(
        parent=location_ref.RelativeName(), pageSize=page_size)
    return list_pager.YieldFromList(
        self._service,
        list_req,
        field='triggers',
        batch_size=page_size,
        limit=limit,
        batch_size_attribute='pageSize')

  def Patch(self, trigger_ref, event_filters, service_account,
            destination_run_service, destination_run_path,
            destination_run_region, update_mask):
    """Updates a Trigger.

    Args:
      trigger_ref: Resource, the Trigger to update.
      event_filters: dict or None, the updated event filters.
      service_account: str or None, the updated service account.
      destination_run_service: str or None, the updated destination service.
      destination_run_path: str or None, the updated destination path.
      destination_run_region: str or None, the updated destination region.
      update_mask: str, a comma-separated list of Trigger fields to update.

    Returns:
      A long-running operation for update.
    """
    trigger_message = self._BuildTriggerMessage(trigger_ref, event_filters,
                                                service_account,
                                                destination_run_service,
                                                destination_run_path,
                                                destination_run_region, None)
    patch_req = self._messages.EventarcProjectsLocationsTriggersPatchRequest(
        name=trigger_ref.RelativeName(),
        trigger=trigger_message,
        updateMask=update_mask)
    return self._service.Patch(patch_req)

  def WaitFor(self, operation, operation_type, trigger_ref):
    """Waits until the given long-running operation is complete.

    Args:
      operation: the long-running operation to wait for.
      operation_type: str, the type of operation
        (Creating, Updating or Deleting).
      trigger_ref: Resource, the Trigger to reference.

    Returns:
      The long-running operation's response.
    """
    poller = waiter.CloudOperationPollerNoResources(self._operation_service)
    operation_ref = resources.REGISTRY.Parse(
        operation.name, collection='eventarc.projects.locations.operations')
    trigger_name = trigger_ref.Name()
    project_name = trigger_ref.Parent().Parent().Name()
    location_name = trigger_ref.Parent().Name()
    message = ('{} trigger [{}] in project [{}], '
               'location [{}]').format(operation_type, trigger_name,
                                       project_name, location_name)
    return waiter.WaitFor(poller, operation_ref, message)


class _TriggersClientBeta(_TriggersClient):
  """Client for Triggers service in the Eventarc beta API."""

  def _BuildTriggerMessage(self, trigger_ref, event_filters, service_account,
                           destination_run_service, destination_run_path,
                           destination_run_region, transport_topic_ref):
    """Builds a Trigger message with the given data."""
    criteria_messages = [] if event_filters is None else [
        self._messages.MatchingCriteria(attribute=key, value=value)
        for key, value in event_filters.items()
    ]
    run_message = self._messages.CloudRunService(
        service=destination_run_service,
        path=destination_run_path,
        region=destination_run_region)
    destination_message = self._messages.Destination(
        cloudRunService=run_message)
    transport = None
    if transport_topic_ref:
      transport_topic_name = transport_topic_ref.RelativeName()
      pubsub = self._messages.Pubsub(topic=transport_topic_name)
      transport = self._messages.Transport(pubsub=pubsub)
    return self._messages.Trigger(
        name=trigger_ref.RelativeName(),
        matchingCriteria=criteria_messages,
        serviceAccount=service_account,
        destination=destination_message,
        transport=transport)

  def BuildUpdateMask(self, event_filters, service_account,
                      destination_run_service, destination_run_path,
                      destination_run_region):
    """Builds an update mask for updating a trigger.

    Args:
      event_filters: bool, whether to update the event filters.
      service_account: bool, whether to update the service account.
      destination_run_service: bool, whether to update the destination service.
      destination_run_path: bool, whether to update the destination path.
      destination_run_region: bool, whether to update the destination region.

    Returns:
      The update mask as a string.

    Raises:
      NoFieldsSpecifiedError: No fields are being updated.
    """
    update_mask = []
    if destination_run_path:
      update_mask.append('destination.cloudRunService.path')
    if destination_run_region:
      update_mask.append('destination.cloudRunService.region')
    if destination_run_service:
      update_mask.append('destination.cloudRunService.service')
    if event_filters:
      update_mask.append('matchingCriteria')
    if service_account:
      update_mask.append('serviceAccount')
    if not update_mask:
      raise NoFieldsSpecifiedError('Must specify at least one field to update.')
    return ','.join(update_mask)

  def GetEventType(self, trigger_message):
    """Gets the Trigger's event type."""
    return types.EventFiltersMessageToType(trigger_message.matchingCriteria)
