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

import pytest

from healthcheck_python.manager import HealthCheckManager
from healthcheck_python.service.periodic_service import PeriodicService


@pytest.fixture(scope='module')
def input_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def output_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def manager_object(input_queue, output_queue):
	return HealthCheckManager(input_queue, output_queue)


def test_success(output_queue, manager_object):
	manager_object._process_message(
		{'type': PeriodicService, 'name': 'test_service', 'start_time': 1, 'end_time': 2, 'timeout': 3}
	)
	message = output_queue.get(block=True, timeout=0.1)
	assert message['test_service']['_last_end'] == 2
