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
from healthcheck_python.utils.utils import ServiceOperation


@pytest.fixture(scope='function')
def queue():
	return mp.Queue()


@healthcheck_python.periodic(timeout=3)
class TestClass:
	pass


def test_periodic_create(queue):
	config.message_queue = queue

	@healthcheck_python.periodic(service="service1", timeout=1)
	def test_function():
		x = 2 + 3

	test_function()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['op'] == ServiceOperation.CREATE
	assert call_args['timeout'] == 1

	TestClass()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "TestClass"
	assert call_args['op'] == ServiceOperation.CREATE
	assert call_args['timeout'] == 3


def test_periodic_add_health(queue):
	config.message_queue = queue

	@healthcheck_python.periodic(service="service1", timeout=1)
	@healthcheck_python.healthy(service="service1")
	def test_function():
		x = 2 + 3

	test_function()
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['op'] == ServiceOperation.ADD_HEALTH_POINT
	assert call_args['end_time'] != 0


def test_fps(queue):
	config.message_queue = queue

	@healthcheck_python.fps(service="service1")
	@healthcheck_python.periodic(service="service1", timeout=1)
	def test_function():
		x = 2 + 3

	test_function()
	queue.get(block=True, timeout=0.1)
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['start_time'] != 0
	assert call_args['op'] == ServiceOperation.ADD_FPS_POINT


def test_mark_done(queue):
	config.message_queue = queue

	@healthcheck_python.mark_done(service="service1")
	@healthcheck_python.periodic(service="service1")
	def test_function():
		x = 2 + 3

	test_function()
	queue.get(block=True, timeout=0.1)
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['op'] == ServiceOperation.MARK_DONE


def test_mark_ready(queue):
	config.message_queue = queue

	@healthcheck_python.mark_ready(service="service1")
	@healthcheck_python.periodic(service="service1")
	def test_function():
		x = 2 + 3

	test_function()
	queue.get(block=True, timeout=0.1)
	call_args = queue.get(block=True, timeout=0.1)
	assert call_args['name'] == "service1"
	assert call_args['op'] == ServiceOperation.MARK_READY
