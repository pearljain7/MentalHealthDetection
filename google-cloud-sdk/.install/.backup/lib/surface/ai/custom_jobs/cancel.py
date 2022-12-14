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
"""Command to cancel a custom job in Vertex AI."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.ai.custom_jobs import client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.ai import constants
from googlecloudsdk.command_lib.ai import endpoint_util
from googlecloudsdk.command_lib.ai.custom_jobs import flags
from googlecloudsdk.core import log

_CUSTOM_JOB_CANCEL_DISPLAY_MESSAGE = """\
Request to cancel custom job [{id}] has been sent

You may view the status of your job with the command

  $ gcloud alpha ai custom-jobs describe {id}
"""


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.ALPHA)
class Cancel(base.SilentCommand):
  """Cancel a running custom job.

  If the job is already finished,
  the command will not perform any operation.
  """

  @staticmethod
  def Args(parser):
    flags.AddCustomJobResourceArg(parser, 'to cancel')

  def Run(self, args):
    custom_job_ref = args.CONCEPTS.custom_job.Parse()
    name = custom_job_ref.Name()
    region = custom_job_ref.AsDict()['locationsId']
    with endpoint_util.AiplatformEndpointOverrides(
        version=constants.BETA_VERSION, region=region):
      response = client.CustomJobsClient(version=constants.BETA_VERSION).Cancel(
          custom_job_ref.RelativeName())
      log.status.Print(_CUSTOM_JOB_CANCEL_DISPLAY_MESSAGE.format(id=name))
      return response
