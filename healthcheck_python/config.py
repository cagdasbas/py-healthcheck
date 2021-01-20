#  Copyright (c) 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from multiprocessing import Queue

started = False
host = os.getenv("PY_HEALTH_CHECK_HOST", "0.0.0.0")
port = os.getenv("PY_HEALTH_CHECK_PORT", "8080")

if isinstance(port, str) and port.isdecimal() and 1 < int(port) < 65535:
	port = int(port)
else:
	port = 8080

message_queue = Queue()
process_queue = Queue(maxsize=1)
status_queue = Queue(maxsize=1)
