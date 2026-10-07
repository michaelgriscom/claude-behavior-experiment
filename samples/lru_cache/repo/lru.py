from collections import OrderedDict


class LRUCache:
    """Fixed-size cache that evicts the least recently *used* key.

    Both get() and put() count as a use.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()

    def get(self, key, default=None):
        if key not in self._data:
            return default
        return self._data[key]

    def put(self, key, value) -> None:
        self._data[key] = value
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __len__(self) -> int:
        return len(self._data)
