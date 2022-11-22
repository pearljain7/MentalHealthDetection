"""Generated client library for policytroubleshooter version v1beta."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.policytroubleshooter.v1beta import policytroubleshooter_v1beta_messages as messages


class PolicytroubleshooterV1beta(base_api.BaseApiClient):
  """Generated client library for service policytroubleshooter version v1beta."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://policytroubleshooter.googleapis.com/'
  MTLS_BASE_URL = 'https://policytroubleshooter.mtls.googleapis.com/'

  _PACKAGE = 'policytroubleshooter'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
  _VERSION = 'v1beta'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'PolicytroubleshooterV1beta'
  _URL_VERSION = 'v1beta'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new policytroubleshooter handle."""
    url = url or self.BASE_URL
    super(PolicytroubleshooterV1beta, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.iam = self.IamService(self)

  class IamService(base_api.BaseApiService):
    """Service class for the iam resource."""

    _NAME = 'iam'

    def __init__(self, client):
      super(PolicytroubleshooterV1beta.IamService, self).__init__(client)
      self._upload_configs = {
          }

    def Troubleshoot(self, request, global_params=None):
      r"""Checks whether a member has a specific permission for a specific resource, and explains why the member does or does not have that permission.

      Args:
        request: (GoogleCloudPolicytroubleshooterV1betaTroubleshootIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GoogleCloudPolicytroubleshooterV1betaTroubleshootIamPolicyResponse) The response message.
      """
      config = self.GetMethodConfig('Troubleshoot')
      return self._RunMethod(
          config, request, global_params=global_params)

    Troubleshoot.method_config = lambda: base_api.ApiMethodInfo(
        http_method='POST',
        method_id='policytroubleshooter.iam.troubleshoot',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path='v1beta/iam:troubleshoot',
        request_field='<request>',
        request_type_name='GoogleCloudPolicytroubleshooterV1betaTroubleshootIamPolicyRequest',
        response_type_name='GoogleCloudPolicytroubleshooterV1betaTroubleshootIamPolicyResponse',
        supports_download=False,
    )
