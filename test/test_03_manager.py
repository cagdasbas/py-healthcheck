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
from healthcheck_python.utils.utils import ServiceOperation, ServiceStatus


@pytest.fixture(scope='module')
def input_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def output_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def manager_object(input_queue, output_queue):
	return HealthCheckManager(input_queue, output_queue)


def test_create(output_queue, manager_object):
	manager_object._process_message(
		{'type': PeriodicService, 'op': ServiceOperation.CREATE, 'name': 'test_service', 'timeout': 3}
	)
	manager_object._process_message(
		{'type': PeriodicService, 'op': ServiceOperation.ADD_HEALTH_POINT, 'name': 'test_service', 'end_time': 2}
	)
	message = output_queue.get(block=True, timeout=0.1)
	assert message[1]['test_service']['_last_end'] == 2

	manager_object._process_message(
		{'type': PeriodicService, 'op': ServiceOperation.ADD_FPS_POINT, 'name': 'test_service', 'start_time': 1,
		 'end_time': 3}
	)
	message = output_queue.get(block=True, timeout=0.1)
	assert message[1]['test_service']['_last_start'] == 1
	assert message[1]['test_service']['_last_end'] == 3

	manager_object._process_message(
		{'type': PeriodicService, 'op': ServiceOperation.MARK_READY, 'name': 'test_service', }
	)
	message = output_queue.get(block=True, timeout=0.1)
	assert message[1]['test_service']['global_status'] == ServiceStatus.READY

	manager_object._process_message(
		{'type': PeriodicService, 'op': ServiceOperation.MARK_DONE, 'name': 'test_service'}
	)
	message = output_queue.get(block=True, timeout=0.1)
	assert message[1]['test_service']['global_status'] == ServiceStatus.DONE
