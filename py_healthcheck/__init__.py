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

import logging
import os
from multiprocessing import Queue

from py_healthcheck.api import HealthCheckApi
from py_healthcheck.decorators import periodic
from py_healthcheck.manager import HealthCheckManager

__all__ = ['periodic']

from py_healthcheck.updater import HealthCheckUpdater

message_queue = Queue()
process_queue = Queue(maxsize=1)
status_queue = Queue(maxsize=1)

HEALTH_CHECK_PORT = os.getenv("PY_HEALTH_CHECK_PORT", "8080")

if isinstance(HEALTH_CHECK_PORT, str) and \
		HEALTH_CHECK_PORT.isdecimal() and \
		1 < int(HEALTH_CHECK_PORT) < 65535:
	HEALTH_CHECK_PORT = int(HEALTH_CHECK_PORT)
else:
	HEALTH_CHECK_PORT = 8080

api = HealthCheckApi(HEALTH_CHECK_PORT, status_queue, daemon=True)
updater = HealthCheckUpdater(process_queue, status_queue, daemon=True)
manager = HealthCheckManager(message_queue, process_queue, daemon=True)

api.start()
updater.start()
manager.start()
logging.info("done init")
