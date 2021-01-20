"""
Initializer for py-healthcheck
Creates three multiprocessing processes and queues between them
Listen on port env(PY_HEALTH_CHECK_PORT) and respond the health check requests

"""
import logging
import os
from multiprocessing import Queue

from py_healthcheck.api import HealthCheckApi
from py_healthcheck.decorators import periodic
from py_healthcheck.manager import HealthCheckManager

__all__ = ['periodic']

from py_healthcheck.updater import HealthCheckUpdater

message_queue = Queue()
process_queue = Queue(maxsize=1)
status_queue = Queue(maxsize=1)

HEALTH_CHECK_PORT = os.getenv("PY_HEALTH_CHECK_PORT", "8080")

if isinstance(HEALTH_CHECK_PORT, str) and \
		HEALTH_CHECK_PORT.isdecimal() and \
		1 < int(HEALTH_CHECK_PORT) < 65535:
	HEALTH_CHECK_PORT = int(HEALTH_CHECK_PORT)
else:
	HEALTH_CHECK_PORT = 8080

api = HealthCheckApi(HEALTH_CHECK_PORT, status_queue, daemon=True)
updater = HealthCheckUpdater(process_queue, status_queue, daemon=True)
manager = HealthCheckManager(message_queue, process_queue, daemon=True)

api.start()
updater.start()
manager.start()
logging.info("done init")
