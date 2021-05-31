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
import multiprocessing as mp
import time

import pytest

from healthcheck_python.api import HealthCheckApi
from healthcheck_python.release import __version__


@pytest.fixture(scope='module')
def queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def api_object(queue):
	return HealthCheckApi("0.0.0.0", 1234, queue)


def test_index(api_object):
	assert api_object._index() == f"Hello there! I'm healthcheck-python v{__version__}"


def test_failed_response(api_object):
	response = api_object._health()
	assert response == {'status': False}


def test_healthy(queue, api_object):
	queue.put((time.time() + 5, {'status': True, 'ready': True, 'services': {}}))
	queue.put((time.time() + 5, {'status': True, 'ready': True, 'services': {}}))
	time.sleep(0.1)
	response = api_object._health()
	assert response == {'status': True}

	response = api_object._ready()
	assert response == {'ready': True}
