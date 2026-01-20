"""
Garbage collection analyzer for studying cyclic reference collection.
"""

import gc
import sys
from typing import List, Dict, Any, Type
from collections import defaultdict


class GarbageCollectionAnalyzer:
    """
    Analyze garbage collection behavior, specifically for cyclic references.
    """
    
    def __init__(self):
        self.gc_enabled = gc.isenabled()
        self.original_flags = gc.get_debug()
    
    def enable_debug_mode(self):
        """
        Enable debug mode to track garbage collection.
        WARNING: This can slow down execution significantly!
        """
        gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE)
    
    def disable_debug_mode(self):
        """Restore original GC debug settings."""
        gc.set_debug(self.original_flags)
    
    def analyze_object_types(self) -> Dict[str, int]:
        """
        Count objects by type in memory.
        
        Returns:
            Dictionary mapping type name to count
        """
        type_counts = defaultdict(int)
        
        for obj in gc.get_objects():
            type_name = type(obj).__name__
            type_counts[type_name] += 1
        
        return dict(type_counts)
    
    def find_objects_by_type(self, cls: Type) -> List[Any]:
        """
        Find all instances of a specific class.
        
        Args:
            cls: Class to search for
            
        Returns:
            List of instances
        """
        return [obj for obj in gc.get_objects() if isinstance(obj, cls)]
    
    def analyze_referrers(self, obj: Any, max_depth: int = 3) -> Dict[str, Any]:
        """
        Analyze what objects reference a given object.
        
        Args:
            obj: Object to analyze
            max_depth: Maximum depth to traverse
            
        Returns:
            Analysis results
        """
        referrers = gc.get_referrers(obj)
        
        analysis = {
            'object': str(obj),
            'type': type(obj).__name__,
            'size_bytes': sys.getsizeof(obj),
            'referrer_count': len(referrers),
            'referrers': []
        }
        
        for ref in referrers[:10]:  # Limit to 10 to avoid huge output
            analysis['referrers'].append({
                'type': type(ref).__name__,
                'size_bytes': sys.getsizeof(ref),
                'id': id(ref)
            })
        
        return analysis
    
    def detect_cycles(self, obj: Any) -> bool:
        """
        Check if an object is part of a reference cycle.
        
        Args:
            obj: Object to check
            
        Returns:
            True if object is part of a cycle
        """
        visited = set()
        
        def _has_cycle(current, path):
            if id(current) in path:
                return True
            
            if id(current) in visited:
                return False
            
            visited.add(id(current))
            path.add(id(current))
            
            referents = gc.get_referents(current)
            for ref in referents:
                if _has_cycle(ref, path.copy()):
                    return True
            
            return False
        
        return _has_cycle(obj, set())
    
    def compare_collection_strategies(
        self, 
        create_objects_func, 
        num_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Compare memory behavior with and without manual GC.
        
        Args:
            create_objects_func: Function that creates objects with circular refs
            num_iterations: Number of test iterations
            
        Returns:
            Comparison results
        """
        results = {
            'with_manual_gc': [],
            'without_manual_gc': []
        }
        
        # Test WITH manual GC
        gc.collect()
        start_objects = len(gc.get_objects())
        
        for i in range(num_iterations):
            create_objects_func()
            gc.collect()  # Manual collection
            current_objects = len(gc.get_objects())
            results['with_manual_gc'].append(current_objects - start_objects)
        
        # Test WITHOUT manual GC (relying on automatic collection)
        gc.collect()  # Clean slate
        start_objects = len(gc.get_objects())
        
        for i in range(num_iterations):
            create_objects_func()
            # Don't call gc.collect() - let Python decide
            current_objects = len(gc.get_objects())
            results['without_manual_gc'].append(current_objects - start_objects)
        
        # Final cleanup
        gc.collect()
        
        # Calculate averages
        results['avg_with_gc'] = sum(results['with_manual_gc']) / len(results['with_manual_gc'])
        results['avg_without_gc'] = sum(results['without_manual_gc']) / len(results['without_manual_gc'])
        
        return results
    
    def generate_report(self, obj_classes: List[Type] = None, return_data: bool = True):
        """
        Generate a comprehensive GC report.
        
        Args:
            obj_classes: Specific classes to report on (optional)
            return_data: If True, return data instead of printing (default: True)
        
        Returns:
            Dict with report data
        """
        gc_count = gc.get_count()
        thresholds = gc.get_threshold()
        total_objects = len(gc.get_objects())
        type_counts = self.analyze_object_types()
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        
        report_data = {
            'gc_enabled': gc.isenabled(),
            'gc_thresholds': thresholds,
            'gc_collections': gc_count,
            'total_objects': total_objects,
            'top_types': sorted_types[:10],
            'specific_classes': {}
        }
        
        if obj_classes:
            for cls in obj_classes:
                instances = self.find_objects_by_type(cls)
                report_data['specific_classes'][cls.__name__] = len(instances)
        
        return report_data
