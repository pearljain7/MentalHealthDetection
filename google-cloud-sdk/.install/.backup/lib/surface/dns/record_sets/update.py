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
"""gcloud dns record-sets update command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.dns import resource_record_sets as rrsets_util
from googlecloudsdk.api_lib.dns import util
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.dns import flags
from googlecloudsdk.core import properties


class Update(base.UpdateCommand):
  """Update a record-set in a managed-zone.

  This command updates a record-set contained within the specified
  managed-zone.

  ## EXAMPLES

  To update a record-set with dnsName foo.bar.com., record type A to have rrdata
  [1.2.3.4, 9.8.7.6] and ttl 60 in my_zone, run:

    $ {command} foo.bar.com. --rrdatas=1.2.3.4,9.8.7.6 --type=A --ttl=60
       --zone=my_zone

  """

  @classmethod
  def Args(cls, parser):
    flags.GetZoneArg().AddToParser(parser)
    flags.GetResourceRecordSetsNameArg().AddToParser(parser)
    flags.GetResourceRecordSetsTypeArg(True).AddToParser(parser)
    flags.GetResourceRecordSetsTtlArg(False).AddToParser(parser)
    flags.GetResourceRecordSetsRrdatasArg(False).AddToParser(parser)
    parser.display_info.AddCacheUpdater(None)
    parser.display_info.AddFormat(flags.RESOURCERECORDSETS_FORMAT)

  def Run(self, args):
    api_version = util.GetApiFromTrack(self.ReleaseTrack())

    messages = apis.GetMessagesModule('dns', api_version)

    dns_client = util.GetApiClient(api_version)

    zone_ref = util.GetRegistry(api_version).Parse(
        args.zone,
        params={
            'project': properties.VALUES.core.project.GetOrFail,
        },
        collection='dns.managedZones')

    resource_record_set = rrsets_util.CreateRecordSetFromArgs(args, api_version)

    result = dns_client.resourceRecordSets.Patch(
        messages.DnsResourceRecordSetsPatchRequest(
            project=zone_ref.project,
            managedZone=zone_ref.Name(),
            name=util.AppendTrailingDot(resource_record_set.name),
            type=resource_record_set.type,
            resourceRecordSet=resource_record_set))

    return result
