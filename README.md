# Nova 5.0 VADRYK Edition 🚀

An advanced AI-powered voice assistant with comprehensive system control, automation, and research capabilities.

## 🌟 Features

### V - Veda (Knowledge & Intelligence)
- 🌐 **Web Search & Research**: Intelligent information retrieval without browser opening
- 📊 **Financial Data**: Real-time gold rates, stock prices, market data
- 🔍 **Smart Search**: Wikipedia integration, news aggregation
- 🧠 **Knowledge Base**: Quick fact checks and comprehensive research

### A - Artha (Logic & System Flow)
- ⚡ **System Control**: Shutdown, restart, lock computer
- 🪟 **Window Management**: Organize and control active windows
- 🚀 **Application Launch**: Smart app launching and management
- 🔄 **Multi-tasking**: Execute multiple tasks simultaneously

### D - Dhwani (Voice & Sound Control)
- 🎙️ **Voice Recording**: High-quality audio recording and playback
- 🎵 **Media Control**: Spotify integration, YouTube playback
- 🔊 **Volume Control**: System audio management
- 📢 **Voice Commands**: Complete voice-driven interface

### R - Rachna (Creation & Design)
- 🎨 **AI Image Generation**: Create stunning visuals
- 💻 **Code Generation**: Automated code writing and execution
- 📝 **Document Creation**: Notepad integration, PDF conversion
- 📊 **Data Visualization**: Excel analysis and charting

### Y - Yukt (Connectivity & Communication)
- 📱 **WhatsApp Integration**: Send messages and media
- 📧 **Email Support**: Automated email sending
- 📋 **Smart Clipboard**: Advanced clipboard management
- 💬 **Cross-App Communication**: Seamless app integration

### K - Kriya (Action & Execution)
- ⌨️ **Keyboard Automation**: Smart typing and keystroke simulation
- 🖱️ **Desktop Control**: Complete desktop automation
- 🔒 **Security Features**: Virus scanning, lockdown mode
- 📸 **Screen Analysis**: OCR and visual processing

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- LiveKit account and API keys
- PyAudio for voice recording

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Nova-5.0.git
   cd Nova-5.0
   ```

2. **Install dependencies**
   ```bash
   pip install -r lockdown_requirements.txt
   pip install pyaudio  # For voice recording
   ```

3. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Add your LiveKit API credentials
   - Configure user preferences

4. **Run Nova**
   ```bash
   python agent.py console
   ```

## 📁 Project Structure

```
Nova-5.0/
├── 📁 Tools/                    # All AI tools and modules
│   ├── 🎙️ voice_recorder.py     # Voice recording functionality
│   ├── 🔍 search_and_tell.py     # Research without browser
│   ├── 📱 send_whatsapp_message.py
│   ├── 🎵 spotify.py
│   ├── 🖼️ generate_ai_image.py
│   └── 📊 [50+ specialized tools]
├── 🤖 agent.py                 # Main AI agent
├── 📋 prompts.py               # AI behavior and instructions
├── 🔧 tools.py                 # Tool integration
├── 📄 LIVEKIT_INTEGRATION_GUIDE.md
└── 📁 Preciosa-Monitor-satellite/  # Satellite monitoring system
```

## 🎯 Key Tools

### Voice Recording
- **Start Recording**: `start_voice_recording(filename, duration)`
- **Stop Recording**: `stop_voice_recording()`
- **Play Recording**: `play_recording(filename)`
- **List Recordings**: `list_recordings()`

### Smart Search
- **Research Mode**: `search_and_tell(query)` - No browser opening
- **Browser Mode**: `search_web(query)` - Only when explicitly requested

### System Control
- **Power Management**: `system_power_action(action)`
- **Window Control**: `manage_window(action)`
- **App Launcher**: `open_app(app_name)`

### Communication
- **WhatsApp**: `send_whatsapp_message(contact, message)`
- **Email**: `send_email(to, subject, message)`

## 🔧 Configuration

### Environment Variables
```env
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_secret
USER_NAME=Sir
LAN=Hindi
NOVA_VARIANT=Elite
GOOGLE_API_KEY=your_google_key  # Optional for enhanced search
```

### Customization
- Modify `prompts.py` to change AI behavior
- Add new tools in `Tools/` directory
- Update `agent.py` to register new tools

## 🌟 Recent Updates

### ✅ Voice Recording System
- High-quality WAV recording (44.1kHz, 16-bit)
- Automatic file organization
- Cross-platform compatibility

### ✅ Smart Search Enhancement
- Research without browser opening
- Financial data integration
- Gold rates, stock prices, market data

### ✅ Security Features
- Lockdown mode with password protection
- System virus scanning
- Emergency unlock functionality

## 🤖 Usage Examples

```bash
# Voice commands
"Start recording voice memo"
"What is today's gold rate"
"Send WhatsApp to John"
"Play study playlist"
"Take screenshot"
"Lock my computer"

# System control
"Open VS Code"
"Show desktop"
"Increase volume"
"Scan for viruses"
```

## 📚 Documentation

- [LiveKit Integration Guide](LIVEKIT_INTEGRATION_GUIDE.md)
- [Tool Documentation](Tools/)
- [API Reference](docs/api/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tool or enhancement
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Creator

**Lalit Manjunatha**  
Nova 5.0 VADRYK Edition - Advanced AI Assistant

## 🙏 Acknowledgments

- LiveKit for voice processing
- OpenAI for AI capabilities
- All contributors and testers

---

**Nova 5.0 VADRYK Edition** - *Intelligent Assistance, Redefined* 🚀
