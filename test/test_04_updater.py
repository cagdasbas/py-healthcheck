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

from healthcheck_python.service import PeriodicService
from healthcheck_python.updater import HealthCheckUpdater


@pytest.fixture(scope='module')
def input_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def output_queue():
	return mp.Queue()


@pytest.fixture(scope='module')
def updater_object(input_queue, output_queue):
	return HealthCheckUpdater(input_queue, output_queue)


def test_parse(updater_object):
	service1 = PeriodicService("service1")
	processes = updater_object.parse_message({'service1_key': service1.serialize()})
	assert "service1_key" in processes.keys()
	assert isinstance(processes['service1_key'], PeriodicService)
	assert processes['service1_key'].name == "service1"


def test_success(output_queue, updater_object):
	service1 = PeriodicService("service1")
	service1.add_health_point({'start_time': 1, 'end_time': 2, 'timeout': 3})
	updater_object._processes = {'test_service': service1}

	updater_object._check_health()
	message = output_queue.get(block=True, timeout=0.1)
	assert not message[1]['status']

	service2 = PeriodicService("service2")
	service2.add_health_point({'start_time': 1, 'end_time': time.time(), 'timeout': 10000})
	updater_object._processes = {'test_service': service2}

	updater_object._check_health()
	message = output_queue.get(block=True, timeout=0.1)
	assert message[1]['status']
