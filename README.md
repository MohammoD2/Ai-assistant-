# 🧠 AI Assistant - Brain-like Command Processing and Task Execution

A sophisticated AI assistant that works like a human brain - it can understand natural language commands, detect what tasks need to be done, and execute them automatically. The system includes learning capabilities, memory management, and knowledge integration.

## 🌟 Features

### 🧠 Brain-like Architecture
- **Command Processor**: Natural language understanding and intent detection
- **Task Executor**: Automatic task execution like the motor cortex
- **Memory Manager**: Short-term and long-term memory like the hippocampus
- **Knowledge Base**: Information storage and reasoning like the cerebral cortex

### 🎯 Core Capabilities
- **Natural Language Understanding**: Process commands in plain English
- **Intelligent Task Detection**: Automatically identify what needs to be done
- **Automatic Task Execution**: Execute tasks without manual intervention
- **Learning & Memory**: Learn from interactions and remember past experiences
- **Knowledge Integration**: Build and use knowledge for better decision making

### 📋 Supported Tasks

#### File Operations
- Create, open, read, write, save, delete files
- Copy, move, rename files and folders
- File format detection and handling

#### Web Operations
- Web searches and information gathering
- Website opening and navigation
- File downloads from the web

#### System Operations
- Package installation and management
- Program execution and script running
- System monitoring and status checks

#### Data Operations
- Data analysis and processing
- Format conversion and transformation
- Data backup and export

#### Communication
- Email composition and sending
- Meeting scheduling and reminders
- Information sharing

#### Information Gathering
- Question answering and explanations
- Topic research and learning
- Knowledge synthesis

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai_assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the AI assistant**:
   ```bash
   python main.py
   ```

### Basic Usage

#### Interactive Mode
Start the AI assistant in interactive mode to have a conversation:
```bash
python main.py
```

#### Single Command
Execute a single command:
```bash
python main.py "create a new file called test.txt"
python main.py "search for Python tutorials"
python main.py "check system status"
```

#### Demo Mode
See the AI assistant in action:
```bash
python main.py --demo
```

#### Status Check
View the brain's current status:
```bash
python main.py --status
```

## 💬 Example Commands

### File Operations
```
"create a new file called report.txt"
"open the document.pdf file"
"delete the old backup file"
"copy the important files to the backup folder"
```

### Web Operations
```
"search for machine learning tutorials"
"open https://www.github.com"
"download the latest Python installer"
"find information about artificial intelligence"
```

### System Operations
```
"install the numpy package"
"run the analysis script"
"check my computer's memory usage"
"update all installed packages"
```

### Information Gathering
```
"what is deep learning?"
"tell me about Python programming"
"explain how neural networks work"
"find the best practices for data science"
```

### Special Commands
```
"status"           # Show brain status
"think about AI"   # Use brain to think
"sleep"           # Put brain to sleep
"help"            # Show available commands
"quit"            # Exit the assistant
```

## 🏗️ Architecture

### Brain Components

#### 🧠 AI Brain (`src/brain.py`)
The central nervous system that coordinates all components:
- Command processing and understanding
- Task detection and planning
- Memory management and learning
- Knowledge integration
- Task execution monitoring

#### 🗣️ Command Processor (`src/command_processor.py`)
Processes natural language commands like the language centers of the brain:
- Intent recognition and classification
- Entity extraction and understanding
- Pattern learning and improvement
- Context awareness

#### ⚡ Task Executor (`src/task_executor.py`)
Executes tasks like the motor cortex:
- File operations (create, open, delete, etc.)
- Web operations (search, download, etc.)
- System operations (install, run, monitor)
- Data operations (analyze, convert, backup)
- Communication tasks (email, scheduling)

#### 🧠 Memory Manager (`src/memory_manager.py`)
Manages memory like the hippocampus:
- Short-term memory (working memory)
- Long-term memory (persistent storage)
- Memory consolidation and optimization
- Memory search and retrieval

#### 🧠 Knowledge Base (`src/knowledge_base.py`)
Stores and manages knowledge like the cerebral cortex:
- Factual knowledge storage
- Conceptual knowledge organization
- Reasoning rules and patterns
- Learning from interactions

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
# Logging level
LOG_LEVEL=INFO

# Memory settings
MEMORY_DIR=data/memory
KNOWLEDGE_DIR=data/knowledge

# Task execution settings
MAX_CONCURRENT_TASKS=5
TASK_TIMEOUT=300
```

### Customization
You can customize the AI assistant by:
- Adding new task types in `src/task_executor.py`
- Extending command patterns in `src/command_processor.py`
- Modifying memory settings in `src/memory_manager.py`
- Adding knowledge rules in `src/knowledge_base.py`

## 📊 Monitoring and Statistics

### Brain Status
View comprehensive brain statistics:
```bash
python main.py --status
```

This shows:
- Consciousness, energy, and focus levels
- Current tasks and total interactions
- Knowledge items and memory usage
- Recent activity and performance metrics

### Logging
The system provides detailed logging:
- Command processing logs
- Task execution logs
- Memory and knowledge operations
- Error tracking and debugging

## 🧪 Testing

### Run Tests
```bash
python -m pytest tests/
```

### Run Demo
```bash
python main.py --demo
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by human brain architecture and cognitive science
- Built with modern Python libraries and best practices
- Designed for extensibility and learning capabilities

## 🔮 Future Enhancements

- **Advanced NLP**: Integration with large language models
- **Computer Vision**: Image and video processing capabilities
- **Voice Interface**: Speech recognition and synthesis
- **Multi-modal Learning**: Learning from text, images, and audio
- **Collaborative Learning**: Sharing knowledge between instances
- **Advanced Reasoning**: More sophisticated decision-making algorithms

---

**🧠 The AI Assistant - Where artificial intelligence meets human-like understanding and execution!**
