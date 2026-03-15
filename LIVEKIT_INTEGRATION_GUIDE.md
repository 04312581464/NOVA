# 🌐 LiveKit Integration - Complete Reference Guide

## 📋 **Overview**

LiveKit is the core communication platform that powers Nova AI's voice chat capabilities. This guide covers all integration codes, functions, and related components used in your Nova AI implementation.

## 🏗️ **Core LiveKit Architecture**

### **📦 Main Imports**
```python
# Core LiveKit imports
from livekit import agents                    # Main agents framework
from livekit.agents import Agent, AgentSession, RoomInputOptions  # Core classes
from livekit.plugins import noise_cancellation            # Audio processing
from livekit.plugins.google.beta.realtime import RealtimeModel  # LLM integration
```

### **🎯 Key Components**

#### **1. Agent Class**
```python
from livekit.agents import Agent

class UltimateAdvancedNova(Agent):
    def __init__(self):
        super().__init__(
            instructions=self._build_instructions(),
            tools=tools,
            llm=self._init_llm(),
        )
```

#### **2. AgentSession**
```python
from livekit.agents import AgentSession

# Session management
session = AgentSession()
await session.start(
    room=ctx.room,
    agent=agent,
    room_input_options=RoomInputOptions(...)
)
```

#### **3. RoomInputOptions**
```python
from livekit.agents import RoomInputOptions

# Configuration for room interaction
RoomInputOptions(
    video_enabled=False,                    # Disable video
    noise_cancellation=noise_cancellation.BVC(),  # Audio processing
)
```

#### **4. JobContext**
```python
from livekit import agents

# Entry point context
async def entrypoint(ctx: agents.JobContext):
    # ctx contains job information and room connection
    await ctx.connect()
```

## 🔧 **LiveKit Functions & Methods**

### **🚀 Agent Initialization**

#### **Core Agent Setup**
```python
class UltimateAdvancedNova(Agent):
    def __init__(self):
        # Initialize agent state
        self._reminders: Dict[str, Dict[str, Any]] = {}
        self._reminder_task: Optional[asyncio.Task] = None
        self._session: Optional[AgentSession] = None
        self._reminder_counter = 0
        
        # Define available tools
        tools = [tool1, tool2, tool3, ...]
        
        # Initialize with LiveKit
        super().__init__(
            instructions=self._build_instructions(),
            tools=tools,
            llm=self._init_llm(),
        )
```

#### **LLM Initialization**
```python
def _init_llm(self):
    """Initialize language model with LiveKit"""
    network_available = self._check_network()
    if network_available:
        try:
            from livekit.plugins.google.beta.realtime import RealtimeModel
            return RealtimeModel(
                model="gemini-2.5-flash-native-audio-preview-12-2025",
                voice="Charon",
                temperature=0.9,
                max_output_tokens=1024,
            )
        except Exception as e:
            print(f"⚠️ LLM init failed: {e}")
            return None
    return None
```

#### **Network Detection**
```python
def _check_network(self):
    """Check network availability for LiveKit"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except Exception:
        return False
```

### **🎤 Session Management**

#### **Session Setup**
```python
async def entrypoint(ctx: agents.JobContext):
    print("🚀 Starting Nova...")
    
    # Create agent and session
    agent = UltimateAdvancedNova()
    session = AgentSession()

    # Start LiveKit session
    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            video_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Connect to room
    await ctx.connect()
    
    # Start conversation
    await session.generate_reply(instructions=SESSION_INSTRUCTION)
```

#### **Session Linking**
```python
def set_session(self, session: AgentSession):
    """Link session to agent for tool access"""
    self._session = session
    print("🔔 Session linked for reminders")
    
    # Connect session to other systems
    from Tools.smart_reminder import smart_reminder
    smart_reminder.set_session(session)
```

### **🔊 Audio Processing**

#### **Noise Cancellation**
```python
from livekit.plugins import noise_cancellation

# BVC (Background Voice Cancellation) plugin
RoomInputOptions(
    noise_cancellation=noise_cancellation.BVC(),
)
```

#### **Audio I/O Configuration**
```python
# LiveKit automatically handles audio I/O
# - Microphone input
# - Speaker output
# - Audio processing
# - Voice recognition
```

## 🛠️ **Tool Integration with LiveKit**

### **🔧 Function Tools**
```python
from livekit.agents import function_tool

@function_tool()
async def my_tool(param: str) -> str:
    """Tool description for AI"""
    try:
        # Tool logic here
        result = f"Processed: {param}"
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

### **📋 Tool Registration**
```python
class UltimateAdvancedNova(Agent):
    def __init__(self):
        # List of all available tools
        tools = [
            search_web,
            get_time_info,
            open_app,
            lockdown_mode_on,
            lockdown_mode_off,
            # ... more tools
        ]
        
        super().__init__(
            instructions=self._build_instructions(),
            tools=tools,  # Register tools with LiveKit
            llm=self._init_llm(),
        )
```

### **🎤 Tool Usage in Conversation**
```python
# AI automatically uses tools based on conversation
# User: "What time is it?"
# AI: Automatically calls get_time_info() tool

# User: "Lock my PC"
# AI: Automatically calls lockdown_mode_on() tool
```

## 🌐 **LiveKit Configuration**

### **📝 Environment Variables**
```python
# LiveKit connection settings (from .env)
LIVEKIT_URL=wss://nova-iezs0u48.livekit.cloud
LIVEKIT_API_KEY=APIdTAS9xXXKpUB
LIVEKIT_API_SECRET=biut0M8OLG7v1JYh6vqB2y2YDtmSFHpXWfgTi6dsDgF
```

### **🔑 Agent Identification**
```python
# Agent ID extracted from URL
Agent ID: nova-iezs0u48
URL: wss://nova-iezs0u48.livekit.cloud
```

### **🎛️ Room Configuration**
```python
# LiveKit room setup
RoomInputOptions(
    video_enabled=False,                    # Video disabled for voice-only
    noise_cancellation=noise_cancellation.BVC(),  # Audio enhancement
)
```

## 🚀 **LiveKit CLI Commands**

### **📱 Console Mode**
```bash
# Start Nova in console mode
python agent.py console

# LiveKit CLI options:
# - [Ctrl+B] Toggle Text/Audio mode
# - [Q] Quit application
```

### **🔧 Available Commands**
```bash
python agent.py --help

# Commands:
# connect         Connect to specific room
# console         Start console conversation
# dev             Development mode
# download-files  Download dependencies
# start           Production mode
```

### **🌐 Connection Options**
```python
# LiveKit worker options
agents.WorkerOptions(entrypoint_fnc=entrypoint)

# Handles:
# - Room connection
# - Session management
# - Audio processing
# - Tool execution
# - Error handling
```

## 🔄 **LiveKit Lifecycle**

### **📊 Session Flow**
```python
1. 🚀 entrypoint() called
2. 🤖 Agent instance created
3. 📱 AgentSession created
4. 🔗 session.start() called
5. 🌐 ctx.connect() executed
6. 💬 session.generate_reply() started
7. 🎤 Voice interaction begins
8. 🛑 Session ends on cancellation
```

### **⚡ Async Operations**
```python
# All LiveKit operations are async
async def some_function():
    # Await LiveKit operations
    await session.generate_reply(instructions)
    await ctx.connect()
    await session.start(...)
```

### **🔄 Event Loop**
```python
# Main event loop
try:
    await asyncio.Future()  # Keep running
except asyncio.CancelledError:
    print("🛑 Nova stopped")
```

## 🎯 **LiveKit Features Used**

### **🎤 Voice Chat**
```python
# Real-time voice conversation
# - Speech-to-text
# - Text-to-speech
# - Natural conversation flow
# - Voice activity detection
```

### **🔊 Audio Processing**
```python
# Advanced audio handling
noise_cancellation.BVC()  # Background voice cancellation
# - Echo cancellation
# - Noise reduction
# - Audio normalization
# - Real-time processing
```

### **🤖 AI Integration**
```python
# LLM integration via LiveKit
RealtimeModel(
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    voice="Charon",      # Voice model
    temperature=0.9,     # Creativity
    max_output_tokens=1024, # Response length
)
```

### **🛠️ Tool Execution**
```python
# LiveKit automatically executes tools
@function_tool() decorators
# - Parameter validation
# - Error handling
# - Result formatting
# - Async execution
```

## 🔧 **LiveKit Error Handling**

### **⚠️ Common Errors**
```python
# Network issues
socket.create_connection(("8.8.8.8", 53), timeout=3)

# LLM initialization
except Exception as e:
    print(f"⚠️ LLM init failed: {e}")
    return None

# Session errors
except asyncio.CancelledError:
    print("🛑 Nova stopped")
```

### **🔄 Fallback Modes**
```python
# Network unavailable
if not network_available:
    print("⚠️ Network issue → Offline fallback mode")
    return None  # No LLM

# LLM unavailable
if agent.llm is None:
    # Basic conversation without AI
    print("💬 Basic mode ready")
```

## 📊 **LiveKit Performance**

### **⚡ Optimization Features**
```python
# Async operations for performance
await session.generate_reply()  # Non-blocking

# Efficient audio processing
noise_cancellation.BVC()  # Optimized algorithms

# Resource management
asyncio.Task  # Proper async handling
```

### **📈 Monitoring**
```python
# LiveKit provides built-in monitoring
# - Connection status
# - Audio quality metrics
# - Performance statistics
# - Error tracking
```

## 🎯 **LiveKit Best Practices**

### **✅ Do's**
```python
# ✅ Use async/await for all LiveKit operations
# ✅ Handle network failures gracefully
# ✅ Validate tool parameters
# ✅ Use proper error handling
# ✅ Configure audio options properly
# ✅ Link sessions for tool access
```

### **❌ Don'ts**
```python
# ❌ Use blocking operations
# ❌ Ignore network failures
# ❌ Skip error handling
# ❌ Use hardcoded credentials
# ❌ Forget session linking
# ❌ Disable noise cancellation
```

## 🔧 **LiveKit Extension Points**

### **🛠️ Adding New Tools**
```python
# 1. Create tool with @function_tool decorator
@function_tool()
async def new_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

# 2. Import and register
from tools.new_tool import new_tool

# 3. Add to tools list
tools = [existing_tools, new_tool]
```

### **🎨 Customizing Voice**
```python
# Change voice model
RealtimeModel(
    voice="Aria",      # Different voice
    temperature=0.7,   # Different personality
    max_output_tokens=2048, # Longer responses
)
```

### **🌐 Custom Configuration**
```python
# Custom room options
RoomInputOptions(
    video_enabled=True,  # Enable video
    noise_cancellation=noise_cancellation.BVC(),
)
```

## 📚 **LiveKit Dependencies**

### **📦 Required Packages**
```python
# Core LiveKit
livekit>=1.2.5
livekit-agents>=1.2.5

# Audio processing
livekit-plugins>=1.2.5

# Google integration
livekit-plugins-google>=1.2.5
```

### **🔧 System Requirements**
```python
# Python requirements
python>=3.8
asyncio (built-in)
socket (built-in)

# Audio requirements
Microphone access
Speaker access
Audio drivers
```

## 🎉 **Summary**

This LiveKit integration provides:

✅ **Voice Chat Interface** - Natural conversation
✅ **AI Integration** - Gemini LLM connectivity
✅ **Tool System** - Extensible functionality
✅ **Audio Processing** - Professional audio quality
✅ **Session Management** - Robust connection handling
✅ **Error Handling** - Graceful failure recovery
✅ **Performance** - Optimized async operations
✅ **Extensibility** - Easy to add features

**LiveKit is the foundation that makes Nova AI a powerful voice assistant!** 🌐🎤🤖✨
