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

import healthcheck_python.config as config


def start():
	"""
	Create instances and start the healthcheck pipeline
	"""
	if config.STARTED:
		return

	from healthcheck_python.api import HealthCheckApi
	from healthcheck_python.manager import HealthCheckManager
	from healthcheck_python.updater import HealthCheckUpdater

	api = HealthCheckApi(config.HOST, config.PORT, config.status_queue, daemon=True)
	updater = HealthCheckUpdater(config.process_queue, config.status_queue, daemon=True)
	manager = HealthCheckManager(config.message_queue, config.process_queue, daemon=True)

	api.start()
	updater.start()
	manager.start()
	config.STARTED = True
