"""
py-healthcheck updater
"""
import multiprocessing as mp
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
				self._processes = message
			except queue.Empty:
				pass

			self._check_health()
			time.sleep(0.5)

	def __del__(self):
		self.continue_running = False

	def _check_health(self):
		"""
		check every services ending time to current time
		Every service should ended within defined timeout interval
		Free the status queue and put the latest status.
		"""
		call_time = time.time()
		self.index += 1
		status = True
		for _, value in self._processes.items():
			end_time = value['latest_end']
			timeout = value['timeout']
			if call_time - end_time > timeout:
				status = False
				break
		while not self._status_queue.empty():
			self._status_queue.get()
		self._status_queue.put({'status': status, 'data': self._processes})
