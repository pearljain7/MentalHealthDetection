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
"""Updates a AlloyDB cluster."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.alloydb import api_util
from googlecloudsdk.api_lib.alloydb import cluster_operations
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.alloydb import flags
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Update(base.UpdateCommand):
  """Updates an AlloyDB cluster within a given project and region."""

  @staticmethod
  def Args(parser):
    """Specifies additional command flags.

      --region: The region the cluster will be located in.

    Args:
      parser: argparse.Parser: Parser object for command line inputs.

    """
    base.ASYNC_FLAG.AddToParser(parser)
    flags.AddRegion(parser)
    flags.AddCluster(parser)

  def Run(self, args):
    """This is what gets called when the user runs the command.

    Args:
      args: argparse.Namespace, An object that contains the values for the
          arguments specified in the .Args() method.

    Returns:
      A resource object dispatched by display.Displayer().
    """
    args.format = 'default'
    client = api_util.AlloyDBClient(api_util.API_VERSION_DEFAULT)
    alloydb_client = client.alloydb_client
    alloydb_messages = client.alloydb_messages
    project_ref = client.resource_parser.Create(
        'alloydbadmin.projects.locations.clusters',
        projectsId=properties.VALUES.core.project.GetOrFail,
        locationsId=args.region, clustersId=args.cluster)
    req = alloydb_messages.AlloydbadminProjectsLocationsClustersPatchRequest(
        name=project_ref.RelativeName())
    op = alloydb_client.projects_locations_clusters.Patch(req)
    if not args.async_:
      cluster_operations.Await(op, 'Updating cluster', False)
    return op

