import pytest

from healthcheck_python.utils.circular_queue import CircularQueue


@pytest.fixture(scope='function')
def queue():
	return CircularQueue(4)


def test_circular_queue(queue):
	queue.enqueue(1)
	queue.enqueue(2)
	queue.enqueue(3)
	queue.enqueue(4)
	assert queue.peek_tail() == 1
	queue.enqueue(5)
	assert queue.peek_tail() == 2
	queue.enqueue(6)
	assert queue.peek_tail() == 3


def test_mean(queue):
	queue.enqueue(2)
	queue.enqueue(3)
	queue.enqueue(4)
	assert 0.33 == pytest.approx(queue.mean_nonzero(), 0.1)
	queue.enqueue(5)
	assert 0.28 == pytest.approx(queue.mean_nonzero(), 0.1)
