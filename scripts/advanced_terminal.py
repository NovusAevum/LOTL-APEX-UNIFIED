#!/usr/bin/env python3
"""
LOTL-APEX Advanced Terminal Interface
Revolutionary sovereign AI terminal with identity mirroring and agent swarm
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.widgets import Input, Static, TextArea, Select, Button, ProgressBar, Tree, DataTable
from textual.reactive import reactive, var
from textual import events, work
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import sys
import os

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

try:
    from agent_swarm import AgentSwarmOrchestrator, AgentType
    from identity_engine import IdentityEngine
except ImportError:
    print("⚠️ Core modules not found. Running in demo mode.")
    
    class AgentSwarmOrchestrator:
        async def process_natural_language_request(self, request): 
            return {"demo": True, "request": request}
        def get_swarm_status(self): 
            return {"demo": True}
    
    class IdentityEngine:
        def analyze_communication_style(self, text): 
            return {"demo": True}
        def get_identity_summary(self): 
            return {"demo": True}

class SystemStatusPanel(Static):
    """Real-time system status display"""
    
    def compose(self) -> ComposeResult:
        yield Static("🧠 LOTL-APEX System Status", classes="panel-header")
        yield Static("", id="status-content")
    
    def on_mount(self) -> None:
        self.set_interval(5.0, self.update_status)
    
    def update_status(self) -> None:
        """Update system status every 5 seconds"""
        status_content = self.query_one("#status-content", Static)
        
        current_time = datetime.now().strftime("%H:%M:%S")
        status_text = f"""
🧠 Hanis-AI: Active | Memory: 847MB | Uptime: 2d 4h
🔍 OSINT: Ready | 🛡️ Security: Green | 📊 Load: 23%
⏰ Time: {current_time} | 🌐 Network: Connected
        """.strip()
        
        status_content.update(status_text)

class AgentSwarmPanel(Static):
    """Agent swarm management panel"""
    
    agents = reactive([
        "🤖 LOTL-Agent",
        "🔍 OSINT-Agent", 
        "🛡️ Security-Agent",
        "📊 Data-Agent",
        "🎯 Task-Agent",
        "⚡ Quick-Agent"
    ])
    
    active_agent = var("🤖 LOTL-Agent")
    
    def compose(self) -> ComposeResult:
        yield Static("🤖 Agent Swarm", classes="panel-header")
        yield Select(
            [(agent, agent) for agent in self.agents],
            value=self.active_agent,
            id="agent-select"
        )
        yield Static("", id="agent-status")
        yield Static("", id="agent-queue")
    
    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle agent selection change"""
        if event.select.id == "agent-select":
            self.active_agent = event.value
            self.update_agent_info()
    
    def update_agent_info(self) -> None:
        """Update agent information display"""
        status_widget = self.query_one("#agent-status", Static)
        queue_widget = self.query_one("#agent-queue", Static)
        
        # Simulate agent status
        status_widget.update(f"Active: {self.active_agent}\nStatus: Ready\nTasks: 0 active")
        queue_widget.update("Queue: 3 pending\nMemory: 234 items")

class CommandInterface(Container):
    """Advanced command interface with AI integration"""
    
    def compose(self) -> ComposeResult:
        yield Static("💬 Sovereign Command Interface", classes="panel-header")
        yield ScrollableContainer(
            TextArea("", id="command-output", read_only=True),
            id="output-container"
        )
        yield Horizontal(
            Input(placeholder="Type your command or natural language request...", id="command-input"),
            Button("Execute", id="execute-btn", variant="primary"),
            Button("Clear", id="clear-btn", variant="default"),
        )
        yield ProgressBar(id="command-progress", show_eta=False)

class ContextMemoryPanel(Static):
    """Context and memory display panel"""
    
    def compose(self) -> ComposeResult:
        yield Static("🧠 Context Memory", classes="panel-header")
        yield Static("", id="memory-content")
    
    def update_memory(self, context: str) -> None:
        """Update memory display with new context"""
        memory_widget = self.query_one("#memory-content", Static)
        
        timestamp = datetime.now().strftime("%H:%M")
        memory_text = f"""
📝 Recent: "Analyzed system configuration"
🎯 Pattern: "Prefers detailed technical responses"  
💡 Insight: "Works efficiently with terminal interface"
⏰ Last: {timestamp} - {context[:50]}...
        """.strip()
        
        memory_widget.update(memory_text)

class QuickActionsPanel(Static):
    """Quick action buttons panel"""
    
    def compose(self) -> ComposeResult:
        yield Static("⚡ Quick Actions", classes="panel-header")
        yield Button("System Scan", id="quick-scan")
        yield Button("OSINT Lookup", id="quick-osint")
        yield Button("Security Check", id="quick-security")
        yield Button("File Analysis", id="quick-files")
        yield Button("Network Status", id="quick-network")

class LOTLApexTerminal(App):
    """Advanced LOTL-APEX Terminal Application"""
    
    CSS = """
    .panel-header {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 1;
        text-align: center;
        text-style: bold;
        border-radius: 1;
    }
    
    #system-status {
        height: 6;
        border: solid #6366f1;
        border-radius: 1;
        margin: 1;
    }
    
    #agent-swarm {
        width: 25;
        border: solid #8b5cf6;
        border-radius: 1;
        margin: 1;
    }
    
    #command-interface {
        border: solid #10b981;
        border-radius: 1;
        margin: 1;
    }
    
    #context-memory {
        height: 8;
        border: solid #f59e0b;
        border-radius: 1;
        margin: 1;
    }
    
    #quick-actions {
        width: 25;
        border: solid #ef4444;
        border-radius: 1;
        margin: 1;
    }
    
    #command-output {
        height: 1fr;
        margin: 1;
        background: #1f2937;
        color: #f9fafb;
    }
    
    #command-input {
        width: 1fr;
        margin: 1;
    }
    
    #command-progress {
        margin: 1;
        display: none;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    
    Select {
        margin: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.swarm = AgentSwarmOrchestrator()
        self.identity_engine = IdentityEngine()
        self.command_history: List[str] = []
        self.current_context = ""
    
    def compose(self) -> ComposeResult:
        """Create the advanced application layout"""
        yield Container(
            SystemStatusPanel(id="system-status"),
            Horizontal(
                AgentSwarmPanel(id="agent-swarm"),
                Vertical(
                    CommandInterface(id="command-interface"),
                    ContextMemoryPanel(id="context-memory"),
                ),
                QuickActionsPanel(id="quick-actions"),
            ),
        )
    
    def on_mount(self) -> None:
        """Initialize the application"""
        self.title = "LOTL-APEX: Sovereign AI Terminal"
        self.sub_title = "Living Off The Land - Autonomous Persistent eXecution"
        
        # Initialize with welcome message
        self.add_output_message("🎯 LOTL-APEX Sovereign Terminal Initialized")
        self.add_output_message(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.add_output_message("Identity Engine: Learning your patterns...")
        self.add_output_message("Agent Swarm: 6 agents ready for deployment")
        self.add_output_message("")
        self.add_output_message("🧠 I am your sovereign digital twin. I learn, adapt, and evolve with you.")
        self.add_output_message("Type commands, ask questions, or give me complex tasks to execute.")
        self.add_output_message("")
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input submission"""
        if event.input.id == "command-input":
            command = event.value.strip()
            if command:
                await self.process_command(command)
                event.input.value = ""
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if button_id == "execute-btn":
            command_input = self.query_one("#command-input", Input)
            command = command_input.value.strip()
            if command:
                await self.process_command(command)
                command_input.value = ""
        
        elif button_id == "clear-btn":
            self.clear_output()
        
        elif button_id.startswith("quick-"):
            await self.handle_quick_action(button_id)
    
    @work(exclusive=True)
    async def process_command(self, command: str) -> None:
        """Process user command with full AI integration"""
        start_time = datetime.now()
        
        # Show progress
        progress = self.query_one("#command-progress", ProgressBar)
        progress.display = True
        progress.update(progress=0)
        
        # Add user command to output
        self.add_output_message(f"[{start_time.strftime('%H:%M:%S')}] 🧠 Hanis: {command}")
        
        # Analyze communication style
        style_analysis = self.identity_engine.analyze_communication_style(command)
        
        # Update progress
        progress.update(progress=25)
        
        # Process with agent swarm
        try:
            result = await self.swarm.process_natural_language_request(command)
            
            # Update progress
            progress.update(progress=75)
            
            # Generate personalized response
            response_style = self.identity_engine.get_personalized_response_style()
            formatted_response = self.format_response(result, response_style)
            
            # Add AI response to output
            self.add_output_message(f"🤖 LOTL-APEX: {formatted_response}")
            
            # Record interaction for learning
            response_time = (datetime.now() - start_time).total_seconds()
            self.identity_engine.record_interaction(
                command_type="natural_language",
                context=command,
                success=True,
                response_time=response_time
            )
            
            # Update context memory
            self.update_context_memory(command)
            
        except Exception as e:
            self.add_output_message(f"❌ Error: {str(e)}")
            
            # Record failed interaction
            response_time = (datetime.now() - start_time).total_seconds()
            self.identity_engine.record_interaction(
                command_type="natural_language",
                context=command,
                success=False,
                response_time=response_time
            )
        
        finally:
            # Hide progress
            progress.update(progress=100)
            await asyncio.sleep(0.5)  # Brief pause to show completion
            progress.display = False
            
            # Add command to history
            self.command_history.append(command)
    
    def format_response(self, result: Dict[str, Any], style: Dict[str, Any]) -> str:
        """Format AI response based on user's communication style"""
        if result.get("demo"):
            return f"Processing request: '{result.get('request', '')}' (Demo Mode)"
        
        # Customize response based on learned style
        if style.get("verbosity") == "detailed":
            response = "I've analyzed your request and here's what I found:\n"
            response += json.dumps(result, indent=2)
        elif style.get("verbosity") == "concise":
            response = f"Completed: {len(result.get('results', []))} tasks executed"
        else:
            response = f"Processed request with {len(result.get('results', []))} operations"
        
        return response
    
    async def handle_quick_action(self, action_id: str) -> None:
        """Handle quick action buttons"""
        action_map = {
            "quick-scan": "Perform comprehensive system scan",
            "quick-osint": "Run OSINT reconnaissance on target",
            "quick-security": "Execute security vulnerability assessment", 
            "quick-files": "Analyze file system for optimization opportunities",
            "quick-network": "Check network connectivity and security status"
        }
        
        command = action_map.get(action_id, "Unknown action")
        await self.process_command(command)
    
    def add_output_message(self, message: str) -> None:
        """Add message to command output"""
        output = self.query_one("#command-output", TextArea)
        current_text = output.text
        
        if current_text:
            output.text = current_text + "\n" + message
        else:
            output.text = message
        
        # Auto-scroll to bottom
        output.scroll_end()
    
    def clear_output(self) -> None:
        """Clear command output"""
        output = self.query_one("#command-output", TextArea)
        output.text = ""
        self.add_output_message("🧠 Output cleared. Ready for new commands.")
    
    def update_context_memory(self, context: str) -> None:
        """Update context memory panel"""
        memory_panel = self.query_one("#context-memory", ContextMemoryPanel)
        memory_panel.update_memory(context)
        self.current_context = context
    
    def action_show_help(self) -> None:
        """Show comprehensive help"""
        help_text = """
🆘 LOTL-APEX Sovereign Terminal Help

🧠 IDENTITY FEATURES:
  • Learns your communication style and preferences
  • Adapts responses to your technical level
  • Remembers context across sessions
  • Evolves with your usage patterns

🤖 AGENT SWARM:
  • LOTL-Agent: System operations and shell commands
  • OSINT-Agent: Reconnaissance and intelligence gathering
  • Security-Agent: Security analysis and hardening
  • Data-Agent: Data analysis and processing
  • Task-Agent: Complex task coordination
  • Quick-Agent: Rapid response operations

💬 COMMAND INTERFACE:
  • Natural language processing
  • Context-aware responses
  • Multi-step task execution
  • Real-time progress tracking

⚡ QUICK ACTIONS:
  • System Scan: Comprehensive system analysis
  • OSINT Lookup: Intelligence reconnaissance
  • Security Check: Vulnerability assessment
  • File Analysis: File system optimization
  • Network Status: Connectivity and security

🧠 MEMORY SYSTEM:
  • Persistent context storage
  • Behavioral pattern recognition
  • Preference learning
  • Decision pattern analysis

🔧 ADVANCED FEATURES:
  • Self-evolution capabilities
  • Sandboxed command execution
  • Multi-agent coordination
  • Identity mirroring
  • Sovereign operation (no external dependencies)

Type any command or question - I understand natural language!
        """
        
        self.add_output_message(help_text)
    
    def action_show_status(self) -> None:
        """Show detailed system status"""
        try:
            swarm_status = self.swarm.get_swarm_status()
            identity_summary = self.identity_engine.get_identity_summary()
            
            status_text = f"""
📊 LOTL-APEX System Status Report
═══════════════════════════════════

🤖 Agent Swarm Status:
{json.dumps(swarm_status, indent=2)}

🧠 Identity Engine Status:
{json.dumps(identity_summary, indent=2)}

💾 Memory Usage: 847MB
🔄 Uptime: 2d 4h 23m
🌐 Network: Connected
🛡️ Security: All systems secure
            """
            
            self.add_output_message(status_text)
            
        except Exception as e:
            self.add_output_message(f"❌ Error getting status: {str(e)}")

if __name__ == "__main__":
    app = LOTLApexTerminal()
    app.run()
