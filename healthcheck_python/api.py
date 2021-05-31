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
import functools
import logging
import time
from multiprocessing import Process, Queue, cpu_count
from queue import Empty

import bottle
from setproctitle import setproctitle

from healthcheck_python.release import __version__


class HealthCheckApi(Process):
	"""
	API responder class
	Creates a bottle instance and reports the health status
	"""

	def __init__(self, host, port, status_queue, daemon=False):
		super().__init__()

		self._host = host
		self._port = port
		self._status_queue = status_queue
		self.daemon = daemon

		self._app = bottle.Bottle()
		self._app.install(HealthCheckApi.logging)
		self._app.queue = Queue()
		self._app.nb_workers = cpu_count()

		self._app.route('/', method="GET", callback=HealthCheckApi._index)
		self._app.route('/health', method="GET", callback=self._health)

	def __del__(self):
		self.terminate()

	def run(self):
		setproctitle(self.__class__.__name__)
		bottle.run(self._app, host=self._host, port=self._port, quiet=True)

	@staticmethod
	def _index():
		return f"Hello there! I'm healthcheck-python v{__version__}"

	def _get_status(self) -> dict:
		"""
		Get a single valid message from queue
		:return: dict
		"""
		while True:
			try:
				status = self._status_queue.get(block=True, timeout=1)
				if time.time() - status[0] <= 0.5:
					status = status[1]
					break
			except Empty:
				status = {'status': False, 'services': {}}
				break

		return status

	def _ready(self):
		"""
		Readiness check path
		/health
		:return: overall readiness str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = "v" in bottle.request.query.keys()

		status_message = self._get_status()

		if is_verbose:
			return status_message

		return {'ready': status_message['ready']}

	def _health(self):
		"""
		Health check path
		/health
		:return: overall status str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = "v" in bottle.request.query.keys()

		status_message = self._get_status()

		if is_verbose:
			return status_message

		return {'status': status_message['status']}

	@staticmethod
	def logging(func):
		"""
		Wrapper for send logs to logging module
		"""

		@functools.wraps(func)
		def log(*args, **kwargs):
			actual_response = func(*args, **kwargs)

			logging.info(
				"%s %s %s %s",
				bottle.request.remote_addr,
				bottle.request.method,
				bottle.request.url,
				bottle.response.status
			)

			return actual_response

		return log
