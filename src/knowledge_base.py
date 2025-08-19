"""
Knowledge Base - The Cerebral Cortex of the AI Assistant
======================================================

This module handles:
- Knowledge storage and organization
- Information retrieval and reasoning
- Learning from interactions
- Knowledge synthesis and inference
- Contextual understanding
"""

import json
import os
import pickle
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

class KnowledgeBase:
    """
    Manages knowledge storage and reasoning for the AI assistant.
    Works like the cerebral cortex of the human brain.
    """
    
    def __init__(self, knowledge_dir: str = "data/knowledge"):
        """Initialize the knowledge base."""
        self.logger = logging.getLogger(__name__)
        self.knowledge_dir = knowledge_dir
        
        # Create knowledge directory if it doesn't exist
        os.makedirs(knowledge_dir, exist_ok=True)
        
        # Knowledge storage
        self.facts = {}  # Factual knowledge
        self.concepts = {}  # Conceptual knowledge
        self.rules = []  # Reasoning rules
        self.patterns = defaultdict(list)  # Learned patterns
        self.relationships = defaultdict(list)  # Knowledge relationships
        
        # Knowledge statistics
        self.knowledge_stats = {
            'total_facts': 0,
            'total_concepts': 0,
            'total_rules': 0,
            'total_patterns': 0,
            'last_update': datetime.now(),
            'learning_sessions': 0
        }
        
        # Load existing knowledge
        self._load_knowledge()
        
        # Initialize with basic knowledge
        self._initialize_basic_knowledge()
    
    def add_fact(self, fact: str, category: str = "general", confidence: float = 1.0, source: str = "user"):
        """Add a factual piece of knowledge."""
        fact_id = self._generate_knowledge_id(fact)
        
        fact_entry = {
            'id': fact_id,
            'content': fact,
            'category': category,
            'confidence': confidence,
            'source': source,
            'timestamp': datetime.now(),
            'access_count': 0,
            'last_accessed': datetime.now()
        }
        
        self.facts[fact_id] = fact_entry
        self.knowledge_stats['total_facts'] += 1
        
        # Index the fact
        self._index_knowledge(fact_entry, 'fact')
        
        self.logger.debug(f"Added fact: {fact[:50]}...")
    
    def add_concept(self, concept: str, definition: str, examples: List[str] = None, category: str = "general"):
        """Add a conceptual piece of knowledge."""
        concept_id = self._generate_knowledge_id(concept)
        
        concept_entry = {
            'id': concept_id,
            'name': concept,
            'definition': definition,
            'examples': examples or [],
            'category': category,
            'timestamp': datetime.now(),
            'access_count': 0,
            'last_accessed': datetime.now()
        }
        
        self.concepts[concept_id] = concept_entry
        self.knowledge_stats['total_concepts'] += 1
        
        # Index the concept
        self._index_knowledge(concept_entry, 'concept')
        
        self.logger.debug(f"Added concept: {concept}")
    
    def add_rule(self, condition: str, action: str, confidence: float = 1.0):
        """Add a reasoning rule."""
        rule_id = self._generate_knowledge_id(f"{condition} -> {action}")
        
        rule_entry = {
            'id': rule_id,
            'condition': condition,
            'action': action,
            'confidence': confidence,
            'timestamp': datetime.now(),
            'usage_count': 0,
            'success_count': 0
        }
        
        self.rules.append(rule_entry)
        self.knowledge_stats['total_rules'] += 1
        
        self.logger.debug(f"Added rule: {condition} -> {action}")
    
    def search_knowledge(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """
        Search for knowledge relevant to a query.
        
        Args:
            query: Search query
            category: Optional category filter
            limit: Maximum number of results
            
        Returns:
            List of relevant knowledge items
        """
        query_lower = query.lower()
        relevant_items = []
        
        # Search facts
        for fact_id, fact in self.facts.items():
            if category and fact['category'] != category:
                continue
            
            relevance = self._calculate_knowledge_relevance(fact, query_lower)
            if relevance > 0.1:
                fact['relevance_score'] = relevance
                fact['access_count'] += 1
                fact['last_accessed'] = datetime.now()
                relevant_items.append({
                    'type': 'fact',
                    'data': fact,
                    'relevance_score': relevance
                })
        
        # Search concepts
        for concept_id, concept in self.concepts.items():
            if category and concept['category'] != category:
                continue
            
            relevance = self._calculate_knowledge_relevance(concept, query_lower)
            if relevance > 0.1:
                concept['access_count'] += 1
                concept['last_accessed'] = datetime.now()
                relevant_items.append({
                    'type': 'concept',
                    'data': concept,
                    'relevance_score': relevance
                })
        
        # Sort by relevance
        relevant_items.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return relevant_items[:limit]
    
    def think_about(self, prompt: str) -> List[str]:
        """
        Use knowledge to think about a problem or question.
        
        Args:
            prompt: Question or problem to think about
            
        Returns:
            List of thoughts and insights
        """
        thoughts = []
        prompt_lower = prompt.lower()
        
        # Find relevant knowledge
        relevant_knowledge = self.search_knowledge(prompt, limit=20)
        
        # Generate thoughts based on knowledge
        for item in relevant_knowledge:
            if item['type'] == 'fact':
                fact = item['data']
                thoughts.append(f"Fact: {fact['content']}")
            
            elif item['type'] == 'concept':
                concept = item['data']
                thoughts.append(f"Concept: {concept['name']} - {concept['definition']}")
        
        # Apply reasoning rules
        applicable_rules = self._find_applicable_rules(prompt)
        for rule in applicable_rules:
            thoughts.append(f"Rule: If {rule['condition']}, then {rule['action']}")
        
        # Generate insights
        insights = self._generate_insights(prompt, relevant_knowledge)
        thoughts.extend(insights)
        
        return thoughts
    
    def update_from_interaction(self, interaction: Dict):
        """Learn from an interaction to update knowledge."""
        self.knowledge_stats['learning_sessions'] += 1
        
        # Extract knowledge from interaction
        command = interaction.get('command', '')
        tasks = interaction.get('tasks', [])
        results = interaction.get('results', [])
        
        # Learn patterns
        self._learn_patterns(command, tasks, results)
        
        # Extract facts from successful tasks
        for result in results:
            if result.get('success', False):
                output = result.get('output', {})
                if isinstance(output, dict):
                    # Extract facts from output
                    for key, value in output.items():
                        if isinstance(value, str) and len(value) > 10:
                            fact = f"{key}: {value}"
                            self.add_fact(fact, category="task_result", source="interaction")
        
        # Update knowledge statistics
        self.knowledge_stats['last_update'] = datetime.now()
        
        self.logger.debug(f"Updated knowledge from interaction: {command[:50]}...")
    
    def get_knowledge_summary(self, category: str = None) -> Dict[str, Any]:
        """Get a summary of knowledge in a category."""
        if category:
            facts = [f for f in self.facts.values() if f['category'] == category]
            concepts = [c for c in self.concepts.values() if c['category'] == category]
        else:
            facts = list(self.facts.values())
            concepts = list(self.concepts.values())
        
        return {
            'category': category or 'all',
            'fact_count': len(facts),
            'concept_count': len(concepts),
            'rule_count': len(self.rules),
            'pattern_count': len(self.patterns),
            'most_accessed_facts': sorted(facts, key=lambda x: x['access_count'], reverse=True)[:5],
            'most_accessed_concepts': sorted(concepts, key=lambda x: x['access_count'], reverse=True)[:5]
        }
    
    def save_knowledge(self):
        """Save knowledge to persistent storage."""
        try:
            # Save facts
            facts_file = os.path.join(self.knowledge_dir, 'facts.pkl')
            with open(facts_file, 'wb') as f:
                pickle.dump(self.facts, f)
            
            # Save concepts
            concepts_file = os.path.join(self.knowledge_dir, 'concepts.pkl')
            with open(concepts_file, 'wb') as f:
                pickle.dump(self.concepts, f)
            
            # Save rules
            rules_file = os.path.join(self.knowledge_dir, 'rules.pkl')
            with open(rules_file, 'wb') as f:
                pickle.dump(self.rules, f)
            
            # Save patterns
            patterns_file = os.path.join(self.knowledge_dir, 'patterns.pkl')
            with open(patterns_file, 'wb') as f:
                pickle.dump(dict(self.patterns), f)
            
            # Save statistics
            stats_file = os.path.join(self.knowledge_dir, 'knowledge_stats.json')
            with open(stats_file, 'w') as f:
                json.dump(self.knowledge_stats, f, default=str)
            
            self.logger.info("Knowledge saved to persistent storage")
            
        except Exception as e:
            self.logger.error(f"Failed to save knowledge: {e}")
    
    def get_item_count(self) -> int:
        """Get the total number of knowledge items."""
        return (self.knowledge_stats['total_facts'] + 
                self.knowledge_stats['total_concepts'] + 
                self.knowledge_stats['total_rules'])
    
    def _load_knowledge(self):
        """Load knowledge from persistent storage."""
        try:
            # Load facts
            facts_file = os.path.join(self.knowledge_dir, 'facts.pkl')
            if os.path.exists(facts_file):
                with open(facts_file, 'rb') as f:
                    self.facts = pickle.load(f)
            
            # Load concepts
            concepts_file = os.path.join(self.knowledge_dir, 'concepts.pkl')
            if os.path.exists(concepts_file):
                with open(concepts_file, 'rb') as f:
                    self.concepts = pickle.load(f)
            
            # Load rules
            rules_file = os.path.join(self.knowledge_dir, 'rules.pkl')
            if os.path.exists(rules_file):
                with open(rules_file, 'rb') as f:
                    self.rules = pickle.load(f)
            
            # Load patterns
            patterns_file = os.path.join(self.knowledge_dir, 'patterns.pkl')
            if os.path.exists(patterns_file):
                with open(patterns_file, 'rb') as f:
                    self.patterns = defaultdict(list, pickle.load(f))
            
            # Load statistics
            stats_file = os.path.join(self.knowledge_dir, 'knowledge_stats.json')
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    self.knowledge_stats = json.load(f)
            
            self.logger.info("Knowledge loaded from persistent storage")
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge: {e}")
    
    def _initialize_basic_knowledge(self):
        """Initialize the knowledge base with basic information."""
        # Add basic facts about the AI assistant
        self.add_fact("I am an AI assistant that can understand natural language commands", "system", 1.0, "system")
        self.add_fact("I can perform file operations like creating, opening, and deleting files", "capabilities", 1.0, "system")
        self.add_fact("I can perform web searches and open websites", "capabilities", 1.0, "system")
        self.add_fact("I can install packages and run programs", "capabilities", 1.0, "system")
        self.add_fact("I can analyze data and perform system checks", "capabilities", 1.0, "system")
        
        # Add basic concepts
        self.add_concept("Command Processing", "The ability to understand and interpret natural language commands", 
                        ["file operations", "web searches", "system tasks"], "system")
        self.add_concept("Task Execution", "The process of carrying out detected tasks automatically", 
                        ["file creation", "program execution", "data analysis"], "system")
        self.add_concept("Memory Management", "The ability to store and retrieve information from past interactions", 
                        ["short-term memory", "long-term memory", "memory consolidation"], "system")
        
        # Add basic rules
        self.add_rule("user wants to create a file", "use file creation task", 1.0)
        self.add_rule("user wants to search the web", "use web search task", 1.0)
        self.add_rule("user wants to install something", "use package installation task", 1.0)
        self.add_rule("user wants to check system status", "use system monitoring task", 1.0)
    
    def _generate_knowledge_id(self, content: str) -> str:
        """Generate a unique ID for a knowledge item."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_knowledge_relevance(self, item: Dict, query: str) -> float:
        """Calculate relevance between a knowledge item and a query."""
        relevance = 0.0
        query_words = set(query.split())
        
        # Check content
        if 'content' in item:
            content_words = set(item['content'].lower().split())
            if content_words:
                overlap = len(query_words.intersection(content_words))
                relevance += overlap / len(query_words) * 0.6
        
        # Check name/title
        if 'name' in item:
            name_words = set(item['name'].lower().split())
            if name_words:
                overlap = len(query_words.intersection(name_words))
                relevance += overlap / len(query_words) * 0.4
        
        # Check definition
        if 'definition' in item:
            def_words = set(item['definition'].lower().split())
            if def_words:
                overlap = len(query_words.intersection(def_words))
                relevance += overlap / len(query_words) * 0.3
        
        # Check category
        if item.get('category', '').lower() in query:
            relevance += 0.2
        
        return min(1.0, relevance)
    
    def _index_knowledge(self, item: Dict, item_type: str):
        """Index knowledge for search."""
        # Extract key terms
        if item_type == 'fact':
            text = item['content']
        elif item_type == 'concept':
            text = f"{item['name']} {item['definition']}"
        else:
            return
        
        words = set(text.lower().split())
        
        # Index by important words
        for word in words:
            if len(word) > 3:  # Only index words longer than 3 characters
                self.patterns[word].append(item['id'])
    
    def _find_applicable_rules(self, prompt: str) -> List[Dict]:
        """Find rules that apply to a given prompt."""
        applicable_rules = []
        prompt_lower = prompt.lower()
        
        for rule in self.rules:
            condition_lower = rule['condition'].lower()
            if any(word in prompt_lower for word in condition_lower.split()):
                applicable_rules.append(rule)
                rule['usage_count'] += 1
        
        return applicable_rules
    
    def _generate_insights(self, prompt: str, knowledge_items: List[Dict]) -> List[str]:
        """Generate insights based on knowledge and prompt."""
        insights = []
        
        # Simple insight generation based on patterns
        if 'file' in prompt.lower():
            insights.append("File operations are common tasks that I can help with")
        
        if 'search' in prompt.lower() or 'find' in prompt.lower():
            insights.append("I can perform web searches to find information")
        
        if 'install' in prompt.lower():
            insights.append("I can install packages and software for you")
        
        if 'system' in prompt.lower() or 'computer' in prompt.lower():
            insights.append("I can check system status and monitor your computer")
        
        return insights
    
    def _learn_patterns(self, command: str, tasks: List[Dict], results: List[Dict]):
        """Learn patterns from interactions."""
        # Extract command patterns
        words = command.lower().split()
        if len(words) >= 2:
            pattern = f"{words[0]} {words[1]}"
            self.patterns[pattern].append({
                'command': command,
                'tasks': [task['name'] for task in tasks],
                'success': all(result.get('success', False) for result in results),
                'timestamp': datetime.now()
            })
            self.knowledge_stats['total_patterns'] += 1
        
        # Learn from task results
        for result in results:
            if result.get('success', False):
                output = result.get('output', {})
                if isinstance(output, dict) and 'message' in output:
                    # Extract success patterns
                    success_pattern = f"successful_{result['task_name'].lower().replace(' ', '_')}"
                    self.patterns[success_pattern].append({
                        'task': result['task_name'],
                        'output': output,
                        'timestamp': datetime.now()
                    })
