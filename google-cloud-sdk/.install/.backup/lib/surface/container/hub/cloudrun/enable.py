# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
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
"""The command to enable the CloudRun feature."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.command_lib.container.hub.features import base


class Enable(base.EnableCommand):
  """Enable the CloudRun feature.

  This command enables the CloudRun feature in Anthos clusters.

  ## Examples

  Enable the CloudRun feature:

    $ {command}
  """

  FEATURE_NAME = 'appdevexperience'
  FEATURE_DISPLAY_NAME = 'CloudRun'
  FEATURE_API = 'appdevelopmentexperience.googleapis.com'

  @classmethod
  def Args(cls, parser):
    pass

  def Run(self, args):
    self.RunCommand(
        args,
        appdevexperienceFeatureSpec=(base.CreateAppDevExperienceFeatureSpec()))
