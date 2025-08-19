#!/usr/bin/env python3
"""
Test script for the AI Assistant
================================

This script tests the basic functionality of the AI assistant to ensure
everything is working correctly.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from brain import AIBrain

def test_brain_initialization():
    """Test that the AI brain can be initialized correctly."""
    print("🧠 Testing brain initialization...")
    
    try:
        brain = AIBrain()
        print("✅ Brain initialized successfully")
        return brain
    except Exception as e:
        print(f"❌ Brain initialization failed: {e}")
        return None

def test_brain_wake_up():
    """Test that the brain can wake up."""
    print("🌅 Testing brain wake up...")
    
    brain = test_brain_initialization()
    if not brain:
        return None
    
    try:
        brain.wake_up()
        print("✅ Brain woke up successfully")
        return brain
    except Exception as e:
        print(f"❌ Brain wake up failed: {e}")
        return None

def test_command_processing():
    """Test basic command processing."""
    print("🗣️ Testing command processing...")
    
    brain = test_brain_wake_up()
    if not brain:
        return False
    
    test_commands = [
        "create a new file called test.txt",
        "search for Python programming",
        "check system status"
    ]
    
    success_count = 0
    for command in test_commands:
        try:
            print(f"   Testing: {command}")
            result = brain.process_command(command)
            
            if result.get('success'):
                print(f"   ✅ Success: {result.get('results', [{}])[0].get('output', {}).get('message', 'Command executed')}")
                success_count += 1
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print(f"📊 Command processing results: {success_count}/{len(test_commands)} successful")
    return success_count > 0

def test_memory_management():
    """Test memory management functionality."""
    print("🧠 Testing memory management...")
    
    brain = test_brain_wake_up()
    if not brain:
        return False
    
    try:
        # Test memory storage
        brain.process_command("create a test file")
        
        # Test memory retrieval
        memories = brain.memory_manager.get_recent_memories(hours=1, limit=5)
        print(f"✅ Memory management working: {len(memories)} recent memories")
        
        # Test memory statistics
        stats = brain.memory_manager.get_memory_stats()
        print(f"✅ Memory stats: {stats['total_memories']} total memories")
        
        return True
    except Exception as e:
        print(f"❌ Memory management failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality."""
    print("📚 Testing knowledge base...")
    
    brain = test_brain_wake_up()
    if not brain:
        return False
    
    try:
        # Test knowledge search
        knowledge = brain.knowledge_base.search_knowledge("file operations", limit=5)
        print(f"✅ Knowledge search working: {len(knowledge)} results found")
        
        # Test thinking capability
        thoughts = brain.think("What is artificial intelligence?")
        print(f"✅ Thinking capability working: {len(thoughts)} thoughts generated")
        
        return True
    except Exception as e:
        print(f"❌ Knowledge base failed: {e}")
        return False

def test_brain_status():
    """Test brain status functionality."""
    print("📊 Testing brain status...")
    
    brain = test_brain_wake_up()
    if not brain:
        return False
    
    try:
        # Process a command to generate some activity
        brain.process_command("create a status test file")
        
        # Get brain status
        status = brain.get_brain_status()
        
        print(f"✅ Brain status working:")
        print(f"   - Active: {status['is_active']}")
        print(f"   - Consciousness: {status['consciousness_level']:.2f}")
        print(f"   - Energy: {status['energy_level']:.2f}")
        print(f"   - Focus: {status['focus_level']:.2f}")
        print(f"   - Interactions: {status['total_interactions']}")
        
        return True
    except Exception as e:
        print(f"❌ Brain status failed: {e}")
        return False

def test_brain_sleep():
    """Test that the brain can go to sleep."""
    print("😴 Testing brain sleep...")
    
    brain = test_brain_wake_up()
    if not brain:
        return False
    
    try:
        brain.sleep()
        print("✅ Brain went to sleep successfully")
        return True
    except Exception as e:
        print(f"❌ Brain sleep failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide a summary."""
    print("🧪 Starting AI Assistant Tests")
    print("=" * 50)
    
    tests = [
        ("Brain Initialization", test_brain_initialization),
        ("Brain Wake Up", test_brain_wake_up),
        ("Command Processing", test_command_processing),
        ("Memory Management", test_memory_management),
        ("Knowledge Base", test_knowledge_base),
        ("Brain Status", test_brain_status),
        ("Brain Sleep", test_brain_sleep)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The AI Assistant is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

def cleanup_test_files():
    """Clean up any test files created during testing."""
    print("\n🧹 Cleaning up test files...")
    
    test_files = [
        "test.txt",
        "new_file_*.txt",
        "demo.txt",
        "status_test_file.txt"
    ]
    
    for pattern in test_files:
        for file_path in Path(".").glob(pattern):
            try:
                file_path.unlink()
                print(f"   Deleted: {file_path}")
            except Exception as e:
                print(f"   Could not delete {file_path}: {e}")

if __name__ == "__main__":
    try:
        success = run_all_tests()
        cleanup_test_files()
        
        if success:
            print("\n🎉 AI Assistant is ready to use!")
            print("Run 'python main.py' to start the interactive mode.")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Please fix the issues before using the AI Assistant.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        cleanup_test_files()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        cleanup_test_files()
        sys.exit(1)
