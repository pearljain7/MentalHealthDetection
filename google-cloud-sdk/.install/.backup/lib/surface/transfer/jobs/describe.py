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
"""Command to get details on a Transfer job."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.transfer import jobs_util
from googlecloudsdk.calliope import base
from googlecloudsdk.core.resource import resource_printer


class Describe(base.ListCommand):
  """Get configuration and latest operation details about transfer job."""

  detailed_help = {
      'DESCRIPTION':
          """\
      Get configuration and latest operation details about a specific transfer
      job.
      """,
      'EXAMPLES':
          '$ {command} JOB-NAME',
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'job_name', help='The name of the job you want to describe.')

  def Display(self, args, resources):
    del args  # Unsued.
    resource_printer.Print(resources, 'json')

  def Run(self, args):
    return jobs_util.api_get(args.job_name)
