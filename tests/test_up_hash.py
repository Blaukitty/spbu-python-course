import time
import pytest
from multiprocessing import Process, Manager
from project.up_hash import UpHashTable

class TestThreadSafeHashTable:
    """Test suite for thread-safe HashTable implementation using pytest"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initialize fresh HashTable before each test"""
        self.ht = UpHashTable(num_locks=4, len_table=50)

    def test_basic_functionality(self):
        """Test that all basic dictionary methods work correctly"""
        # Test set and get operations
        self.ht["key1"] = "value1"
        self.ht["key2"] = "value2"
        assert self.ht["key1"] == "value1"
        assert self.ht["key2"] == "value2"
        
        # Test contains operation
        assert "key1" in self.ht
        assert "key3" not in self.ht
        
        # Test length operation
        assert len(self.ht) == 2
        
        # Test delete operation
        del self.ht["key1"]
        assert "key1" not in self.ht
        assert len(self.ht) == 1
        
        # Test iteration
        self.ht["key3"] = "value3"
        keys = list(self.ht)
        assert set(keys) == {"key2", "key3"}

    def test_concurrent_writes_no_data_loss(self):
        """
        Test that no data is lost during concurrent write operations from multiple processes
        """
        num_processes = 5
        writes_per_process = 50
        
        def writer(process_id, shared_ht, results):
            """Process function that writes multiple key-value pairs"""
            successful_writes = 0
            for i in range(writes_per_process):
                key = f"key_{process_id}_{i}"
                value = f"value_{process_id}_{i}"
                try:
                    shared_ht[key] = value
                    successful_writes += 1
                except Exception as e:
                    results['errors'].append(f"Process {process_id} error: {e}")
            results['write_counts'].append(successful_writes)
        
        with Manager() as manager:
            results = manager.dict({
                'write_counts': manager.list(),
                'errors': manager.list()
            })
            
            processes = []
            for i in range(num_processes):
                p = Process(target=writer, args=(i, self.ht, results))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join()
            
            assert len(results['errors']) == 0
            total_writes = sum(results['write_counts'])
            assert len(self.ht) == total_writes
            
            for i in range(num_processes):
                for j in range(writes_per_process):
                    key = f"key_{i}_{j}"
                    expected_value = f"value_{i}_{j}"
                    assert self.ht[key] == expected_value

    def test_lock_correctness_high_contention(self):
        """
        Test that locks work correctly under high contention
        Uses minimal locks to maximize lock competition
        """
        num_processes = 8
        operations_per_process = 50
        
        high_contention_ht = UpHashTable(num_locks=2, len_table=10)
        
        def worker(process_id, shared_ht, results):
            """Worker process performing mixed operations under high lock contention"""
            try:
                for i in range(operations_per_process):
                    operation = i % 4
                    
                    if operation == 0:  # Write
                        key = f"key_{process_id}_{i}"
                        shared_ht[key] = f"value_{process_id}_{i}"
                    
                    elif operation == 1:  # Read
                        key = f"key_{process_id}_{i // 2}"
                        if key in shared_ht:
                            _ = shared_ht[key]
                    
                    elif operation == 2:  # Contains check
                        key = f"key_{process_id}_{i // 3}"
                        _ = key in shared_ht
                    
                    elif operation == 3:  # Delete
                        key = f"key_{process_id}_{i // 4}"
                        if key in shared_ht:
                            del shared_ht[key]
                
                results['workers_completed'].append(process_id)
            except Exception as e:
                results['errors'].append(f"Worker {process_id} error: {e}")
        
        with Manager() as manager:
            results = manager.dict({
                'workers_completed': manager.list(),
                'errors': manager.list()
            })
            
            processes = []
            for i in range(num_processes):
                p = Process(target=worker, args=(i, high_contention_ht, results))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join()
            
            assert len(results['errors']) == 0
            assert len(results['workers_completed']) == num_processes

    def test_concurrent_updates_race_condition_prevention(self):
        """
        Test that race conditions are prevented during concurrent updates
        Multiple processes increment the same counters
        """
        num_processes = 4
        updates_per_process = 25
        
        for i in range(5):
            self.ht[f"counter_{i}"] = 0
        
        def updater(process_id, shared_ht, results):
            """Process that performs read-modify-write operations on shared counters"""
            try:
                for _ in range(updates_per_process):
                    for i in range(5):
                        key = f"counter_{i}"
                        current = shared_ht[key]
                        shared_ht[key] = current + 1
                results['completed'].append(process_id)
            except Exception as e:
                results['errors'].append(f"Updater {process_id} error: {e}")
        
        with Manager() as manager:
            results = manager.dict({
                'completed': manager.list(),
                'errors': manager.list()
            })
            
            processes = []
            for i in range(num_processes):
                p = Process(target=updater, args=(i, self.ht, results))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join()
            
            assert len(results['errors']) == 0
            assert len(results['completed']) == num_processes
            
            expected_value = num_processes * updates_per_process
            for i in range(5):
                key = f"counter_{i}"
                assert self.ht[key] == expected_value, f"Race condition detected for {key}"

    def test_deadlock_prevention(self):
        """
        Test that the implementation is free from deadlocks
        Uses complex access patterns that could cause circular waiting
        """
        num_processes = 6
        operations_per_process = 30
        timeout_seconds = 10
        
        def complex_worker(process_id, shared_ht, results):
            """Process performing operations that could potentially cause deadlocks"""
            try:
                for i in range(operations_per_process):
                    keys = [f"key_{j}" for j in range(3)]
                    
                    for key in keys:
                        shared_ht[f"{key}_{process_id}_{i}"] = f"value_{process_id}_{i}"
                    
                    for key in keys:
                        other_key = f"{key}_{(process_id + 1) % num_processes}_{i // 2}"
                        if other_key in shared_ht:
                            _ = shared_ht[other_key]
                
                results['completed'].append(process_id)
            except Exception as e:
                results['errors'].append(f"Worker {process_id} error: {e}")
        
        with Manager() as manager:
            results = manager.dict({
                'completed': manager.list(),
                'errors': manager.list()
            })
            
            processes = []
            for i in range(num_processes):
                p = Process(target=complex_worker, args=(i, self.ht, results))
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join(timeout=timeout_seconds)
                assert not p.is_alive(), f"Process {p.pid} hung - possible deadlock"
            
            assert len(results['completed']) == num_processes
            assert len(results['errors']) == 0
