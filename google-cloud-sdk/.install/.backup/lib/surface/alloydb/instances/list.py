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
"""Lists AlloyDB instances in a given cluster."""


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


from apitools.base.py import list_pager
from googlecloudsdk.api_lib.alloydb import api_util
from googlecloudsdk.calliope import base
from googlecloudsdk.core import properties

_INSTANCE_FORMAT = """
    table(
        name,
        tier,
        instanceType:label="INSTANCE_TYPE",
        state:label=STATUS
    )
"""


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class List(base.ListCommand):
  """Lists AlloyDB instances in a given cluster."""

  @staticmethod
  def Args(parser):
    """Specifies additional command flags.

    --cluster: An optional flag that, if specified, will only list instances
        within that given cluster.

    --region: A flag that must specify the region of the cluster, if --cluster
        is specified.

    Args:
      parser: argparse.Parser: Parser object for command line inputs
    """
    cluster_args = parser.add_argument_group(help='Cluster')
    cluster_args.add_argument(
        '--region',
        required=True,
        default='-',
        help=('Regional location (e.g. asia-east1, us-east1) of CLUSTER. '
              'See the full list of regions at '
              'https://cloud.google.com/sql/docs/instance-locations. '
              'Default: list clusters in all regions.'))
    cluster_args.add_argument(
        '--cluster',
        required=True,
        default='-',
        help=('AlloyDB cluster ID'))
    parser.display_info.AddFormat(_INSTANCE_FORMAT)

  def Run(self, args):
    """Entry point for command.

    Args:
      args: argparse.Namespace, An object that contains the values for the
          arguments specified in the .Args() method.

    Returns:
      A resource object dispatched by display.Displayer().

    Raises:
      InvalidArgumentException: An error if either --cluster or --region is
          is specified but not both.
    """
    client = api_util.AlloyDBClient(api_util.API_VERSION_DEFAULT)
    alloydb_client = client.alloydb_client
    alloydb_messages = client.alloydb_messages
    project_ref = client.resource_parser.Create(
        'alloydbadmin.projects.locations.clusters',
        projectsId=properties.VALUES.core.project.GetOrFail,
        locationsId=args.region,
        clustersId=args.cluster)

    result = list_pager.YieldFromList(
        alloydb_client.projects_locations_clusters_instances,
        alloydb_messages
        .AlloydbadminProjectsLocationsClustersInstancesListRequest(
            parent=project_ref.RelativeName()),
        field='instances',
        limit=args.limit,
        batch_size=args.page_size,
        batch_size_attribute='pageSize')

    return result
