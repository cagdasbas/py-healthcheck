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
import time

import healthcheck_python.config as config
from healthcheck_python.service.periodic_service import PeriodicService
from healthcheck_python.utils.pipeline import start
from healthcheck_python.utils.utils import ServiceStatus, ServiceOperation


def periodic(_func=None, *, service='', timeout=5):
	"""
	Periodic check decorator
	This decorator only defines a new periodic service
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call.
	If it's empty, class name, if wraps a class, or function name, if wraps a function, will be used
	:param timeout: The timeout in seconds needed between to consecutive _func() calls
	before marking the service down
	:return: original return values of _func()
	"""
	start()

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			service_name = service
			if service_name == '':
				service_name = func.__qualname__.split(".")[0]
			ret_val = func(*args, **kwargs)

			config.message_queue.put(
				{
					'type': PeriodicService, 'op': ServiceOperation.CREATE,
					'name': service_name, 'timeout': timeout
				}
			)

			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper

	return wrapper(_func)


def healthy(_func=None, *, service=''):
	"""
	Periodic health check decorator
	Add this to your periodically called functions to report a service healthy
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	If it's empty, class name, if wraps a class, or function name, if wraps a function, will be used
	The service has to be already defined before healthy is called
	:return: original return values of _func()
	"""
	start()

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			service_name = service
			if service_name == '':
				service_name = func.__qualname__.split(".")[0]
			ret_val = func(*args, **kwargs)
			end_time = time.time()

			config.message_queue.put(
				{
					'name': service_name, 'op': ServiceOperation.ADD_HEALTH_POINT, 'end_time': end_time
				}
			)

			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper

	return wrapper(_func)


def fps(_func=None, *, service=''):
	"""
	FPS Calculation decorator
	Add this to your periodically called functions to calculate the fps
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	If it's empty, class name, if wraps a class, or function name, if wraps a function, will be used
	The service has to be already defined before healthy is called
	:return: original return values of _func()
	"""

	start()

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			service_name = service
			if service_name == '':
				service_name = func.__qualname__.split(".")[0]
			start_time = time.time()
			ret_val = func(*args, **kwargs)
			end_time = time.time()

			config.message_queue.put(
				{
					'name': service_name, 'op': ServiceOperation.ADD_FPS_POINT,
					'start_time': start_time, 'end_time': end_time
				}
			)

			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper

	return wrapper(_func)


def mark_ready(_func=None, *, service=''):
	"""
	Mark a service ready to serve
	Also clears done flag
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	If it's empty, class name, if wraps a class, or function name, if wraps a function, will be used
	The service has to be already defined before healthy is called
	:return: original return values of _func()
	"""

	start()

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			service_name = service
			if service_name == '':
				service_name = func.__qualname__.split(".")[0]
			ret_val = func(*args, **kwargs)

			config.message_queue.put(
				{
					'name': service_name, 'op': ServiceOperation.MARK_READY,
					'status': ServiceStatus.READY
				}
			)

			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper

	return wrapper(_func)


def mark_done(_func=None, *, service=''):
	"""
	Mark a service done and make it successful indefinitely
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	If it's empty, class name, if wraps a class, or function name, if wraps a function, will be used
	The service has to be already defined before healthy is called
	:return: original return values of _func()
	"""

	start()

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			service_name = service
			if service_name == '':
				service_name = func.__qualname__.split(".")[0]
			ret_val = func(*args, **kwargs)

			config.message_queue.put(
				{
					'name': service_name, 'op': ServiceOperation.MARK_DONE,
					'status': ServiceStatus.DONE
				}
			)

			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper

	return wrapper(_func)
