### A Health Check API Library for Multiprocessing Python Apps

![passing](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/passing.json)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/coverage.json)
![version](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cagdasbas/07e196561fb7496e619da3ef402209a6/raw/version.json)
[![license](https://img.shields.io/badge/license-Apache%202-blue)](LICENSE)

This library adds a health check REST API to your multiprocessing apps. You can add decorators to your periodic running
functions and library will track the function calls. This library supports ```multiprocessing``` threads. You can fetch
a single overall app status by fetching
```http://<ip>:<port>/health```, a single overall app readiness by fetching
```http://<ip>:<port>/ready```, or detailed statuses of all service with fetching
```http://<ip>:<port>/health?v```
```http://<ip>:<port>/ready?v```

#### Usage

Set ```PY_HEALTH_CHECK_HOST``` and ```PY_HEALTH_CHECK_PORT``` environment variable and add the appropriate decorator to
your periodic functions or class methods

```python
import time
import multiprocessing as mp

import healthcheck_python


def run_continuously():
	while True:
		run_once()
		time.sleep(1)


@healthcheck_python.periodic(service="my_service1", timeout=10)
@healthcheck_python.healthy(service="my_service1")
def run_once():
	do_something()


@healthcheck_python.periodic(timeout=5)
class MyProcess(mp.Process):

	def __init__(self, queue):
		super().__init__()
		self.queue = queue

		self.continue_running = True
		self.var = 0

	def run(self):
		self.init()
		while self.continue_running:
			self.do_the_thing_once()
			time.sleep(1)

	@healthcheck_python.healthy
	def do_the_thing_once(self):
		self.do_something()

	@healthcheck_python.mark_ready
	def init(self):
		self.var = 1

	@healthcheck_python.mark_done
	def cleanup(self):
		self.queue.close()
```

With these wrappers, ```run_once()``` has to called every 10 seconds and ```MyProcess.do_the_thing_once()```
has to be called every 5 seconds. If at least one fails, the app status will be down.

```shell
$ curl http://localhost:8080/health
{"status": true}
$ curl http://localhost:8080/health?v
{"status": true, "ready": false, "services": {"my_service1": {"ready", false, "latest_start": 1611137135.3203568, "latest_end": 1611137135.3203998, "fps":0, "timeout": 10},"MyProcess": {"ready":true, "latest_start": 1611137135.3203568, "latest_end": 1611137135.3203998, "fps":0, "timeout": 5}}}
```