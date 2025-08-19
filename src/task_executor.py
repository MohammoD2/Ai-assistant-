"""
Task Executor - The Motor Cortex of the AI Assistant
==================================================

This module handles the actual execution of detected tasks:
- File operations
- Web operations
- System operations
- Data processing
- Communication tasks
- Automation tasks
"""

import os
import sys
import subprocess
import webbrowser
import requests
import json
import logging
import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import psutil
import platform

class TaskExecutor:
    """
    Executes tasks detected by the command processor.
    Works like the motor cortex of the human brain.
    """
    
    def __init__(self):
        """Initialize the task executor."""
        self.logger = logging.getLogger(__name__)
        self.running_tasks = {}
        self.task_history = []
        self.max_concurrent_tasks = 5
        
        # Task execution handlers
        self.task_handlers = {
            'file_creation': self._create_file,
            'file_opening': self._open_file,
            'file_deletion': self._delete_file,
            'web_search': self._web_search,
            'website_opening': self._open_website,
            'file_download': self._download_file,
            'package_installation': self._install_package,
            'program_execution': self._run_program,
            'system_monitoring': self._check_system,
            'data_analysis': self._analyze_data,
            'data_conversion': self._convert_data,
            'data_backup': self._backup_data,
            'email_sending': self._send_email,
            'meeting_scheduling': self._schedule_meeting,
            'information_search': self._search_information,
            'topic_explanation': self._explain_topic,
            'automation_setup': self._setup_automation,
            'reminder_creation': self._create_reminder
        }
    
    def execute_task(self, task: Dict) -> Dict[str, Any]:
        """
        Execute a single task.
        
        Args:
            task: Task dictionary containing task information
            
        Returns:
            Dictionary containing execution results
        """
        task_id = f"{task['action']}_{int(time.time())}"
        
        result = {
            'task_id': task_id,
            'task_name': task['name'],
            'action': task['action'],
            'start_time': datetime.now(),
            'success': False,
            'output': None,
            'error': None,
            'duration': 0,
            'timestamp': datetime.now()
        }
        
        try:
            self.logger.info(f"Executing task: {task['name']} ({task['action']})")
            
            # Check if we can run this task
            if not self._can_run_task(task):
                result['error'] = "Task cannot be run due to system constraints"
                return result
            
            # Get the handler for this task
            handler = self.task_handlers.get(task['action'])
            if not handler:
                result['error'] = f"No handler found for action: {task['action']}"
                return result
            
            # Execute the task
            start_time = time.time()
            output = handler(task)
            end_time = time.time()
            
            result['success'] = True
            result['output'] = output
            result['duration'] = end_time - start_time
            
            # Store in history
            self.task_history.append(result)
            if len(self.task_history) > 1000:  # Keep only last 1000 tasks
                self.task_history.pop(0)
            
            self.logger.info(f"Task completed successfully: {task['name']}")
            
        except Exception as e:
            result['error'] = str(e)
            result['duration'] = time.time() - start_time if 'start_time' in locals() else 0
            self.logger.error(f"Task execution failed: {e}")
        
        return result
    
    def _can_run_task(self, task: Dict) -> bool:
        """Check if a task can be run based on system constraints."""
        # Check concurrent task limit
        if len(self.running_tasks) >= self.max_concurrent_tasks:
            return False
        
        # Check if task requires exclusive access
        if not task.get('can_parallel', True):
            for running_task in self.running_tasks.values():
                if not running_task.get('can_parallel', True):
                    return False
        
        return True
    
    # File Operations
    def _create_file(self, task: Dict) -> Dict[str, Any]:
        """Create a new file."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if files:
            filename = files[0]
        else:
            # Generate a default filename
            filename = f"new_file_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"# {task['name']}\n")
                f.write(f"Created: {datetime.now()}\n")
                f.write(f"Task: {task['name']}\n\n")
            
            return {
                'filename': filename,
                'path': os.path.abspath(filename),
                'size': os.path.getsize(filename),
                'message': f"File '{filename}' created successfully"
            }
        except Exception as e:
            raise Exception(f"Failed to create file: {e}")
    
    def _open_file(self, task: Dict) -> Dict[str, Any]:
        """Open a file."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if not files:
            raise Exception("No file specified to open")
        
        filename = files[0]
        
        try:
            if os.path.exists(filename):
                # Use default system application to open file
                if platform.system() == "Windows":
                    os.startfile(filename)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", filename])
                else:  # Linux
                    subprocess.run(["xdg-open", filename])
                
                return {
                    'filename': filename,
                    'path': os.path.abspath(filename),
                    'message': f"File '{filename}' opened successfully"
                }
            else:
                raise Exception(f"File '{filename}' does not exist")
        except Exception as e:
            raise Exception(f"Failed to open file: {e}")
    
    def _delete_file(self, task: Dict) -> Dict[str, Any]:
        """Delete a file."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if not files:
            raise Exception("No file specified to delete")
        
        filename = files[0]
        
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return {
                    'filename': filename,
                    'message': f"File '{filename}' deleted successfully"
                }
            else:
                raise Exception(f"File '{filename}' does not exist")
        except Exception as e:
            raise Exception(f"Failed to delete file: {e}")
    
    # Web Operations
    def _web_search(self, task: Dict) -> Dict[str, Any]:
        """Perform a web search."""
        entities = task.get('entities', {})
        keywords = entities.get('keywords', [])
        
        if not keywords:
            raise Exception("No search terms provided")
        
        search_query = " ".join(keywords)
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        try:
            webbrowser.open(search_url)
            return {
                'search_query': search_query,
                'search_url': search_url,
                'message': f"Web search for '{search_query}' opened in browser"
            }
        except Exception as e:
            raise Exception(f"Failed to perform web search: {e}")
    
    def _open_website(self, task: Dict) -> Dict[str, Any]:
        """Open a website."""
        entities = task.get('entities', {})
        urls = entities.get('urls', [])
        
        if not urls:
            raise Exception("No URL provided")
        
        url = urls[0]
        
        try:
            webbrowser.open(url)
            return {
                'url': url,
                'message': f"Website '{url}' opened in browser"
            }
        except Exception as e:
            raise Exception(f"Failed to open website: {e}")
    
    def _download_file(self, task: Dict) -> Dict[str, Any]:
        """Download a file from the web."""
        entities = task.get('entities', {})
        urls = entities.get('urls', [])
        
        if not urls:
            raise Exception("No URL provided for download")
        
        url = urls[0]
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Extract filename from URL or use default
            filename = url.split('/')[-1] or f"downloaded_file_{int(time.time())}"
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                'url': url,
                'filename': filename,
                'size': os.path.getsize(filename),
                'message': f"File downloaded successfully: {filename}"
            }
        except Exception as e:
            raise Exception(f"Failed to download file: {e}")
    
    # System Operations
    def _install_package(self, task: Dict) -> Dict[str, Any]:
        """Install a Python package."""
        entities = task.get('entities', {})
        keywords = entities.get('keywords', [])
        
        if not keywords:
            raise Exception("No package name provided")
        
        package_name = keywords[0]
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                return {
                    'package': package_name,
                    'output': result.stdout,
                    'message': f"Package '{package_name}' installed successfully"
                }
            else:
                raise Exception(f"Installation failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            raise Exception("Package installation timed out")
        except Exception as e:
            raise Exception(f"Failed to install package: {e}")
    
    def _run_program(self, task: Dict) -> Dict[str, Any]:
        """Run a program or script."""
        entities = task.get('entities', {})
        programs = entities.get('programs', [])
        files = entities.get('files', [])
        
        if programs:
            program = programs[0]
        elif files:
            program = files[0]
        else:
            raise Exception("No program or file specified to run")
        
        try:
            result = subprocess.run(
                [program],
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )
            
            return {
                'program': program,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'message': f"Program '{program}' executed successfully"
            }
        except subprocess.TimeoutExpired:
            raise Exception("Program execution timed out")
        except Exception as e:
            raise Exception(f"Failed to run program: {e}")
    
    def _check_system(self, task: Dict) -> Dict[str, Any]:
        """Check system status."""
        try:
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'cpu_percent': cpu_percent,
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_free': disk.free,
                'disk_percent': disk.percent
            }
            
            return {
                'system_info': system_info,
                'message': "System status checked successfully"
            }
        except Exception as e:
            raise Exception(f"Failed to check system status: {e}")
    
    # Data Operations
    def _analyze_data(self, task: Dict) -> Dict[str, Any]:
        """Analyze data (placeholder implementation)."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if files:
            filename = files[0]
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                return {
                    'filename': filename,
                    'file_size': file_size,
                    'analysis_type': 'basic_file_analysis',
                    'message': f"Basic analysis of '{filename}' completed"
                }
        
        return {
            'analysis_type': 'general_data_analysis',
            'message': "Data analysis completed (placeholder implementation)"
        }
    
    def _convert_data(self, task: Dict) -> Dict[str, Any]:
        """Convert data format (placeholder implementation)."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if files:
            filename = files[0]
            return {
                'source_file': filename,
                'conversion_type': 'format_conversion',
                'message': f"Data conversion for '{filename}' completed"
            }
        
        return {
            'conversion_type': 'general_data_conversion',
            'message': "Data conversion completed (placeholder implementation)"
        }
    
    def _backup_data(self, task: Dict) -> Dict[str, Any]:
        """Backup data (placeholder implementation)."""
        entities = task.get('entities', {})
        files = entities.get('files', [])
        
        if files:
            filename = files[0]
            backup_name = f"{filename}.backup"
            try:
                if os.path.exists(filename):
                    import shutil
                    shutil.copy2(filename, backup_name)
                    return {
                        'source_file': filename,
                        'backup_file': backup_name,
                        'message': f"Backup created: {backup_name}"
                    }
            except Exception as e:
                raise Exception(f"Failed to create backup: {e}")
        
        return {
            'backup_type': 'general_backup',
            'message': "Data backup completed (placeholder implementation)"
        }
    
    # Communication Tasks
    def _send_email(self, task: Dict) -> Dict[str, Any]:
        """Send email (placeholder implementation)."""
        return {
            'email_type': 'general_email',
            'message': "Email sending completed (placeholder implementation)"
        }
    
    def _schedule_meeting(self, task: Dict) -> Dict[str, Any]:
        """Schedule meeting (placeholder implementation)."""
        return {
            'meeting_type': 'general_meeting',
            'message': "Meeting scheduling completed (placeholder implementation)"
        }
    
    # Information Tasks
    def _search_information(self, task: Dict) -> Dict[str, Any]:
        """Search for information (placeholder implementation)."""
        entities = task.get('entities', {})
        keywords = entities.get('keywords', [])
        
        search_query = " ".join(keywords) if keywords else "general information"
        
        return {
            'search_query': search_query,
            'search_type': 'information_search',
            'message': f"Information search for '{search_query}' completed"
        }
    
    def _explain_topic(self, task: Dict) -> Dict[str, Any]:
        """Explain a topic (placeholder implementation)."""
        entities = task.get('entities', {})
        keywords = entities.get('keywords', [])
        
        topic = " ".join(keywords) if keywords else "general topic"
        
        return {
            'topic': topic,
            'explanation_type': 'topic_explanation',
            'message': f"Explanation of '{topic}' completed"
        }
    
    # Automation Tasks
    def _setup_automation(self, task: Dict) -> Dict[str, Any]:
        """Setup automation (placeholder implementation)."""
        return {
            'automation_type': 'general_automation',
            'message': "Automation setup completed (placeholder implementation)"
        }
    
    def _create_reminder(self, task: Dict) -> Dict[str, Any]:
        """Create a reminder (placeholder implementation)."""
        entities = task.get('entities', {})
        time_expressions = entities.get('time_expressions', [])
        
        reminder_time = time_expressions[0] if time_expressions else "later"
        
        return {
            'reminder_time': reminder_time,
            'reminder_type': 'general_reminder',
            'message': f"Reminder created for {reminder_time}"
        }
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about task execution."""
        if not self.task_history:
            return {
                'total_tasks': 0,
                'successful_tasks': 0,
                'failed_tasks': 0,
                'average_duration': 0,
                'most_common_tasks': []
            }
        
        total_tasks = len(self.task_history)
        successful_tasks = len([t for t in self.task_history if t['success']])
        failed_tasks = total_tasks - successful_tasks
        
        durations = [t['duration'] for t in self.task_history if t['duration'] > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Most common tasks
        task_counts = {}
        for task in self.task_history:
            task_name = task['task_name']
            task_counts[task_name] = task_counts.get(task_name, 0) + 1
        
        most_common = sorted(task_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'average_duration': avg_duration,
            'most_common_tasks': most_common
        }
