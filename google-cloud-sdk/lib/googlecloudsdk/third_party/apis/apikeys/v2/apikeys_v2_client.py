"""Generated client library for apikeys version v2."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.apikeys.v2 import apikeys_v2_messages as messages


class ApikeysV2(base_api.BaseApiClient):
  """Generated client library for service apikeys version v2."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://apikeys.googleapis.com/'
  MTLS_BASE_URL = 'https://apikeys.mtls.googleapis.com/'

  _PACKAGE = 'apikeys'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/cloud-platform.read-only']
  _VERSION = 'v2'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'ApikeysV2'
  _URL_VERSION = 'v2'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new apikeys handle."""
    url = url or self.BASE_URL
    super(ApikeysV2, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.keys = self.KeysService(self)
    self.operations = self.OperationsService(self)
    self.projects_locations_keys = self.ProjectsLocationsKeysService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class KeysService(base_api.BaseApiService):
    """Service class for the keys resource."""

    _NAME = 'keys'

    def __init__(self, client):
      super(ApikeysV2.KeysService, self).__init__(client)
      self._upload_configs = {
          }

    def LookupKey(self, request, global_params=None):
      r"""Find the parent project and resource name of the API key that matches the key string in the request. If the API key has been purged, resource name will not be set. The service account must have the `apikeys.keys.lookup` permission on the parent project.

      Args:
        request: (ApikeysKeysLookupKeyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (V2LookupKeyResponse) The response message.
      """
      config = self.GetMethodConfig('LookupKey')
      return self._RunMethod(
          config, request, global_params=global_params)

    LookupKey.method_config = lambda: base_api.ApiMethodInfo(
        http_method='GET',
        method_id='apikeys.keys.lookupKey',
        ordered_params=[],
        path_params=[],
        query_params=['keyString'],
        relative_path='v2/keys:lookupKey',
        request_field='',
        request_type_name='ApikeysKeysLookupKeyRequest',
        response_type_name='V2LookupKeyResponse',
        supports_download=False,
    )

  class OperationsService(base_api.BaseApiService):
    """Service class for the operations resource."""

    _NAME = 'operations'

    def __init__(self, client):
      super(ApikeysV2.OperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (ApikeysOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/operations/{operationsId}',
        http_method='GET',
        method_id='apikeys.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v2/{+name}',
        request_field='',
        request_type_name='ApikeysOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class ProjectsLocationsKeysService(base_api.BaseApiService):
    """Service class for the projects_locations_keys resource."""

    _NAME = 'projects_locations_keys'

    def __init__(self, client):
      super(ApikeysV2.ProjectsLocationsKeysService, self).__init__(client)
      self._upload_configs = {
          }

    def Clone(self, request, global_params=None):
      r"""Clones the existing key's restriction and display name to a new API key. The service account must have the `apikeys.keys.get` and `apikeys.keys.create` permissions in the project. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysCloneRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Clone')
      return self._RunMethod(
          config, request, global_params=global_params)

    Clone.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}:clone',
        http_method='POST',
        method_id='apikeys.projects.locations.keys.clone',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v2/{+name}:clone',
        request_field='v2CloneKeyRequest',
        request_type_name='ApikeysProjectsLocationsKeysCloneRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Create(self, request, global_params=None):
      r"""Creates a new API key. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys',
        http_method='POST',
        method_id='apikeys.projects.locations.keys.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['keyId'],
        relative_path='v2/{+parent}/keys',
        request_field='v2Key',
        request_type_name='ApikeysProjectsLocationsKeysCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes an API key. Deleted key can be retrieved within 30 days of deletion. Afterward, key will be purged from the project. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}',
        http_method='DELETE',
        method_id='apikeys.projects.locations.keys.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['etag'],
        relative_path='v2/{+name}',
        request_field='',
        request_type_name='ApikeysProjectsLocationsKeysDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the metadata for an API key. The key string of the API key isn't included in the response. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (V2Key) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}',
        http_method='GET',
        method_id='apikeys.projects.locations.keys.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v2/{+name}',
        request_field='',
        request_type_name='ApikeysProjectsLocationsKeysGetRequest',
        response_type_name='V2Key',
        supports_download=False,
    )

    def GetKeyString(self, request, global_params=None):
      r"""Get the key string for an API key. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysGetKeyStringRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (V2GetKeyStringResponse) The response message.
      """
      config = self.GetMethodConfig('GetKeyString')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetKeyString.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}/keyString',
        http_method='GET',
        method_id='apikeys.projects.locations.keys.getKeyString',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v2/{+name}/keyString',
        request_field='',
        request_type_name='ApikeysProjectsLocationsKeysGetKeyStringRequest',
        response_type_name='V2GetKeyStringResponse',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists the API keys owned by a project. The key string of the API key isn't included in the response. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (V2ListKeysResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys',
        http_method='GET',
        method_id='apikeys.projects.locations.keys.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v2/{+parent}/keys',
        request_field='',
        request_type_name='ApikeysProjectsLocationsKeysListRequest',
        response_type_name='V2ListKeysResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Patches the modifiable fields of an API key. The key string of the API key isn't included in the response. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}',
        http_method='PATCH',
        method_id='apikeys.projects.locations.keys.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['updateMask'],
        relative_path='v2/{+name}',
        request_field='v2Key',
        request_type_name='ApikeysProjectsLocationsKeysPatchRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Undelete(self, request, global_params=None):
      r"""Undeletes an API key which was deleted within 30 days. NOTE: Key is a global resource; hence the only supported value for location is `global`.

      Args:
        request: (ApikeysProjectsLocationsKeysUndeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Undelete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Undelete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v2/projects/{projectsId}/locations/{locationsId}/keys/{keysId}:undelete',
        http_method='POST',
        method_id='apikeys.projects.locations.keys.undelete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v2/{+name}:undelete',
        request_field='v2UndeleteKeyRequest',
        request_type_name='ApikeysProjectsLocationsKeysUndeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(ApikeysV2.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(ApikeysV2.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }