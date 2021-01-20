"""
py-healthcheck decorators
"""
import functools
import time

import py_healthcheck


def periodic(_func=None, *, service='unknown', timeout=5):
	"""
	Periodic check decorator
	Add this to your periodically called functions
	:param _func: Wrapped function
	:param service: Service name. This name will be reported with API call
	:param timeout: The timeout in seconds needed between to consecutive _func() calls
	before marking the service down
	:return: original return values of _func()
	"""

	def wrapper(func):
		@functools.wraps(func)
		def wrapper_func(*args, **kwargs):
			start_time = time.time()
			ret_val = func(*args, **kwargs)
			end_time = time.time()
			py_healthcheck.message_queue.put(
				{'name': service, 'start_time': start_time, 'end_time': end_time, 'timeout': timeout}
			)
			return ret_val

		return wrapper_func

	if _func is None:
		return wrapper
	return wrapper(_func)
