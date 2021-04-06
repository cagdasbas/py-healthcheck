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
import logging
import sys


class CircularQueue:
	"""
	A circular queue implementation
	only enqueues data and allow peeking the first added element
	"""

	def __init__(self, k):
		self.k = k
		self.queue = [0.0] * k
		self.head = -1
		self.tail = 0
		self.first_full = False

	def enqueue(self, data):
		"""
		Add new data to queue
		:param data: new data to add
		"""
		self.head = (self.head + 1) % self.k
		if self.first_full:
			self.tail += 1
		if self.head == self.k - 1:
			self.first_full = True
		self.queue[self.head] = data

	def __len__(self) -> int:
		if self.first_full:
			return self.k
		return self.head + 1

	def peek_tail(self):
		"""
		Get the data added earliest
		:return: earliest added data
		"""
		return self.queue[self.tail]

	def peek_head(self):
		"""
		Get the data added earliest
		:return: earliest added data
		"""
		return self.queue[self.head]

	def diff_head_tail(self) -> float:
		"""
		Get the head and tail elements difference in time
		:return: diff in seconds
		"""
		diff = sys.float_info.epsilon
		if self.head == -1:
			return diff
		logging.info(
			f"len {len(self)}, head: {self.queue[self.head]}, tail: {self.queue[self.tail]}, diff {self.queue[self.head] - self.queue[self.tail]}")
		return self.queue[self.head] - self.queue[self.tail] + diff
