import threading
from collections.abc import MutableMapping
from multiprocessing import Manager
from multiprocessing.managers import ListProxy
from typing import Any, Iterator, List, Optional, Tuple, Union


class HashTable(MutableMapping):
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

        Args:
            num_locks: Number of locks for fine-grained synchronization
            len_table: Size of the hash table
            dict_data: Initial data to populate the table
        """
        self.dict_data = dict_data or {}
        self.num_locks = num_locks
        self.len_table = len_table
        self.manager = Manager()
        self.hesh_table: Union[
            ListProxy,
            List[Optional[List[Tuple[Any, Any]]]]
        ] = self._init_hesh_table()

    def _init_hesh_table(
        self
    ) -> Union[ListProxy, List[Optional[List[Tuple[Any, Any]]]]]:
        """
        Initialize hash table from dictionary data.

        Returns:
            List representing the hash table
        """
        hesh_table: ListProxy = self.manager.list([None] * self.len_table)
        self._lock = [threading.Lock() for _ in range(self.num_locks)]

        for key, value in self.dict_data.items():
            bucket_index = self._get_bucket_index(key)
            lock_index = self._get_lock_index(key)
            with self._lock[lock_index]:
                existing_list = hesh_table[bucket_index]
                if existing_list is not None:
                    new_list = self.manager.list(existing_list)
                    new_list.append((key, value))
                    hesh_table[bucket_index] = new_list
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

        Args:
            key: Key to look up

        Returns:
            Value associated with the key

        Raises:
            KeyError: If key is not found
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                raise KeyError(f"Key not found")

            for stored_key, value in data_list:
                if stored_key == key:
                    return value

            raise KeyError(f"Key not found")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the key in the table.

        Args:
            key: Key to set
            value: Value to associate with the key
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]

            if data_list is None:
                self.hesh_table[bucket_index] = self.manager.list([(key, value)])
                return

            new_list = self.manager.list()
            key_found = False
            for stored_key, stored_value in data_list:
                if stored_key == key:
                    new_list.append((key, value))
                    key_found = True
                else:
                    new_list.append((stored_key, stored_value))

            if not key_found:
                new_list.append((key, value))

            self.hesh_table[bucket_index] = new_list

    def __delitem__(self, key: Any) -> None:
        """
        Delete the key-value pair from the table.

        Args:
            key: Key to delete

        Raises:
            KeyError: If key is not found
        """
        bucket_index = self._get_bucket_index(key)
        lock_index = self._get_lock_index(key)

        with self._lock[lock_index]:
            data_list = self.hesh_table[bucket_index]
            if data_list is None:
                raise KeyError(f"Key not found")

            new_list = self.manager.list()
            key_found = False
            for stored_key, stored_value in data_list:
                if stored_key == key:
                    key_found = True
                else:
                    new_list.append((stored_key, stored_value))

            if not key_found:
                raise KeyError(f"Key not found")

            if len(new_list) == 0:
                self.hesh_table[bucket_index] = None
            else:
                self.hesh_table[bucket_index] = new_list

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the table.

        Returns:
            Iterator over all keys
        """
        acquired_locks = []
        try:
            for lock in self._lock:
                lock.acquire()
                acquired_locks.append(lock)

            for data_list in self.hesh_table:
                if data_list is not None:
                    for key, _ in data_list:
                        yield key
        finally:
            for lock in reversed(acquired_locks):
                lock.release()

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the table.

        Returns:
            Number of key-value pairs
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

        Args:
            key: Key to check

        Returns:
            True if key exists, False otherwise
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

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Get value for key, return default if key not found.

        Args:
            key: Key to look up
            default: Default value to return if key not found

        Returns:
            Value or default
        """
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        """Remove all items from the hash table."""
        acquired_locks = []
        try:
            for lock in self._lock:
                lock.acquire()
                acquired_locks.append(lock)

            for i in range(self.len_table):
                self.hesh_table[i] = None
        finally:
            for lock in reversed(acquired_locks):
                lock.release()
