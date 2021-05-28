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

import healthcheck_python
from healthcheck_python import config


@pytest.fixture(scope='module')
def queue():
	return mp.Queue()


def test_periodic_wo_fps(queue):
	config.message_queue = queue

	@healthcheck_python.periodic(service="service1", timeout=1)
	def test_function():
		x = 2 + 3

	test_function()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['start_time'] == 0
	assert call_args['timeout'] == 1
	assert call_args['name'] == "service1"


def test_periodic_fps(queue):
	config.message_queue = queue

	@healthcheck_python.periodic(service="service1", calc_fps=True, timeout=1)
	def test_function():
		x = 2 + 3

	test_function()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['start_time'] != 0
	assert call_args['timeout'] == 1


def test_fps(queue):
	config.message_queue = queue

	@healthcheck_python.fps(service="service1")
	def test_function():
		x = 2 + 3

	test_function()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['start_time'] != 0
