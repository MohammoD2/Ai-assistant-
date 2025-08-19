#!/usr/bin/env python3
"""
AI Assistant - Brain-like Command Processing and Task Execution
=============================================================

Main entry point for the AI assistant that works like a human brain:
- Understands natural language commands
- Detects what tasks need to be done
- Executes tasks automatically
- Learns from interactions
- Manages memory and knowledge

Usage:
    python main.py                    # Start interactive mode
    python main.py "your command"     # Execute single command
    python main.py --demo             # Run demo commands
    python main.py --status           # Show brain status
"""

import sys
import argparse
import logging
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.text import Text

from src.brain import AIBrain

console = Console()

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ai_assistant.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def print_banner():
    """Print the AI Assistant banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🧠 AI ASSISTANT 🧠                        ║
    ║                                                              ║
    ║  Brain-like Command Processing and Task Execution System     ║
    ║                                                              ║
    ║  • Natural Language Understanding                            ║
    ║  • Intelligent Task Detection                               ║
    ║  • Automatic Task Execution                                 ║
    ║  • Learning and Memory Management                           ║
    ║  • Knowledge Integration                                    ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold blue"))

def print_help():
    """Print help information."""
    help_text = """
    [bold]Available Commands:[/bold]
    
    [green]File Operations:[/green]
    • "create a new file called test.txt"
    • "open the file document.pdf"
    • "delete the file old_file.txt"
    
    [green]Web Operations:[/green]
    • "search for Python tutorials"
    • "open https://www.google.com"
    • "download a file from https://example.com/file.zip"
    
    [green]System Operations:[/green]
    • "install the numpy package"
    • "run the python script"
    • "check system status"
    
    [green]Data Operations:[/green]
    • "analyze this data file"
    • "convert the file to CSV format"
    • "backup my important files"
    
    [green]Information Gathering:[/green]
    • "what is machine learning?"
    • "tell me about artificial intelligence"
    • "find information about Python programming"
    
    [green]Special Commands:[/green]
    • "status" - Show brain status
    • "think about [topic]" - Use brain to think
    • "sleep" - Put brain to sleep
    • "help" - Show this help
    • "quit" - Exit the assistant
    """
    console.print(Panel(help_text, title="[bold]AI Assistant Help[/bold]"))

def show_brain_status(brain: AIBrain):
    """Show the current brain status."""
    status = brain.get_brain_status()
    
    # Create status table
    table = Table(title="🧠 Brain Status")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("Active", "✅ Yes" if status['is_active'] else "❌ No")
    table.add_row("Consciousness Level", f"{status['consciousness_level']:.2f}")
    table.add_row("Energy Level", f"{status['energy_level']:.2f}")
    table.add_row("Focus Level", f"{status['focus_level']:.2f}")
    table.add_row("Current Tasks", str(status['current_tasks']))
    table.add_row("Total Interactions", str(status['total_interactions']))
    table.add_row("Knowledge Items", str(status['knowledge_items']))
    table.add_row("Memory Usage", f"{status['memory_usage']['memory_usage_mb']:.2f} MB")
    
    console.print(table)
    
    # Show recent activity
    if status['total_interactions'] > 0:
        console.print("\n[bold]Recent Activity:[/bold]")
        recent_memories = brain.memory_manager.get_recent_memories(hours=1, limit=5)
        for memory in recent_memories:
            data = memory['data']
            if 'command' in data:
                console.print(f"• {data['command'][:50]}...")

def run_demo(brain: AIBrain):
    """Run a demonstration of the AI assistant capabilities."""
    console.print(Panel("[bold green]🎬 Starting AI Assistant Demo[/bold green]"))
    
    demo_commands = [
        "create a new file called demo.txt",
        "search for artificial intelligence",
        "check system status",
        "think about machine learning",
        "what is Python programming?"
    ]
    
    for i, command in enumerate(demo_commands, 1):
        console.print(f"\n[bold cyan]Demo {i}/{len(demo_commands)}:[/bold cyan] {command}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing...", total=None)
            result = brain.process_command(command)
            progress.update(task, completed=True)
        
        if result.get('success'):
            console.print(f"[bold green]✅ Success![/bold green]")
            if result.get('results'):
                for task_result in result['results']:
                    if task_result.get('output', {}).get('message'):
                        console.print(f"   {task_result['output']['message']}")
        else:
            console.print(f"[bold red]❌ Error: {result.get('error')}[/bold red]")
        
        # Small delay for demo effect
        import time
        time.sleep(1)
    
    console.print(Panel("[bold green]🎉 Demo completed![/bold green]"))

def interactive_mode(brain: AIBrain):
    """Run the AI assistant in interactive mode."""
    console.print(Panel("[bold green]🔄 Starting Interactive Mode[/bold green]"))
    console.print("Type 'help' for available commands, 'quit' to exit\n")
    
    while brain.is_active:
        try:
            # Get command from user
            command = Prompt.ask("\n[bold cyan]🧠 Command[/bold cyan]")
            
            if not command.strip():
                continue
            
            # Handle special commands
            if command.lower() == 'quit' or command.lower() == 'exit':
                if Confirm.ask("Are you sure you want to quit?"):
                    break
            
            elif command.lower() == 'help':
                print_help()
                continue
            
            elif command.lower() == 'status':
                show_brain_status(brain)
                continue
            
            elif command.lower() == 'sleep':
                brain.sleep()
                break
            
            elif command.lower() == 'think':
                topic = Prompt.ask("What should I think about?")
                thoughts = brain.think(topic)
                console.print(Panel(thoughts, title="🤔 Thoughts"))
                continue
            
            # Process the command
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Processing command...", total=None)
                result = brain.process_command(command)
                progress.update(task, completed=True)
            
            # Show results
            if result.get('success'):
                console.print(f"[bold green]✅ Command processed successfully![/bold green]")
                
                # Show task results
                if result.get('results'):
                    for task_result in result['results']:
                        if task_result.get('success'):
                            if task_result.get('output', {}).get('message'):
                                console.print(f"   {task_result['output']['message']}")
                        else:
                            console.print(f"   [red]Task failed: {task_result.get('error')}[/red]")
            else:
                console.print(f"[bold red]❌ Error: {result.get('error')}[/bold red]")
                
        except KeyboardInterrupt:
            console.print("\n[bold yellow]⚠️ Interrupted by user[/bold yellow]")
            if Confirm.ask("Do you want to quit?"):
                break
        except Exception as e:
            console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
            logging.error(f"Interactive mode error: {e}")

def main():
    """Main entry point for the AI assistant."""
    parser = argparse.ArgumentParser(
        description="AI Assistant - Brain-like Command Processing and Task Execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Start interactive mode
  python main.py "create a new file"       # Execute single command
  python main.py --demo                    # Run demonstration
  python main.py --status                  # Show brain status
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        help='Command to execute (if not provided, starts interactive mode)'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demonstration of AI assistant capabilities'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show brain status and exit'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        setup_logging()
    
    # Print banner
    print_banner()
    
    try:
        # Initialize the AI brain
        console.print("[bold yellow]🧠 Initializing AI Brain...[/bold yellow]")
        brain = AIBrain()
        
        # Wake up the brain
        brain.wake_up()
        
        # Handle different modes
        if args.status:
            show_brain_status(brain)
            return
        
        elif args.demo:
            run_demo(brain)
            return
        
        elif args.command:
            # Execute single command
            console.print(f"[bold cyan]Executing command:[/bold cyan] {args.command}")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Processing...", total=None)
                result = brain.process_command(args.command)
                progress.update(task, completed=True)
            
            if result.get('success'):
                console.print(f"[bold green]✅ Command executed successfully![/bold green]")
                for task_result in result.get('results', []):
                    if task_result.get('output', {}).get('message'):
                        console.print(f"   {task_result['output']['message']}")
            else:
                console.print(f"[bold red]❌ Error: {result.get('error')}[/bold red]")
                return 1
        
        else:
            # Interactive mode
            interactive_mode(brain)
        
        # Put brain to sleep before exiting
        brain.sleep()
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ Interrupted by user[/bold yellow]")
        return 1
    except Exception as e:
        console.print(f"[bold red]❌ Fatal error: {e}[/bold red]")
        logging.error(f"Fatal error: {e}")
        return 1
    
    console.print("[bold green]👋 Goodbye![/bold green]")
    return 0

if __name__ == "__main__":
    sys.exit(main())
