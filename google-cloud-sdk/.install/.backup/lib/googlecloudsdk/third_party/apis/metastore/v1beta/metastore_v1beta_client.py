"""Generated client library for metastore version v1beta."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.metastore.v1beta import metastore_v1beta_messages as messages


class MetastoreV1beta(base_api.BaseApiClient):
  """Generated client library for service metastore version v1beta."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://metastore.googleapis.com/'
  MTLS_BASE_URL = 'https://metastore.mtls.googleapis.com/'

  _PACKAGE = 'metastore'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
  _VERSION = 'v1beta'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'MetastoreV1beta'
  _URL_VERSION = 'v1beta'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new metastore handle."""
    url = url or self.BASE_URL
    super(MetastoreV1beta, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.projects_locations_operations = self.ProjectsLocationsOperationsService(self)
    self.projects_locations_services_backups = self.ProjectsLocationsServicesBackupsService(self)
    self.projects_locations_services_metadataImports = self.ProjectsLocationsServicesMetadataImportsService(self)
    self.projects_locations_services = self.ProjectsLocationsServicesService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)

  class ProjectsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the projects_locations_operations resource."""

    _NAME = 'projects_locations_operations'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns google.rpc.Code.UNIMPLEMENTED.

      Args:
        request: (MetastoreProjectsLocationsOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='DELETE',
        method_id='metastore.projects.locations.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (MetastoreProjectsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method='GET',
        method_id='metastore.projects.locations.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns UNIMPLEMENTED.NOTE: the name binding allows API services to override the binding to use different resource name schemes, such as users/*/operations. To override the binding, API services can add a binding such as "/v1/{name=users/*}/operations" to their service configuration. For backwards compatibility, the default name includes the operations collection id, however overriding users must ensure the name binding is the parent resource, without the operations collection id.

      Args:
        request: (MetastoreProjectsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/operations',
        http_method='GET',
        method_id='metastore.projects.locations.operations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1beta/{+name}/operations',
        request_field='',
        request_type_name='MetastoreProjectsLocationsOperationsListRequest',
        response_type_name='ListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsServicesBackupsService(base_api.BaseApiService):
    """Service class for the projects_locations_services_backups resource."""

    _NAME = 'projects_locations_services_backups'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsLocationsServicesBackupsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new backup in a given project and location.

      Args:
        request: (MetastoreProjectsLocationsServicesBackupsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/backups',
        http_method='POST',
        method_id='metastore.projects.locations.services.backups.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['backupId', 'requestId'],
        relative_path='v1beta/{+parent}/backups',
        request_field='backup',
        request_type_name='MetastoreProjectsLocationsServicesBackupsCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a single backup.

      Args:
        request: (MetastoreProjectsLocationsServicesBackupsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/backups/{backupsId}',
        http_method='DELETE',
        method_id='metastore.projects.locations.services.backups.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['requestId'],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesBackupsDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details of a single backup.

      Args:
        request: (MetastoreProjectsLocationsServicesBackupsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Backup) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/backups/{backupsId}',
        http_method='GET',
        method_id='metastore.projects.locations.services.backups.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesBackupsGetRequest',
        response_type_name='Backup',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists backups in a service.

      Args:
        request: (MetastoreProjectsLocationsServicesBackupsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListBackupsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/backups',
        http_method='GET',
        method_id='metastore.projects.locations.services.backups.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1beta/{+parent}/backups',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesBackupsListRequest',
        response_type_name='ListBackupsResponse',
        supports_download=False,
    )

  class ProjectsLocationsServicesMetadataImportsService(base_api.BaseApiService):
    """Service class for the projects_locations_services_metadataImports resource."""

    _NAME = 'projects_locations_services_metadataImports'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsLocationsServicesMetadataImportsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new MetadataImport in a given project and location.

      Args:
        request: (MetastoreProjectsLocationsServicesMetadataImportsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/metadataImports',
        http_method='POST',
        method_id='metastore.projects.locations.services.metadataImports.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['metadataImportId', 'requestId'],
        relative_path='v1beta/{+parent}/metadataImports',
        request_field='metadataImport',
        request_type_name='MetastoreProjectsLocationsServicesMetadataImportsCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets details of a single import.

      Args:
        request: (MetastoreProjectsLocationsServicesMetadataImportsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (MetadataImport) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/metadataImports/{metadataImportsId}',
        http_method='GET',
        method_id='metastore.projects.locations.services.metadataImports.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesMetadataImportsGetRequest',
        response_type_name='MetadataImport',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists imports in a service.

      Args:
        request: (MetastoreProjectsLocationsServicesMetadataImportsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListMetadataImportsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/metadataImports',
        http_method='GET',
        method_id='metastore.projects.locations.services.metadataImports.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1beta/{+parent}/metadataImports',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesMetadataImportsListRequest',
        response_type_name='ListMetadataImportsResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates a single import. Only the description field of MetadataImport is supported to be updated.

      Args:
        request: (MetastoreProjectsLocationsServicesMetadataImportsPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}/metadataImports/{metadataImportsId}',
        http_method='PATCH',
        method_id='metastore.projects.locations.services.metadataImports.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['requestId', 'updateMask'],
        relative_path='v1beta/{+name}',
        request_field='metadataImport',
        request_type_name='MetastoreProjectsLocationsServicesMetadataImportsPatchRequest',
        response_type_name='Operation',
        supports_download=False,
    )

  class ProjectsLocationsServicesService(base_api.BaseApiService):
    """Service class for the projects_locations_services resource."""

    _NAME = 'projects_locations_services'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsLocationsServicesService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a metastore service in a project and location.

      Args:
        request: (MetastoreProjectsLocationsServicesCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services',
        http_method='POST',
        method_id='metastore.projects.locations.services.create',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['requestId', 'serviceId'],
        relative_path='v1beta/{+parent}/services',
        request_field='service',
        request_type_name='MetastoreProjectsLocationsServicesCreateRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a single service.

      Args:
        request: (MetastoreProjectsLocationsServicesDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}',
        http_method='DELETE',
        method_id='metastore.projects.locations.services.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['requestId'],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesDeleteRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def ExportMetadata(self, request, global_params=None):
      r"""Exports metadata from a service.

      Args:
        request: (MetastoreProjectsLocationsServicesExportMetadataRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('ExportMetadata')
      return self._RunMethod(
          config, request, global_params=global_params)

    ExportMetadata.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}:exportMetadata',
        http_method='POST',
        method_id='metastore.projects.locations.services.exportMetadata',
        ordered_params=['service'],
        path_params=['service'],
        query_params=[],
        relative_path='v1beta/{+service}:exportMetadata',
        request_field='exportMetadataRequest',
        request_type_name='MetastoreProjectsLocationsServicesExportMetadataRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the details of a single service.

      Args:
        request: (MetastoreProjectsLocationsServicesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Service) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}',
        http_method='GET',
        method_id='metastore.projects.locations.services.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesGetRequest',
        response_type_name='Service',
        supports_download=False,
    )

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.

      Args:
        request: (MetastoreProjectsLocationsServicesGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}:getIamPolicy',
        http_method='GET',
        method_id='metastore.projects.locations.services.getIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=['options_requestedPolicyVersion'],
        relative_path='v1beta/{+resource}:getIamPolicy',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesGetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists services in a project and location.

      Args:
        request: (MetastoreProjectsLocationsServicesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListServicesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services',
        http_method='GET',
        method_id='metastore.projects.locations.services.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'orderBy', 'pageSize', 'pageToken'],
        relative_path='v1beta/{+parent}/services',
        request_field='',
        request_type_name='MetastoreProjectsLocationsServicesListRequest',
        response_type_name='ListServicesResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates the parameters of a single service.

      Args:
        request: (MetastoreProjectsLocationsServicesPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}',
        http_method='PATCH',
        method_id='metastore.projects.locations.services.patch',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['requestId', 'updateMask'],
        relative_path='v1beta/{+name}',
        request_field='service',
        request_type_name='MetastoreProjectsLocationsServicesPatchRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Restore(self, request, global_params=None):
      r"""Restores a service from a backup.

      Args:
        request: (MetastoreProjectsLocationsServicesRestoreRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Restore')
      return self._RunMethod(
          config, request, global_params=global_params)

    Restore.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}:restore',
        http_method='POST',
        method_id='metastore.projects.locations.services.restore',
        ordered_params=['service'],
        path_params=['service'],
        query_params=[],
        relative_path='v1beta/{+service}:restore',
        request_field='restoreServiceRequest',
        request_type_name='MetastoreProjectsLocationsServicesRestoreRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy on the specified resource. Replaces any existing policy.Can return NOT_FOUND, INVALID_ARGUMENT, and PERMISSION_DENIED errors.

      Args:
        request: (MetastoreProjectsLocationsServicesSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}:setIamPolicy',
        http_method='POST',
        method_id='metastore.projects.locations.services.setIamPolicy',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1beta/{+resource}:setIamPolicy',
        request_field='setIamPolicyRequest',
        request_type_name='MetastoreProjectsLocationsServicesSetIamPolicyRequest',
        response_type_name='Policy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a NOT_FOUND error.Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.

      Args:
        request: (MetastoreProjectsLocationsServicesTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}/services/{servicesId}:testIamPermissions',
        http_method='POST',
        method_id='metastore.projects.locations.services.testIamPermissions',
        ordered_params=['resource'],
        path_params=['resource'],
        query_params=[],
        relative_path='v1beta/{+resource}:testIamPermissions',
        request_field='testIamPermissionsRequest',
        request_type_name='MetastoreProjectsLocationsServicesTestIamPermissionsRequest',
        response_type_name='TestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = 'projects_locations'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets information about a location.

      Args:
        request: (MetastoreProjectsLocationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Location) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations/{locationsId}',
        http_method='GET',
        method_id='metastore.projects.locations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1beta/{+name}',
        request_field='',
        request_type_name='MetastoreProjectsLocationsGetRequest',
        response_type_name='Location',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists information about the supported locations for this service.

      Args:
        request: (MetastoreProjectsLocationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLocationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1beta/projects/{projectsId}/locations',
        http_method='GET',
        method_id='metastore.projects.locations.list',
        ordered_params=['name'],
        path_params=['name'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1beta/{+name}/locations',
        request_field='',
        request_type_name='MetastoreProjectsLocationsListRequest',
        response_type_name='ListLocationsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = 'projects'

    def __init__(self, client):
      super(MetastoreV1beta.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }
