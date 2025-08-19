"""
Command Processor - Natural Language Understanding and Task Detection
==================================================================

This module handles:
- Natural language command understanding
- Task detection and classification
- Intent recognition
- Pattern learning
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

class CommandProcessor:
    """
    Processes natural language commands and detects tasks to be executed.
    Works like the language processing centers of the human brain.
    """
    
    def __init__(self):
        """Initialize the command processor with patterns and knowledge."""
        self.logger = logging.getLogger(__name__)
        
        # Command patterns and intents
        self.intent_patterns = {
            'file_operations': [
                r'\b(create|make|new|open|read|write|save|delete|remove|copy|move|rename)\b.*\b(file|document|folder|directory)\b',
                r'\b(create|make|new)\b.*\b(\.\w+)\b',
                r'\b(open|read|view)\b.*\b(\.\w+)\b'
            ],
            'web_operations': [
                r'\b(search|find|look up|google)\b.*\b(for|about)\b',
                r'\b(open|go to|visit|navigate)\b.*\b(website|url|link|page)\b',
                r'\b(download|get|fetch)\b.*\b(from|from the web)\b'
            ],
            'system_operations': [
                r'\b(install|uninstall|update|upgrade)\b.*\b(package|software|program)\b',
                r'\b(run|execute|start|launch)\b.*\b(program|application|script)\b',
                r'\b(check|monitor|status)\b.*\b(system|computer|memory|cpu)\b'
            ],
            'data_operations': [
                r'\b(analyze|process|calculate|compute)\b.*\b(data|information|numbers)\b',
                r'\b(convert|transform|format)\b.*\b(data|file|format)\b',
                r'\b(backup|export|import)\b.*\b(data|files|database)\b'
            ],
            'communication': [
                r'\b(send|write|compose)\b.*\b(email|message|text)\b',
                r'\b(call|phone|dial)\b.*\b(someone|person|number)\b',
                r'\b(meeting|schedule|appointment)\b'
            ],
            'information_gathering': [
                r'\b(what|how|when|where|why|who)\b.*\b(is|are|was|were|will|can)\b',
                r'\b(tell me|explain|describe|show me)\b',
                r'\b(find out|discover|learn about)\b'
            ],
            'automation': [
                r'\b(automate|schedule|repeat|loop)\b',
                r'\b(set up|configure|setup)\b.*\b(automation|task|job)\b',
                r'\b(remind|alert|notify)\b.*\b(when|if|about)\b'
            ]
        }
        
        # Task templates
        self.task_templates = {
            'file_operations': {
                'create_file': {
                    'name': 'Create File',
                    'action': 'file_creation',
                    'priority': 3,
                    'complexity': 1,
                    'estimated_time': 2,
                    'can_parallel': True
                },
                'open_file': {
                    'name': 'Open File',
                    'action': 'file_opening',
                    'priority': 2,
                    'complexity': 1,
                    'estimated_time': 1,
                    'can_parallel': True
                },
                'delete_file': {
                    'name': 'Delete File',
                    'action': 'file_deletion',
                    'priority': 4,
                    'complexity': 1,
                    'estimated_time': 1,
                    'can_parallel': True
                }
            },
            'web_operations': {
                'web_search': {
                    'name': 'Web Search',
                    'action': 'web_search',
                    'priority': 2,
                    'complexity': 2,
                    'estimated_time': 5,
                    'can_parallel': True
                },
                'open_website': {
                    'name': 'Open Website',
                    'action': 'website_opening',
                    'priority': 2,
                    'complexity': 1,
                    'estimated_time': 3,
                    'can_parallel': True
                },
                'download_file': {
                    'name': 'Download File',
                    'action': 'file_download',
                    'priority': 3,
                    'complexity': 2,
                    'estimated_time': 10,
                    'can_parallel': True
                }
            },
            'system_operations': {
                'install_package': {
                    'name': 'Install Package',
                    'action': 'package_installation',
                    'priority': 4,
                    'complexity': 3,
                    'estimated_time': 30,
                    'can_parallel': False
                },
                'run_program': {
                    'name': 'Run Program',
                    'action': 'program_execution',
                    'priority': 3,
                    'complexity': 2,
                    'estimated_time': 5,
                    'can_parallel': True
                },
                'system_check': {
                    'name': 'System Check',
                    'action': 'system_monitoring',
                    'priority': 1,
                    'complexity': 2,
                    'estimated_time': 8,
                    'can_parallel': True
                }
            },
            'data_operations': {
                'analyze_data': {
                    'name': 'Analyze Data',
                    'action': 'data_analysis',
                    'priority': 3,
                    'complexity': 4,
                    'estimated_time': 60,
                    'can_parallel': True
                },
                'convert_data': {
                    'name': 'Convert Data',
                    'action': 'data_conversion',
                    'priority': 2,
                    'complexity': 2,
                    'estimated_time': 15,
                    'can_parallel': True
                },
                'backup_data': {
                    'name': 'Backup Data',
                    'action': 'data_backup',
                    'priority': 4,
                    'complexity': 2,
                    'estimated_time': 45,
                    'can_parallel': True
                }
            },
            'communication': {
                'send_email': {
                    'name': 'Send Email',
                    'action': 'email_sending',
                    'priority': 3,
                    'complexity': 2,
                    'estimated_time': 10,
                    'can_parallel': True
                },
                'schedule_meeting': {
                    'name': 'Schedule Meeting',
                    'action': 'meeting_scheduling',
                    'priority': 3,
                    'complexity': 3,
                    'estimated_time': 15,
                    'can_parallel': True
                }
            },
            'information_gathering': {
                'search_info': {
                    'name': 'Search Information',
                    'action': 'information_search',
                    'priority': 2,
                    'complexity': 2,
                    'estimated_time': 8,
                    'can_parallel': True
                },
                'explain_topic': {
                    'name': 'Explain Topic',
                    'action': 'topic_explanation',
                    'priority': 2,
                    'complexity': 3,
                    'estimated_time': 12,
                    'can_parallel': True
                }
            },
            'automation': {
                'setup_automation': {
                    'name': 'Setup Automation',
                    'action': 'automation_setup',
                    'priority': 4,
                    'complexity': 4,
                    'estimated_time': 120,
                    'can_parallel': False
                },
                'create_reminder': {
                    'name': 'Create Reminder',
                    'action': 'reminder_creation',
                    'priority': 2,
                    'complexity': 1,
                    'estimated_time': 3,
                    'can_parallel': True
                }
            }
        }
        
        # Learned patterns
        self.learned_patterns = defaultdict(list)
        
        # Context memory
        self.context_memory = []
        
    def understand(self, command: str) -> Dict[str, Any]:
        """
        Understand a natural language command.
        
        Args:
            command: Natural language command
            
        Returns:
            Dictionary containing understanding of the command
        """
        command_lower = command.lower().strip()
        
        # Extract basic information
        understanding = {
            'original_command': command,
            'normalized_command': command_lower,
            'intents': [],
            'entities': {},
            'confidence': 0.0,
            'timestamp': datetime.now()
        }
        
        # Detect intents
        detected_intents = self._detect_intents(command_lower)
        understanding['intents'] = detected_intents
        
        # Extract entities
        entities = self._extract_entities(command_lower)
        understanding['entities'] = entities
        
        # Calculate confidence
        confidence = self._calculate_confidence(detected_intents, entities)
        understanding['confidence'] = confidence
        
        # Add context
        understanding['context'] = self._get_context(command_lower)
        
        self.logger.info(f"Command understood: {understanding}")
        return understanding
    
    def detect_tasks(self, understanding: Dict[str, Any]) -> List[Dict]:
        """
        Detect tasks from command understanding.
        
        Args:
            understanding: Command understanding dictionary
            
        Returns:
            List of tasks to be executed
        """
        tasks = []
        
        for intent in understanding['intents']:
            intent_type = intent['type']
            confidence = intent['confidence']
            
            if intent_type in self.task_templates:
                # Get all possible tasks for this intent
                possible_tasks = self.task_templates[intent_type]
                
                # Select the most appropriate task based on context
                selected_task = self._select_best_task(intent_type, understanding)
                
                if selected_task:
                    task = {
                        **selected_task,
                        'intent': intent,
                        'entities': understanding['entities'],
                        'context': understanding['context'],
                        'confidence': confidence,
                        'timestamp': datetime.now()
                    }
                    tasks.append(task)
        
        # Sort tasks by priority
        tasks.sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        self.logger.info(f"Detected {len(tasks)} tasks: {[task['name'] for task in tasks]}")
        return tasks
    
    def _detect_intents(self, command: str) -> List[Dict]:
        """Detect intents from the command."""
        intents = []
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, command, re.IGNORECASE)
                if matches:
                    confidence = len(matches) / len(patterns)  # Simple confidence calculation
                    intents.append({
                        'type': intent_type,
                        'pattern': pattern,
                        'matches': matches,
                        'confidence': confidence
                    })
        
        # Also check learned patterns
        for pattern, intent_info in self.learned_patterns.items():
            if pattern.lower() in command.lower():
                intents.append({
                    'type': intent_info['type'],
                    'pattern': pattern,
                    'matches': [pattern],
                    'confidence': intent_info['confidence'],
                    'learned': True
                })
        
        return intents
    
    def _extract_entities(self, command: str) -> Dict[str, Any]:
        """Extract entities from the command."""
        entities = {
            'files': [],
            'urls': [],
            'programs': [],
            'keywords': [],
            'numbers': [],
            'time_expressions': []
        }
        
        # Extract file names/extensions
        file_pattern = r'\b\w+\.\w+\b'
        entities['files'] = re.findall(file_pattern, command)
        
        # Extract URLs
        url_pattern = r'https?://[^\s]+'
        entities['urls'] = re.findall(url_pattern, command)
        
        # Extract program names
        program_pattern = r'\b(python|java|node|npm|pip|git|docker)\b'
        entities['programs'] = re.findall(program_pattern, command, re.IGNORECASE)
        
        # Extract numbers
        number_pattern = r'\b\d+\b'
        entities['numbers'] = re.findall(number_pattern, command)
        
        # Extract time expressions
        time_pattern = r'\b(today|tomorrow|next week|in \d+ (hours|days|weeks))\b'
        entities['time_expressions'] = re.findall(time_pattern, command, re.IGNORECASE)
        
        # Extract keywords (words that might be important)
        words = command.split()
        keywords = [word for word in words if len(word) > 3 and word not in ['with', 'from', 'into', 'that', 'this', 'they', 'have', 'will', 'been', 'were']]
        entities['keywords'] = keywords[:5]  # Limit to top 5 keywords
        
        return entities
    
    def _calculate_confidence(self, intents: List[Dict], entities: Dict) -> float:
        """Calculate confidence score for the understanding."""
        if not intents:
            return 0.0
        
        # Base confidence from intent detection
        max_intent_confidence = max(intent['confidence'] for intent in intents)
        
        # Bonus for having relevant entities
        entity_bonus = 0.0
        if entities['files']:
            entity_bonus += 0.1
        if entities['urls']:
            entity_bonus += 0.1
        if entities['programs']:
            entity_bonus += 0.1
        if entities['keywords']:
            entity_bonus += 0.05 * len(entities['keywords'])
        
        confidence = min(1.0, max_intent_confidence + entity_bonus)
        return confidence
    
    def _get_context(self, command: str) -> Dict[str, Any]:
        """Get context for the command."""
        context = {
            'time_of_day': self._get_time_context(),
            'recent_commands': self.context_memory[-5:] if self.context_memory else [],
            'common_patterns': self._get_common_patterns()
        }
        return context
    
    def _get_time_context(self) -> str:
        """Get time context."""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def _get_common_patterns(self) -> List[str]:
        """Get common patterns from recent commands."""
        if not self.context_memory:
            return []
        
        patterns = []
        for cmd in self.context_memory[-10:]:
            words = cmd.split()
            if len(words) >= 2:
                patterns.append(f"{words[0]} {words[1]}")
        
        return list(set(patterns))[:3]
    
    def _select_best_task(self, intent_type: str, understanding: Dict) -> Optional[Dict]:
        """Select the best task for the given intent and understanding."""
        if intent_type not in self.task_templates:
            return None
        
        possible_tasks = self.task_templates[intent_type]
        
        # Simple selection based on entities and context
        if intent_type == 'file_operations':
            if understanding['entities']['files']:
                return possible_tasks['open_file']
            else:
                return possible_tasks['create_file']
        
        elif intent_type == 'web_operations':
            if understanding['entities']['urls']:
                return possible_tasks['open_website']
            else:
                return possible_tasks['web_search']
        
        elif intent_type == 'system_operations':
            if understanding['entities']['programs']:
                return possible_tasks['run_program']
            else:
                return possible_tasks['system_check']
        
        elif intent_type == 'data_operations':
            return possible_tasks['analyze_data']
        
        elif intent_type == 'communication':
            return possible_tasks['send_email']
        
        elif intent_type == 'information_gathering':
            return possible_tasks['search_info']
        
        elif intent_type == 'automation':
            return possible_tasks['create_reminder']
        
        # Default to first task
        return list(possible_tasks.values())[0] if possible_tasks else None
    
    def learn_pattern(self, command: str, understanding: Dict):
        """Learn from a command pattern to improve future understanding."""
        # Extract key phrases
        words = command.lower().split()
        if len(words) >= 2:
            key_phrase = f"{words[0]} {words[1]}"
            
            # Store the pattern with its understanding
            self.learned_patterns[key_phrase] = {
                'type': understanding['intents'][0]['type'] if understanding['intents'] else 'unknown',
                'confidence': understanding['confidence'],
                'entities': understanding['entities'],
                'timestamp': datetime.now()
            }
        
        # Store in context memory
        self.context_memory.append(command)
        if len(self.context_memory) > 100:  # Keep only last 100 commands
            self.context_memory.pop(0)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get statistics about learned patterns."""
        return {
            'learned_patterns': len(self.learned_patterns),
            'context_memory_size': len(self.context_memory),
            'pattern_types': list(set(pattern['type'] for pattern in self.learned_patterns.values())),
            'most_common_patterns': self._get_most_common_patterns()
        }
    
    def _get_most_common_patterns(self) -> List[str]:
        """Get the most common learned patterns."""
        if not self.context_memory:
            return []
        
        pattern_counts = defaultdict(int)
        for cmd in self.context_memory:
            words = cmd.split()
            if len(words) >= 2:
                pattern = f"{words[0]} {words[1]}"
                pattern_counts[pattern] += 1
        
        # Return top 5 most common patterns
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        return [pattern for pattern, count in sorted_patterns[:5]]
