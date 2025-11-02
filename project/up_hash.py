import threading
from collections.abc import MutableMapping
from multiprocessing import Manager
from typing import Any, Iterator, List, Optional, Tuple


class UpHashTable(MutableMapping):
    """
    A thread-safe hash table implementation using multiprocessing Manager
    for inter-process communication with fine-grained locking.
    """

    def __init__(
        self,
        num_locks: int = 20,
        len_table: int = 1000,
        dict_data: Optional[dict] = None
    ) -> None:
        """
        Initialize the hash table.
        """
        self.dict_data = dict_data or {}
        self.num_locks = num_locks
        self.len_table = len_table
        self.manager = Manager()
        self.hesh_table = self._init_hesh_table()
        
    def _init_hesh_table(self) -> Any:
        """
        Initialize hash table from dictionary data.
        """
        hesh_table = self.manager.list()
        for _ in range(self.len_table):
            hesh_table.append(None)
            
        self._lock = [self.manager.Lock() for _ in range(self.num_locks)]

        for key, value in self.dict_data.items():
            bucket_index = self._get_bucket_index(key)
            lock_index = self._get_lock_index(key)
            with self._lock[lock_index]:
                existing_list = hesh_table[bucket_index]
                if existing_list is not None:
                    new_list = list(existing_list)
                    for i, (k, v) in enumerate(new_list):
                        if k == key:
                            new_list[i] = (key, value)
                            break
                    else:
                        new_list.append((key, value))
                    hesh_table[bucket_index] = self.manager.list(new_list)
                else:
                    hesh_table[bucket_index] = self.manager.list([(key, value)])

        return hesh_table

    def _get_lock_index(self, key: Any) -> int:
        """Get lock index for a key."""
        return hash(key) % self.num_locks

    def _get_bucket_index(self, key: Any) -> int:
        """Get bucket index for a key."""
        return abs(hash(key)) % self.len_table

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value associated with the key.
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                raise KeyError(f"Key '{key}' not found")

            for stored_key, value in data_list:
                if stored_key == key:
                    return value

            raise KeyError(f"Key '{key}' not found")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the key in the table.
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                self.hesh_table[bucket_index] = self.manager.list([(key, value)])
                return

            items = list(data_list)
            key_found = False
            
            for i, (stored_key, stored_value) in enumerate(items):
                if stored_key == key:
                    items[i] = (key, value)
                    key_found = True
                    break

            if not key_found:
                items.append((key, value))

            self.hesh_table[bucket_index] = self.manager.list(items)

    def __delitem__(self, key: Any) -> None:
        """
        Delete the key-value pair from the table.
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                raise KeyError(f"Key '{key}' not found")

            new_list = self.manager.list()
            key_found = False
            
            for stored_key, stored_value in data_list:
                if stored_key == key:
                    key_found = True
                else:
                    new_list.append((stored_key, stored_value))

            if not key_found:
                raise KeyError(f"Key '{key}' not found")

            if len(new_list) == 0:
                self.hesh_table[bucket_index] = None
            else:
                self.hesh_table[bucket_index] = new_list

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the table.
        """
        acquired_locks = []
        try:
            for i in range(self.num_locks):
                self._lock[i].acquire()
                acquired_locks.append(i)

            for data_list in self.hesh_table:
                if data_list is not None:
                    for key, _ in data_list:
                        yield key
        finally:
            for lock_index in reversed(acquired_locks):
                self._lock[lock_index].release()

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the table.
        """
        count = 0
        acquired_locks = []
        try:
            for lock in self._lock:
                lock.acquire()
                acquired_locks.append(lock)

            for data_list in self.hesh_table:
                if data_list is not None:
                    count += len(data_list)
            return count
        finally:
            for lock in reversed(acquired_locks):
                lock.release()

    def __contains__(self, key: Any) -> bool:
        """
        Check if the key exists in the table.
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                return False

            for stored_key, _ in data_list:
                if stored_key == key:
                    return True
            return False
