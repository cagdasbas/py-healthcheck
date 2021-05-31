import pytest

from healthcheck_python.service import PeriodicService


@pytest.fixture(scope="function")
def service():
	service = PeriodicService("service1", timeout=3)
	service.add_fps_point({'start_time': 1, 'end_time': 2})
	return service


def test_serialize(service):
	_dict = service.serialize()
	assert _dict['_last_start'] == 1
	assert _dict['_last_end'] == 2
	assert _dict['_timeout'] == 3

	assert _dict['_queue']['queue'][0] == 1


def test_deserialize(service):
	_dict = service.serialize()

	new_service = PeriodicService.parse_from_dict(_dict)
	assert new_service._last_start == 1
	assert new_service._last_end == 2
	assert new_service._timeout == 3
	assert new_service._queue.head == 0
	assert new_service._queue.peek_head() == 1
