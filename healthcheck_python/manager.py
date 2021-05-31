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

from setproctitle import setproctitle


class HealthCheckManager(mp.Process):
	"""
	HealthCheckManager
	Gets decorator messages and keeps track of process calls
	"""

	def __init__(self, message_queue, process_queue, daemon=False):
		super().__init__()
		self.message_queue = message_queue
		self.process_queue = process_queue
		self.daemon = daemon

		self.continue_running = True
		self.processes = {}

	def run(self):
		setproctitle(self.__class__.__name__)
		while self.continue_running:
			try:
				message = self.message_queue.get()
				if message is None:
					break
			except queue.Empty:
				continue

			self._process_message(message)

	def __del__(self):
		self.continue_running = False

	def _process_message(self, message):
		"""
		Process a single decorator message and put it into update queue
		:param message: A decorator message includes service name,
		functions start and end time and the timeout
		"""
		process_name = message['name']
		service = self.processes.get(process_name)
		if service is None:
			process_type = message['type']
			service = process_type(process_name)

		service.add_new_point(message)
		self.processes[process_name] = service

		while not self.process_queue.empty():
			self.process_queue.get()

		self.process_queue.put(
			{key: value.serialize() for key, value in self.processes.items()}
		)
