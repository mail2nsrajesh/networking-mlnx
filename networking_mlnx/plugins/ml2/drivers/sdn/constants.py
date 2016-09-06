# Copyright 2015 Mellanox Technologies, Ltd
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

# Config file groups name
GROUP_OPT = "sdn"

# RESTful API paths:
NETWORK = "Network"
PORT = "Port"

# HTTP request methods:
DELETE = "DELETE"
POST = "POST"
PUT = "PUT"

# HTTP headers
LOGIN_HTTP_HEADER = {'content-type': 'application/x-www-form-urlencoded'}
JSON_HTTP_HEADER = {"Content-Type": "application/json"}

# Port device owner
PORT_DEVICE_OWNER_COMPUTE = 'compute:'

# Constants for journal operation states
PENDING = 'pending'
PROCESSING = 'processing'
MONITORING = 'monitoring'
FAILED = 'failed'
COMPLETED = 'completed'
