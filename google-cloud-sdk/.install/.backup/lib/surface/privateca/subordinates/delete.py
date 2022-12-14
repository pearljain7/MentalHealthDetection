# Lint as: python3
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
"""Delete a subordinate certificate authority."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from dateutil import tz

from googlecloudsdk.api_lib.privateca import base as privateca_base
from googlecloudsdk.api_lib.privateca import request_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.privateca import flags
from googlecloudsdk.command_lib.privateca import flags_v1
from googlecloudsdk.command_lib.privateca import operations
from googlecloudsdk.command_lib.privateca import resource_args
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io
from googlecloudsdk.core.util import times


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class DeleteBeta(base.DeleteCommand):
  r"""Schedule a subordinate certificate authority for deletion.

    Schedule a subordinate certificate authority for deletion in 30 days.

    Note that any user-managed KMS keys or Google Cloud Storage buckets
    will not be affected by this operation. You will need to delete the user-
    managed resources separately once the CA is deleted. Any Google-managed
    resources will be cleaned up.

    The CA specified in this command MUST:

      1) be disabled.
      2) have no un-revoked or un-expired certificates. Use the revoke command
         to revoke any active certificates.

    You can use the restore command to halt this process.

    ## EXAMPLES

    To schedule a subordinate CA for deletion:

      $ {command} server-tls-1 --location='us-west1'

    To schedule a subordinate CA for deletion while skipping the confirmation
    input:

      $ {command} server-tls-1 --location='us-west1' --quiet

    To un-do the scheduled deletion for a subordinate CA:

      $ {parent_command} restore server-tls-1 --location='us-west1'
  """

  @staticmethod
  def Args(parser):
    resource_args.AddCertificateAuthorityPositionalResourceArg(
        parser, 'to schedule deletion for')
    flags.AddIgnoreActiveCertificatesFlag(parser)

  def Run(self, args):
    client = privateca_base.GetClientInstance()
    messages = privateca_base.GetMessagesModule()

    ca_ref = args.CONCEPTS.certificate_authority.Parse()

    if not console_io.PromptContinue(
        message='You are about to schedule Certificate Authority [{}] for deletion in 30 days'
        .format(ca_ref.RelativeName()),
        default=True):
      log.status.Print('Aborted by user.')
      return

    current_ca = client.projects_locations_certificateAuthorities.Get(
        messages.PrivatecaProjectsLocationsCertificateAuthoritiesGetRequest(
            name=ca_ref.RelativeName()))

    resource_args.CheckExpectedCAType(
        messages.CertificateAuthority.TypeValueValuesEnum.SUBORDINATE,
        current_ca)

    operation = client.projects_locations_certificateAuthorities.ScheduleDelete(
        messages
        .PrivatecaProjectsLocationsCertificateAuthoritiesScheduleDeleteRequest(
            name=ca_ref.RelativeName(),
            scheduleDeleteCertificateAuthorityRequest=messages
            .ScheduleDeleteCertificateAuthorityRequest(
                ignoreActiveCertificates=args.ignore_active_certificates,
                requestId=request_utils.GenerateRequestId())))

    ca_response = operations.Await(operation,
                                   'Scheduling Subordinate CA for deletion')
    ca = operations.GetMessageFromResponse(ca_response,
                                           messages.CertificateAuthority)

    formatted_deletion_time = times.ParseDateTime(ca.deleteTime).astimezone(
        tz.tzutc()).strftime('%Y-%m-%dT%H:%MZ')

    log.status.Print('Scheduled Subordinate CA [{}] for deletion at {}.'.format(
        ca_ref.RelativeName(), formatted_deletion_time))


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Delete(base.DeleteCommand):
  r"""Delete a subordinate certificate authority.

    Delete a Subordinate Certificate Authority. Deleted Subordinate Certificate
    Authorities may be recovered with the `{parent_command} undelete` command
    within a grace period of 30 days.

    Note that any user-managed KMS keys or Google Cloud Storage buckets
    will not be affected by this operation. You will need to delete the user-
    managed resources separately once the CA is deleted. Any Google-managed
    resources will be cleaned up.

    The CA specified in this command MUST:

      1) be disabled.
      2) have no un-revoked or un-expired certificates. Use the revoke command
         to revoke any active certificates.

    Use the `--ignore-active-certificates` flag to remove 2) as a requirement.

    ## EXAMPLES

    To delete a subordinate CA:

      $ {command} server-tls-1 --pool=my-pool --location='us-west1'

    To delete a CA while skipping the confirmation input:

      $ {command} server-tls-1s --pool=my-pool --location='us-west1' --quiet

    To undo the deletion for a subordinate CA:

      $ {parent_command} undelete server-tls-1 --pool=my-pool
      --location='us-west1'
  """

  @staticmethod
  def Args(parser):
    resource_args.AddCertAuthorityPositionalResourceArg(parser, 'to delete')
    flags_v1.AddIgnoreActiveCertificatesFlag(parser)

  def Run(self, args):
    client = privateca_base.GetClientInstance(api_version='v1')
    messages = privateca_base.GetMessagesModule(api_version='v1')

    ca_ref = args.CONCEPTS.certificate_authority.Parse()
    ca_name = ca_ref.RelativeName()

    if not console_io.PromptContinue(
        message='You are about to delete Certificate Authority [{}]'.format(
            ca_ref.RelativeName()),
        default=True):
      log.status.Print('Aborted by user.')
      return

    current_ca = client.projects_locations_caPools_certificateAuthorities.Get(
        messages
        .PrivatecaProjectsLocationsCaPoolsCertificateAuthoritiesGetRequest(
            name=ca_name))

    resource_args.CheckExpectedCAType(
        messages.CertificateAuthority.TypeValueValuesEnum.SUBORDINATE,
        current_ca,
        version='v1')

    operation = client.projects_locations_caPools_certificateAuthorities.Delete(
        messages
        .PrivatecaProjectsLocationsCaPoolsCertificateAuthoritiesDeleteRequest(
            name=ca_name,
            ignoreActiveCertificates=args.ignore_active_certificates,
            requestId=request_utils.GenerateRequestId()))

    ca_response = operations.Await(operation, 'Deleting Subordinate CA')
    ca = operations.GetMessageFromResponse(ca_response,
                                           messages.CertificateAuthority)

    formatted_deletion_time = times.ParseDateTime(ca.deleteTime).astimezone(
        tz.tzutc()).strftime('%Y-%m-%dT%H:%MZ')

    log.status.Print(
        'Deleted Subordinate CA [{}]. CA can be undeleted until {}.'.format(
            ca_name, formatted_deletion_time))
