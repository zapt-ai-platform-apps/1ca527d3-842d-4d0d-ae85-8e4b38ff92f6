import tkinter as tk
from tkinter import ttk

class EqualizerFrame(ttk.Frame):
    def __init__(self, parent, audio_processor):
        super().__init__(parent)
        self.audio_processor = audio_processor
        
        self.freq_bands = [32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        self.eq_vars = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Container frame
        eq_container = ttk.Frame(self)
        eq_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(eq_container, text="10-Band Equalizer", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Frame for sliders
        sliders_frame = ttk.Frame(eq_container)
        sliders_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create sliders for each frequency band
        for i, freq in enumerate(self.freq_bands):
            frame = ttk.Frame(sliders_frame)
            frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=2)
            
            # Convert frequency to display string
            freq_text = f"{freq}Hz" if freq < 1000 else f"{freq/1000}kHz"
            
            # Label for frequency
            ttk.Label(frame, text=freq_text).pack(side=tk.BOTTOM)
            
            # Slider for gain
            self.eq_vars[freq] = tk.DoubleVar(value=0)
            slider = ttk.Scale(
                frame, from_=12, to=-12, length=200, orient=tk.VERTICAL,
                variable=self.eq_vars[freq], command=lambda v, f=freq: self.update_eq(f)
            )
            slider.pack(side=tk.BOTTOM, fill=tk.Y, pady=5)
            
            # Label for current value
            value_label = ttk.Label(frame, text="0 dB")
            value_label.pack(side=tk.BOTTOM)
            
            # Update label when slider changes
            self.eq_vars[freq].trace_add("write", lambda *args, label=value_label, var=self.eq_vars[freq]: 
                                         label.config(text=f"{var.get():.1f} dB"))
        
        # Preset buttons frame
        presets_frame = ttk.LabelFrame(eq_container, text="Equalizer Presets")
        presets_frame.pack(fill=tk.X, pady=10)
        
        # Preset buttons
        presets = [
            ("Flat", self.preset_flat),
            ("Bass Boost", self.preset_bass_boost),
            ("Treble Boost", self.preset_treble_boost),
            ("V-Shape", self.preset_v_shape),
            ("Vocal Boost", self.preset_vocal_boost)
        ]
        
        for name, command in presets:
            ttk.Button(presets_frame, text=name, command=command).pack(side=tk.LEFT, expand=True, padx=5, pady=5)
    
    def update_eq(self, freq):
        # Get all EQ band values and update the processor
        eq_values = {freq: self.eq_vars[freq].get() for freq in self.freq_bands}
        self.audio_processor.set_equalizer(eq_values)
    
    def preset_flat(self):
        for freq in self.freq_bands:
            self.eq_vars[freq].set(0)
        self.update_all_eq()
    
    def preset_bass_boost(self):
        values = {
            32: 10, 64: 8, 125: 6, 250: 3, 500: 0,
            1000: 0, 2000: 0, 4000: 0, 8000: 0, 16000: 0
        }
        self.set_preset_values(values)
    
    def preset_treble_boost(self):
        values = {
            32: 0, 64: 0, 125: 0, 250: 0, 500: 0,
            1000: 2, 2000: 4, 4000: 6, 8000: 8, 16000: 10
        }
        self.set_preset_values(values)
    
    def preset_v_shape(self):
        values = {
            32: 6, 64: 5, 125: 3, 250: 0, 500: -2,
            1000: -3, 2000: -1, 4000: 2, 8000: 4, 16000: 6
        }
        self.set_preset_values(values)
    
    def preset_vocal_boost(self):
        values = {
            32: -3, 64: -2, 125: -1, 250: 1, 500: 5,
            1000: 6, 2000: 5, 4000: 2, 8000: 0, 16000: -2
        }
        self.set_preset_values(values)
    
    def set_preset_values(self, values):
        for freq, value in values.items():
            self.eq_vars[freq].set(value)
        self.update_all_eq()
    
    def update_all_eq(self):
        eq_values = {freq: self.eq_vars[freq].get() for freq in self.freq_bands}
        self.audio_processor.set_equalizer(eq_values)