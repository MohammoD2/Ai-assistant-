#!/usr/bin/env python3
"""
Example Usage of the AI Assistant
================================

This script demonstrates how to use the AI assistant programmatically
and shows various capabilities and features.
"""

import sys
import os
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from brain import AIBrain

def example_basic_usage():
    """Demonstrate basic usage of the AI assistant."""
    print("=" * 60)
    print("🧠 AI Assistant - Basic Usage Example")
    print("=" * 60)
    
    # Initialize the AI brain
    brain = AIBrain()
    brain.wake_up()
    
    # Example 1: File operations
    print("\n📁 Example 1: File Operations")
    print("-" * 30)
    
    commands = [
        "create a new file called example.txt",
        "create a new file called report.md"
    ]
    
    for command in commands:
        print(f"Command: {command}")
        result = brain.process_command(command)
        
        if result.get('success'):
            for task_result in result.get('results', []):
                if task_result.get('output', {}).get('message'):
                    print(f"  ✅ {task_result['output']['message']}")
        else:
            print(f"  ❌ Error: {result.get('error')}")
    
    # Example 2: Web operations
    print("\n🌐 Example 2: Web Operations")
    print("-" * 30)
    
    web_commands = [
        "search for Python programming tutorials",
        "search for machine learning basics"
    ]
    
    for command in web_commands:
        print(f"Command: {command}")
        result = brain.process_command(command)
        
        if result.get('success'):
            for task_result in result.get('results', []):
                if task_result.get('output', {}).get('message'):
                    print(f"  ✅ {task_result['output']['message']}")
        else:
            print(f"  ❌ Error: {result.get('error')}")
    
    # Example 3: System operations
    print("\n⚙️ Example 3: System Operations")
    print("-" * 30)
    
    system_commands = [
        "check system status"
    ]
    
    for command in system_commands:
        print(f"Command: {command}")
        result = brain.process_command(command)
        
        if result.get('success'):
            for task_result in result.get('results', []):
                if task_result.get('output', {}).get('message'):
                    print(f"  ✅ {task_result['output']['message']}")
                if task_result.get('output', {}).get('system_info'):
                    sys_info = task_result['output']['system_info']
                    print(f"  📊 Platform: {sys_info.get('platform')}")
                    print(f"  📊 CPU Usage: {sys_info.get('cpu_percent')}%")
                    print(f"  📊 Memory Usage: {sys_info.get('memory_percent')}%")
        else:
            print(f"  ❌ Error: {result.get('error')}")
    
    brain.sleep()

def example_advanced_features():
    """Demonstrate advanced features of the AI assistant."""
    print("\n" + "=" * 60)
    print("🧠 AI Assistant - Advanced Features Example")
    print("=" * 60)
    
    # Initialize the AI brain
    brain = AIBrain()
    brain.wake_up()
    
    # Example 1: Memory and Learning
    print("\n🧠 Example 1: Memory and Learning")
    print("-" * 30)
    
    # Process some commands to build memory
    learning_commands = [
        "create a learning file",
        "search for AI tutorials",
        "check system performance"
    ]
    
    for command in learning_commands:
        print(f"Learning command: {command}")
        brain.process_command(command)
    
    # Check memory statistics
    memory_stats = brain.memory_manager.get_memory_stats()
    print(f"📊 Memory Statistics:")
    print(f"  - Total memories: {memory_stats['total_memories']}")
    print(f"  - Short-term: {memory_stats['short_term_count']}")
    print(f"  - Long-term: {memory_stats['long_term_count']}")
    
    # Example 2: Knowledge Base
    print("\n📚 Example 2: Knowledge Base")
    print("-" * 30)
    
    # Search for knowledge
    knowledge_results = brain.knowledge_base.search_knowledge("file operations", limit=3)
    print(f"📚 Found {len(knowledge_results)} knowledge items about file operations")
    
    for item in knowledge_results:
        if item['type'] == 'fact':
            print(f"  📖 Fact: {item['data']['content'][:50]}...")
        elif item['type'] == 'concept':
            print(f"  📖 Concept: {item['data']['name']}")
    
    # Example 3: Thinking Capability
    print("\n🤔 Example 3: Thinking Capability")
    print("-" * 30)
    
    thoughts = brain.think("What is artificial intelligence?")
    print("🤔 Brain thoughts about AI:")
    for thought in thoughts[:3]:  # Show first 3 thoughts
        print(f"  💭 {thought}")
    
    # Example 4: Brain Status
    print("\n📊 Example 4: Brain Status")
    print("-" * 30)
    
    status = brain.get_brain_status()
    print(f"🧠 Brain Status:")
    print(f"  - Active: {status['is_active']}")
    print(f"  - Consciousness: {status['consciousness_level']:.2f}")
    print(f"  - Energy: {status['energy_level']:.2f}")
    print(f"  - Focus: {status['focus_level']:.2f}")
    print(f"  - Total Interactions: {status['total_interactions']}")
    print(f"  - Knowledge Items: {status['knowledge_items']}")
    
    brain.sleep()

def example_custom_integration():
    """Demonstrate how to integrate the AI assistant into your own applications."""
    print("\n" + "=" * 60)
    print("🔧 AI Assistant - Custom Integration Example")
    print("=" * 60)
    
    # Initialize the AI brain
    brain = AIBrain()
    brain.wake_up()
    
    # Example: Automated workflow
    print("\n🔄 Example: Automated Workflow")
    print("-" * 30)
    
    workflow_commands = [
        "create a new file called workflow.txt",
        "search for automation tools",
        "check system status"
    ]
    
    print("🔄 Starting automated workflow...")
    
    for i, command in enumerate(workflow_commands, 1):
        print(f"\nStep {i}: {command}")
        
        # Process command
        result = brain.process_command(command)
        
        if result.get('success'):
            print(f"  ✅ Step {i} completed successfully")
            
            # Extract useful information from results
            for task_result in result.get('results', []):
                if task_result.get('output', {}).get('message'):
                    print(f"    📝 {task_result['output']['message']}")
        else:
            print(f"  ❌ Step {i} failed: {result.get('error')}")
    
    print("\n🎉 Workflow completed!")
    
    # Example: Batch processing
    print("\n📦 Example: Batch Processing")
    print("-" * 30)
    
    batch_commands = [
        "create file1.txt",
        "create file2.txt", 
        "create file3.txt"
    ]
    
    print("📦 Processing batch commands...")
    
    successful_commands = 0
    for command in batch_commands:
        result = brain.process_command(command)
        if result.get('success'):
            successful_commands += 1
    
    print(f"📊 Batch processing results: {successful_commands}/{len(batch_commands)} successful")
    
    brain.sleep()

def example_error_handling():
    """Demonstrate error handling and robustness."""
    print("\n" + "=" * 60)
    print("🛡️ AI Assistant - Error Handling Example")
    print("=" * 60)
    
    # Initialize the AI brain
    brain = AIBrain()
    brain.wake_up()
    
    # Example: Invalid commands
    print("\n❌ Example: Invalid Commands")
    print("-" * 30)
    
    invalid_commands = [
        "",  # Empty command
        "this is a completely invalid command that should fail",
        "open a file that definitely does not exist.txt"
    ]
    
    for command in invalid_commands:
        print(f"Testing invalid command: '{command}'")
        result = brain.process_command(command)
        
        if result.get('success'):
            print(f"  ✅ Unexpected success: {result}")
        else:
            print(f"  ❌ Expected failure: {result.get('error')}")
    
    # Example: System resilience
    print("\n🛡️ Example: System Resilience")
    print("-" * 30)
    
    # Process many commands to test system stability
    print("🔄 Testing system resilience with multiple commands...")
    
    resilience_commands = [
        "create test file",
        "search for Python",
        "check system",
        "create another file",
        "search for AI"
    ]
    
    successful = 0
    for i, command in enumerate(resilience_commands, 1):
        try:
            result = brain.process_command(command)
            if result.get('success'):
                successful += 1
            print(f"  Command {i}: {'✅' if result.get('success') else '❌'}")
        except Exception as e:
            print(f"  Command {i}: ❌ Exception: {e}")
    
    print(f"📊 Resilience test: {successful}/{len(resilience_commands)} successful")
    
    brain.sleep()

def main():
    """Run all examples."""
    print("🧠 AI Assistant Examples")
    print("This script demonstrates various capabilities of the AI assistant.")
    print("Press Enter to continue after each example...")
    
    try:
        # Run basic usage example
        example_basic_usage()
        input("\nPress Enter to continue to advanced features...")
        
        # Run advanced features example
        example_advanced_features()
        input("\nPress Enter to continue to custom integration...")
        
        # Run custom integration example
        example_custom_integration()
        input("\nPress Enter to continue to error handling...")
        
        # Run error handling example
        example_error_handling()
        
        print("\n" + "=" * 60)
        print("🎉 All examples completed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("  • Run 'python main.py' for interactive mode")
        print("  • Run 'python main.py --demo' for a demonstration")
        print("  • Use the AI assistant in your own applications")
        print("  • Extend the functionality with custom tasks")
        
    except KeyboardInterrupt:
        print("\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
