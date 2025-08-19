"""
AI Assistant - Brain-like Command Processing and Task Execution
=============================================================

This module provides a comprehensive AI assistant that works like a human brain:
- Understands natural language commands
- Detects what tasks need to be done
- Executes tasks automatically
- Learns from interactions
- Manages multiple concurrent tasks
"""

from .brain import AIBrain
from .command_processor import CommandProcessor
from .task_executor import TaskExecutor
from .memory_manager import MemoryManager
from .knowledge_base import KnowledgeBase

__version__ = "1.0.0"
__author__ = "AI Assistant Team"

__all__ = [
    "AIBrain",
    "CommandProcessor", 
    "TaskExecutor",
    "MemoryManager",
    "KnowledgeBase"
]
