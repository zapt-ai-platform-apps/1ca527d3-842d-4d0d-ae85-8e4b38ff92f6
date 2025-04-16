import numpy as np
import soundfile as sf
from scipy import signal
import simpleaudio as sa
import threading
import time
from pydub import AudioSegment
import io
import os
import tempfile

class AudioProcessor:
    def __init__(self):
        self.audio_data = None
        self.sample_rate = None
        self.file_path = None
        self.play_obj = None
        self.is_playing = False
        
        # Processing settings
        self.volume = 1.0
        self.equalizer_values = {32: 0, 64: 0, 125: 0, 250: 0, 500: 0, 
                               1000: 0, 2000: 0, 4000: 0, 8000: 0, 16000: 0}
        
        # Effects settings
        self.surround_enabled = False
        self.surround_intensity = 0.5
        self.audio_8d_enabled = False
        self.audio_8d_speed = 30
        self.binaural_enabled = False
        self.binaural_freq = 30
        self.bass_boost_enabled = False
        self.bass_boost_amount = 0.5
        self.reverb_enabled = False
        self.reverb_amount = 0.3
        
        # Processing thread
        self.processing_thread = None
        self.stop_thread = False
    
    def load_file(self, file_path):
        self.file_path = file_path
        
        # Use pydub to load various audio formats
        audio = AudioSegment.from_file(file_path)
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples())
        
        # Convert to float32 in range [-1, 1]
        if audio.sample_width == 2:  # 16-bit audio
            samples = samples / 32768.0
        elif audio.sample_width == 1:  # 8-bit audio
            samples = (samples / 128.0) - 1.0
        elif audio.sample_width == 3:  # 24-bit audio
            samples = samples / 8388608.0
        elif audio.sample_width == 4:  # 32-bit audio
            samples = samples / 2147483648.0
        
        # Convert to stereo if mono
        if audio.channels == 1:
            self.audio_data = np.column_stack((samples, samples))
        else:
            # Reshape to (n_samples, n_channels)
            self.audio_data = samples.reshape(-1, audio.channels)
            # Ensure we have exactly 2 channels (stereo)
            if audio.channels > 2:
                self.audio_data = self.audio_data[:, :2]
        
        self.sample_rate = audio.frame_rate
        
        # Stop any current playback
        self.stop()
    
    def play(self):
        if self.audio_data is None:
            return
        
        # Stop any current playback
        self.stop()
        
        # Set playing flag
        self.is_playing = True
        self.stop_thread = False
        
        # Start processing in a separate thread
        self.processing_thread = threading.Thread(target=self._process_and_play)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def stop(self):
        self.is_playing = False
        self.stop_thread = True
        
        if self.play_obj is not None and self.play_obj.is_playing():
            self.play_obj.stop()
            self.play_obj = None
        
        if self.processing_thread is not None:
            self.processing_thread.join(1.0)  # Wait for 1 second
            self.processing_thread = None
    
    def _process_and_play(self):
        # Get processed audio
        processed_audio = self._apply_all_processing()
        
        # Convert to int16 for simpleaudio
        audio_int16 = (processed_audio * 32767).astype(np.int16)
        
        # Play audio
        self.play_obj = sa.play_buffer(
            audio_int16, num_channels=2, bytes_per_sample=2, sample_rate=self.sample_rate
        )
        
        # Wait for playback to finish
        while self.play_obj.is_playing() and not self.stop_thread:
            time.sleep(0.1)
        
        # Set playing flag to False when done
        self.is_playing = False
    
    def _apply_all_processing(self):
        # Make a copy of the original audio
        processed = np.copy(self.audio_data)
        
        # Apply equalizer
        processed = self._apply_equalizer(processed)
        
        # Apply effects
        if self.surround_enabled:
            processed = self._apply_surround(processed)
        
        if self.audio_8d_enabled:
            processed = self._apply_8d_audio(processed)
        
        if self.binaural_enabled:
            processed = self._apply_binaural(processed)
        
        if self.bass_boost_enabled:
            processed = self._apply_bass_boost(processed)
        
        if self.reverb_enabled:
            processed = self._apply_reverb(processed)
        
        # Apply volume
        processed = processed * self.volume
        
        # Clip to [-1, 1] to avoid distortion
        processed = np.clip(processed, -1.0, 1.0)
        
        return processed
    
    def set_volume(self, volume):
        self.volume = volume
    
    def set_equalizer(self, values):
        self.equalizer_values = values
    
    def set_surround(self, enabled, intensity):
        self.surround_enabled = enabled
        self.surround_intensity = intensity
    
    def set_8d_audio(self, enabled, speed):
        self.audio_8d_enabled = enabled
        self.audio_8d_speed = speed
    
    def set_binaural(self, enabled, freq):
        self.binaural_enabled = enabled
        self.binaural_freq = freq
    
    def set_bass_boost(self, enabled, amount):
        self.bass_boost_enabled = enabled
        self.bass_boost_amount = amount
    
    def set_reverb(self, enabled, amount):
        self.reverb_enabled = enabled
        self.reverb_amount = amount
    
    def reset_effects(self):
        self.surround_enabled = False
        self.audio_8d_enabled = False
        self.binaural_enabled = False
        self.bass_boost_enabled = False
        self.reverb_enabled = False
    
    def save_file(self, output_path):
        if self.audio_data is None:
            return
        
        # Apply all processing
        processed_audio = self._apply_all_processing()
        
        # Save using soundfile
        sf.write(output_path, processed_audio, self.sample_rate)
    
    def get_visualization_data(self):
        if self.audio_data is None:
            return np.zeros(1000)
        
        # Get a representative sample of the audio for visualization
        # We'll use the average of left and right channels
        mono_data = np.mean(self.audio_data, axis=1)
        
        # Downsample to 1000 points for visualization
        downsample_factor = max(1, len(mono_data) // 1000)
        return mono_data[::downsample_factor][:1000]