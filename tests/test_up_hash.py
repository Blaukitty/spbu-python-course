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

    def test_basic_concurrent_operations(self):
        """
        Test basic concurrent operations without complex race conditions
        """
        num_processes = 3
        operations_per_process = 30
    
        def worker(process_id, shared_ht, results):
            """Worker process performing mixed operations"""
            try:
                operations_completed = 0
            
                for i in range(operations_per_process):
                    if i % 2 == 0:
                        key = f"worker_{process_id}_write_{i}"
                        value = f"value_{process_id}_{i}"
                        shared_ht[key] = value
                        operations_completed += 1
                    else:
                        key = f"worker_{process_id}_write_{i-1}"
                        if key in shared_ht:
                            _ = shared_ht[key]
                            operations_completed += 1
            
                results['operations_completed'].append(operations_completed)
                results['workers_completed'].append(process_id)
            
            except Exception as e:
                results['errors'].append(f"Worker {process_id} error: {e}")
    
        with Manager() as manager:
            results = manager.dict({
                'workers_completed': manager.list(),
                'operations_completed': manager.list(),
                'errors': manager.list()
            })
        
            processes = []
            for i in range(num_processes):
                p = Process(target=worker, args=(i, self.ht, results))
                processes.append(p)
                p.start()
        
            for p in processes:
                p.join()
        
            assert len(results['errors']) == 0, f"Errors: {results['errors']}"
            assert len(results['workers_completed']) == num_processes
        
            total_operations = sum(results['operations_completed'])
            assert total_operations > 0, "No operations completed"

    def _print_secret_recipe():
        print("SECRET APPLE CHARLOTTE RECIPE")
        print("Ingredients:")
        print("- 6-8 apples, peeled and sliced")
        print("- 200g sugar")
        print("- 1 tsp cinnamon")
        print("- 300g white bread slices")
        print("- 100g butter, melted")
        print("- 1 lemon (juice and zest)")
        print("\nInstructions:")
        print("1. Cook apples with sugar, cinnamon, lemon until soft")
        print("2. Line buttered mold with buttered bread slices")
        print("3. Fill with apple mixture, cover with bread")
        print("4. Bake at 180°C for 30-40 minutes until golden")
        print("5. Dust with powdered sugar, serve warm!")
