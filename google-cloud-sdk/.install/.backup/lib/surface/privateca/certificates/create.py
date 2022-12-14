# Lint as: python3
# -*- coding: utf-8 -*- #
# Copyright 2020 Google LLC. All Rights Reserved.
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
"""Create a certificate."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.privateca import base as privateca_base
from googlecloudsdk.api_lib.privateca import certificate_utils
from googlecloudsdk.api_lib.privateca import request_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.calliope.concepts import deps
from googlecloudsdk.command_lib.privateca import create_utils
from googlecloudsdk.command_lib.privateca import flags
from googlecloudsdk.command_lib.privateca import flags_v1
from googlecloudsdk.command_lib.privateca import key_generation
from googlecloudsdk.command_lib.privateca import resource_args
from googlecloudsdk.command_lib.util.args import labels_util
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs
from googlecloudsdk.core import log
from googlecloudsdk.core.util import files

_KEY_OUTPUT_HELP = """The path where the generated private key file should be written (in PEM format).

Note: possession of this key file could allow anybody to act as this certificate's
subject. Please make sure that you store this key file in a secure location at all
times, and ensure that only authorized users have access to it."""


def _ReadCsr(csr_file):
  try:
    return files.ReadFileContents(csr_file)
  except (files.Error, OSError, IOError):
    raise exceptions.BadFileException(
        "Could not read provided CSR file '{}'.".format(csr_file))


def _WritePemChain(pem_cert, issuing_chain, cert_file):
  try:
    pem_chain = [pem_cert] + issuing_chain
    files.WriteFileContents(cert_file, '\n'.join(pem_chain))
  except (files.Error, OSError, IOError):
    raise exceptions.BadFileException(
        "Could not write certificate to '{}'.".format(cert_file))


# TODO(b/177604350): Remove Beta code paths.
@base.ReleaseTracks(base.ReleaseTrack.BETA)
class CreateBeta(base.CreateCommand):
  r"""Create a new certificate.

  ## EXAMPLES

  To create a certificate using a CSR:

      $ {command} frontend-server-tls \
        --issuer=server-tls-1 --issuer-location=us \
        --csr=./csr.pem \
        --cert-output-file=./cert.pem \
        --validity=P30D

    To create a certificate using a client-generated key:

      $ {command} frontend-server-tls \
        --issuer=server-tls-1 --issuer-location=us \
        --generate-key \
        --key-output-file=./key \
        --cert-output-file=./cert.pem \
        --dns-san=www.joonix.net \
        --reusable-config=server-tls
  """

  @staticmethod
  def Args(parser):
    base.Argument(
        '--cert-output-file',
        help='The path where the resulting PEM-encoded certificate chain file should be written (ordered from leaf to root).',
        required=False).AddToParser(parser)
    flags.AddValidityFlag(parser, 'certificate', 'P30D', '30 days')
    labels_util.AddCreateLabelsFlags(parser)

    cert_generation_group = parser.add_group(
        mutex=True, required=True, help='Certificate generation method.')
    base.Argument(
        '--csr', help='A PEM-encoded certificate signing request file path.'
    ).AddToParser(cert_generation_group)

    key_generation_group = cert_generation_group.add_group(
        help='Alternatively, to generate a new key pair, use the following:')
    base.Argument(
        '--generate-key',
        help='Use this flag to have a new RSA-2048 private key securely generated on your machine.',
        action='store_const',
        const=True,
        default=False,
        required=True).AddToParser(key_generation_group)
    base.Argument(
        '--key-output-file', help=_KEY_OUTPUT_HELP,
        required=True).AddToParser(key_generation_group)

    subject_group = key_generation_group.add_group(
        help='The subject names for the certificate.', required=True)
    flags.AddSubjectFlags(subject_group)
    reusable_config_group = key_generation_group.add_group(
        mutex=True, help='The x509 configuration used for this certificate.')
    flags.AddInlineReusableConfigFlags(
        reusable_config_group, is_ca_command=False, default_max_chain_length=0)

    cert_arg = 'CERTIFICATE'
    concept_parsers.ConceptParser([
        presentation_specs.ResourcePresentationSpec(
            cert_arg,
            resource_args.CreateCertificateResourceSpec(
                cert_arg, [CreateBeta._GenerateCertificateIdFallthrough()]),
            'The name of the certificate to issue. If the certificate ID is '
            'omitted, a random identifier will be generated according to the '
            'following format: {YYYYMMDD}-{3 random alphanumeric characters}-'
            '{3 random alphanumeric characters}. The certificate ID is not '
            'required when the issuing CA is in the DevOps tier.',
            required=True)
    ]).AddToParser(parser)

    concept_parsers.ConceptParser([
        presentation_specs.ResourcePresentationSpec(
            '--reusable-config',
            resource_args.CreateReusableConfigResourceSpec(
                location_fallthroughs=[
                    deps.Fallthrough(
                        function=lambda: '',
                        hint=(
                            'location will default to the same location as the '
                            'certificate'),
                        active=False,
                        plural=False)
                ]),
            'The Reusable Config containing X.509 values for this certificate.',
            flag_name_overrides={
                'location': '',
                'project': '',
            },
            group=reusable_config_group)
    ]).AddToParser(reusable_config_group)

  @classmethod
  def _GenerateCertificateIdFallthrough(cls):
    cls.id_fallthrough_was_used = False

    def FallthroughFn():
      cls.id_fallthrough_was_used = True
      return certificate_utils.GenerateCertId()

    return deps.Fallthrough(
        function=FallthroughFn,
        hint='certificate id will default to an automatically generated id',
        active=False,
        plural=False)

  def _GetIssuingCa(self, ca_name):
    return self.client.projects_locations_certificateAuthorities.Get(
        self.messages
        .PrivatecaProjectsLocationsCertificateAuthoritiesGetRequest(
            name=ca_name))

  @classmethod
  def _ValidateArgsForDevOpsIssuer(cls, args):
    """Validates the command-line args when the issuer is a DevOps CA."""
    if not args.IsSpecified('cert_output_file'):
      raise exceptions.RequiredArgumentException(
          '--cert-output-file',
          'Certificate must be written to a file since the issuing CA does '
          'not support describing certificates after they are issued.')

    unused_args = []
    if not cls.id_fallthrough_was_used:
      unused_args.append('certificate ID')
    if args.IsSpecified('labels'):
      unused_args.append('labels')

    if unused_args:
      names = ', '.join(unused_args)
      verb = 'was' if len(unused_args) == 1 else 'were'
      log.warning('{names} {verb} specified but will not be used since the '
                  'issuing CA is in the DevOps tier, which does not expose '
                  'certificate lifecycle.'.format(names=names, verb=verb))

  def _GenerateCertificateConfig(self, request, args, location):
    private_key, public_key = key_generation.RSAKeyGen(2048)
    key_generation.ExportPrivateKey(args.key_output_file, private_key)

    config = self.messages.CertificateConfig()
    config.publicKey = self.messages.PublicKey()
    config.publicKey.key = public_key
    config.publicKey.type = self.messages.PublicKey.TypeValueValuesEnum.PEM_RSA_KEY
    config.reusableConfig = flags.ParseReusableConfig(
        args, location, is_ca_command=args.is_ca_cert)
    config.subjectConfig = flags.ParseSubjectFlags(args, is_ca=args.is_ca_cert)

    return config

  def Run(self, args):
    self.client = privateca_base.GetClientInstance()
    self.messages = privateca_base.GetMessagesModule()

    cert_ref = args.CONCEPTS.certificate.Parse()
    issuing_ca = self._GetIssuingCa(cert_ref.Parent().RelativeName())

    if issuing_ca.tier == self.messages.CertificateAuthority.TierValueValuesEnum.DEVOPS:
      CreateBeta._ValidateArgsForDevOpsIssuer(args)

    labels = labels_util.ParseCreateArgs(args,
                                         self.messages.Certificate.LabelsValue)

    request = self.messages.PrivatecaProjectsLocationsCertificateAuthoritiesCertificatesCreateRequest(
    )
    request.certificate = self.messages.Certificate()
    request.certificateId = cert_ref.Name()
    request.certificate.lifetime = flags.ParseValidityFlag(args)
    request.certificate.labels = labels
    request.parent = cert_ref.Parent().RelativeName()
    request.requestId = request_utils.GenerateRequestId()

    # TODO(b/12345): only show this for Enterprise certs.
    create_utils.PrintBetaResourceDeletionDisclaimer('certificates')

    if args.csr:
      request.certificate.pemCsr = _ReadCsr(args.csr)
    elif args.generate_key:
      request.certificate.config = self._GenerateCertificateConfig(
          request, args, cert_ref.locationsId)
    else:
      # This should not happen because of the required arg group, but protects
      # in case of future additions.
      raise exceptions.OneOfArgumentsRequiredException(
          ['--csr', '--generate-key'],
          ('To create a certificate, please specify either a CSR or the '
           '--generate-key flag to create a new key.'))

    certificate = self.client.projects_locations_certificateAuthorities_certificates.Create(
        request)

    status_message = 'Created Certificate'
    # DevOps certs won't have a name.
    if certificate.name:
      status_message += ' [{}]'.format(certificate.name)

    if args.IsSpecified('cert_output_file'):
      status_message += ' and saved it to [{}]'.format(args.cert_output_file)
      _WritePemChain(certificate.pemCertificate,
                     certificate.pemCertificateChain, args.cert_output_file)

    status_message += '.'
    log.status.Print(status_message)


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Create(base.CreateCommand):
  r"""Create a new certificate.

  ## EXAMPLES

  To create a certificate using a CSR:

      $ {command} frontend-server-tls \
        --issuer=my-pool --issuer-location=us-west1 \
        --csr=./csr.pem \
        --cert-output-file=./cert.pem \
        --validity=P30D

    To create a certificate using a client-generated key:

      $ {command} frontend-server-tls \
        --issuer=my-pool --issuer-location=us-west1 \
        --generate-key \
        --key-output-file=./key \
        --cert-output-file=./cert.pem \
        --dns-san=www.joonix.net \
        --use-preset-profile=leaf_server_tls
  """

  @staticmethod
  def Args(parser):
    base.Argument(
        '--cert-output-file',
        help='The path where the resulting PEM-encoded certificate chain file should be written (ordered from leaf to root).',
        required=False).AddToParser(parser)
    flags_v1.AddValidityFlag(parser, 'certificate', 'P30D', '30 days')
    labels_util.AddCreateLabelsFlags(parser)

    cert_generation_group = parser.add_group(
        mutex=True, required=True, help='Certificate generation method.')
    base.Argument(
        '--csr', help='A PEM-encoded certificate signing request file path.'
    ).AddToParser(cert_generation_group)

    key_generation_group = cert_generation_group.add_group(
        help='Alternatively, to generate a new key pair, use the following:')
    base.Argument(
        '--generate-key',
        help='Use this flag to have a new RSA-2048 private key securely generated on your machine.',
        action='store_const',
        const=True,
        default=False,
        required=True).AddToParser(key_generation_group)
    base.Argument(
        '--key-output-file', help=_KEY_OUTPUT_HELP,
        required=True).AddToParser(key_generation_group)
    base.Argument(
        '--ca',
        help='The name of an existing certificate authority to use for '
        'issuing the certificate. If omitted, a certificate authority '
        'will be will be chosen from the CA pool by the service on your behalf.',
        required=False).AddToParser(parser)
    base.Argument(
        '--validate-only',
        help='If this flag is set, the certificate resource will not be persisted '
        'and the returned certificate will not contain the pem_certificate field.',
        action='store_true',
        default=False,
        required=False).AddToParser(parser)
    subject_group = key_generation_group.add_group(
        help='The subject names for the certificate.', required=True)
    flags_v1.AddSubjectFlags(subject_group)
    x509_parameters_group = key_generation_group.add_group(
        mutex=True, help='The x509 configuration used for this certificate.')
    flags_v1.AddInlineX509ParametersFlags(
        x509_parameters_group, is_ca_command=False, default_max_chain_length=0)
    flags_v1.AddUsePresetProfilesFlag(x509_parameters_group)

    cert_arg = 'CERTIFICATE'
    concept_parsers.ConceptParser([
        presentation_specs.ResourcePresentationSpec(
            cert_arg,
            resource_args.CreateCertResourceSpec(
                cert_arg, [Create._GenerateCertificateIdFallthrough()]),
            'The name of the certificate to issue. If the certificate ID is '
            'omitted, a random identifier will be generated according to the '
            'following format: {YYYYMMDD}-{3 random alphanumeric characters}-'
            '{3 random alphanumeric characters}. The certificate ID is not '
            'required when the issuing CA is in the DevOps tier.',
            required=True),
        presentation_specs.ResourcePresentationSpec(
            '--template',
            resource_args.CreateCertificateTemplateResourceSpec(
                'certificate_template'),
            'The name of a certificate template to use for issuing this '
            'certificate, if desired. A template may overwrite parts of the '
            'certificate request, and the use of certificate templates may be '
            'required and/or regulated by the issuing CA Pool\'s CA Manager.',
            required=False),
    ]).AddToParser(parser)

  @classmethod
  def _GenerateCertificateIdFallthrough(cls):
    cls.id_fallthrough_was_used = False

    def FallthroughFn():
      cls.id_fallthrough_was_used = True
      return certificate_utils.GenerateCertId()

    return deps.Fallthrough(
        function=FallthroughFn,
        hint='certificate id will default to an automatically generated id',
        active=False,
        plural=False)

  def _GetIssuingCaPool(self, ca_pool_name):
    return self.client.projects_locations_caPools.Get(
        self.messages.PrivatecaProjectsLocationsCaPoolsGetRequest(
            name=ca_pool_name))

  def _ValidateArgs(self, args, issuing_pool):
    """Validates the command-line args."""
    if args.IsSpecified('use_preset_profile') and args.IsSpecified('template'):
      raise exceptions.OneOfArgumentsRequiredException(
          ['--use-preset-profile', '--template'],
          ('To create a certificate, please specify either a preset profile '
           'or a certificate template.'))

    if args.IsSpecified('cert_output_file') and args.IsSpecified(
        'validate_only'):
      raise exceptions.OneOfArgumentsRequiredException(
          ['--cert-output-file', '--validate-only'],
          ('Certificates created in validate-only mode do not have the '
           'PEM-encoded certificate field.'))

    if not args.IsSpecified('csr') and not args.IsSpecified('generate_key'):
      # This should not happen because of the required arg group, but protects
      # in case of future additions.
      raise exceptions.OneOfArgumentsRequiredException(
          ['--csr', '--generate-key'],
          ('To create a certificate, please specify either a CSR or the '
           '--generate-key flag to create a new key.'))

    if issuing_pool.tier == self.messages.CaPool.TierValueValuesEnum.DEVOPS:
      Create._ValidateArgsForDevOpsIssuer(args)

  @classmethod
  def _ValidateArgsForDevOpsIssuer(cls, args):
    """Validates the command-line args when the issuer is a DevOps CA pool."""
    if not args.IsSpecified('cert_output_file'):
      raise exceptions.RequiredArgumentException(
          '--cert-output-file',
          'Certificate must be written to a file since the issuing CA pool '
          'does not support describing certificates after they are issued.')

    unused_args = []
    if not cls.id_fallthrough_was_used:
      unused_args.append('certificate ID')
    if args.IsSpecified('labels'):
      unused_args.append('labels')

    if unused_args:
      names = ', '.join(unused_args)
      verb = 'was' if len(unused_args) == 1 else 'were'
      log.warning(
          '{names} {verb} specified but will not be used since the '
          'issuing CA pool is in the DevOps tier, which does not expose '
          'certificate lifecycle.'.format(names=names, verb=verb))

  def _GenerateCertificateConfig(self, request, args):
    private_key, public_key = key_generation.RSAKeyGen(2048)
    key_generation.ExportPrivateKey(args.key_output_file, private_key)

    config = self.messages.CertificateConfig()
    config.publicKey = self.messages.PublicKey()
    config.publicKey.key = public_key
    config.publicKey.format = self.messages.PublicKey.FormatValueValuesEnum.PEM
    config.subjectConfig = flags_v1.ParseSubjectFlags(
        args, is_ca=args.is_ca_cert)
    config.x509Config = flags_v1.ParseX509Parameters(args, is_ca_command=False)

    return config

  def Run(self, args):
    self.client = privateca_base.GetClientInstance(api_version='v1')
    self.messages = privateca_base.GetMessagesModule(api_version='v1')

    cert_ref = args.CONCEPTS.certificate.Parse()
    issuing_pool = self._GetIssuingCaPool(cert_ref.Parent().RelativeName())

    self._ValidateArgs(args, issuing_pool)

    labels = labels_util.ParseCreateArgs(args,
                                         self.messages.Certificate.LabelsValue)

    request = self.messages.PrivatecaProjectsLocationsCaPoolsCertificatesCreateRequest(
    )
    request.certificate = self.messages.Certificate()
    request.certificateId = cert_ref.Name()
    request.certificate.lifetime = flags_v1.ParseValidityFlag(args)
    request.certificate.labels = labels
    request.parent = cert_ref.Parent().RelativeName()
    request.requestId = request_utils.GenerateRequestId()
    request.validateOnly = args.validate_only
    if args.IsSpecified('ca'):
      request.issuingCertificateAuthorityId = args.ca

    template_ref = args.CONCEPTS.template.Parse()
    if template_ref:
      request.certificate.certificateTemplate = template_ref.RelativeName()

    if args.csr:
      request.certificate.pemCsr = _ReadCsr(args.csr)
    elif args.generate_key:
      request.certificate.config = self._GenerateCertificateConfig(
          request, args)

    certificate = self.client.projects_locations_caPools_certificates.Create(
        request)

    status_message = 'Created Certificate'
    # DevOps certs won't have a name.
    if certificate.name:
      status_message += ' [{}]'.format(certificate.name)

    if args.IsSpecified('cert_output_file'):
      status_message += ' and saved it to [{}]'.format(args.cert_output_file)
      _WritePemChain(certificate.pemCertificate,
                     certificate.pemCertificateChain, args.cert_output_file)
    elif args.validate_only:
      status_message += ' in dry-run mode'

    status_message += '.'
    log.status.Print(status_message)
