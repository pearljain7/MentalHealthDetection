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
"""Utilities for constructing Assured api messages."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.assured import util
from googlecloudsdk.calliope.base import ReleaseTrack


def GetMessages(release_track):
  return util.GetMessagesModule(release_track)


def GetWorkloadMessage(release_track):
  return WORKLOAD_MAP.get(release_track)


def GetKmsSettings(release_track):
  return KMS_SETTINGS_MAP.get(release_track)


def GetResourceSettings(release_track):
  return RESOURCE_SETTINGS_MAP.get(release_track)


def CreateAssuredParent(organization_id, location):
  return 'organizations/{}/locations/{}'.format(organization_id, location)


def CreateAssuredWorkload(display_name=None,
                          compliance_regime=None,
                          billing_account=None,
                          next_rotation_time=None,
                          rotation_period=None,
                          labels=None,
                          etag=None,
                          provisioned_resources_parent=None,
                          resource_settings=None,
                          release_track=ReleaseTrack.GA):
  """Construct an Assured Workload message for Assured Workloads Beta API requests.

  Args:
    display_name: str, display name of the Assured Workloads environment.
    compliance_regime: str, the compliance regime, which is one of:
      FEDRAMP_MODERATE, FEDRAMP_HIGH, IL4 or CJIS.
    billing_account: str, the billing account of the Assured Workloads
      environment in the form: billingAccounts/{BILLING_ACCOUNT_ID}
    next_rotation_time: str, the next key rotation time for the Assured
      Workloads environment, for example: 2020-12-30T10:15:00.00Z
    rotation_period: str, the time between key rotations, for example: 172800s
    labels: dict, dictionary of label keys and values of the Assured Workloads
      environment.
    etag: str, the etag of the Assured Workloads environment.
    provisioned_resources_parent: str, parent of the provisioned projects,
      for example: folders/{FOLDER_ID}
    resource_settings: list of key=value pairs to set customized resource
      settings, which can be one of the following: consumer-project-id,
      consumer-project-name, encryption-keys-project-id,
      encryption-keys-project-name or keyring-id, for example:
      consumer-project-id={ID1},encryption-keys-project-id={ID2}
    release_track: ReleaseTrack, gcloud release track being used

  Returns:
    A populated Assured Workloads message for the Assured Workloads Beta API.
  """

  workload_message = GetWorkloadMessage(release_track)
  workload = workload_message()
  if etag:
    workload.etag = etag
  if billing_account:
    workload.billingAccount = billing_account
  if display_name:
    workload.displayName = display_name
  if labels:
    workload.labels = CreateLabels(labels, workload_message)
  if compliance_regime:
    workload.complianceRegime = workload_message.ComplianceRegimeValueValuesEnum(
        compliance_regime)
  if provisioned_resources_parent:
    workload.provisionedResourcesParent = provisioned_resources_parent
  if next_rotation_time and rotation_period:
    workload.kmsSettings = GetKmsSettings(release_track)(
        nextRotationTime=next_rotation_time, rotationPeriod=rotation_period)
  if resource_settings:
    workload.resourceSettings = CreateResourceSettingsList(
        resource_settings, release_track)
  return workload


def CreateLabels(labels, workload_message):
  workload_labels = []
  for key, value in labels.items():
    new_label = workload_message.LabelsValue.AdditionalProperty(
        key=key, value=value)
    workload_labels.append(new_label)
  return workload_message.LabelsValue(additionalProperties=workload_labels)


def CreateResourceSettingsList(resource_settings, release_track):
  """Construct a list of ResourceSettings for Assured Workload object.

  Args:
    resource_settings: a list of key=value pairs of customized resource
      settings.
    release_track: ReleaseTrack, gcloud release track being used.

  Returns:
    A list of ResourceSettings for the Assured Workload object.
  """
  resource_settings_dict = {}
  for key, value in resource_settings.items():
    resource_type = GetResourceType(key, release_track)
    resource_settings = resource_settings_dict[
        resource_type] if resource_type in resource_settings_dict else CreateResourceSettings(
            resource_type, release_track)
    if key.endswith('-id'):
      resource_settings.resourceId = value
    elif key.endswith('-name'):
      resource_settings.displayName = value
    resource_settings_dict[resource_type] = resource_settings
  return list(resource_settings_dict.values())


def GetResourceType(key, release_track):
  """Returns a resource settings type from the key.

  Args:
    key: str, the setting name, which can be one of the following -
      consumer-project-id, consumer-project-name, encryption-keys-project-id,
      encryption-keys-project-name or keyring-id.
    release_track: ReleaseTrack, gcloud release track being used.
  """
  resource_settings_message = GetResourceSettings(release_track)
  if key.startswith('consumer-project'):
    return resource_settings_message.ResourceTypeValueValuesEnum.CONSUMER_PROJECT
  elif key.startswith('encryption-keys-project'):
    return resource_settings_message.ResourceTypeValueValuesEnum.ENCRYPTION_KEYS_PROJECT
  elif key.startswith('keyring'):
    return resource_settings_message.ResourceTypeValueValuesEnum.KEYRING


def CreateResourceSettings(resource_type, release_track):
  resource_settings_message = GetResourceSettings(release_track)
  return resource_settings_message(resourceType=resource_type)


def CreateUpdateMask(display_name, labels):
  update_mask = []
  if display_name:
    update_mask.append('workload.display_name')
  if labels:
    update_mask.append('workload.labels')
  return ','.join(update_mask)


def CreateCreateRequest(external_id,
                        parent,
                        workload,
                        release_track=ReleaseTrack.GA):
  """Construct an Assured Workload Create Request for Assured Workloads API requests.

  Args:
    external_id: str, the identifier that identifies this Assured Workloads
      environment externally.
    parent: str, the parent organization of the Assured Workloads environment
      to be created, in the form: organizations/{ORG_ID}/locations/{LOCATION}.
    workload: Workload, new Assured Workloads environment containing the values
      to be used.
    release_track: ReleaseTrack, gcloud release track being used

  Returns:
    A populated Assured Workloads Update Request for the Assured Workloads API.
  """
  if release_track == ReleaseTrack.GA:
    return util.GetMessagesModule(
        release_track
    ).AssuredworkloadsOrganizationsLocationsWorkloadsCreateRequest(
        externalId=external_id,
        parent=parent,
        googleCloudAssuredworkloadsV1Workload=workload)
  else:
    return util.GetMessagesModule(
        release_track
    ).AssuredworkloadsOrganizationsLocationsWorkloadsCreateRequest(
        externalId=external_id,
        parent=parent,
        googleCloudAssuredworkloadsV1beta1Workload=workload)


def CreateUpdateRequest(workload,
                        name,
                        update_mask,
                        release_track=ReleaseTrack.GA):
  """Construct an Assured Workload Update Request for Assured Workloads API requests.

  Args:
    workload: googleCloudAssuredworkloadsV1beta1Workload, new Assured Workloads
      environment containing the new configuration values to be used.
    name: str, the name for the Assured Workloads environment being updated
      in the form:
        organizations/{ORG_ID}/locations/{LOCATION}/workloads/{WORKLOAD_ID}.
    update_mask: str, list of the fields to be updated, for example,
      workload.display_name,workload.labels
    release_track: ReleaseTrack, gcloud release track being used

  Returns:
    A populated Assured Workloads Update Request for the Assured Workloads API.
  """
  messages = util.GetMessagesModule(release_track)
  if release_track == ReleaseTrack.GA:
    return messages.AssuredworkloadsOrganizationsLocationsWorkloadsPatchRequest(
        googleCloudAssuredworkloadsV1Workload=workload,
        name=name,
        updateMask=update_mask)
  else:
    return messages.AssuredworkloadsOrganizationsLocationsWorkloadsPatchRequest(
        googleCloudAssuredworkloadsV1beta1Workload=workload,
        name=name,
        updateMask=update_mask)


WORKLOAD_MAP = {
    ReleaseTrack.ALPHA:
        GetMessages(ReleaseTrack.ALPHA
                   ).GoogleCloudAssuredworkloadsV1beta1Workload,
    ReleaseTrack.BETA:
        GetMessages(ReleaseTrack.BETA
                   ).GoogleCloudAssuredworkloadsV1beta1Workload,
    ReleaseTrack.GA:
        GetMessages(ReleaseTrack.GA).GoogleCloudAssuredworkloadsV1Workload
}

KMS_SETTINGS_MAP = {
    ReleaseTrack.ALPHA:
        GetMessages(ReleaseTrack.ALPHA
                   ).GoogleCloudAssuredworkloadsV1beta1WorkloadKMSSettings,
    ReleaseTrack.BETA:
        GetMessages(ReleaseTrack.BETA
                   ).GoogleCloudAssuredworkloadsV1beta1WorkloadKMSSettings,
    ReleaseTrack.GA:
        GetMessages(ReleaseTrack.GA
                   ).GoogleCloudAssuredworkloadsV1WorkloadKMSSettings
}

RESOURCE_SETTINGS_MAP = {
    ReleaseTrack.ALPHA:
        GetMessages(ReleaseTrack.ALPHA
                   ).GoogleCloudAssuredworkloadsV1beta1WorkloadResourceSettings,
    ReleaseTrack.BETA:
        GetMessages(ReleaseTrack.BETA
                   ).GoogleCloudAssuredworkloadsV1beta1WorkloadResourceSettings,
    ReleaseTrack.GA:
        GetMessages(ReleaseTrack.GA
                   ).GoogleCloudAssuredworkloadsV1WorkloadResourceSettings
}
