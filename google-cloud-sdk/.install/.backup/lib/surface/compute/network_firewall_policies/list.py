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
"""Command for listing network firewall policies."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import lister
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.network_firewall_policies import flags
from googlecloudsdk.core import properties


class List(base.ListCommand):
  """List Compute Engine network firewall policies.

  *{command}* is used to list network firewall policies. A network
  firewall policy is a set of rules that controls access to various resources.
  """

  @classmethod
  def Args(cls, parser):
    flags.AddArgsListNetworkFirewallPolicy(parser)
    parser.display_info.AddFormat(flags.DEFAULT_LIST_FORMAT)
    lister.AddBaseListerArgs(parser)
    parser.display_info.AddCacheUpdater(flags.NetworkFirewallPoliciesCompleter)

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client.apitools_client
    messages = client.MESSAGES_MODULE

    if args.project:
      project = args.project
    else:
      project = properties.VALUES.core.project.GetOrFail()

    request = messages.ComputeNetworkFirewallPoliciesListRequest(
        project=project)

    return list_pager.YieldFromList(
        client.networkFirewallPolicies,
        request,
        field='items',
        limit=args.limit,
        batch_size=None)


List.detailed_help = {
    'EXAMPLES':
        """\
    To list network firewall policies under project
    ``my-project'', run:

      $ {command} --project=my-project
    """,
}
