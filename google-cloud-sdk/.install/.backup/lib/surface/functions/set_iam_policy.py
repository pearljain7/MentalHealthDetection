# -*- coding: utf-8 -*- #
# Copyright 2018 Google LLC. All Rights Reserved.
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

"""Sets IAM policy for a Google Cloud Function."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.functions.v1 import util
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.functions import flags
from googlecloudsdk.command_lib.iam import iam_util


class SetIamPolicy(base.Command):
  """Sets IAM policy for a Google Cloud Function."""

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES':
          """\
          To set the iam policy for `FUNCTION-1` to the policy defined in `POLICY-FILE-1` run:

            $ {command} FUNCTION-1 POLICY-FILE-1
          """,
  }

  @staticmethod
  def Args(parser):
    """Register flags for this command."""
    flags.AddFunctionResourceArg(parser, 'to get IAM policy for')
    flags.AddIAMPolicyFileArg(parser)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      The specified function with its description and configured filter.
    """
    client = util.GetApiClientInstance()
    messages = client.MESSAGES_MODULE
    function_ref = args.CONCEPTS.name.Parse()
    policy, update_mask = iam_util.ParseYamlOrJsonPolicyFile(
        args.policy_file, messages.Policy)
    result = client.projects_locations_functions.SetIamPolicy(
        messages.CloudfunctionsProjectsLocationsFunctionsSetIamPolicyRequest(
            resource=function_ref.RelativeName(),
            setIamPolicyRequest=messages.SetIamPolicyRequest(
                policy=policy,
                updateMask=update_mask)))
    iam_util.LogSetIamPolicy(function_ref.Name(), 'function')
    return result
