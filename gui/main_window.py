import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio.processor import AudioProcessor
from gui.equalizer import EqualizerFrame
from gui.effects import EffectsFrame

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Equalizer")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        self.audio_processor = AudioProcessor()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for audio controls
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=10)
        
        # File control buttons
        file_frame = ttk.LabelFrame(top_frame, text="File Controls")
        file_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(file_frame, text="Open Audio File", command=self.open_file).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Play", command=self.play_audio).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Stop", command=self.stop_audio).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Save As", command=self.save_file).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Volume control
        volume_frame = ttk.LabelFrame(top_frame, text="Volume")
        volume_frame.pack(side=tk.RIGHT, padx=5)
        
        self.volume_var = tk.DoubleVar(value=100)
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                 variable=self.volume_var, command=self.update_volume)
        volume_slider.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Visualizer frame
        visualizer_frame = ttk.LabelFrame(main_frame, text="Audio Visualization")
        visualizer_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matplotlib figure for visualization
        self.fig, self.ax = plt.subplots(figsize=(10, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=visualizer_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame with tabs for equalizer and effects
        bottom_frame = ttk.Notebook(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Equalizer tab
        self.equalizer_frame = EqualizerFrame(bottom_frame, self.audio_processor)
        bottom_frame.add(self.equalizer_frame, text="Equalizer")
        
        # Effects tab
        self.effects_frame = EffectsFrame(bottom_frame, self.audio_processor)
        bottom_frame.add(self.effects_frame, text="Audio Effects")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready. No file loaded.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Made on ZAPT footer
        zapt_frame = ttk.Frame(main_frame)
        zapt_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=2)
        zapt_link = ttk.Label(zapt_frame, text="Made on ZAPT", cursor="hand2", foreground="blue")
        zapt_link.pack(side=tk.RIGHT)
        zapt_link.bind("<Button-1>", lambda e: self.open_zapt_website())
        
    def open_zapt_website(self):
        import webbrowser
        webbrowser.open("https://www.zapt.ai")
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")]
        )
        if file_path:
            try:
                self.audio_processor.load_file(file_path)
                filename = file_path.split("/")[-1]
                self.status_var.set(f"Loaded: {filename}")
                self.update_visualization()
            except Exception as e:
                self.status_var.set(f"Error loading file: {str(e)}")
    
    def play_audio(self):
        if self.audio_processor.audio_data is not None:
            self.audio_processor.play()
            self.status_var.set("Playing audio...")
    
    def stop_audio(self):
        self.audio_processor.stop()
        self.status_var.set("Playback stopped.")
    
    def save_file(self):
        if self.audio_processor.audio_data is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    self.audio_processor.save_file(file_path)
                    self.status_var.set(f"Saved to: {file_path}")
                except Exception as e:
                    self.status_var.set(f"Error saving file: {str(e)}")
    
    def update_volume(self, *args):
        volume = self.volume_var.get()
        self.audio_processor.set_volume(volume / 100.0)
    
    def update_visualization(self):
        if self.audio_processor.audio_data is not None:
            # Get a sample of the audio data for visualization
            data = self.audio_processor.get_visualization_data()
            
            self.ax.clear()
            self.ax.plot(data)
            self.ax.set_yticks([])
            self.ax.set_xlabel('Time')
            self.fig.tight_layout()
            self.canvas.draw()