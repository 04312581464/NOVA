"""
Voice Recorder Tool for Nova 5.0
Records audio from microphone and saves to file
"""

import os
import wave
import threading
import time
from datetime import datetime
from pathlib import Path
from livekit.agents import function_tool

# Global recording state
recording_state = {
    'is_recording': False,
    'thread': None,
    'filename': None,
    'start_time': None
}

class VoiceRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.sample_rate = 44100
        self.channels = 2
        self.format = wave.WAVE_FORMAT_PCM
        self.chunk = 1024
        
    def _get_audio_device(self):
        """Initialize audio recording device"""
        try:
            import pyaudio
            self.audio = pyaudio.PyAudio()
            return self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk
            )
        except ImportError:
            raise ImportError("PyAudio not installed. Install with: pip install pyaudio")
        except Exception as e:
            raise Exception(f"Failed to initialize audio device: {e}")
    
    def start_recording(self, filename=None, duration=None):
        """Start recording audio"""
        if self.recording:
            return False, "Already recording"
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"voice_recording_{timestamp}.wav"
            
            # Ensure .wav extension
            if not filename.endswith('.wav'):
                filename += '.wav'
            
            # Create recordings directory if it doesn't exist
            recordings_dir = Path("Recordings")
            recordings_dir.mkdir(exist_ok=True)
            
            self.filename = recordings_dir / filename
            self.frames = []
            self.recording = True
            
            # Start recording thread
            self.recording_thread = threading.Thread(
                target=self._record_audio, 
                args=(duration,)
            )
            self.recording_thread.start()
            
            return True, f"Recording started: {self.filename.name}"
            
        except Exception as e:
            return False, f"Failed to start recording: {str(e)}"
    
    def _record_audio(self, duration=None):
        """Internal recording function"""
        try:
            stream = self._get_audio_device()
            
            if duration:
                # Record for specified duration
                for _ in range(int(self.sample_rate * duration / self.chunk)):
                    if not self.recording:
                        break
                    data = stream.read(self.chunk)
                    self.frames.append(data)
            else:
                # Record until stop is called
                while self.recording:
                    data = stream.read(self.chunk)
                    self.frames.append(data)
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Recording error: {e}")
            self.recording = False
    
    def stop_recording(self):
        """Stop recording and save file"""
        if not self.recording:
            return False, "Not currently recording"
        
        self.recording = False
        
        # Wait for recording thread to finish
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join(timeout=2)
        
        try:
            # Save the recording
            with wave.open(str(self.filename), 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            
            file_size = os.path.getsize(self.filename) / (1024 * 1024)  # MB
            return True, f"Recording saved: {self.filename.name} ({file_size:.2f} MB)"
            
        except Exception as e:
            return False, f"Failed to save recording: {str(e)}"
    
    def get_recording_status(self):
        """Get current recording status"""
        if self.recording:
            elapsed = time.time() - self.start_time if self.start_time else 0
            return f"🔴 Recording in progress... ({elapsed:.1f}s elapsed)"
        else:
            return "⏹️ Not recording"

# Global recorder instance
recorder = VoiceRecorder()

@function_tool()
async def start_voice_recording(filename: str = None, duration: int = None) -> str:
    """
    Start recording voice from microphone.
    
    Args:
        filename: Optional name for the audio file (without extension)
        duration: Optional recording duration in seconds (if not provided, records until stopped)
        
    Returns:
        str: Status message about recording start
    """
    try:
        success, message = recorder.start_recording(filename, duration)
        
        if success:
            recording_state['is_recording'] = True
            recording_state['filename'] = str(recorder.filename)
            recording_state['start_time'] = time.time()
            return f"🎙️ {message}"
        else:
            return f"❌ {message}"
            
    except Exception as e:
        return f"❌ Failed to start voice recording: {str(e)}"

@function_tool()
async def stop_voice_recording() -> str:
    """
    Stop current voice recording and save the file.
    
    Returns:
        str: Status message about recording completion
    """
    try:
        success, message = recorder.stop_recording()
        
        if success:
            recording_state['is_recording'] = False
            recording_state['filename'] = None
            recording_state['start_time'] = None
            return f"✅ {message}"
        else:
            return f"❌ {message}"
            
    except Exception as e:
        return f"❌ Failed to stop voice recording: {str(e)}"

@function_tool()
async def get_recording_status() -> str:
    """
    Get current voice recording status.
    
    Returns:
        str: Current recording status
    """
    try:
        if recording_state['is_recording']:
            elapsed = time.time() - recording_state['start_time']
            return f"🔴 Recording in progress... ({elapsed:.1f}s elapsed)"
        else:
            return "⏹️ Not currently recording"
            
    except Exception as e:
        return f"❌ Failed to get recording status: {str(e)}"

@function_tool()
async def list_recordings() -> str:
    """
    List all saved voice recordings.
    
    Returns:
        str: List of available recordings
    """
    try:
        recordings_dir = Path("Recordings")
        
        if not recordings_dir.exists():
            return "📁 No recordings folder found"
        
        recordings = list(recordings_dir.glob("*.wav"))
        
        if not recordings:
            return "📁 No recordings found"
        
        result = "📁 Available Voice Recordings:\n\n"
        
        for recording in sorted(recordings, key=lambda x: x.stat().st_mtime, reverse=True):
            file_size = recording.stat().st_size / (1024 * 1024)  # MB
            modified_time = datetime.fromtimestamp(recording.stat().st_mtime)
            result += f"🎵 {recording.name}\n"
            result += f"   📊 Size: {file_size:.2f} MB\n"
            result += f"   📅 Created: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Failed to list recordings: {str(e)}"

@function_tool()
async def delete_recording(filename: str) -> str:
    """
    Delete a specific voice recording.
    
    Args:
        filename: Name of the recording file to delete
        
    Returns:
        str: Status message about deletion
    """
    try:
        recordings_dir = Path("Recordings")
        
        # Ensure .wav extension
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        file_path = recordings_dir / filename
        
        if not file_path.exists():
            return f"❌ Recording '{filename}' not found"
        
        file_size = file_path.stat().st_size / (1024 * 1024)  # MB
        file_path.unlink()
        
        return f"✅ Deleted '{filename}' ({file_size:.2f} MB)"
        
    except Exception as e:
        return f"❌ Failed to delete recording: {str(e)}"

@function_tool()
async def play_recording(filename: str) -> str:
    """
    Play a specific voice recording using default system player.
    
    Args:
        filename: Name of the recording file to play
        
    Returns:
        str: Status message about playback
    """
    try:
        import subprocess
        import platform
        
        recordings_dir = Path("Recordings")
        
        # Ensure .wav extension
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        file_path = recordings_dir / filename
        
        if not file_path.exists():
            return f"❌ Recording '{filename}' not found"
        
        # Play based on operating system
        system = platform.system()
        
        if system == "Windows":
            subprocess.run(['start', str(file_path)], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(['afplay', str(file_path)])
        elif system == "Linux":
            subprocess.run(['aplay', str(file_path)])
        else:
            return f"❌ Unsupported operating system: {system}"
        
        return f"🔊 Playing '{filename}'..."
        
    except Exception as e:
        return f"❌ Failed to play recording: {str(e)}"
