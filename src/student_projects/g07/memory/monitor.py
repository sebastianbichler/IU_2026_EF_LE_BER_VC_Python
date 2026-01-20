"""
Memory monitoring utilities for tracking object lifecycles and memory usage.
"""

import gc
import sys
import tracemalloc
from functools import wraps
from typing import Any, Callable, Dict, List
import psutil
import os


class MemoryMonitor:
    """
    Monitor memory usage and garbage collection behavior.
    """
    
    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []
        self.tracking_enabled = False
    
    def start_tracking(self):
        """Start memory tracking."""
        tracemalloc.start()
        self.tracking_enabled = True
    
    def stop_tracking(self):
        """Stop memory tracking."""
        if self.tracking_enabled:
            tracemalloc.stop()
            self.tracking_enabled = False
    
    def take_snapshot(self, label: str = ""):
        """
        Take a memory snapshot.
        
        Args:
            label: Description of this snapshot point
        """
        if not self.tracking_enabled:
            self.start_tracking()
        
        # Get memory statistics
        snapshot = {
            'label': label,
            'tracemalloc': tracemalloc.take_snapshot(),
            'process_memory_mb': self.get_process_memory_mb(),
            'gc_stats': gc.get_stats(),
            'gc_count': gc.get_count(),
            'object_count': len(gc.get_objects())
        }
        
        self.snapshots.append(snapshot)
        return snapshot
    
    @staticmethod
    def get_process_memory_mb() -> float:
        """Get current process memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def compare_snapshots(self, idx1: int = 0, idx2: int = -1) -> Dict[str, Any]:
        """
        Compare two snapshots and return memory growth data.
        
        Args:
            idx1: Index of first snapshot
            idx2: Index of second snapshot
            
        Returns:
            Dictionary with comparison data, or None if insufficient snapshots
        """
        if len(self.snapshots) < 2:
            return None
        
        snap1 = self.snapshots[idx1]
        snap2 = self.snapshots[idx2]
        
        # Process memory
        mem_diff = snap2['process_memory_mb'] - snap1['process_memory_mb']
        
        # Object count
        obj_diff = snap2['object_count'] - snap1['object_count']
        
        # GC collections
        gc1, gc2 = snap1['gc_count'], snap2['gc_count']
        
        return {
            'label_before': snap1['label'],
            'label_after': snap2['label'],
            'memory_before_mb': snap1['process_memory_mb'],
            'memory_after_mb': snap2['process_memory_mb'],
            'memory_diff_mb': mem_diff,
            'objects_before': snap1['object_count'],
            'objects_after': snap2['object_count'],
            'objects_diff': obj_diff,
            'gc_gen0_diff': gc2[0] - gc1[0],
            'gc_gen1_diff': gc2[1] - gc1[1],
            'gc_gen2_diff': gc2[2] - gc1[2]
        }
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current memory statistics.
        
        Returns:
            Dictionary with current memory stats
        """
        return {
            'process_memory_mb': self.get_process_memory_mb(),
            'objects_tracked': len(gc.get_objects()),
            'gc_collections': gc.get_count(),
            'gc_thresholds': gc.get_threshold()
        }
    
    def find_circular_references(self) -> List[Any]:
        """
        Find objects with circular references.
        
        Returns:
            List of objects involved in reference cycles
        """
        gc.collect()  # Force collection first
        return gc.garbage
    
    def get_circular_refs_report(self) -> Dict[str, Any]:
        """Get report on circular references found.
        
        Returns:
            Dictionary with circular reference analysis
        """
        garbage = self.find_circular_references()
        
        return {
            'has_garbage': len(garbage) > 0,
            'garbage_count': len(garbage),
            'garbage_objects': [
                {'type': str(type(obj)), 'size_bytes': sys.getsizeof(obj)}
                for obj in garbage[:10]
            ]
        }


def track_memory(func: Callable) -> Callable:
    """
    Decorator to track memory usage of a function.
    
    Usage:
        @track_memory
        def create_large_family_tree():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        monitor = MemoryMonitor()
        
        # Before
        gc.collect()
        monitor.start_tracking()
        snapshot_before = monitor.take_snapshot(f"Before {func.__name__}")
        
        # Execute
        result = func(*args, **kwargs)
        
        # After
        snapshot_after = monitor.take_snapshot(f"After {func.__name__}")
        monitor.compare_snapshots(0, 1)
        monitor.stop_tracking()
        
        return result
    
    return wrapper
