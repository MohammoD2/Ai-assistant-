"""
Memory Manager - The Hippocampus of the AI Assistant
=================================================

This module handles:
- Short-term memory (working memory)
- Long-term memory (persistent storage)
- Memory consolidation
- Memory retrieval and search
- Memory cleanup and optimization
"""

import json
import os
import pickle
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib

class MemoryManager:
    """
    Manages memory storage and retrieval for the AI assistant.
    Works like the hippocampus of the human brain.
    """
    
    def __init__(self, memory_dir: str = "data/memory"):
        """Initialize the memory manager."""
        self.logger = logging.getLogger(__name__)
        self.memory_dir = memory_dir
        
        # Create memory directory if it doesn't exist
        os.makedirs(memory_dir, exist_ok=True)
        
        # Memory storage
        self.short_term_memory = deque(maxlen=1000)  # Working memory
        self.long_term_memory = {}  # Persistent memory
        self.memory_index = defaultdict(list)  # Search index
        
        # Memory statistics
        self.memory_stats = {
            'total_memories': 0,
            'short_term_count': 0,
            'long_term_count': 0,
            'last_consolidation': datetime.now(),
            'consolidation_count': 0
        }
        
        # Load existing memories
        self._load_memories()
    
    def store_interaction(self, interaction: Dict[str, Any]):
        """Store an interaction in short-term memory."""
        memory_item = {
            'id': self._generate_memory_id(interaction),
            'type': 'interaction',
            'data': interaction,
            'timestamp': datetime.now(),
            'access_count': 0,
            'importance': self._calculate_importance(interaction)
        }
        
        self.short_term_memory.append(memory_item)
        self.memory_stats['short_term_count'] = len(self.short_term_memory)
        self.memory_stats['total_memories'] += 1
        
        # Index the memory for search
        self._index_memory(memory_item)
        
        self.logger.debug(f"Stored interaction in short-term memory: {memory_item['id']}")
    
    def store_task_result(self, task: Dict, result: Dict):
        """Store a task result in memory."""
        memory_item = {
            'id': self._generate_memory_id(task),
            'type': 'task_result',
            'data': {
                'task': task,
                'result': result
            },
            'timestamp': datetime.now(),
            'access_count': 0,
            'importance': self._calculate_importance({'task': task, 'result': result})
        }
        
        self.short_term_memory.append(memory_item)
        self.memory_stats['short_term_count'] = len(self.short_term_memory)
        self.memory_stats['total_memories'] += 1
        
        # Index the memory for search
        self._index_memory(memory_item)
        
        self.logger.debug(f"Stored task result in memory: {memory_item['id']}")
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search memories for relevant information.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of relevant memories
        """
        query_lower = query.lower()
        relevant_memories = []
        
        # Search in short-term memory
        for memory in self.short_term_memory:
            relevance_score = self._calculate_relevance(memory, query_lower)
            if relevance_score > 0.1:  # Threshold for relevance
                memory['relevance_score'] = relevance_score
                memory['access_count'] += 1
                relevant_memories.append(memory)
        
        # Search in long-term memory
        for memory_id, memory in self.long_term_memory.items():
            relevance_score = self._calculate_relevance(memory, query_lower)
            if relevance_score > 0.1:
                memory['relevance_score'] = relevance_score
                memory['access_count'] += 1
                relevant_memories.append(memory)
        
        # Sort by relevance and recency
        relevant_memories.sort(key=lambda x: (
            x['relevance_score'], 
            x['timestamp']
        ), reverse=True)
        
        # Return top results
        return relevant_memories[:limit]
    
    def get_recent_memories(self, hours: int = 24, limit: int = 20) -> List[Dict]:
        """Get recent memories from the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_memories = []
        
        # Check short-term memory
        for memory in self.short_term_memory:
            if memory['timestamp'] >= cutoff_time:
                recent_memories.append(memory)
        
        # Check long-term memory
        for memory in self.long_term_memory.values():
            if memory['timestamp'] >= cutoff_time:
                recent_memories.append(memory)
        
        # Sort by timestamp
        recent_memories.sort(key=lambda x: x['timestamp'], reverse=True)
        return recent_memories[:limit]
    
    def consolidate_memories(self):
        """Consolidate short-term memories into long-term memory."""
        if len(self.short_term_memory) < 50:  # Only consolidate if we have enough memories
            return
        
        memories_to_consolidate = []
        
        # Select memories for consolidation based on importance and access count
        for memory in self.short_term_memory:
            if (memory['importance'] > 0.5 or 
                memory['access_count'] > 2 or
                memory['timestamp'] < datetime.now() - timedelta(hours=1)):
                memories_to_consolidate.append(memory)
        
        # Move important memories to long-term storage
        for memory in memories_to_consolidate:
            memory_id = memory['id']
            self.long_term_memory[memory_id] = memory
            self.memory_stats['long_term_count'] += 1
        
        # Remove consolidated memories from short-term memory
        self.short_term_memory = deque(
            [m for m in self.short_term_memory if m not in memories_to_consolidate],
            maxlen=1000
        )
        
        self.memory_stats['short_term_count'] = len(self.short_term_memory)
        self.memory_stats['last_consolidation'] = datetime.now()
        self.memory_stats['consolidation_count'] += 1
        
        self.logger.info(f"Consolidated {len(memories_to_consolidate)} memories to long-term storage")
    
    def cleanup_old_memories(self, days: int = 30):
        """Remove old memories to free up space."""
        cutoff_time = datetime.now() - timedelta(days=days)
        removed_count = 0
        
        # Clean up long-term memory
        memories_to_remove = []
        for memory_id, memory in self.long_term_memory.items():
            if (memory['timestamp'] < cutoff_time and 
                memory['access_count'] < 3 and 
                memory['importance'] < 0.3):
                memories_to_remove.append(memory_id)
        
        for memory_id in memories_to_remove:
            del self.long_term_memory[memory_id]
            removed_count += 1
        
        self.memory_stats['long_term_count'] = len(self.long_term_memory)
        
        self.logger.info(f"Cleaned up {removed_count} old memories")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            **self.memory_stats,
            'memory_usage_mb': self._calculate_memory_usage(),
            'index_size': len(self.memory_index),
            'oldest_memory': self._get_oldest_memory_date(),
            'newest_memory': self._get_newest_memory_date()
        }
    
    def save_memory(self):
        """Save memories to persistent storage."""
        try:
            # Save long-term memory
            memory_file = os.path.join(self.memory_dir, 'long_term_memory.pkl')
            with open(memory_file, 'wb') as f:
                pickle.dump(self.long_term_memory, f)
            
            # Save memory index
            index_file = os.path.join(self.memory_dir, 'memory_index.pkl')
            with open(index_file, 'wb') as f:
                pickle.dump(dict(self.memory_index), f)
            
            # Save memory stats
            stats_file = os.path.join(self.memory_dir, 'memory_stats.json')
            with open(stats_file, 'w') as f:
                json.dump(self.memory_stats, f, default=str)
            
            self.logger.info("Memory saved to persistent storage")
            
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")
    
    def _load_memories(self):
        """Load memories from persistent storage."""
        try:
            # Load long-term memory
            memory_file = os.path.join(self.memory_dir, 'long_term_memory.pkl')
            if os.path.exists(memory_file):
                with open(memory_file, 'rb') as f:
                    self.long_term_memory = pickle.load(f)
            
            # Load memory index
            index_file = os.path.join(self.memory_dir, 'memory_index.pkl')
            if os.path.exists(index_file):
                with open(index_file, 'rb') as f:
                    self.memory_index = defaultdict(list, pickle.load(f))
            
            # Load memory stats
            stats_file = os.path.join(self.memory_dir, 'memory_stats.json')
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    self.memory_stats = json.load(f)
            
            self.logger.info("Memory loaded from persistent storage")
            
        except Exception as e:
            self.logger.error(f"Failed to load memory: {e}")
    
    def _generate_memory_id(self, data: Dict) -> str:
        """Generate a unique ID for a memory."""
        content = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_importance(self, data: Dict) -> float:
        """Calculate the importance of a memory."""
        importance = 0.0
        
        # Base importance
        if 'task' in data:
            task = data['task']
            importance += task.get('priority', 1) * 0.2
            importance += task.get('complexity', 1) * 0.1
        
        if 'result' in data:
            result = data['result']
            if result.get('success', False):
                importance += 0.3
            else:
                importance += 0.1  # Failed tasks are still important to remember
        
        # Time-based importance (recent memories are more important)
        if 'timestamp' in data:
            age_hours = (datetime.now() - data['timestamp']).total_seconds() / 3600
            importance += max(0, 1 - age_hours / 24) * 0.2
        
        return min(1.0, importance)
    
    def _calculate_relevance(self, memory: Dict, query: str) -> float:
        """Calculate relevance score between memory and query."""
        relevance = 0.0
        query_words = set(query.split())
        
        # Search in memory data
        memory_text = json.dumps(memory['data'], default=str).lower()
        memory_words = set(memory_text.split())
        
        # Calculate word overlap
        if memory_words:
            overlap = len(query_words.intersection(memory_words))
            relevance += overlap / len(query_words) * 0.5
        
        # Check memory type
        if memory['type'] in query:
            relevance += 0.3
        
        # Check timestamp (recent memories are more relevant)
        age_hours = (datetime.now() - memory['timestamp']).total_seconds() / 3600
        relevance += max(0, 1 - age_hours / 24) * 0.2
        
        return min(1.0, relevance)
    
    def _index_memory(self, memory: Dict):
        """Index memory for search."""
        # Extract key terms from memory
        memory_text = json.dumps(memory['data'], default=str).lower()
        words = set(memory_text.split())
        
        # Index by important words
        for word in words:
            if len(word) > 3:  # Only index words longer than 3 characters
                self.memory_index[word].append(memory['id'])
    
    def _calculate_memory_usage(self) -> float:
        """Calculate memory usage in MB."""
        try:
            total_size = 0
            
            # Calculate size of in-memory data structures
            import sys
            total_size += sys.getsizeof(self.short_term_memory)
            total_size += sys.getsizeof(self.long_term_memory)
            total_size += sys.getsizeof(self.memory_index)
            
            # Add size of individual memory items
            for memory in self.short_term_memory:
                total_size += sys.getsizeof(memory)
            
            for memory in self.long_term_memory.values():
                total_size += sys.getsizeof(memory)
            
            return total_size / (1024 * 1024)  # Convert to MB
            
        except Exception:
            return 0.0
    
    def _get_oldest_memory_date(self) -> Optional[str]:
        """Get the date of the oldest memory."""
        oldest = None
        
        for memory in self.short_term_memory:
            if oldest is None or memory['timestamp'] < oldest:
                oldest = memory['timestamp']
        
        for memory in self.long_term_memory.values():
            if oldest is None or memory['timestamp'] < oldest:
                oldest = memory['timestamp']
        
        return oldest.isoformat() if oldest else None
    
    def _get_newest_memory_date(self) -> Optional[str]:
        """Get the date of the newest memory."""
        newest = None
        
        for memory in self.short_term_memory:
            if newest is None or memory['timestamp'] > newest:
                newest = memory['timestamp']
        
        for memory in self.long_term_memory.values():
            if newest is None or memory['timestamp'] > newest:
                newest = memory['timestamp']
        
        return newest.isoformat() if newest else None
    
    def get_interaction_count(self) -> int:
        """Get the total number of interactions stored."""
        return self.memory_stats['total_memories']
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get detailed memory usage information."""
        return {
            'short_term_count': self.memory_stats['short_term_count'],
            'long_term_count': self.memory_stats['long_term_count'],
            'total_memories': self.memory_stats['total_memories'],
            'memory_usage_mb': self._calculate_memory_usage(),
            'index_size': len(self.memory_index)
        }
