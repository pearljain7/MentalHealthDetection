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
"""Command to create a new GKE cluster on Azure."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.azure import util as azure_api_util
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import actions
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.container.azure import resource_args
from googlecloudsdk.command_lib.container.azure import util as command_util
from googlecloudsdk.command_lib.container.gkemulticloud import endpoint_util
from googlecloudsdk.command_lib.container.gkemulticloud import flags
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import log
from googlecloudsdk.core import properties


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Create(base.CreateCommand):
  """Create a GKE cluster on Azure."""

  @staticmethod
  def Args(parser):
    arg_parser = concept_parsers.ConceptParser(
        [
            presentation_specs.ResourcePresentationSpec(
                "cluster",
                resource_args.GetAzureClusterResourceSpec(),
                "Azure cluster to create.",
                required=True),
            presentation_specs.ResourcePresentationSpec(
                "--client",
                resource_args.GetAzureClientResourceSpec(),
                "Azure client to use for cluster creation.",
                required=True,
                flag_name_overrides={"region": ""})
        ],
        command_level_fallthroughs={"--client.region": ["cluster.region"]})
    arg_parser.AddToParser(parser)

    parser.add_argument(
        "--azure-region",
        action=actions.StoreProperty(properties.VALUES.azure.azure_region),
        required=True,
        help=("Azure location to deploy the cluster. "
              "Refer to your Azure subscription for available locations."))
    parser.add_argument(
        "--resource-group-id",
        required=True,
        help=("ID of the Azure Resource Group "
              "to associate the cluster with."))
    parser.add_argument(
        "--vnet-id",
        required=True,
        help=("ID of the Azure Virtual Network "
              "to associate with the cluster."))
    parser.add_argument(
        "--cluster-ipv4-cidr",
        required=True,
        help=("IP address range for the pods in this cluster in CIDR "
              "notation (e.g. 10.0.0.0/8). Can be any RFC 1918 IP range."))
    parser.add_argument(
        "--service-ipv4-cidr",
        required=True,
        help=("IP address range for the services IPs in CIDR notation "
              "(e.g. 10.0.0.0/8). Can be any RFC 1918 IP range."))
    flags.AddClusterVersion(parser)
    flags.AddSubnetID(parser, "the cluster control plane")
    flags.AddVMSize(parser)
    flags.AddSSHPublicKey(parser)
    flags.AddRootVolumeSize(parser, required=True)
    flags.AddMainVolumeSize(parser, required=True)
    flags.AddTags(parser)
    flags.AddValidateOnly(parser, "creation of the cluster")
    base.ASYNC_FLAG.AddToParser(parser)
    parser.display_info.AddFormat(command_util.CLUSTERS_FORMAT)

  def Run(self, args):
    """Run the create command."""

    cluster_ref = resource_args.ParseAzureClusterResourceArg(args)
    client_ref = resource_args.ParseAzureClientResourceArg(args)

    azure_region = getattr(args, "azure_region", None)
    if not azure_region:
      try:
        azure_region = properties.VALUES.azure.azure_region.GetOrFail()
      except properties.RequiredPropertyError:
        raise exceptions.RequiredArgumentException("--azure-region",
                                                   "Must be specified.")

    resource_group_id = args.resource_group_id
    vnet_id = args.vnet_id
    cluster_ipv4_cidr = args.cluster_ipv4_cidr
    service_ipv4_cidr = args.service_ipv4_cidr
    cluster_version = flags.GetClusterVersion(args)
    subnet_id = flags.GetSubnetID(args)
    vm_size = flags.GetVMSize(args)
    ssh_public_key = flags.GetSSHPublicKey(args)
    root_volume_size = flags.GetRootVolumeSize(args)
    main_volume_size = flags.GetMainVolumeSize(args)
    validate_only = flags.GetValidateOnly(args)
    tags = flags.GetTags(args)
    admin_users = [properties.VALUES.core.account.Get()]
    async_ = getattr(args, "async_", False)

    with endpoint_util.GkemulticloudEndpointOverride(cluster_ref.locationsId,
                                                     self.ReleaseTrack()):
      cluster_client = azure_api_util.ClustersClient(track=self.ReleaseTrack())
      op = cluster_client.Create(
          cluster_ref=cluster_ref,
          client_ref=client_ref,
          azure_region=azure_region,
          resource_group_id=resource_group_id,
          vnet_id=vnet_id,
          cluster_ipv4_cidr=cluster_ipv4_cidr,
          service_ipv4_cidr=service_ipv4_cidr,
          cluster_version=cluster_version,
          subnet_id=subnet_id,
          vm_size=vm_size,
          ssh_public_key=ssh_public_key,
          root_volume_size=root_volume_size,
          main_volume_size=main_volume_size,
          validate_only=validate_only,
          tags=tags,
          admin_users=admin_users)

      op_ref = resource_args.GetOperationResource(op)

      if validate_only:
        args.format = "disable"
        return

      if not async_:
        waiter.WaitFor(
            waiter.CloudOperationPollerNoResources(
                cluster_client.client.projects_locations_operations), op_ref,
            "Creating cluster {} in Azure region {}".format(
                cluster_ref.azureClustersId, azure_region))

      log.CreatedResource(cluster_ref)
      return cluster_client.Get(cluster_ref)
