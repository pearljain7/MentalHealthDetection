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
"""Command for spanner instances update."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import textwrap

from googlecloudsdk.api_lib.spanner import instance_operations
from googlecloudsdk.api_lib.spanner import instances
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.spanner import flags


@base.ReleaseTracks(base.ReleaseTrack.GA, base.ReleaseTrack.BETA)
class Update(base.Command):
  """Update a Cloud Spanner instance."""

  detailed_help = {
      'EXAMPLES':
          textwrap.dedent("""\
        To update the display name of a Cloud Spanner instance, run:

          $ {command} my-instance-id --description=my-new-display-name

        To update the node count of a Cloud Spanner instance, run:

          $ {command} my-instance-id --nodes=1
        """),
  }

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Please add arguments in alphabetical order except for no- or a clear-
    pair for that argument which can follow the argument itself.
    Args:
      parser: An argparse parser that you can use to add arguments that go
          on the command line after this command. Positional arguments are
          allowed.
    """
    flags.Instance().AddToParser(parser)
    flags.Description(required=False).AddToParser(parser)
    flags.Nodes(required=False).AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      Some value that we want to have printed later.
    """
    op = instances.Patch(
        args.instance, description=args.description, nodes=args.nodes)
    if args.async_:
      return op
    instance_operations.Await(op, 'Updating instance')


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaUpdate(Update):
  """Update a Cloud Spanner instance with ALPHA features."""

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command.

    Please add arguments in alphabetical order except for no- or a clear-
    pair for that argument which can follow the argument itself.
    Args:
      parser: An argparse parser that you can use to add arguments that go on
        the command line after this command. Positional arguments are allowed.
    """
    flags.Instance().AddToParser(parser)
    flags.Description(required=False).AddToParser(parser)
    base.ASYNC_FLAG.AddToParser(parser)
    group_parser = parser.add_argument_group(mutex=True)
    flags.Nodes(required=False).AddToParser(group_parser)
    flags.ProcessingUnits(required=False).AddToParser(group_parser)

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      Some value that we want to have printed later.
    """
    op = instances.Patch(
        args.instance,
        description=args.description,
        nodes=args.nodes,
        processing_units=args.processing_units)
    if args.async_:
      return op
    instance_operations.Await(op, 'Updating instance')
