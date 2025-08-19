"""
AI Brain - The Central Nervous System of the AI Assistant
=======================================================

This module contains the main AI brain that coordinates all components:
- Command processing and understanding
- Task detection and planning
- Memory management
- Knowledge integration
- Task execution and monitoring
"""

import asyncio
import logging
import threading
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .command_processor import CommandProcessor
from .task_executor import TaskExecutor
from .memory_manager import MemoryManager
from .knowledge_base import KnowledgeBase

console = Console()

class AIBrain:
    """
    The main AI brain that works like a human brain:
    - Processes natural language commands
    - Detects tasks and creates execution plans
    - Manages memory and learning
    - Coordinates task execution
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the AI brain with all its components."""
        self.config = config or {}
        self.is_active = False
        self.current_tasks = []
        self.task_history = []
        
        # Initialize brain components
        self.command_processor = CommandProcessor()
        self.task_executor = TaskExecutor()
        self.memory_manager = MemoryManager()
        self.knowledge_base = KnowledgeBase()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Brain state
        self.consciousness_level = 1.0  # 0.0 to 1.0
        self.energy_level = 1.0  # 0.0 to 1.0
        self.focus_level = 1.0  # 0.0 to 1.0
        
        console.print(Panel.fit(
            "[bold green]🧠 AI Brain Initialized[/bold green]\n"
            "Ready to process commands and execute tasks!",
            title="AI Assistant Brain"
        ))
    
    def wake_up(self):
        """Activate the AI brain and start processing."""
        self.is_active = True
        self.consciousness_level = 1.0
        self.energy_level = 1.0
        self.focus_level = 1.0
        
        console.print("[bold green]🌅 AI Brain is now awake and ready![/bold green]")
        self.logger.info("AI Brain activated")
    
    def sleep(self):
        """Deactivate the AI brain and save state."""
        self.is_active = False
        self.memory_manager.save_memory()
        self.knowledge_base.save_knowledge()
        
        console.print("[bold blue]😴 AI Brain is going to sleep...[/bold blue]")
        self.logger.info("AI Brain deactivated")
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process a natural language command and return the response.
        
        Args:
            command: Natural language command from user
            
        Returns:
            Dictionary containing response and task information
        """
        if not self.is_active:
            return {"error": "Brain is not active. Please wake up first."}
        
        console.print(f"[bold cyan]🧠 Processing command:[/bold cyan] {command}")
        
        try:
            # Step 1: Understand the command
            understanding = self.command_processor.understand(command)
            
            # Step 2: Detect tasks
            tasks = self.command_processor.detect_tasks(understanding)
            
            # Step 3: Plan execution
            execution_plan = self.plan_execution(tasks)
            
            # Step 4: Execute tasks
            results = self.execute_tasks(execution_plan)
            
            # Step 5: Learn from the interaction
            self.learn_from_interaction(command, understanding, tasks, results)
            
            return {
                "command": command,
                "understanding": understanding,
                "tasks": tasks,
                "results": results,
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return {
                "command": command,
                "error": str(e),
                "success": False
            }
    
    def plan_execution(self, tasks: List[Dict]) -> Dict[str, Any]:
        """
        Create an execution plan for detected tasks.
        
        Args:
            tasks: List of detected tasks
            
        Returns:
            Execution plan with task priorities and dependencies
        """
        plan = {
            "tasks": tasks,
            "priority_order": [],
            "dependencies": {},
            "estimated_time": 0,
            "parallel_tasks": []
        }
        
        # Sort tasks by priority
        priority_tasks = sorted(tasks, key=lambda x: x.get('priority', 0), reverse=True)
        plan["priority_order"] = priority_tasks
        
        # Calculate estimated time
        total_time = sum(task.get('estimated_time', 5) for task in tasks)
        plan["estimated_time"] = total_time
        
        # Identify parallel tasks
        parallel_tasks = [task for task in tasks if task.get('can_parallel', True)]
        plan["parallel_tasks"] = parallel_tasks
        
        console.print(f"[bold yellow]📋 Execution Plan Created:[/bold yellow] {len(tasks)} tasks, {total_time}s estimated")
        
        return plan
    
    def execute_tasks(self, plan: Dict[str, Any]) -> List[Dict]:
        """
        Execute tasks according to the plan.
        
        Args:
            plan: Execution plan
            
        Returns:
            List of task results
        """
        results = []
        
        for task in plan["priority_order"]:
            try:
                console.print(f"[bold green]⚡ Executing:[/bold green] {task['name']}")
                
                # Execute the task
                result = self.task_executor.execute_task(task)
                results.append(result)
                
                # Update brain state
                self.update_brain_state(task, result)
                
                # Store in memory
                self.memory_manager.store_task_result(task, result)
                
            except Exception as e:
                error_result = {
                    "task": task,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now()
                }
                results.append(error_result)
                self.logger.error(f"Task execution failed: {e}")
        
        return results
    
    def update_brain_state(self, task: Dict, result: Dict):
        """Update brain state based on task execution."""
        # Adjust energy level
        if result.get('success', False):
            self.energy_level = min(1.0, self.energy_level + 0.1)
        else:
            self.energy_level = max(0.0, self.energy_level - 0.2)
        
        # Adjust focus level
        task_complexity = task.get('complexity', 1)
        self.focus_level = max(0.0, self.focus_level - (task_complexity * 0.05))
        
        # Restore focus over time
        if self.focus_level < 0.5:
            self.focus_level = min(1.0, self.focus_level + 0.1)
    
    def learn_from_interaction(self, command: str, understanding: Dict, tasks: List[Dict], results: List[Dict]):
        """Learn from the interaction to improve future performance."""
        # Store interaction in memory
        interaction = {
            "command": command,
            "understanding": understanding,
            "tasks": tasks,
            "results": results,
            "timestamp": datetime.now(),
            "brain_state": {
                "consciousness": self.consciousness_level,
                "energy": self.energy_level,
                "focus": self.focus_level
            }
        }
        
        self.memory_manager.store_interaction(interaction)
        
        # Update knowledge base
        self.knowledge_base.update_from_interaction(interaction)
        
        # Learn patterns
        self.command_processor.learn_pattern(command, understanding)
    
    def get_brain_status(self) -> Dict[str, Any]:
        """Get current brain status and statistics."""
        return {
            "is_active": self.is_active,
            "consciousness_level": self.consciousness_level,
            "energy_level": self.energy_level,
            "focus_level": self.focus_level,
            "current_tasks": len(self.current_tasks),
            "total_interactions": self.memory_manager.get_interaction_count(),
            "knowledge_items": self.knowledge_base.get_item_count(),
            "memory_usage": self.memory_manager.get_memory_usage()
        }
    
    def think(self, prompt: str) -> str:
        """
        Use the brain to think about a problem or question.
        
        Args:
            prompt: Question or problem to think about
            
        Returns:
            Thought process and conclusion
        """
        console.print(f"[bold magenta]🤔 Thinking about:[/bold magenta] {prompt}")
        
        # Use knowledge base to think
        thoughts = self.knowledge_base.think_about(prompt)
        
        # Use memory to enhance thinking
        relevant_memories = self.memory_manager.search_memories(prompt)
        
        # Combine thoughts and memories
        conclusion = self.synthesize_thoughts(thoughts, relevant_memories)
        
        return conclusion
    
    def synthesize_thoughts(self, thoughts: List[str], memories: List[Dict]) -> str:
        """Synthesize thoughts and memories into a coherent conclusion."""
        # This is a simplified synthesis - in a real implementation,
        # you might use more sophisticated reasoning
        synthesis = f"Based on my analysis:\n"
        
        for thought in thoughts:
            synthesis += f"• {thought}\n"
        
        if memories:
            synthesis += f"\nRelevant past experiences:\n"
            for memory in memories[:3]:  # Top 3 relevant memories
                synthesis += f"• {memory.get('summary', 'Past experience')}\n"
        
        return synthesis
    
    def run_continuous_mode(self):
        """Run the brain in continuous mode, listening for commands."""
        console.print("[bold green]🔄 Starting continuous mode...[/bold green]")
        console.print("Type 'sleep' to stop, 'status' for brain status")
        
        while self.is_active:
            try:
                command = input("\n🧠 Command: ").strip()
                
                if command.lower() == 'sleep':
                    self.sleep()
                    break
                elif command.lower() == 'status':
                    status = self.get_brain_status()
                    console.print(Panel.fit(
                        f"Consciousness: {status['consciousness_level']:.2f}\n"
                        f"Energy: {status['energy_level']:.2f}\n"
                        f"Focus: {status['focus_level']:.2f}\n"
                        f"Active Tasks: {status['current_tasks']}\n"
                        f"Total Interactions: {status['total_interactions']}",
                        title="Brain Status"
                    ))
                elif command.lower() == 'think':
                    prompt = input("What should I think about? ")
                    thoughts = self.think(prompt)
                    console.print(Panel(thoughts, title="🤔 Thoughts"))
                elif command:
                    result = self.process_command(command)
                    if result.get('success'):
                        console.print(f"[bold green]✅ Task completed![/bold green]")
                    else:
                        console.print(f"[bold red]❌ Error: {result.get('error')}[/bold red]")
                        
            except KeyboardInterrupt:
                console.print("\n[bold yellow]⚠️ Interrupted by user[/bold yellow]")
                break
            except Exception as e:
                console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
                self.logger.error(f"Continuous mode error: {e}")
    
    def __str__(self):
        """String representation of the AI brain."""
        status = self.get_brain_status()
        return f"AIBrain(active={status['is_active']}, consciousness={status['consciousness_level']:.2f})"
