"""Memory monitoring utilities."""

import psutil
import os


class MemoryMonitor:
    """Monitor process memory usage."""
    
    def __init__(self):
        self.snapshots = []
    
    def take_snapshot(self, label: str = ""):
        """
        Take a memory snapshot.
        
        Args:
            label: Description of this snapshot point
        """
        snapshot = {
            'label': label,
            'process_memory_mb': self.get_process_memory_mb()
        }
        self.snapshots.append(snapshot)
        return snapshot
    
    @staticmethod
    def get_process_memory_mb() -> float:
        """Get current process memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
