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

"""Command to list Azure clients."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.azure import util as azure_api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.azure import resource_args
from googlecloudsdk.command_lib.container.azure import util as command_util
from googlecloudsdk.command_lib.container.gkemulticloud import endpoint_util


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class List(base.ListCommand):
  """List Azure clients."""

  @staticmethod
  def Args(parser):
    resource_args.AddRegionResourceArg(parser, 'to list Azure clients')
    parser.display_info.AddFormat(command_util.CLIENT_FORMAT)

  def Run(self, args):
    """Run the list command."""
    region_ref = args.CONCEPTS.region.Parse()
    with endpoint_util.GkemulticloudEndpointOverride(region_ref.locationsId,
                                                     self.ReleaseTrack()):
      api_client = azure_api_util.ClientsClient(track=self.ReleaseTrack())
      return api_client.List(
          region_ref, page_size=args.page_size, limit=args.limit)
