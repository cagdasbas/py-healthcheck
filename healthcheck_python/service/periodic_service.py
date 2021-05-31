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

import time

from healthcheck_python.service.base_service import BaseService
from healthcheck_python.utils.circular_queue import CircularQueue
from healthcheck_python.utils.utils import ServiceStatus


class PeriodicService(BaseService):
	"""
	Periodic Service
	This service has to be updated periodically, otherwise it is marked as failed
	"""

	def __init__(self, name, timeout=999):
		super().__init__(name)
		self._timeout = timeout

		self._last_start = None
		self._last_end = None

		self._status = False

		self._fps = 0
		self._queue = CircularQueue(50)

	def json(self):
		"""
		Returns all attributes as dict
		:return: dict, all object attributes
		"""
		return {
			'status': self._status,
			'ready': self.global_status == ServiceStatus.READY,
			'last_start': self._last_start, 'last_end': self._last_end, 'timeout': self._timeout,
			'fps': self._fps
		}

	def serialize(self):
		return dict(self.__dict__, **{'_queue': self._queue.__dict__, 'class': self.__class__.__name__})

	@staticmethod
	def parse_from_dict(_dict):
		new_service = PeriodicService(_dict['name'])
		new_queue = CircularQueue(_dict['_queue']['k'])
		new_queue.__dict__ = _dict['_queue']
		_dict.pop('_queue')
		new_service.__dict__ = _dict
		new_service._queue = new_queue
		return new_service

	def add_health_point(self, point):
		"""
		Add new function call
		:param point: dict, new function call service
		"""
		if point is None:
			return

		self._last_end = point['end_time']

	def add_fps_point(self, point):
		"""
		Add new function call
		:param point: dict, new function call service
		"""
		if point is None:
			return

		self._last_end = point['end_time']
		self._last_start = point['start_time']
		self._queue.enqueue(self._last_end - self._last_start)

	def is_healthy(self, current_time=None):
		"""
		Check if last call is within timeout limits
		:param current_time: time.time() object, Optional, check the status with specific time
		:return: boolean, service status
		"""
		if self._last_end is None:
			return False
		if current_time is None:
			current_time = time.time()

		self._fps = self._queue.mean_nonzero()

		if self.global_status == ServiceStatus.DONE:
			self._status = True
		else:
			self._status = current_time - self._last_end <= self._timeout
		return self._status
