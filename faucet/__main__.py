"""Launch forwarder script for Faucet/Gauge"""

# Copyright (C) 2015 Brad Cowie, Christopher Lorier and Joe Stringer.
# Copyright (C) 2015 Research and Education Advanced Network New Zealand Ltd.
# Copyright (C) 2015--2017 The Contributors
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

import argparse
import os
import sys


def parse_args():
    """Parse Faucet/Gauge arguments.

    Returns:
        argparse.Namespace: command line arguments
    """
    args = argparse.ArgumentParser(
        prog='faucet', description='Faucet SDN Controller')
    args.add_argument('--gauge', action='store_true', help='run Gauge instead')
    args.add_argument(
        '-v', '--verbose', action='store_true', help='produce verbose output')
    args.add_argument(
        '-V', '--version', action='store_true', help='print version and exit')
    args.add_argument(
        '--ca-certs', help='CA certificates')
    args.add_argument(
        '--ctl-cert', help='controller certificate')
    args.add_argument(
        '--ctl-privkey', help='controller private key')
    args.add_argument(
        '--ryu-app',
        action='append',
        help='add Ryu app (can be specified multiple times)',
        metavar='APP')
    return args.parse_args()


def print_version():
    """Print version number and exit."""
    from pbr.version import VersionInfo
    version = VersionInfo('faucet').semantic_version().release_string()
    message = 'Faucet %s' % version
    print(message)
    sys.exit(0)


def main():
    """Main program."""
    args = parse_args()
    ryu_args = []

    # Checking version number?
    if args.version:
        print_version()

    # Verbose output?
    if args.verbose:
        ryu_args.append("--verbose")

    # Set certificates for OpenFlow TLS control channel
    if args.ca_certs:
        ryu_args.append("--ca-certs=%s" % args.ca_certs)
    if args.ctl_cert:
        ryu_args.append("--ctl-cert=%s" % args.ctl_cert)
    if args.ctl_privkey:
        ryu_args.append("--ctl-privkey=%s" % args.ctl_privkey)

    # Running Faucet or Gauge?
    if args.gauge or os.path.basename(sys.argv[0]) == 'gauge':
        ryu_args.append('faucet.gauge')
    else:
        ryu_args.append('faucet.faucet')

    # Check for additional Ryu apps.
    if args.ryu_app:
        ryu_args.extend(args.ryu_app)

    # Replace current process with ryu-manager from PATH (no PID change).
    ryu_args.insert(0, 'ryu-manager')
    os.execvp('ryu-manager', ryu_args)


if __name__ == '__main__':
    main()
