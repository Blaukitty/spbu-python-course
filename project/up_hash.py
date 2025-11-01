import threading
from collections.abc import MutableMapping
from typing import Any, Iterator, List, Tuple, Optional
from multiprocessing import Manager


class HashTable(MutableMapping):
    def __init__(self, num_locks: int = 20, len_table: int = 1000, dict_data: Optional[dict] = None) -> None:
        """
        Initialize the hash table.
        Args:
            dict_data: Dictionary with initial data to populate the table.
        """
        self.dict_data = dict_data or {}
        self.num_locks = num_locks
        self.len_table = len_table
        self.manager = Manager()
        self.hesh_table = self._init_hesh_table()
        
    def _init_hesh_table(self) -> List[Optional[List[Tuple[Any, Any]]]]:
        """
        Initialize hash table from dictionary data.
        Returns:
            List representing the hash table.
        """
        hesh_table: List[Optional[List[Tuple[Any, Any]]]] = self.manager.list([None] * self.len_table)
        self._lock = [threading.Lock() for _ in range(self.num_locks)]
        
        for key, value in self.dict_data.items():
            k = self._get_hesh(key)
            lock_k = self._get_lock(key)
            with self._lock[lock_k]:
                exist_list = hesh_table[k]
                if exist_list is not None:
                    n_list = self.manager.list(exist_list)
                    n_list.append((key, value))
                    hesh_table = n_list
                else:
                    hesh_table[k] = self.manager.list[(key, value)]
        return hesh_table
    
    def _get_lock(self, key):
        """Get lock index for a key"""
        return hash(key) % self.num_locks
        
    def _get_hesh(self, key):
        """Get index for a key""" 
        return abs(hash(key))% self.len_table
    
    def __getitem__(self, key: Any) -> Any:
        """
        Get the value associated with the key.
        Args:
            key: Key to look up.
        """
        hesh_k = self._get_hesh(key)
        lock_k = self._get_lock(key)

        with self._lock[lock_k]:
            data_list = self.hesh_table[hesh_k]
            if data_list is None:
                raise KeyError(f"Key not found")

            for k, v in data_list:
                if k == key:
                    return v

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the key in the table.
        Args:
            key: Key to set.
            value: Value to associate with the key.
        """
        hesh_k = self._get_hesh(key)
        lock_k = self._get_lock(key)

        with self._lock[lock_k]:
            data_list = self.hesh_table[hesh_k]
            if data_list is None:
                self.hesh_table[hesh_k] = [(key, value)]
                return
            
            n_list = self.manager.list()
            n_key_k_key = False
            for k, v in data_list:
                if k == key:
                    n_list.append((key, value))
                    n_key_k_key = True
                else:
                    n_list.append((k, v))
            if not n_key_k_key:
                n_list.append((key, value))
        
            self.hesh_table[hesh_k] = n_list

    def __delitem__(self, key: Any) -> None:
        """
        Delete the key-value pair from the table.
        Args:
            key: Key to delete.
        """
        hesh_k = self._get_hesh(key)
        lock_k = self._get_lock(key)

        with self._lock[lock_k]:
            data_list = self.hesh_table[hesh_k]
            if data_list is None:
                raise KeyError(f"Key not found")

            n_list = self.manager.list()
            fckn_key = False
            for k, v in data_list:
                if k == key:
                    fckn_key = False
                else:
                    n_list.append((k, v))
            if not fckn_key:
                raise KeyError(f"Key not found") 
            if len(n_list) == 0:
                self.hesh_table[hesh_k] = None
            else:
                self.hesh_table[hesh_k] = n_list       
            

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the table.
        """
        frozen_locks = []
        try:
            for lock in self._lock:
                lock.acquire()
                frozen_locks.append(lock)

            for data_list in self.hesh_table:
                if data_list is not None:
                    for k, v in data_list:
                        yield k
        finally:
            for lock in reversed(frozen_locks):
                lock.release()

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the table.
        """
        lens = 0
        frozen_locks = []
        try:
            for lock in self._lock:
                lock.acquire()
                frozen_locks.append(lock)

            for data_list in self.hesh_table:
                if data_list is not None:
                    lens += len(data_list)
            return lens
        finally:
            for lock in reversed(frozen_locks):
                lock.release()

    def __contains__(self, key: Any) -> bool:
        """
        Check if the key exists in the table.
        Args:
            key: Key to check.
        """
        hesh_k = self._get_hesh(key)
        lock_k = self._get_lock(key)

        with self._lock[lock_k]:
            data_list = self.hesh_table[hesh_k]
            if data_list is None:
                return False

            for k, v in data_list:
                if k == key:
                    return True
            return False
