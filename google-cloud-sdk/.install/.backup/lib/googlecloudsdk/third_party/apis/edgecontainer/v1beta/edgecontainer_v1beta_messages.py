"""Generated message classes for edgecontainer version v1beta.

"""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.protorpclite import messages as _messages
from apitools.base.py import encoding
from apitools.base.py import extra_types


package = 'edgecontainer'


class CancelOperationRequest(_messages.Message):
  r"""The request message for Operations.CancelOperation."""


class Cluster(_messages.Message):
  r"""A Google Edge Cloud Kubernetes cluster.

  Messages:
    LabelsValue: Labels associated with this resource.

  Fields:
    createTime: Output only. The time when the cluster was created.
    defaultMaxPodsPerNode: The default maximum number of pods per node used if
      a maximum value is not specified explicitly for a node pool in this
      cluster. If unspecified, the Kubernetes default value will be used.
    endpoint: Output only. The IP address of the Kubernetes API server.
    hub: Required. GKE Hub configuration.
    labels: Labels associated with this resource.
    name: Required. The resource name of the cluster.
    networking: Required. Cluster-wide networking configuration.
    updateTime: Output only. The time when the cluster was last updated.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class LabelsValue(_messages.Message):
    r"""Labels associated with this resource.

    Messages:
      AdditionalProperty: An additional property for a LabelsValue object.

    Fields:
      additionalProperties: Additional properties of type LabelsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a LabelsValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  createTime = _messages.StringField(1)
  defaultMaxPodsPerNode = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  endpoint = _messages.StringField(3)
  hub = _messages.MessageField('Hub', 4)
  labels = _messages.MessageField('LabelsValue', 5)
  name = _messages.StringField(6)
  networking = _messages.MessageField('ClusterNetworking', 7)
  updateTime = _messages.StringField(8)


class ClusterNetworking(_messages.Message):
  r"""Cluster-wide networking configuration.

  Fields:
    clusterIpv4CidrBlocks: Required. All pods in the cluster are assigned an
      RFC1918 IPv4 address from these blocks. Only a single block is
      supported. This field cannot be changed after creation.
    servicesIpv4CidrBlocks: Required. All services in the cluster are assigned
      an RFC1918 IPv4 address from these blocks. Only a single block is
      supported. This field cannot be changed after creation.
  """

  clusterIpv4CidrBlocks = _messages.StringField(1, repeated=True)
  servicesIpv4CidrBlocks = _messages.StringField(2, repeated=True)


class EdgecontainerProjectsLocationsClustersCreateRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersCreateRequest object.

  Fields:
    cluster: A Cluster resource to be passed as the request body.
    clusterId: Required. A client-specified unique identifier for the cluster.
    parent: Required. The parent location where this cluster will be created.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
  """

  cluster = _messages.MessageField('Cluster', 1)
  clusterId = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)
  requestId = _messages.StringField(4)


class EdgecontainerProjectsLocationsClustersDeleteRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersDeleteRequest object.

  Fields:
    name: Required. The resource name of the cluster.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
  """

  name = _messages.StringField(1, required=True)
  requestId = _messages.StringField(2)


class EdgecontainerProjectsLocationsClustersGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersGetRequest object.

  Fields:
    name: Required. The resource name of the cluster.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsClustersListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersListRequest object.

  Fields:
    filter: Only resources matching this filter will be listed.
    orderBy: Specifies the order in which resources will be listed.
    pageSize: The maximum number of resources to list.
    pageToken: A page token received from previous list request. A page token
      received from previous list request.
    parent: Required. The parent location, which owns this collection of
      clusters.
  """

  filter = _messages.StringField(1)
  orderBy = _messages.StringField(2)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)
  parent = _messages.StringField(5, required=True)


class EdgecontainerProjectsLocationsClustersNodePoolsCreateRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersNodePoolsCreateRequest object.

  Fields:
    nodePool: A NodePool resource to be passed as the request body.
    nodePoolId: Required. A client-specified unique identifier for the node
      pool.
    parent: Required. The parent cluster where this node pool will be created.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
  """

  nodePool = _messages.MessageField('NodePool', 1)
  nodePoolId = _messages.StringField(2)
  parent = _messages.StringField(3, required=True)
  requestId = _messages.StringField(4)


class EdgecontainerProjectsLocationsClustersNodePoolsDeleteRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersNodePoolsDeleteRequest object.

  Fields:
    name: Required. The resource name of the node pool.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
  """

  name = _messages.StringField(1, required=True)
  requestId = _messages.StringField(2)


class EdgecontainerProjectsLocationsClustersNodePoolsGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersNodePoolsGetRequest object.

  Fields:
    name: Required. The resource name of the node pool.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsClustersNodePoolsListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersNodePoolsListRequest object.

  Fields:
    filter: Only resources matching this filter will be listed.
    orderBy: Specifies the order in which resources will be listed.
    pageSize: The maximum number of resources to list.
    pageToken: A page token received from previous list request.
    parent: Required. The parent cluster, which owns this collection of node
      pools.
  """

  filter = _messages.StringField(1)
  orderBy = _messages.StringField(2)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)
  parent = _messages.StringField(5, required=True)


class EdgecontainerProjectsLocationsClustersNodePoolsPatchRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersNodePoolsPatchRequest object.

  Fields:
    name: Required. The resource name of the node pool.
    nodePool: A NodePool resource to be passed as the request body.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
    updateMask: Field mask is used to specify the fields to be overwritten in
      the NodePool resource by the update. The fields specified in the
      update_mask are relative to the resource, not the full request. A field
      will be overwritten if it is in the mask. If the user does not provide a
      mask then all fields will be overwritten.
  """

  name = _messages.StringField(1, required=True)
  nodePool = _messages.MessageField('NodePool', 2)
  requestId = _messages.StringField(3)
  updateMask = _messages.StringField(4)


class EdgecontainerProjectsLocationsClustersPatchRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsClustersPatchRequest object.

  Fields:
    cluster: A Cluster resource to be passed as the request body.
    name: Required. The resource name of the cluster.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
    updateMask: Field mask is used to specify the fields to be overwritten in
      the Cluster resource by the update. The fields specified in the
      update_mask are relative to the resource, not the full request. A field
      will be overwritten if it is in the mask. If the user does not provide a
      mask then all fields will be overwritten.
  """

  cluster = _messages.MessageField('Cluster', 1)
  name = _messages.StringField(2, required=True)
  requestId = _messages.StringField(3)
  updateMask = _messages.StringField(4)


class EdgecontainerProjectsLocationsGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsGetRequest object.

  Fields:
    name: Resource name for the location.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsListRequest object.

  Fields:
    filter: A filter to narrow down results to a preferred subset. The
      filtering language accepts strings like "displayName=tokyo", and is
      documented in more detail in [AIP-160](https://google.aip.dev/160).
    name: The resource that owns the locations collection, if applicable.
    pageSize: The maximum number of results to return. If not set, the service
      selects a default.
    pageToken: A page token received from the `next_page_token` field in the
      response. Send that page token to receive the subsequent page.
  """

  filter = _messages.StringField(1)
  name = _messages.StringField(2, required=True)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)


class EdgecontainerProjectsLocationsMachinesGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsMachinesGetRequest object.

  Fields:
    name: Required. The resource name of the machine.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsMachinesListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsMachinesListRequest object.

  Fields:
    filter: Only resources matching this filter will be listed.
    orderBy: Specifies the order in which resources will be listed.
    pageSize: The maximum number of resources to list.
    pageToken: A page token received from previous list request.
    parent: Required. The parent site, which owns this collection of machines.
  """

  filter = _messages.StringField(1)
  orderBy = _messages.StringField(2)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)
  parent = _messages.StringField(5, required=True)


class EdgecontainerProjectsLocationsOperationsCancelRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsOperationsCancelRequest object.

  Fields:
    cancelOperationRequest: A CancelOperationRequest resource to be passed as
      the request body.
    name: The name of the operation resource to be cancelled.
  """

  cancelOperationRequest = _messages.MessageField('CancelOperationRequest', 1)
  name = _messages.StringField(2, required=True)


class EdgecontainerProjectsLocationsOperationsDeleteRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsOperationsDeleteRequest object.

  Fields:
    name: The name of the operation resource to be deleted.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsOperationsGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsOperationsGetRequest object.

  Fields:
    name: The name of the operation resource.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsOperationsListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsOperationsListRequest object.

  Fields:
    filter: The standard list filter.
    name: The name of the operation's parent resource.
    pageSize: The standard list page size.
    pageToken: The standard list page token.
  """

  filter = _messages.StringField(1)
  name = _messages.StringField(2, required=True)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)


class EdgecontainerProjectsLocationsSitesMachinesGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsSitesMachinesGetRequest object.

  Fields:
    name: Required. The resource name of the machine.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsVpnConnectionsCreateRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsVpnConnectionsCreateRequest object.

  Fields:
    parent: Required. The parent location where this vpn connection will be
      created.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
    vpnConnection: A VpnConnection resource to be passed as the request body.
    vpnConnectionId: Required. The VPN connection identifier.
  """

  parent = _messages.StringField(1, required=True)
  requestId = _messages.StringField(2)
  vpnConnection = _messages.MessageField('VpnConnection', 3)
  vpnConnectionId = _messages.StringField(4)


class EdgecontainerProjectsLocationsVpnConnectionsDeleteRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsVpnConnectionsDeleteRequest object.

  Fields:
    name: Required. The resource name of the vpn connection.
    requestId: A unique identifier for this request. Restricted to 36 ASCII
      characters. A random UUID is recommended. This request is only
      idempotent if `request_id` is provided.
  """

  name = _messages.StringField(1, required=True)
  requestId = _messages.StringField(2)


class EdgecontainerProjectsLocationsVpnConnectionsGetRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsVpnConnectionsGetRequest object.

  Fields:
    name: Required. The resource name of the vpn connection.
  """

  name = _messages.StringField(1, required=True)


class EdgecontainerProjectsLocationsVpnConnectionsListRequest(_messages.Message):
  r"""A EdgecontainerProjectsLocationsVpnConnectionsListRequest object.

  Fields:
    filter: Only resources matching this filter will be listed.
    orderBy: Specifies the order in which resources will be listed.
    pageSize: The maximum number of resources to list.
    pageToken: A page token received from previous list request.
    parent: Required. The parent location, which owns this collection of VPN
      connections.
  """

  filter = _messages.StringField(1)
  orderBy = _messages.StringField(2)
  pageSize = _messages.IntegerField(3, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(4)
  parent = _messages.StringField(5, required=True)


class Empty(_messages.Message):
  r"""A generic empty message that you can re-use to avoid defining duplicated
  empty messages in your APIs. A typical example is to use it as the request
  or the response type of an API method. For instance: service Foo { rpc
  Bar(google.protobuf.Empty) returns (google.protobuf.Empty); } The JSON
  representation for `Empty` is empty JSON object `{}`.
  """



class Hub(_messages.Message):
  r"""GKE Hub configuration.

  Fields:
    membership: Required. The resource name of the membership resource to use
      when registering this cluster to GKE Hub e.g.
      projects/{project}/locations/global/memberships/{membership}.
  """

  membership = _messages.StringField(1)


class ListClustersResponse(_messages.Message):
  r"""List of clusters in a location.

  Fields:
    clusters: Clusters in the location.
    nextPageToken: A token to retrieve next page of results.
    unreachable: Locations that could not be reached.
  """

  clusters = _messages.MessageField('Cluster', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  unreachable = _messages.StringField(3, repeated=True)


class ListLocationsResponse(_messages.Message):
  r"""The response message for Locations.ListLocations.

  Fields:
    locations: A list of locations that matches the specified filter in the
      request.
    nextPageToken: The standard List next-page token.
  """

  locations = _messages.MessageField('Location', 1, repeated=True)
  nextPageToken = _messages.StringField(2)


class ListMachinesResponse(_messages.Message):
  r"""List of machines in a site.

  Fields:
    machines: Machines in the site.
    nextPageToken: A token to retrieve next page of results.
    unreachable: Locations that could not be reached.
  """

  machines = _messages.MessageField('Machine', 1, repeated=True)
  nextPageToken = _messages.StringField(2)
  unreachable = _messages.StringField(3, repeated=True)


class ListNodePoolsResponse(_messages.Message):
  r"""List of node pools in a cluster.

  Fields:
    nextPageToken: A token to retrieve next page of results.
    nodePools: Node pools in the cluster.
    unreachable: Locations that could not be reached.
  """

  nextPageToken = _messages.StringField(1)
  nodePools = _messages.MessageField('NodePool', 2, repeated=True)
  unreachable = _messages.StringField(3, repeated=True)


class ListOperationsResponse(_messages.Message):
  r"""The response message for Operations.ListOperations.

  Fields:
    nextPageToken: The standard List next-page token.
    operations: A list of operations that matches the specified filter in the
      request.
  """

  nextPageToken = _messages.StringField(1)
  operations = _messages.MessageField('Operation', 2, repeated=True)


class ListVpnConnectionsResponse(_messages.Message):
  r"""List of VPN connections in a site.

  Fields:
    nextPageToken: A token to retrieve next page of results.
    unreachable: Locations that could not be reached.
    vpnConnections: VpnConnections in the location.
  """

  nextPageToken = _messages.StringField(1)
  unreachable = _messages.StringField(2, repeated=True)
  vpnConnections = _messages.MessageField('VpnConnection', 3, repeated=True)


class Location(_messages.Message):
  r"""A resource that represents Google Cloud Platform location.

  Messages:
    LabelsValue: Cross-service attributes for the location. For example
      {"cloud.googleapis.com/region": "us-east1"}
    MetadataValue: Service-specific metadata. For example the available
      capacity at the given location.

  Fields:
    displayName: The friendly name for this location, typically a nearby city
      name. For example, "Tokyo".
    labels: Cross-service attributes for the location. For example
      {"cloud.googleapis.com/region": "us-east1"}
    locationId: The canonical id for this location. For example: `"us-east1"`.
    metadata: Service-specific metadata. For example the available capacity at
      the given location.
    name: Resource name for the location, which may vary between
      implementations. For example: `"projects/example-project/locations/us-
      east1"`
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class LabelsValue(_messages.Message):
    r"""Cross-service attributes for the location. For example
    {"cloud.googleapis.com/region": "us-east1"}

    Messages:
      AdditionalProperty: An additional property for a LabelsValue object.

    Fields:
      additionalProperties: Additional properties of type LabelsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a LabelsValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  @encoding.MapUnrecognizedFields('additionalProperties')
  class MetadataValue(_messages.Message):
    r"""Service-specific metadata. For example the available capacity at the
    given location.

    Messages:
      AdditionalProperty: An additional property for a MetadataValue object.

    Fields:
      additionalProperties: Properties of the object. Contains field @type
        with type URL.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a MetadataValue object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  displayName = _messages.StringField(1)
  labels = _messages.MessageField('LabelsValue', 2)
  locationId = _messages.StringField(3)
  metadata = _messages.MessageField('MetadataValue', 4)
  name = _messages.StringField(5)


class Machine(_messages.Message):
  r"""A Google Edge Cloud machine capable of acting as a Kubernetes node.

  Messages:
    LabelsValue: Labels associated with this resource.

  Fields:
    createTime: Output only. The time when the node pool was created.
    hostedNode: Canonical resource name of the node that this machine is
      responsible for hosting e.g. projects/{project}/locations/{location}/clu
      sters/{cluster_id}/nodePools/{pool_id}/{node}, Or empty if the machine
      is not assigned to assume the role of a node.
    labels: Labels associated with this resource.
    location: The Google Edge Cloud location of this machine.
    name: Required. The resource name of the machine.
    updateTime: Output only. The time when the node pool was last updated.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class LabelsValue(_messages.Message):
    r"""Labels associated with this resource.

    Messages:
      AdditionalProperty: An additional property for a LabelsValue object.

    Fields:
      additionalProperties: Additional properties of type LabelsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a LabelsValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  createTime = _messages.StringField(1)
  hostedNode = _messages.StringField(2)
  labels = _messages.MessageField('LabelsValue', 3)
  location = _messages.StringField(4)
  name = _messages.StringField(5)
  updateTime = _messages.StringField(6)


class NodePool(_messages.Message):
  r"""A set of Kubernetes nodes in a cluster with common configuration and
  specification.

  Messages:
    LabelsValue: Labels associated with this resource.

  Fields:
    createTime: Output only. The time when the node pool was created.
    labels: Labels associated with this resource.
    name: Required. The resource name of the node pool.
    nodeCount: Required. The number of nodes in the pool.
    site: Canonical resource name of the site responsible for provisioning
      machines to assume the role of nodes in this node pool e.g.
      projects/{project}/locations/{location}/sites/{site_id}. When a node
      pool is created, the site will be notified, and the site is thereafter
      responsible for ensuring that machines exist to assume the role of the
      node (or reporting that provisioning is not possible).
    updateTime: Output only. The time when the node pool was last updated.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class LabelsValue(_messages.Message):
    r"""Labels associated with this resource.

    Messages:
      AdditionalProperty: An additional property for a LabelsValue object.

    Fields:
      additionalProperties: Additional properties of type LabelsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a LabelsValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  createTime = _messages.StringField(1)
  labels = _messages.MessageField('LabelsValue', 2)
  name = _messages.StringField(3)
  nodeCount = _messages.IntegerField(4, variant=_messages.Variant.INT32)
  site = _messages.StringField(5)
  updateTime = _messages.StringField(6)


class Operation(_messages.Message):
  r"""This resource represents a long-running operation that is the result of
  a network API call.

  Messages:
    MetadataValue: Service-specific metadata associated with the operation. It
      typically contains progress information and common metadata such as
      create time. Some services might not provide such metadata. Any method
      that returns a long-running operation should document the metadata type,
      if any.
    ResponseValue: The normal response of the operation in case of success. If
      the original method returns no data on success, such as `Delete`, the
      response is `google.protobuf.Empty`. If the original method is standard
      `Get`/`Create`/`Update`, the response should be the resource. For other
      methods, the response should have the type `XxxResponse`, where `Xxx` is
      the original method name. For example, if the original method name is
      `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.

  Fields:
    done: If the value is `false`, it means the operation is still in
      progress. If `true`, the operation is completed, and either `error` or
      `response` is available.
    error: The error result of the operation in case of failure or
      cancellation.
    metadata: Service-specific metadata associated with the operation. It
      typically contains progress information and common metadata such as
      create time. Some services might not provide such metadata. Any method
      that returns a long-running operation should document the metadata type,
      if any.
    name: The server-assigned name, which is only unique within the same
      service that originally returns it. If you use the default HTTP mapping,
      the `name` should be a resource name ending with
      `operations/{unique_id}`.
    response: The normal response of the operation in case of success. If the
      original method returns no data on success, such as `Delete`, the
      response is `google.protobuf.Empty`. If the original method is standard
      `Get`/`Create`/`Update`, the response should be the resource. For other
      methods, the response should have the type `XxxResponse`, where `Xxx` is
      the original method name. For example, if the original method name is
      `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class MetadataValue(_messages.Message):
    r"""Service-specific metadata associated with the operation. It typically
    contains progress information and common metadata such as create time.
    Some services might not provide such metadata. Any method that returns a
    long-running operation should document the metadata type, if any.

    Messages:
      AdditionalProperty: An additional property for a MetadataValue object.

    Fields:
      additionalProperties: Properties of the object. Contains field @type
        with type URL.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a MetadataValue object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  @encoding.MapUnrecognizedFields('additionalProperties')
  class ResponseValue(_messages.Message):
    r"""The normal response of the operation in case of success. If the
    original method returns no data on success, such as `Delete`, the response
    is `google.protobuf.Empty`. If the original method is standard
    `Get`/`Create`/`Update`, the response should be the resource. For other
    methods, the response should have the type `XxxResponse`, where `Xxx` is
    the original method name. For example, if the original method name is
    `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.

    Messages:
      AdditionalProperty: An additional property for a ResponseValue object.

    Fields:
      additionalProperties: Properties of the object. Contains field @type
        with type URL.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a ResponseValue object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  done = _messages.BooleanField(1)
  error = _messages.MessageField('Status', 2)
  metadata = _messages.MessageField('MetadataValue', 3)
  name = _messages.StringField(4)
  response = _messages.MessageField('ResponseValue', 5)


class OperationMetadata(_messages.Message):
  r"""Long-running operation metadata for Edge Container API methods.

  Fields:
    apiVersion: API version used to start the operation.
    createTime: The time the operation was created.
    endTime: The time the operation finished running.
    requestedCancellation: Identifies whether the user has requested
      cancellation of the operation. Operations that have successfully been
      cancelled have Operation.error value with a google.rpc.Status.code of 1,
      corresponding to `Code.CANCELLED`.
    statusMessage: Human-readable status of the operation, if any.
    target: Server-defined resource path for the target of the operation.
    verb: The verb executed by the operation.
  """

  apiVersion = _messages.StringField(1)
  createTime = _messages.StringField(2)
  endTime = _messages.StringField(3)
  requestedCancellation = _messages.BooleanField(4)
  statusMessage = _messages.StringField(5)
  target = _messages.StringField(6)
  verb = _messages.StringField(7)


class StandardQueryParameters(_messages.Message):
  r"""Query parameters accepted by all methods.

  Enums:
    FXgafvValueValuesEnum: V1 error format.
    AltValueValuesEnum: Data format for response.

  Fields:
    f__xgafv: V1 error format.
    access_token: OAuth access token.
    alt: Data format for response.
    callback: JSONP
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    uploadType: Legacy upload protocol for media (e.g. "media", "multipart").
    upload_protocol: Upload protocol for media (e.g. "raw", "multipart").
  """

  class AltValueValuesEnum(_messages.Enum):
    r"""Data format for response.

    Values:
      json: Responses with Content-Type of application/json
      media: Media download with context-dependent Content-Type
      proto: Responses with Content-Type of application/x-protobuf
    """
    json = 0
    media = 1
    proto = 2

  class FXgafvValueValuesEnum(_messages.Enum):
    r"""V1 error format.

    Values:
      _1: v1 error format
      _2: v2 error format
    """
    _1 = 0
    _2 = 1

  f__xgafv = _messages.EnumField('FXgafvValueValuesEnum', 1)
  access_token = _messages.StringField(2)
  alt = _messages.EnumField('AltValueValuesEnum', 3, default='json')
  callback = _messages.StringField(4)
  fields = _messages.StringField(5)
  key = _messages.StringField(6)
  oauth_token = _messages.StringField(7)
  prettyPrint = _messages.BooleanField(8, default=True)
  quotaUser = _messages.StringField(9)
  trace = _messages.StringField(10)
  uploadType = _messages.StringField(11)
  upload_protocol = _messages.StringField(12)


class Status(_messages.Message):
  r"""The `Status` type defines a logical error model that is suitable for
  different programming environments, including REST APIs and RPC APIs. It is
  used by [gRPC](https://github.com/grpc). Each `Status` message contains
  three pieces of data: error code, error message, and error details. You can
  find out more about this error model and how to work with it in the [API
  Design Guide](https://cloud.google.com/apis/design/errors).

  Messages:
    DetailsValueListEntry: A DetailsValueListEntry object.

  Fields:
    code: The status code, which should be an enum value of google.rpc.Code.
    details: A list of messages that carry the error details. There is a
      common set of message types for APIs to use.
    message: A developer-facing error message, which should be in English. Any
      user-facing error message should be localized and sent in the
      google.rpc.Status.details field, or localized by the client.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class DetailsValueListEntry(_messages.Message):
    r"""A DetailsValueListEntry object.

    Messages:
      AdditionalProperty: An additional property for a DetailsValueListEntry
        object.

    Fields:
      additionalProperties: Properties of the object. Contains field @type
        with type URL.
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a DetailsValueListEntry object.

      Fields:
        key: Name of the additional property.
        value: A extra_types.JsonValue attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('extra_types.JsonValue', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  code = _messages.IntegerField(1, variant=_messages.Variant.INT32)
  details = _messages.MessageField('DetailsValueListEntry', 2, repeated=True)
  message = _messages.StringField(3)


class VpnConnection(_messages.Message):
  r"""A VPN connection .

  Enums:
    BgpRoutingModeValueValuesEnum: Dynamic routing mode of the VPC network,
      `regional` or `global`.

  Messages:
    LabelsValue: Labels associated with this resource.

  Fields:
    bgpRoutingMode: Dynamic routing mode of the VPC network, `regional` or
      `global`.
    cluster: The canonical Cluster name to connect to. It is in the form of
      projects/{project}/locations/{location}/clusters/{cluster}.
    createTime: Output only. The time when the VPN connection was created.
    labels: Labels associated with this resource.
    name: Required. The resource name of VPN connection
    natGatewayIp: NAT gateway IP, or WAN IP address. If a customer has
      multiple NAT IPs, the customer needs to configure NAT such that only one
      external IP maps to the GMEC Anthos cluster. This is empty if NAT is not
      used.
    updateTime: Output only. The time when the VPN connection was last
      updated.
    vpc: The canonical VPC name to connect to. It is in the form of
      projects/{project}/global/networks/{network}.
  """

  class BgpRoutingModeValueValuesEnum(_messages.Enum):
    r"""Dynamic routing mode of the VPC network, `regional` or `global`.

    Values:
      BGP_ROUTING_MODE_UNSPECIFIED: Unknown.
      REGIONAL: Regional mode.
      GLOBAL: Global mode.
    """
    BGP_ROUTING_MODE_UNSPECIFIED = 0
    REGIONAL = 1
    GLOBAL = 2

  @encoding.MapUnrecognizedFields('additionalProperties')
  class LabelsValue(_messages.Message):
    r"""Labels associated with this resource.

    Messages:
      AdditionalProperty: An additional property for a LabelsValue object.

    Fields:
      additionalProperties: Additional properties of type LabelsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a LabelsValue object.

      Fields:
        key: Name of the additional property.
        value: A string attribute.
      """

      key = _messages.StringField(1)
      value = _messages.StringField(2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  bgpRoutingMode = _messages.EnumField('BgpRoutingModeValueValuesEnum', 1)
  cluster = _messages.StringField(2)
  createTime = _messages.StringField(3)
  labels = _messages.MessageField('LabelsValue', 4)
  name = _messages.StringField(5)
  natGatewayIp = _messages.StringField(6)
  updateTime = _messages.StringField(7)
  vpc = _messages.StringField(8)


encoding.AddCustomJsonFieldMapping(
    StandardQueryParameters, 'f__xgafv', '$.xgafv')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_1', '1')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_2', '2')
