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
import pickle
import queue
import time


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
		self.index = 0

	def run(self):
		while self.continue_running:
			try:
				message = self._process_queue.get(block=False)
				if message is None:
					break
				self._processes = HealthCheckUpdater.parse_message(message)
			except queue.Empty:
				pass

			self._check_health()
			time.sleep(0.5)

	def __del__(self):
		self.continue_running = False

	@staticmethod
	def parse_message(message):
		"""
		Parse incoming struct to create own copy of process data
		:param message: dict with pickled values. Each value has to be a instance of BaseService
		:return: dict with object values
		"""
		processes = {}
		for key, pickled_value in message.items():
			if isinstance(pickled_value, bytes):
				service = pickle.loads(pickled_value)
				processes[key] = service
		return processes

	def _check_health(self):
		"""
		check every services ending time to current time
		Every service should ended within defined timeout interval
		Free the status queue and put the latest status.
		"""
		call_time = time.time()
		self.index += 1
		status = True
		for _, service in self._processes.items():
			service_status = service.is_healthy(call_time)
			if not service_status:
				status = False

		while not self._status_queue.empty():
			self._status_queue.get()

		self._status_queue.put(
			{
				'status': status,
				'data': {key: service.json() for key, service in self._processes.items()}
			}
		)
