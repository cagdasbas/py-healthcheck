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
from healthcheck_python.utils.utils import ServiceStatus


class BaseService:
	"""
	Base service template
	All services has to implement this
	"""

	def __init__(self, name):
		self.name = name

		self.global_status = ServiceStatus.UNDEFINED

	def json(self) -> dict:
		"""
		Returns all attributes as dict
		:return: dict, all object attributes
		"""
		raise NotImplementedError()

	def serialize(self) -> dict:
		"""
		Serialize the object to a dict. serialize object instances as well
		:return: dict, all object attributes
		"""
		raise NotImplementedError()

	@staticmethod
	def parse_from_dict(_dict: dict):
		"""
		Create an object instance from the _dict serialized by self.serialize()
		:return: object
		"""
		raise NotImplementedError()

	def add_health_point(self, point: dict) -> None:
		"""
		Add new function call
		:param point: dict, new function call service
		"""
		raise NotImplementedError()

	def add_fps_point(self, point: dict) -> None:
		"""
		Add new function call
		:param point: dict, new function call service
		"""
		raise NotImplementedError()

	def mark_ready(self) -> None:
		"""
		Mark the service ready
		It means this service is ready to serve
		Clears done flag
		:return:
		"""
		self.global_status = ServiceStatus.READY

	def mark_done(self) -> None:
		"""
		Mark the service done
		It means this service is always up
		:return:
		"""
		self.global_status = ServiceStatus.DONE

	def is_ready(self) -> bool:
		"""
		Return ready status
		:return:
		"""
		return self.global_status == ServiceStatus.READY

	def is_healthy(self, current_time: float = None) -> bool:
		"""
		Check if last call is within timeout limits
		:param current_time: time.time() object, Optional, check the status with specific time
		:return: boolean, service status
		"""
		raise NotImplementedError()
