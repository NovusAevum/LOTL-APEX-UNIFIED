#!/usr/bin/env python3
"""
LOTL-APEX Terminal Interface
Living Off The Land - Autonomous Persistent eXecution
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Input, Static, TextArea, Select, Button
from textual.reactive import reactive
from textual import events
import asyncio
import subprocess
import json
from datetime import datetime

class TipsPanel(Static):
    """Tips and suggestions panel"""
    
    def compose(self) -> ComposeResult:
        yield Static("💡 Tips & Suggestions", classes="panel-header")
        yield Static("• Ask questions, edit files, or run commands")
        yield Static("• Be specific for the best results") 
        yield Static("• /help for more information")

class ToolsPanel(Static):
    """Available tools sidebar"""
    
    def compose(self) -> ComposeResult:
        yield Static("🛠️ Available Tools", classes="panel-header")
        yield Button("📁 File Operations", id="tool-files")
        yield Button("☁️ AWS CLI", id="tool-aws")
        yield Button("🔍 OSINT Suite", id="tool-osint")
        yield Button("🐚 Shell Commands", id="tool-shell")
        yield Button("🤖 AI Operations", id="tool-ai")

class AgentsPanel(Static):
    """List of available agents"""
    
    agents = reactive(["Amazon Q", "Claude", "LOTL Agent", "OSINT Agent"])
    
    def compose(self) -> ComposeResult:
        yield Static("🤖 List of Agents", classes="panel-header")
        yield Select(
            [(agent, agent) for agent in self.agents],
            value="LOTL Agent",
            id="agent-select"
        )

class ChatInterface(Container):
    """Main chat and command interface"""
    
    def compose(self) -> ComposeResult:
        yield Static("💬 Chat Interface", classes="panel-header")
        yield TextArea("", id="chat-output", read_only=True)
        yield Input(placeholder="Type your message or @path/file...", id="chat-input")

class QuickCommands(Static):
    """Quick command buttons"""
    
    def compose(self) -> ComposeResult:
        yield Static("⚡ Quick Commands", classes="panel-header")
        yield Button("ls -la", id="cmd-ls")
        yield Button("pwd", id="cmd-pwd")
        yield Button("whoami", id="cmd-whoami")
        yield Button("df -h", id="cmd-df")

class LOTLTerminalApp(App):
    """Main LOTL Terminal Application"""
    
    CSS = """
    .panel-header {
        background: $primary;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
    }
    
    #tips-panel {
        height: 6;
        border: solid $primary;
    }
    
    #tools-panel {
        width: 25;
        border: solid $secondary;
    }
    
    #agents-panel {
        width: 25;
        border: solid $accent;
    }
    
    #chat-interface {
        border: solid $success;
    }
    
    #quick-commands {
        height: 8;
        border: solid $warning;
    }
    
    #chat-output {
        height: 1fr;
        margin: 1;
    }
    
    #chat-input {
        margin: 1;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create the application layout"""
        yield Container(
            TipsPanel(id="tips-panel"),
            Horizontal(
                ToolsPanel(id="tools-panel"),
                Vertical(
                    ChatInterface(id="chat-interface"),
                    QuickCommands(id="quick-commands"),
                ),
                AgentsPanel(id="agents-panel"),
            ),
        )
    
    def on_mount(self) -> None:
        """Initialize the application"""
        self.title = "LOTL-APEX Terminal Interface"
        self.sub_title = "Living Off The Land - Autonomous Persistent eXecution"
        
        # Add welcome message
        chat_output = self.query_one("#chat-output", TextArea)
        welcome_msg = f"""
🎯 LOTL-APEX Terminal Interface Initialized
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent: LOTL Agent (Active)
Status: Ready for commands

Type 'help' for available commands or select tools from the sidebar.
        """
        chat_output.text = welcome_msg.strip()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle chat input submission"""
        if event.input.id == "chat-input":
            message = event.value
            if message.strip():
                await self.process_command(message)
                event.input.value = ""
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if button_id.startswith("cmd-"):
            command = event.button.label
            await self.execute_shell_command(command)
        elif button_id.startswith("tool-"):
            tool = button_id.replace("tool-", "")
            await self.activate_tool(tool)
    
    async def process_command(self, command: str) -> None:
        """Process user commands"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        # Add user message
        timestamp = datetime.now().strftime('%H:%M:%S')
        chat_output.text += f"\n[{timestamp}] User: {command}"
        
        # Process different command types
        if command.startswith('/'):
            await self.handle_system_command(command)
        elif command.startswith('@'):
            await self.handle_file_operation(command)
        elif command.lower() in ['help', 'h']:
            await self.show_help()
        else:
            await self.handle_ai_query(command)
    
    async def handle_system_command(self, command: str) -> None:
        """Handle system commands starting with /"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        if command == '/help':
            await self.show_help()
        elif command == '/status':
            await self.show_status()
        elif command == '/agents':
            await self.list_agents()
        else:
            chat_output.text += f"\n🤖 LOTL: Unknown system command: {command}"
    
    async def handle_file_operation(self, command: str) -> None:
        """Handle file operations starting with @"""
        chat_output = self.query_one("#chat-output", TextArea)
        filepath = command[1:]  # Remove @
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            chat_output.text += f"\n📁 File: {filepath}\n{content[:500]}..."
        except Exception as e:
            chat_output.text += f"\n❌ Error reading file: {e}"
    
    async def handle_ai_query(self, query: str) -> None:
        """Handle AI queries"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        # Simulate AI response (integrate with actual LLM later)
        chat_output.text += f"\n🤖 LOTL: Processing query: {query}"
        chat_output.text += f"\n🤖 LOTL: [AI response would appear here]"
    
    async def execute_shell_command(self, command: str) -> None:
        """Execute shell commands"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            chat_output.text += f"\n[{timestamp}] $ {command}"
            
            if result.stdout:
                chat_output.text += f"\n{result.stdout}"
            if result.stderr:
                chat_output.text += f"\n❌ {result.stderr}"
                
        except subprocess.TimeoutExpired:
            chat_output.text += f"\n⏰ Command timed out: {command}"
        except Exception as e:
            chat_output.text += f"\n❌ Error executing command: {e}"
    
    async def activate_tool(self, tool: str) -> None:
        """Activate specific tools"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        tool_messages = {
            "files": "📁 File Operations activated. Use @path/file to read files.",
            "aws": "☁️ AWS CLI activated. Use 'aws' commands.",
            "osint": "🔍 OSINT Suite activated. Use 'osint' commands.",
            "shell": "🐚 Shell Commands activated. Direct command execution enabled.",
            "ai": "🤖 AI Operations activated. Enhanced AI responses enabled."
        }
        
        message = tool_messages.get(tool, f"🛠️ Tool '{tool}' activated.")
        chat_output.text += f"\n{message}"
    
    async def show_help(self) -> None:
        """Show help information"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        help_text = """
🆘 LOTL-APEX Help

Commands:
  /help     - Show this help
  /status   - Show system status  
  /agents   - List available agents
  @file     - Read file content
  help      - General help

Tools:
  📁 Files  - File operations and editing
  ☁️ AWS    - AWS CLI commands
  🔍 OSINT  - Reconnaissance tools
  🐚 Shell  - Direct shell access
  🤖 AI     - AI-powered assistance

Quick Commands:
  ls -la    - List directory contents
  pwd       - Show current directory
  whoami    - Show current user
  df -h     - Show disk usage
        """
        
        chat_output.text += help_text
    
    async def show_status(self) -> None:
        """Show system status"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        status_text = f"""
📊 System Status
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Agent: LOTL Agent (Active)
Tools: All systems operational
Memory: Context preserved
Network: Connected
        """
        
        chat_output.text += status_text
    
    async def list_agents(self) -> None:
        """List available agents"""
        chat_output = self.query_one("#chat-output", TextArea)
        
        agents_text = """
🤖 Available Agents:
  • LOTL Agent    - System operations and shell commands
  • Amazon Q      - AWS and cloud operations  
  • Claude        - General AI assistance
  • OSINT Agent   - Reconnaissance and data gathering
        """
        
        chat_output.text += agents_text

if __name__ == "__main__":
    app = LOTLTerminalApp()
    app.run()
