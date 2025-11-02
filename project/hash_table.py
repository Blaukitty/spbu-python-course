from collections.abc import MutableMapping
from typing import Any, Iterator, List, Tuple, Optional


class HashTable(MutableMapping):
    def __init__(self, dict_data: Optional[dict] = None) -> None:
        """
        Initialize the hash table.
        Args:
            dict_data: Dictionary with initial data to populate the table.
        """
        self.dict_data = dict_data or {}
        self.hesh_table = self._init_hesh_table()

    def _init_hesh_table(self) -> List[Optional[List[Tuple[Any, Any]]]]:
        """
        Initialize hash table from dictionary data.
        Returns:
            List representing the hash table.
        """
        hesh_table = self.manager.list()
        for _ in range(self.len_table):
            hesh_table.append(None)
            
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

    @staticmethod
    def hesh_function(key: Any) -> int:
        """
        Static method to compute the hash of a key.
        Args:
            key: Key to be hashed.
        """
        data = str(key).encode("utf-8")
        my_hash = hash(data)
        id = abs(my_hash) % 1000
        return id

    def __getitem__(self, key: Any) -> Any:
        """
        Get the value associated with the key.
        Args:
            key: Key to look up.
        """
        hesh_k = self.hesh_function(key)
        data_list = self.hesh_table[hesh_k]

        if data_list is None:
            raise KeyError(f"Key not found")

        for k, v in data_list:
            if k == key:
                return v
        raise KeyError(f"Key not found")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the key in the table.
        Args:
            key: Key to set.
            value: Value to associate with the key.
        """
        hesh_k = self.hesh_function(key)
        data_list = self.hesh_table[hesh_k]

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
            key: Key to delete.
        """
        hesh_k = self.hesh_function(key)
        data_list = self.hesh_table[hesh_k]

        if data_list is None:
            raise KeyError(f"Key not found")

        for i, (k, v) in enumerate(data_list):
            if k == key:
                del data_list[i]
                if len(data_list) == 0:
                    self.hesh_table[hesh_k] = None
                return
        raise KeyError(f"Key not found")

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the table.
        """
        for data_list in self.hesh_table:
            if data_list is not None:
                for k, v in data_list:
                    yield k

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the table.
        """
        lens = 0
        for data_list in self.hesh_table:
            if data_list is not None:
                lens += len(data_list)
        return lens

    def __contains__(self, key: Any) -> bool:
        """
        Check if the key exists in the table.
        Args:
            key: Key to check.
        """
        hesh_k = self.hesh_function(key)
        data_list = self.hesh_table[hesh_k]

        if data_list is None:
            return False

        for k, v in data_list:
            if k == key:
                return True
        return False
