# Copyright 2016 Mellanox Technologies, Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

sdn_opts = [
        cfg.StrOpt('url',
                   help=_("HTTP URL of SDN Provider."),
                   ),
        cfg.StrOpt('domain',
                   help=_("Cloud domain name in SDN provider "
                          "(for example: cloudx)"),
                   default='cloudx'
                   ),
        cfg.StrOpt('username',
                   help=_("HTTP username for authentication."),
                   ),
        cfg.StrOpt('password',
                   help=_("HTTP password for authentication."),
                   secret=True
                   ),
        cfg.IntOpt('timeout',
                   help=_("HTTP timeout in seconds."),
                   default=10
                   ),
]