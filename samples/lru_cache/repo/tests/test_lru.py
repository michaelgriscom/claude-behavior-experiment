from lru import LRUCache


def test_put_and_get():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("missing", "dflt") == "dflt"


def test_evicts_oldest_insert():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.get("a") is None
    assert len(cache) == 2


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # "a" is now most recently used, so "b" should be evicted
    cache.put("c", 3)
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3
