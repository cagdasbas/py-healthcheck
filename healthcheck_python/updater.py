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

import multiprocessing as mp
import queue
import time

from setproctitle import setproctitle

from healthcheck_python.utils.utils import class_for_name


class HealthCheckUpdater(mp.Process):
	"""
	Health Check Updater
	Regularly tries to fetch latest process structure and updates health status
	Updates the overall status every 0.5 seconds
	"""

	def __init__(self, process_queue, status_queue, daemon=False):
		super().__init__()
		self._process_queue = process_queue
		self._status_queue = status_queue
		self.daemon = daemon

		self.continue_running = True
		self._processes = {}
		self._classes = {}

	def run(self):
		setproctitle(self.__class__.__name__)

		while self.continue_running:
			while True:
				try:
					message = self._process_queue.get(block=True, timeout=0.1)
				except queue.Empty:
					break
				if message is None:
					break

				if time.time() - message[0] <= 0.5:
					self._processes = self.parse_message(message[1])
					break

			self._check_health()

	def __del__(self):
		self.continue_running = False

	def parse_message(self, message) -> dict:
		"""
		Parse incoming struct to create own copy of process service
		:param message: dict with pickled values. Each value has to be a instance of BaseService
		:return: dict with object values
		"""
		processes = {}
		for key, data in message.items():
			service_class = self._classes.get(data['class'])
			if service_class is None:
				service_class = class_for_name(data['class'])
				self._classes[data['class']] = service_class
			data.pop('class')
			new_service = service_class.parse_from_dict(data)
			processes[key] = new_service
		return processes

	def _check_health(self):
		"""
		check every services ending time to current time
		Every service should ended within defined timeout interval
		Free the status queue and put the latest status.
		"""
		call_time = time.time()
		status = True
		ready = True
		for _, service in self._processes.items():
			service_status = service.is_healthy(call_time)
			ready_status = service.is_ready()
			status &= service_status
			ready &= ready_status

		while True:
			try:
				self._status_queue.get_nowait()
			except queue.Empty:
				break

		self._status_queue.put((
			time.time(),
			{
				'status': status,
				'ready': ready,
				'services': {key: service.json() for key, service in self._processes.items()}
			}
		))
