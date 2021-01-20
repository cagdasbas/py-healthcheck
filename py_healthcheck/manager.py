"""
py-healthcheck manager
"""
import multiprocessing as mp
import queue
import time


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
		while self.continue_running:
			try:
				message = self.message_queue.get(block=False)
				if message is None:
					break

				self._process_message(message)
			except queue.Empty:
				time.sleep(0.1)

	def __del__(self):
		self.continue_running = False

	def _process_message(self, message):
		"""
		Process a single decorator message and put it into update queue
		:param message: A decorator message includes service name,
		functions start and end time and the timeout
		"""
		process_name = message['name']
		start_time = message['start_time']
		end_time = message['end_time']
		timeout = message['timeout']

		self.processes[process_name] = {
			'latest_start': start_time, 'latest_end': end_time, 'timeout': timeout
		}
		self.process_queue.put(self.processes.copy())
