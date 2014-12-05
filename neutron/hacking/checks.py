# Copyright (c) 2014 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re

import pep8

"""
Guidelines for writing new hacking checks

 - Use only for Neutron specific tests. OpenStack general tests
   should be submitted to the common 'hacking' module.
 - Pick numbers in the range N3xx. Find the current test with
   the highest allocated number and then pick the next value.
 - Keep the test method code in the source file ordered based
   on the N3xx value.
 - List the new rule in the top level HACKING.rst file
 - Add test cases for each new rule to
   neutron/tests/unit/test_hacking.py

"""

log_translation = re.compile(
    r"(.)*LOG\.(audit|error|info|warn|warning|critical|exception)\(\s*('|\")")
author_tag_re = (re.compile("^\s*#\s*@?(a|A)uthor"),
                 re.compile("^\.\.\s+moduleauthor::"))
_all_hints = set(['_', '_LI', '_LE', '_LW', '_LC'])
_all_log_levels = {
    # NOTE(yamamoto): Following nova which uses _() for audit.
    'audit': '_',
    'error': '_LE',
    'info': '_LI',
    'warn': '_LW',
    'warning': '_LW',
    'critical': '_LC',
    'exception': '_LE',
}
log_translation_hints = []
for level, hint in _all_log_levels.iteritems():
    r = "(.)*LOG\.%(level)s\(\s*((%(wrong_hints)s)\(|'|\")" % {
        'level': level,
        'wrong_hints': '|'.join(_all_hints - set([hint])),
    }
    log_translation_hints.append(re.compile(r))


def _directory_to_check_translation(filename):
    # In order to try and speed up the integration of this we will
    # do it on a directory by directory basis. The last patch of the
    # series will remove this and the entire code base will be validated.
    dirs = ["neutron/agent",
            "neutron/api",
            "neutron/cmd",
            "neutron/common",
            "neutron/db",
            "neutron/debug",
            "neutron/extensions",
            "neutron/hacking",
            "neutron/locale",
            "neutron/notifiers",
            "neutron/openstack",
            "neutron/scheduler",
            "neutron/server",
            "neutron/services",
            #"neutron/plugins",
            "neutron/plugins/bigswitch",
            "neutron/plugins/brocade",
            "neutron/plugins/cisco",
            "neutron/plugins/common",
            "neutron/plugins/embrane",
            "neutron/plugins/hyperv",
            #"neutron/plugins/ibm",
            "neutron/plugins/linuxbridge",
            "neutron/plugins/metaplugin",
            "neutron/plugins/midonet",
            "neutron/plugins/ml2",
            "neutron/plugins/mlnx",
            "neutron/plugins/nec",
            "neutron/plugins/nuage",
            #"neutron/plugins/ofagent",
            #"neutron/plugins/oneconvergence",
            "neutron/plugins/opencontrail",
            "neutron/plugins/openvswitch",
            "neutron/plugins/plumgrid",
            "neutron/plugins/sriovnicagent",
            "neutron/plugins/vmware"]
    return any([dir in filename for dir in dirs])


def validate_log_translations(logical_line, physical_line, filename):
    # Translations are not required in the test directory
    if "neutron/tests" in filename:
        return
    if pep8.noqa(physical_line):
        return
    msg = "N320: Log messages require translations!"
    if log_translation.match(logical_line):
        yield (0, msg)

    if _directory_to_check_translation(filename):
        msg = "N320: Log messages require translation hints!"
        for log_translation_hint in log_translation_hints:
            if log_translation_hint.match(logical_line):
                yield (0, msg)


def use_jsonutils(logical_line, filename):
    msg = "N321: jsonutils.%(fun)s must be used instead of json.%(fun)s"

    # Some files in the tree are not meant to be run from inside Neutron
    # itself, so we should not complain about them not using jsonutils
    json_check_skipped_patterns = [
        "neutron/plugins/openvswitch/agent/xenapi/etc/xapi.d/plugins/netwrap",
    ]

    for pattern in json_check_skipped_patterns:
        if pattern in filename:
            return

    if "json." in logical_line:
        json_funcs = ['dumps(', 'dump(', 'loads(', 'load(']
        for f in json_funcs:
            pos = logical_line.find('json.%s' % f)
            if pos != -1:
                yield (pos, msg % {'fun': f[:-1]})


def no_author_tags(physical_line):
    for regex in author_tag_re:
        if regex.match(physical_line):
            physical_line = physical_line.lower()
            pos = physical_line.find('moduleauthor')
            if pos < 0:
                pos = physical_line.find('author')
            return pos, "N322: Don't use author tags"


def no_translate_debug_logs(logical_line, filename):
    """Check for 'LOG.debug(_('

    As per our translation policy,
    https://wiki.openstack.org/wiki/LoggingStandards#Log_Translation
    we shouldn't translate debug level logs.

    * This check assumes that 'LOG' is a logger.
    N319
    """
    if _directory_to_check_translation(filename):
        if logical_line.startswith("LOG.debug(_("):
            yield(0, "N319 Don't translate debug level logs")


def check_assert_called_once_with(logical_line, filename):
    # Try to detect unintended calls of nonexistent mock methods like:
    #    assert_called_once
    #    assertCalledOnceWith
    if 'neutron/tests/' in filename:
        if '.assert_called_once_with(' in logical_line:
            return
        if '.assertcalledonce' in logical_line.lower().replace('_', ''):
            msg = ("N323: Possible use of no-op mock method. "
                   "please use assert_called_once_with.")
            yield (0, msg)


def factory(register):
    register(validate_log_translations)
    register(use_jsonutils)
    register(no_author_tags)
    register(check_assert_called_once_with)
    register(no_translate_debug_logs)
