"""
Health Check API
"""
import json
from multiprocessing import Process, Queue, cpu_count
from queue import Empty

import bottle


class HealthCheckApi(Process):
	"""
	API responder class
	Creates a bottle instance and reports the health status
	"""

	def __init__(self, port, status_queue, daemon=False):
		super().__init__()

		self._port = port
		self._status_queue = status_queue
		self.daemon = daemon

		self._app = bottle.Bottle()
		self._app.queue = Queue()
		self._app.nb_workers = cpu_count()

		self._app.route('/', method="GET", callback=HealthCheckApi._index)
		self._app.route('/health', method="GET", callback=self._health)

	def __del__(self):
		self.terminate()

	def run(self):
		bottle.run(self._app, host='0.0.0.0', port=self._port)

	@staticmethod
	def _index():
		return 'Hello there!'

	def _health(self):
		"""
		Health check path
		/health
		:return: overall status str(boolean).
		:return: If verbose mode enabled, return a dict with details about every service
		"""
		is_verbose = 'v' in bottle.request.query.keys()
		try:
			status = self._status_queue.get(block=False, timeout=1)
		except Empty:
			status = {'status': False, 'data': {}}

		if is_verbose:
			return json.dumps(status)

		return str(status['status']).lower()
