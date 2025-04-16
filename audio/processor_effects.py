import numpy as np
from scipy import signal

def apply_equalizer(audio, sample_rate, equalizer_values):
    # Skip if no audio data
    if audio is None or len(audio) == 0:
        return audio
    
    # Get FFT of audio
    fft_size = 2048
    hop_size = fft_size // 4
    
    # Process each channel
    result = np.zeros_like(audio)
    
    for channel in range(audio.shape[1]):
        # Get channel data
        channel_data = audio[:, channel]
        
        # Create empty output
        output = np.zeros_like(channel_data)
        
        # Process in frames
        for frame_start in range(0, len(channel_data) - fft_size, hop_size):
            # Get frame data
            frame = channel_data[frame_start:frame_start + fft_size]
            
            # Apply window
            window = signal.windows.hann(fft_size)
            frame = frame * window
            
            # Calculate FFT
            frame_fft = np.fft.rfft(frame)
            
            # Apply EQ
            freq_resolution = sample_rate / fft_size
            for band_freq, gain_db in equalizer_values.items():
                # Convert gain from dB to linear
                gain_linear = 10 ** (gain_db / 20)
                
                # Calculate frequency bin indices
                band_idx = int(band_freq / freq_resolution)
                
                # Calculate band width (one octave)
                band_width = band_idx
                
                # Apply gain to frequency range (with smooth transition)
                for i in range(max(0, band_idx - band_width), min(len(frame_fft), band_idx + band_width)):
                    # Calculate distance from center frequency (normalized to [-1, 1])
                    dist = (i - band_idx) / band_width
                    
                    # Apply smooth transition based on distance
                    transition = 0.5 * (1 + np.cos(dist * np.pi))
                    
                    # Apply gain
                    frame_fft[i] *= transition * (gain_linear - 1) + 1
            
            # Inverse FFT
            frame_processed = np.fft.irfft(frame_fft)
            
            # Apply window again
            frame_processed = frame_processed * window
            
            # Overlap-add to output
            output[frame_start:frame_start + fft_size] += frame_processed
        
        # Normalize
        result[:, channel] = output / (fft_size / hop_size)
    
    return result

def apply_surround(audio, intensity):
    # Skip if no audio data or mono
    if audio is None or audio.shape[1] < 2:
        return audio
    
    # Apply different filter to left and right channel
    left = audio[:, 0]
    right = audio[:, 1]
    
    # Create filtered copies
    b, a = signal.butter(2, 0.5, btype='lowpass')
    left_low = signal.filtfilt(b, a, left)
    right_low = signal.filtfilt(b, a, right)
    
    b, a = signal.butter(2, 0.5, btype='highpass')
    left_high = signal.filtfilt(b, a, left)
    right_high = signal.filtfilt(b, a, right)
    
    # Mix channels with phase-shifted versions
    result = np.zeros_like(audio)
    result[:, 0] = left + intensity * right_high - intensity * left_high
    result[:, 1] = right + intensity * left_high - intensity * right_high
    
    return result

def apply_8d_audio(audio, sample_rate, speed):
    # Skip if no audio data or mono
    if audio is None or audio.shape[1] < 2:
        return audio
    
    # Create output
    result = np.zeros_like(audio)
    
    # Calculate pan based on time
    num_samples = audio.shape[0]
    duration = num_samples / sample_rate
    
    # Create pan envelope (0 = full left, 1 = full right)
    t = np.linspace(0, duration, num_samples)
    cycles = duration * speed / 60  # cycles per minute to cycles per duration
    pan = 0.5 + 0.5 * np.sin(2 * np.pi * cycles * t)
    
    # Apply pan
    for i in range(num_samples):
        # Calculate left/right gain
        left_gain = np.sqrt(1 - pan[i])
        right_gain = np.sqrt(pan[i])
        
        # Apply to both channels
        result[i, 0] = audio[i, 0] * left_gain
        result[i, 1] = audio[i, 1] * right_gain
    
    return result

def apply_binaural(audio, sample_rate, beat_freq):
    # Skip if no audio data
    if audio is None:
        return audio
    
    # Create a copy
    result = np.copy(audio)
    
    # Get parameters
    base_freq = 200  # Base frequency in Hz
    
    # Calculate frequencies for left and right ear
    left_freq = base_freq
    right_freq = base_freq + beat_freq
    
    # Create sine waves
    t = np.arange(audio.shape[0]) / sample_rate
    left_sine = 0.2 * np.sin(2 * np.pi * left_freq * t)
    right_sine = 0.2 * np.sin(2 * np.pi * right_freq * t)
    
    # Apply to audio
    if audio.shape[1] >= 2:
        result[:, 0] = result[:, 0] * 0.8 + left_sine
        result[:, 1] = result[:, 1] * 0.8 + right_sine
    else:
        # If mono, convert to stereo
        stereo = np.zeros((audio.shape[0], 2))
        stereo[:, 0] = audio[:, 0] * 0.8 + left_sine
        stereo[:, 1] = audio[:, 0] * 0.8 + right_sine
        result = stereo
    
    return result

def apply_bass_boost(audio, sample_rate, amount):
    # Skip if no audio data
    if audio is None:
        return audio
    
    # Design a bass boost filter
    cutoff = 150 / (sample_rate / 2)  # Normalized cutoff frequency
    gain_db = 12 * amount  # Max gain = 12dB
    
    # Convert gain to linear scale
    gain = 10 ** (gain_db / 20)
    
    # Create a low-shelf filter
    b, a = signal.butter(2, cutoff, btype='lowpass')
    
    # Apply filter to each channel
    result = np.zeros_like(audio)
    for channel in range(audio.shape[1]):
        # Get the low frequencies
        low_freq = signal.filtfilt(b, a, audio[:, channel])
        
        # Boost low frequencies
        result[:, channel] = audio[:, channel] + (gain - 1) * low_freq
    
    return result

def apply_reverb(audio, sample_rate, amount):
    # Skip if no audio data
    if audio is None:
        return audio
    
    # Design a simple reverb effect
    delay_ms = int(50 + 150 * amount)  # 50-200ms
    decay = 0.3 + 0.6 * amount  # 0.3-0.9
    
    # Convert delay to samples
    delay_samples = int(delay_ms * sample_rate / 1000)
    
    # Create output
    result = np.copy(audio)
    
    # Apply multiple delays with decreasing amplitude
    n_delays = 5
    for i in range(1, n_delays + 1):
        delay = i * delay_samples
        amplitude = decay ** i
        
        # Add delayed signal
        if delay < audio.shape[0]:
            result[delay:] += amplitude * audio[:-delay]
    
    return result