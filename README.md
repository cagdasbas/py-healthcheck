### A Health Check API Library for Multi Thread Python Apps
This library adds a health check REST API to your multithread apps. 
You can add decorators to your periodic running functions and library will track 
the function calls. This library supports ```multiprocessing``` threads.
You can fetch a single overall app status by fetching
```http://<ip>:<port>/health``` 
or detailed statuses of all service with fetching
```http://<ip>:<port>/health?v```

#### Usage
Set ```PY_HEALTH_CHECK_PORT``` environment variable and add the appropriate decorator to your periodic functions 
or class methods
```python
def run_continuously():
	while continue_running:
		run_once()
		time.sleep(1)

@py_healthcheck.periodic(service="my_service1", timeout=10)
def run_once():
	do_something()

class MyProcess(mp.Process):
	def run(self):
		while self.continue_running:
			self.do_the_thing_once()
			time.sleep(1)

	@py_healthcheck.periodic(service="MyProcessService", timeout=5)
	def do_the_thing_once(self):
		self.do_something()
```
With these wrappers, ```run_once()``` has to called every 10 seconds and ```MyProcess.do_the_thing_once()``` 
has to be called every 5 seconds. If at least one fails, the app status will be down.
```shell
$ curl http://localhost:8080/health
true
$ curl http://localhost:8080/health?v
{"status": true, "data": {"my_service1": {"latest_start": 1611137135.3203568, "latest_end": 1611137135.3203998, "timeout": 10},"MyProcessService": {"latest_start": 1611137135.3203568, "latest_end": 1611137135.3203998, "timeout": 5}}}
```

### TODO
- [ ] Unit tests
- [ ] Support different types of checks