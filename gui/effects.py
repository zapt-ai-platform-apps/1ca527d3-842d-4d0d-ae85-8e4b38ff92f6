import tkinter as tk
from tkinter import ttk

class EffectsFrame(ttk.Frame):
    def __init__(self, parent, audio_processor):
        super().__init__(parent)
        self.audio_processor = audio_processor
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        effects_container = ttk.Frame(self)
        effects_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        ttk.Label(effects_container, text="Audio Effects", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Create frames for different effect categories
        spatial_frame = ttk.LabelFrame(effects_container, text="Spatial Effects")
        spatial_frame.pack(fill=tk.X, pady=10)
        
        dynamics_frame = ttk.LabelFrame(effects_container, text="Dynamic Effects")
        dynamics_frame.pack(fill=tk.X, pady=10)
        
        # 3D Surround effect
        self.surround_var = tk.BooleanVar(value=False)
        surround_check = ttk.Checkbutton(
            spatial_frame, text="3D Surround", variable=self.surround_var,
            command=self.update_surround
        )
        surround_check.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Surround intensity
        ttk.Label(spatial_frame, text="Intensity:").grid(row=0, column=1, padx=5, pady=5)
        self.surround_intensity_var = tk.DoubleVar(value=50)
        surround_intensity = ttk.Scale(
            spatial_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
            variable=self.surround_intensity_var, command=self.update_surround_intensity
        )
        surround_intensity.grid(row=0, column=2, padx=5, pady=5)
        
        # 8D Audio effect
        self.audio_8d_var = tk.BooleanVar(value=False)
        audio_8d_check = ttk.Checkbutton(
            spatial_frame, text="8D Audio", variable=self.audio_8d_var,
            command=self.update_8d_audio
        )
        audio_8d_check.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        # 8D Audio speed
        ttk.Label(spatial_frame, text="Speed:").grid(row=1, column=1, padx=5, pady=5)
        self.audio_8d_speed_var = tk.DoubleVar(value=30)
        audio_8d_speed = ttk.Scale(
            spatial_frame, from_=5, to=60, orient=tk.HORIZONTAL, length=200,
            variable=self.audio_8d_speed_var, command=self.update_8d_speed
        )
        audio_8d_speed.grid(row=1, column=2, padx=5, pady=5)
        
        # Binaural effect
        self.binaural_var = tk.BooleanVar(value=False)
        binaural_check = ttk.Checkbutton(
            spatial_frame, text="Binaural Effect", variable=self.binaural_var,
            command=self.update_binaural
        )
        binaural_check.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Binaural frequency
        ttk.Label(spatial_frame, text="Frequency:").grid(row=2, column=1, padx=5, pady=5)
        self.binaural_freq_var = tk.DoubleVar(value=30)
        binaural_freq = ttk.Scale(
            spatial_frame, from_=5, to=100, orient=tk.HORIZONTAL, length=200,
            variable=self.binaural_freq_var, command=self.update_binaural_freq
        )
        binaural_freq.grid(row=2, column=2, padx=5, pady=5)
        
        # Bass boost
        self.bass_boost_var = tk.BooleanVar(value=False)
        bass_boost_check = ttk.Checkbutton(
            dynamics_frame, text="Bass Boost", variable=self.bass_boost_var,
            command=self.update_bass_boost
        )
        bass_boost_check.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Bass boost amount
        ttk.Label(dynamics_frame, text="Amount:").grid(row=0, column=1, padx=5, pady=5)
        self.bass_amount_var = tk.DoubleVar(value=50)
        bass_amount = ttk.Scale(
            dynamics_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
            variable=self.bass_amount_var, command=self.update_bass_amount
        )
        bass_amount.grid(row=0, column=2, padx=5, pady=5)
        
        # Reverb effect
        self.reverb_var = tk.BooleanVar(value=False)
        reverb_check = ttk.Checkbutton(
            dynamics_frame, text="Reverb", variable=self.reverb_var,
            command=self.update_reverb
        )
        reverb_check.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        # Reverb amount
        ttk.Label(dynamics_frame, text="Room Size:").grid(row=1, column=1, padx=5, pady=5)
        self.reverb_amount_var = tk.DoubleVar(value=30)
        reverb_amount = ttk.Scale(
            dynamics_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200,
            variable=self.reverb_amount_var, command=self.update_reverb_amount
        )
        reverb_amount.grid(row=1, column=2, padx=5, pady=5)
        
        # Reset button
        ttk.Button(
            effects_container, text="Reset All Effects",
            command=self.reset_effects
        ).pack(pady=10)
        
    def update_surround(self):
        enabled = self.surround_var.get()
        intensity = self.surround_intensity_var.get() / 100
        self.audio_processor.set_surround(enabled, intensity)
    
    def update_surround_intensity(self, *args):
        if self.surround_var.get():
            intensity = self.surround_intensity_var.get() / 100
            self.audio_processor.set_surround(True, intensity)
    
    def update_8d_audio(self):
        enabled = self.audio_8d_var.get()
        speed = self.audio_8d_speed_var.get()
        self.audio_processor.set_8d_audio(enabled, speed)
    
    def update_8d_speed(self, *args):
        if self.audio_8d_var.get():
            speed = self.audio_8d_speed_var.get()
            self.audio_processor.set_8d_audio(True, speed)
    
    def update_binaural(self):
        enabled = self.binaural_var.get()
        freq = self.binaural_freq_var.get()
        self.audio_processor.set_binaural(enabled, freq)
    
    def update_binaural_freq(self, *args):
        if self.binaural_var.get():
            freq = self.binaural_freq_var.get()
            self.audio_processor.set_binaural(True, freq)
    
    def update_bass_boost(self):
        enabled = self.bass_boost_var.get()
        amount = self.bass_amount_var.get() / 100
        self.audio_processor.set_bass_boost(enabled, amount)
    
    def update_bass_amount(self, *args):
        if self.bass_boost_var.get():
            amount = self.bass_amount_var.get() / 100
            self.audio_processor.set_bass_boost(True, amount)
    
    def update_reverb(self):
        enabled = self.reverb_var.get()
        amount = self.reverb_amount_var.get() / 100
        self.audio_processor.set_reverb(enabled, amount)
    
    def update_reverb_amount(self, *args):
        if self.reverb_var.get():
            amount = self.reverb_amount_var.get() / 100
            self.audio_processor.set_reverb(True, amount)
    
    def reset_effects(self):
        # Reset all effects to default state
        self.surround_var.set(False)
        self.audio_8d_var.set(False)
        self.binaural_var.set(False)
        self.bass_boost_var.set(False)
        self.reverb_var.set(False)
        
        # Update processor
        self.audio_processor.reset_effects()