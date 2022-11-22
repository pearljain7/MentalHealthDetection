"""Generated message classes for accessapproval version v1.

An API for controlling access to data by Google personnel.
"""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.protorpclite import messages as _messages
from apitools.base.py import encoding


package = 'accessapproval'


class AccessApprovalSettings(_messages.Message):
  r"""Settings on a Project/Folder/Organization related to Access Approval.

  Fields:
    enrolledAncestor: Output only. This field is read only (not settable via
      UpdateAccessAccessApprovalSettings method). If the field is true, that
      indicates that at least one service is enrolled for Access Approval in
      one or more ancestors of the Project or Folder (this field will always
      be unset for the organization since organizations do not have
      ancestors).
    enrolledServices: A list of Google Cloud Services for which the given
      resource has Access Approval enrolled. Access requests for the resource
      given by name against any of these services contained here will be
      required to have explicit approval. If name refers to an organization,
      enrollment can be done for individual services. If name refers to a
      folder or project, enrollment can only be done on an all or nothing
      basis. If a cloud_product is repeated in this list, the first entry will
      be honored and all following entries will be discarded. A maximum of 10
      enrolled services will be enforced, to be expanded as the set of
      supported services is expanded.
    name: The resource name of the settings. Format is one of: *
      "projects/{project}/accessApprovalSettings" *
      "folders/{folder}/accessApprovalSettings" *
      "organizations/{organization}/accessApprovalSettings"
    notificationEmails: A list of email addresses to which notifications
      relating to approval requests should be sent. Notifications relating to
      a resource will be sent to all emails in the settings of ancestor
      resources of that resource. A maximum of 50 email addresses are allowed.
  """

  enrolledAncestor = _messages.BooleanField(1)
  enrolledServices = _messages.MessageField('EnrolledService', 2, repeated=True)
  name = _messages.StringField(3)
  notificationEmails = _messages.StringField(4, repeated=True)


class AccessLocations(_messages.Message):
  r"""Home office and physical location of the principal.

  Fields:
    principalOfficeCountry: The "home office" location of the principal. A
      two-letter country code (ISO 3166-1 alpha-2), such as "US", "DE" or "GB"
      or a region code. In some limited situations Google systems may refer
      refer to a region code instead of a country code. Possible Region Codes:
      * ASI: Asia * EUR: Europe * OCE: Oceania * AFR: Africa * NAM: North
      America * SAM: South America * ANT: Antarctica * ANY: Any location
    principalPhysicalLocationCountry: Physical location of the principal at
      the time of the access. A two-letter country code (ISO 3166-1 alpha-2),
      such as "US", "DE" or "GB" or a region code. In some limited situations
      Google systems may refer refer to a region code instead of a country
      code. Possible Region Codes: * ASI: Asia * EUR: Europe * OCE: Oceania *
      AFR: Africa * NAM: North America * SAM: South America * ANT: Antarctica
      * ANY: Any location
  """

  principalOfficeCountry = _messages.StringField(1)
  principalPhysicalLocationCountry = _messages.StringField(2)


class AccessReason(_messages.Message):
  r"""A AccessReason object.

  Enums:
    TypeValueValuesEnum: Type of access justification.

  Fields:
    detail: More detail about certain reason types. See comments for each type
      above.
    type: Type of access justification.
  """

  class TypeValueValuesEnum(_messages.Enum):
    r"""Type of access justification.

    Values:
      TYPE_UNSPECIFIED: Default value for proto, shouldn't be used.
      CUSTOMER_INITIATED_SUPPORT: Customer made a request or raised an issue
        that required the principal to access customer data. `detail` is of
        the form ("#####" is the issue ID): * "Feedback Report: #####" * "Case
        Number: #####" * "Case ID: #####" * "E-PIN Reference: #####" *
        "Google-#####" * "T-#####"
      GOOGLE_INITIATED_SERVICE: The principal accessed customer data in order
        to diagnose or resolve a suspected issue in services or a known
        outage. Often this access is used to confirm that customers are not
        affected by a suspected service issue or to remediate a reversible
        system issue.
      GOOGLE_INITIATED_REVIEW: Google initiated service for security, fraud,
        abuse, or compliance purposes.
    """
    TYPE_UNSPECIFIED = 0
    CUSTOMER_INITIATED_SUPPORT = 1
    GOOGLE_INITIATED_SERVICE = 2
    GOOGLE_INITIATED_REVIEW = 3

  detail = _messages.StringField(1)
  type = _messages.EnumField('TypeValueValuesEnum', 2)


class AccessapprovalFoldersApprovalRequestsApproveRequest(_messages.Message):
  r"""A AccessapprovalFoldersApprovalRequestsApproveRequest object.

  Fields:
    approveApprovalRequestMessage: A ApproveApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the approval request to approve.
  """

  approveApprovalRequestMessage = _messages.MessageField('ApproveApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalFoldersApprovalRequestsDismissRequest(_messages.Message):
  r"""A AccessapprovalFoldersApprovalRequestsDismissRequest object.

  Fields:
    dismissApprovalRequestMessage: A DismissApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the ApprovalRequest to dismiss.
  """

  dismissApprovalRequestMessage = _messages.MessageField('DismissApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalFoldersApprovalRequestsGetRequest(_messages.Message):
  r"""A AccessapprovalFoldersApprovalRequestsGetRequest object.

  Fields:
    name: Name of the approval request to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalFoldersApprovalRequestsListRequest(_messages.Message):
  r"""A AccessapprovalFoldersApprovalRequestsListRequest object.

  Fields:
    filter: A filter on the type of approval requests to retrieve. Must be one
      of the following values: * [not set]: Requests that are pending or have
      active approvals. * ALL: All requests. * PENDING: Only pending requests.
      * ACTIVE: Only active (i.e. currently approved) requests. * DISMISSED:
      Only requests that have been dismissed, or requests that are not
      approved and past expiration. * EXPIRED: Only requests that have been
      approved, and the approval has expired. * HISTORY: Active, dismissed and
      expired requests.
    pageSize: Requested page size.
    pageToken: A token identifying the page of results to return.
    parent: The parent resource. This may be "projects/{project}",
      "folders/{folder}", or "organizations/{organization}".
  """

  filter = _messages.StringField(1)
  pageSize = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(3)
  parent = _messages.StringField(4, required=True)


class AccessapprovalFoldersDeleteAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalFoldersDeleteAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to delete.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalFoldersGetAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalFoldersGetAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalFoldersUpdateAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalFoldersUpdateAccessApprovalSettingsRequest object.

  Fields:
    accessApprovalSettings: A AccessApprovalSettings resource to be passed as
      the request body.
    name: The resource name of the settings. Format is one of: *
      "projects/{project}/accessApprovalSettings" *
      "folders/{folder}/accessApprovalSettings" *
      "organizations/{organization}/accessApprovalSettings"
    updateMask: The update mask applies to the settings. Only the top level
      fields of AccessApprovalSettings (notification_emails &
      enrolled_services) are supported. For each field, if it is included, the
      currently stored value will be entirely overwritten with the value of
      the field passed in this request. For the `FieldMask` definition, see
      https://developers.google.com/protocol-
      buffers/docs/reference/google.protobuf#fieldmask If this field is left
      unset, only the notification_emails field will be updated.
  """

  accessApprovalSettings = _messages.MessageField('AccessApprovalSettings', 1)
  name = _messages.StringField(2, required=True)
  updateMask = _messages.StringField(3)


class AccessapprovalOrganizationsApprovalRequestsApproveRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsApprovalRequestsApproveRequest object.

  Fields:
    approveApprovalRequestMessage: A ApproveApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the approval request to approve.
  """

  approveApprovalRequestMessage = _messages.MessageField('ApproveApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalOrganizationsApprovalRequestsDismissRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsApprovalRequestsDismissRequest object.

  Fields:
    dismissApprovalRequestMessage: A DismissApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the ApprovalRequest to dismiss.
  """

  dismissApprovalRequestMessage = _messages.MessageField('DismissApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalOrganizationsApprovalRequestsGetRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsApprovalRequestsGetRequest object.

  Fields:
    name: Name of the approval request to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalOrganizationsApprovalRequestsListRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsApprovalRequestsListRequest object.

  Fields:
    filter: A filter on the type of approval requests to retrieve. Must be one
      of the following values: * [not set]: Requests that are pending or have
      active approvals. * ALL: All requests. * PENDING: Only pending requests.
      * ACTIVE: Only active (i.e. currently approved) requests. * DISMISSED:
      Only requests that have been dismissed, or requests that are not
      approved and past expiration. * EXPIRED: Only requests that have been
      approved, and the approval has expired. * HISTORY: Active, dismissed and
      expired requests.
    pageSize: Requested page size.
    pageToken: A token identifying the page of results to return.
    parent: The parent resource. This may be "projects/{project}",
      "folders/{folder}", or "organizations/{organization}".
  """

  filter = _messages.StringField(1)
  pageSize = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(3)
  parent = _messages.StringField(4, required=True)


class AccessapprovalOrganizationsDeleteAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsDeleteAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to delete.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalOrganizationsGetAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsGetAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalOrganizationsUpdateAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalOrganizationsUpdateAccessApprovalSettingsRequest object.

  Fields:
    accessApprovalSettings: A AccessApprovalSettings resource to be passed as
      the request body.
    name: The resource name of the settings. Format is one of: *
      "projects/{project}/accessApprovalSettings" *
      "folders/{folder}/accessApprovalSettings" *
      "organizations/{organization}/accessApprovalSettings"
    updateMask: The update mask applies to the settings. Only the top level
      fields of AccessApprovalSettings (notification_emails &
      enrolled_services) are supported. For each field, if it is included, the
      currently stored value will be entirely overwritten with the value of
      the field passed in this request. For the `FieldMask` definition, see
      https://developers.google.com/protocol-
      buffers/docs/reference/google.protobuf#fieldmask If this field is left
      unset, only the notification_emails field will be updated.
  """

  accessApprovalSettings = _messages.MessageField('AccessApprovalSettings', 1)
  name = _messages.StringField(2, required=True)
  updateMask = _messages.StringField(3)


class AccessapprovalProjectsApprovalRequestsApproveRequest(_messages.Message):
  r"""A AccessapprovalProjectsApprovalRequestsApproveRequest object.

  Fields:
    approveApprovalRequestMessage: A ApproveApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the approval request to approve.
  """

  approveApprovalRequestMessage = _messages.MessageField('ApproveApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalProjectsApprovalRequestsDismissRequest(_messages.Message):
  r"""A AccessapprovalProjectsApprovalRequestsDismissRequest object.

  Fields:
    dismissApprovalRequestMessage: A DismissApprovalRequestMessage resource to
      be passed as the request body.
    name: Name of the ApprovalRequest to dismiss.
  """

  dismissApprovalRequestMessage = _messages.MessageField('DismissApprovalRequestMessage', 1)
  name = _messages.StringField(2, required=True)


class AccessapprovalProjectsApprovalRequestsGetRequest(_messages.Message):
  r"""A AccessapprovalProjectsApprovalRequestsGetRequest object.

  Fields:
    name: Name of the approval request to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalProjectsApprovalRequestsListRequest(_messages.Message):
  r"""A AccessapprovalProjectsApprovalRequestsListRequest object.

  Fields:
    filter: A filter on the type of approval requests to retrieve. Must be one
      of the following values: * [not set]: Requests that are pending or have
      active approvals. * ALL: All requests. * PENDING: Only pending requests.
      * ACTIVE: Only active (i.e. currently approved) requests. * DISMISSED:
      Only requests that have been dismissed, or requests that are not
      approved and past expiration. * EXPIRED: Only requests that have been
      approved, and the approval has expired. * HISTORY: Active, dismissed and
      expired requests.
    pageSize: Requested page size.
    pageToken: A token identifying the page of results to return.
    parent: The parent resource. This may be "projects/{project}",
      "folders/{folder}", or "organizations/{organization}".
  """

  filter = _messages.StringField(1)
  pageSize = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(3)
  parent = _messages.StringField(4, required=True)


class AccessapprovalProjectsDeleteAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalProjectsDeleteAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to delete.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalProjectsGetAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalProjectsGetAccessApprovalSettingsRequest object.

  Fields:
    name: Name of the AccessApprovalSettings to retrieve.
  """

  name = _messages.StringField(1, required=True)


class AccessapprovalProjectsUpdateAccessApprovalSettingsRequest(_messages.Message):
  r"""A AccessapprovalProjectsUpdateAccessApprovalSettingsRequest object.

  Fields:
    accessApprovalSettings: A AccessApprovalSettings resource to be passed as
      the request body.
    name: The resource name of the settings. Format is one of: *
      "projects/{project}/accessApprovalSettings" *
      "folders/{folder}/accessApprovalSettings" *
      "organizations/{organization}/accessApprovalSettings"
    updateMask: The update mask applies to the settings. Only the top level
      fields of AccessApprovalSettings (notification_emails &
      enrolled_services) are supported. For each field, if it is included, the
      currently stored value will be entirely overwritten with the value of
      the field passed in this request. For the `FieldMask` definition, see
      https://developers.google.com/protocol-
      buffers/docs/reference/google.protobuf#fieldmask If this field is left
      unset, only the notification_emails field will be updated.
  """

  accessApprovalSettings = _messages.MessageField('AccessApprovalSettings', 1)
  name = _messages.StringField(2, required=True)
  updateMask = _messages.StringField(3)


class ApprovalRequest(_messages.Message):
  r"""A request for the customer to approve access to a resource.

  Fields:
    approve: Access was approved.
    dismiss: The request was dismissed.
    name: The resource name of the request. Format is "{projects|folders|organ
      izations}/{id}/approvalRequests/{approval_request}".
    requestTime: The time at which approval was requested.
    requestedExpiration: The requested expiration for the approval. If the
      request is approved, access will be granted from the time of approval
      until the expiration time.
    requestedLocations: The locations for which approval is being requested.
    requestedReason: The justification for which approval is being requested.
    requestedResourceName: The resource for which approval is being requested.
      The format of the resource name is defined at
      https://cloud.google.com/apis/design/resource_names. The resource name
      here may either be a "full" resource name (e.g.
      "//library.googleapis.com/shelves/shelf1/books/book2") or a "relative"
      resource name (e.g. "shelves/shelf1/books/book2") as described in the
      resource name specification.
    requestedResourceProperties: Properties related to the resource
      represented by requested_resource_name.
  """

  approve = _messages.MessageField('ApproveDecision', 1)
  dismiss = _messages.MessageField('DismissDecision', 2)
  name = _messages.StringField(3)
  requestTime = _messages.StringField(4)
  requestedExpiration = _messages.StringField(5)
  requestedLocations = _messages.MessageField('AccessLocations', 6)
  requestedReason = _messages.MessageField('AccessReason', 7)
  requestedResourceName = _messages.StringField(8)
  requestedResourceProperties = _messages.MessageField('ResourceProperties', 9)


class ApproveApprovalRequestMessage(_messages.Message):
  r"""Request to approve an ApprovalRequest.

  Fields:
    expireTime: The expiration time of this approval.
  """

  expireTime = _messages.StringField(1)


class ApproveDecision(_messages.Message):
  r"""A decision that has been made to approve access to a resource.

  Fields:
    approveTime: The time at which approval was granted.
    expireTime: The time at which the approval expires.
  """

  approveTime = _messages.StringField(1)
  expireTime = _messages.StringField(2)


class DismissApprovalRequestMessage(_messages.Message):
  r"""Request to dismiss an approval request."""


class DismissDecision(_messages.Message):
  r"""A decision that has been made to dismiss an approval request.

  Fields:
    dismissTime: The time at which the approval request was dismissed.
    implicit: This field will be true if the ApprovalRequest was implcitly
      dismissed due to inaction by the access approval approvers (the request
      is not acted on by the approvers before the exiration time).
  """

  dismissTime = _messages.StringField(1)
  implicit = _messages.BooleanField(2)


class Empty(_messages.Message):
  r"""A generic empty message that you can re-use to avoid defining duplicated
  empty messages in your APIs. A typical example is to use it as the request
  or the response type of an API method. For instance: service Foo { rpc
  Bar(google.protobuf.Empty) returns (google.protobuf.Empty); } The JSON
  representation for `Empty` is empty JSON object `{}`.
  """



class EnrolledService(_messages.Message):
  r"""Represents the enrollment of a cloud resource into a specific service.

  Enums:
    EnrollmentLevelValueValuesEnum: The enrollment level of the service.

  Fields:
    cloudProduct: The product for which Access Approval will be enrolled.
      Allowed values are listed below (case-sensitive): * all * App Engine *
      BigQuery * Cloud Bigtable * Cloud Key Management Service * Compute
      Engine * Cloud Dataflow * Cloud Identity and Access Management * Cloud
      Logging * Cloud Pub/Sub * Cloud Spanner * Cloud Storage * Google
      Kubernetes Engine * Persistent Disk Note: These values are supported as
      input for legacy purposes, but will not be returned from the API. * all
      * appengine.googleapis.com * bigquery.googleapis.com *
      bigtable.googleapis.com * container.googleapis.com *
      cloudkms.googleapis.com * compute.googleapis.com *
      dataflow.googleapis.com * iam.googleapis.com * logging.googleapis.com *
      pubsub.googleapis.com * spanner.googleapis.com * storage.googleapis.com
      Calls to UpdateAccessApprovalSettings using 'all' or any of the
      XXX.googleapis.com will be translated to the associated product name
      ('all', 'App Engine', etc.). Note: 'all' will enroll the resource in all
      products supported at both 'GA' and 'Preview' levels. More information
      about levels of support is available at https://cloud.google.com/access-
      approval/docs/supported-services
    enrollmentLevel: The enrollment level of the service.
  """

  class EnrollmentLevelValueValuesEnum(_messages.Enum):
    r"""The enrollment level of the service.

    Values:
      ENROLLMENT_LEVEL_UNSPECIFIED: Default value for proto, shouldn't be
        used.
      BLOCK_ALL: Service is enrolled in Access Approval for all requests
    """
    ENROLLMENT_LEVEL_UNSPECIFIED = 0
    BLOCK_ALL = 1

  cloudProduct = _messages.StringField(1)
  enrollmentLevel = _messages.EnumField('EnrollmentLevelValueValuesEnum', 2)


class ListApprovalRequestsResponse(_messages.Message):
  r"""Response to listing of ApprovalRequest objects.

  Fields:
    approvalRequests: Approval request details.
    nextPageToken: Token to retrieve the next page of results, or empty if
      there are no more.
  """

  approvalRequests = _messages.MessageField('ApprovalRequest', 1, repeated=True)
  nextPageToken = _messages.StringField(2)


class ResourceProperties(_messages.Message):
  r"""The properties associated with the resource of the request.

  Fields:
    excludesDescendants: Whether an approval will exclude the descendants of
      the resource being requested.
  """

  excludesDescendants = _messages.BooleanField(1)


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


encoding.AddCustomJsonFieldMapping(
    StandardQueryParameters, 'f__xgafv', '$.xgafv')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_1', '1')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_2', '2')
