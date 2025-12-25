#!/usr/bin/env python3
"""
DynaMix GUI - Graphical User Interface for all DynaMix tools
A comprehensive GUI application for audio analysis and DJ tools
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Import DynaMix modules
from audio_utils import AudioAnalyzer, analyze_track_compatibility, suggest_mix_points
from dj_tools import DJTools, batch_analyze_tracks
from playlist_manager import PlaylistManager
from audio_effects import AudioEffects, TrackComparer
from export_tools import ExportTools
from mix_enhanced import EnhancedMixAnalyzer


class DynaMixGUI:
    """Main GUI application for DynaMix"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DynaMix - DJ Audio Analysis Tool")
        self.root.geometry("1200x800")
        
        # Variables
        self.current_track1 = None
        self.current_track2 = None
        self.current_playlist_dir = None
        self.analysis_results = {}
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_track_analysis_tab()
        self.create_two_track_tab()
        self.create_playlist_tab()
        self.create_dj_tools_tab()
        self.create_audio_effects_tab()
        self.create_export_tab()
        
        # Status bar
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def create_track_analysis_tab(self):
        """Create single track analysis tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Track Analysis")
        
        # Top frame for file selection
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.track1_path_var = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.track1_path_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Browse", command=self.browse_track1).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Analyze", command=self.analyze_track1).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Text results
        left_panel = ttk.Frame(results_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(left_panel, text="Analysis Results:").pack(anchor=tk.W)
        self.track1_results = scrolledtext.ScrolledText(left_panel, height=30, width=50)
        self.track1_results.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Visualization
        right_panel = ttk.Frame(results_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(right_panel, text="Visualization:").pack(anchor=tk.W)
        self.track1_viz_frame = ttk.Frame(right_panel)
        self.track1_viz_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_two_track_tab(self):
        """Create two-track compatibility analysis tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Two-Track Analysis")
        
        # Track selection
        selection_frame = ttk.Frame(frame)
        selection_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Track 1
        track1_frame = ttk.LabelFrame(selection_frame, text="Track 1")
        track1_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.track1_compat_var = tk.StringVar()
        ttk.Entry(track1_frame, textvariable=self.track1_compat_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(track1_frame, text="Browse", command=self.browse_track1_compat).pack(side=tk.LEFT, padx=5)
        
        # Track 2
        track2_frame = ttk.LabelFrame(selection_frame, text="Track 2")
        track2_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.track2_compat_var = tk.StringVar()
        ttk.Entry(track2_frame, textvariable=self.track2_compat_var, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(track2_frame, text="Browse", command=self.browse_track2_compat).pack(side=tk.LEFT, padx=5)
        
        # Analyze button
        ttk.Button(selection_frame, text="Analyze Compatibility", 
                  command=self.analyze_compatibility).pack(side=tk.LEFT, padx=10)
        
        # Results
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text results
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.compat_results = scrolledtext.ScrolledText(text_frame, height=20)
        self.compat_results.pack(fill=tk.BOTH, expand=True)
        
        # Visualization
        self.compat_viz_frame = ttk.Frame(results_frame)
        self.compat_viz_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_playlist_tab(self):
        """Create playlist management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Playlist Manager")
        
        # Directory selection
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(dir_frame, text="Music Directory:").pack(side=tk.LEFT, padx=5)
        self.playlist_dir_var = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.playlist_dir_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_playlist_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Analyze Playlist", command=self.analyze_playlist).pack(side=tk.LEFT, padx=5)
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Set List Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Duration (minutes):").pack(side=tk.LEFT, padx=5)
        self.set_duration_var = tk.IntVar(value=60)
        ttk.Spinbox(options_frame, from_=15, to=240, textvariable=self.set_duration_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(options_frame, text="Energy Curve:").pack(side=tk.LEFT, padx=5)
        self.energy_curve_var = tk.StringVar(value="build")
        energy_combo = ttk.Combobox(options_frame, textvariable=self.energy_curve_var, 
                                   values=["build", "wave", "peak_middle", "constant"], width=15)
        energy_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(options_frame, text="Create Set List", command=self.create_set_list).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Playlist table
        table_frame = ttk.Frame(results_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for playlist
        columns = ("#", "Filename", "BPM", "Key", "Duration", "Energy")
        self.playlist_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.playlist_tree.heading(col, text=col)
            self.playlist_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.playlist_tree.yview)
        self.playlist_tree.configure(yscrollcommand=scrollbar.set)
        
        self.playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_dj_tools_tab(self):
        """Create DJ tools tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="DJ Tools")
        
        # File selection
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(file_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.dj_tools_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.dj_tools_file_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_dj_tools_file).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(buttons_frame, text="Detect Cue Points", 
                  command=self.detect_cue_points).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Suggest Loops", 
                  command=self.suggest_loops).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Analyze Zones", 
                  command=self.analyze_zones).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Generate DJ Notes", 
                  command=self.generate_dj_notes).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Batch Analyze", 
                  command=self.batch_analyze).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dj_tools_results = scrolledtext.ScrolledText(results_frame, height=30)
        self.dj_tools_results.pack(fill=tk.BOTH, expand=True)
    
    def create_audio_effects_tab(self):
        """Create audio effects analysis tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Audio Effects")
        
        # File selection
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(file_frame, text="Audio File:").pack(side=tk.LEFT, padx=5)
        self.effects_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.effects_file_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_effects_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Analyze Effects", 
                  command=self.analyze_effects).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.effects_results = scrolledtext.ScrolledText(results_frame, height=30)
        self.effects_results.pack(fill=tk.BOTH, expand=True)
    
    def create_export_tab(self):
        """Create export tools tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Export Tools")
        
        # Export options
        options_frame = ttk.LabelFrame(frame, text="Export Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(options_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        self.export_format_var = tk.StringVar(value="JSON")
        format_combo = ttk.Combobox(options_frame, textvariable=self.export_format_var,
                                   values=["JSON", "CSV", "M3U", "Rekordbox XML", "Traktor NML", "TXT"],
                                   width=15, state="readonly")
        format_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(options_frame, text="Export Analysis", 
                  command=self.export_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Export Playlist", 
                  command=self.export_playlist).pack(side=tk.LEFT, padx=5)
        
        # Export log
        log_frame = ttk.LabelFrame(frame, text="Export Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.export_log = scrolledtext.ScrolledText(log_frame, height=20)
        self.export_log.pack(fill=tk.BOTH, expand=True)
    
    # File browsing methods
    def browse_track1(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.track1_path_var.set(filename)
            self.current_track1 = filename
    
    def browse_track1_compat(self):
        filename = filedialog.askopenfilename(
            title="Select Track 1",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.track1_compat_var.set(filename)
            self.current_track1 = filename
    
    def browse_track2_compat(self):
        filename = filedialog.askopenfilename(
            title="Select Track 2",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.track2_compat_var.set(filename)
            self.current_track2 = filename
    
    def browse_playlist_dir(self):
        directory = filedialog.askdirectory(title="Select Music Directory")
        if directory:
            self.playlist_dir_var.set(directory)
            self.current_playlist_dir = directory
    
    def browse_dj_tools_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.dj_tools_file_var.set(filename)
    
    def browse_effects_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio files", "*.mp3 *.wav *.flac *.m4a *.aac *.ogg"), ("All files", "*.*")]
        )
        if filename:
            self.effects_file_var.set(filename)
    
    # Analysis methods
    def analyze_track1(self):
        """Analyze single track"""
        file_path = self.track1_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Analyzing track...")
                analyzer = AudioAnalyzer(file_path)
                features = analyzer.get_audio_features()
                
                # Format results
                result_text = f"Track Analysis: {os.path.basename(file_path)}\n"
                result_text += "=" * 50 + "\n\n"
                result_text += f"Duration: {features['duration']:.1f} seconds\n"
                result_text += f"BPM: {features['bpm']:.1f} (confidence: {features['bpm_confidence']:.2f})\n"
                result_text += f"Key: {features['key']} (confidence: {features['key_confidence']:.2f})\n"
                result_text += f"Average Energy: {features['avg_energy']:.4f}\n"
                result_text += f"Max Energy: {features['max_energy']:.4f}\n"
                result_text += f"Energy Std Dev: {features['energy_std']:.4f}\n"
                result_text += f"Beat Count: {features['beat_count']}\n"
                result_text += f"Section Count: {features['section_count']}\n"
                result_text += f"Drop Count: {features['drop_count']}\n"
                
                # Sections
                if features.get('sections'):
                    result_text += "\nSections:\n"
                    for section_name, start, end in features['sections']:
                        result_text += f"  {section_name}: {start:.1f}s - {end:.1f}s\n"
                
                self.track1_results.delete(1.0, tk.END)
                self.track1_results.insert(1.0, result_text)
                
                # Create visualization
                self.create_track_visualization(analyzer)
                
                self.update_status("Analysis complete")
            except Exception as e:
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")
                self.update_status("Error during analysis")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def create_track_visualization(self, analyzer: AudioAnalyzer):
        """Create visualization for track analysis"""
        # Clear existing plots
        for widget in self.track1_viz_frame.winfo_children():
            widget.destroy()
        
        try:
            fig, axes = plt.subplots(2, 1, figsize=(8, 6))
            
            # Energy profile
            times, rms = analyzer.analyze_energy_profile()
            axes[0].plot(times, rms, label='Energy', color='blue', alpha=0.7)
            axes[0].set_title('Energy Profile')
            axes[0].set_ylabel('RMS Energy')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # Beat grid
            beat_times, beat_strengths = analyzer.analyze_beat_grid()
            axes[1].vlines(beat_times[:100], 0, beat_strengths[:100], alpha=0.6, color='red', label='Beats')
            axes[1].set_title('Beat Grid (first 100 beats)')
            axes[1].set_xlabel('Time (s)')
            axes[1].set_ylabel('Beat Strength')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, self.track1_viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Visualization error: {e}")
    
    def analyze_compatibility(self):
        """Analyze compatibility between two tracks"""
        track1 = self.track1_compat_var.get()
        track2 = self.track2_compat_var.get()
        
        if not track1 or not track2:
            messagebox.showerror("Error", "Please select both tracks")
            return
        
        if not os.path.exists(track1) or not os.path.exists(track2):
            messagebox.showerror("Error", "One or both files not found")
            return
        
        def analyze():
            try:
                self.update_status("Analyzing compatibility...")
                analyzer = EnhancedMixAnalyzer()
                results = analyzer.analyze_tracks(track1, track2)
                
                # Format results
                result_text = "Two-Track Compatibility Analysis\n"
                result_text += "=" * 50 + "\n\n"
                
                compat = results['compatibility']
                result_text += f"BPM Compatibility: {compat['bpm_compatibility']:.1f}%\n"
                result_text += f"Key Compatibility: {compat['key_compatibility']:.1f}%\n"
                result_text += f"Energy Compatibility: {compat['energy_compatibility']:.1f}%\n"
                result_text += f"Overall Score: {compat['overall_score']:.1f}%\n\n"
                
                mix_sugg = results['mix_suggestions']
                result_text += "Mix Suggestions:\n"
                result_text += f"  Recommended Duration: {mix_sugg['recommended_mix_duration']:.1f}s\n"
                result_text += f"  BPM Sync Required: {mix_sugg['bpm_sync_required']}\n"
                
                if mix_sugg.get('track1_exit_points'):
                    result_text += f"  Track 1 Exit Points: {[f'{t:.1f}s' for t in mix_sugg['track1_exit_points'][:3]]}\n"
                if mix_sugg.get('track2_entry_points'):
                    result_text += f"  Track 2 Entry Points: {[f'{t:.1f}s' for t in mix_sugg['track2_entry_points'][:3]]}\n"
                
                self.compat_results.delete(1.0, tk.END)
                self.compat_results.insert(1.0, result_text)
                
                self.analysis_results = results
                self.update_status("Compatibility analysis complete")
            except Exception as e:
                messagebox.showerror("Error", f"Analysis failed: {str(e)}")
                self.update_status("Error during analysis")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_playlist(self):
        """Analyze playlist"""
        directory = self.playlist_dir_var.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        def analyze():
            try:
                self.update_status("Analyzing playlist...")
                manager = PlaylistManager(directory)
                audio_files = manager.scan_directory()
                
                if not audio_files:
                    messagebox.showwarning("Warning", "No audio files found in directory")
                    return
                
                df = manager.analyze_playlist(audio_files)
                
                # Clear and populate tree
                for item in self.playlist_tree.get_children():
                    self.playlist_tree.delete(item)
                
                for idx, row in df.iterrows():
                    duration_min = row['duration'] / 60
                    self.playlist_tree.insert("", tk.END, values=(
                        idx + 1,
                        row['filename'],
                        f"{row['bpm']:.1f}",
                        row['key'],
                        f"{duration_min:.1f}",
                        f"{row['avg_energy']:.4f}"
                    ))
                
                self.playlist_manager = manager
                self.update_status(f"Playlist analyzed: {len(df)} tracks")
            except Exception as e:
                messagebox.showerror("Error", f"Playlist analysis failed: {str(e)}")
                self.update_status("Error during analysis")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def create_set_list(self):
        """Create set list from analyzed playlist"""
        if not hasattr(self, 'playlist_manager'):
            messagebox.showwarning("Warning", "Please analyze playlist first")
            return
        
        try:
            duration = self.set_duration_var.get()
            energy_curve = self.energy_curve_var.get()
            
            set_list = self.playlist_manager.create_set_list(
                duration_minutes=duration,
                energy_curve=energy_curve
            )
            
            # Clear and populate with set list
            for item in self.playlist_tree.get_children():
                self.playlist_tree.delete(item)
            
            for idx, track in enumerate(set_list):
                duration_min = track['duration'] / 60
                self.playlist_tree.insert("", tk.END, values=(
                    idx + 1,
                    track['filename'],
                    f"{track['bpm']:.1f}",
                    track['key'],
                    f"{duration_min:.1f}",
                    f"{track['avg_energy']:.4f}"
                ))
            
            self.current_set_list = set_list
            self.update_status(f"Set list created: {len(set_list)} tracks")
        except Exception as e:
            messagebox.showerror("Error", f"Set list creation failed: {str(e)}")
    
    def detect_cue_points(self):
        """Detect cue points"""
        file_path = self.dj_tools_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Detecting cue points...")
                dj_tools = DJTools(file_path)
                cue_points = dj_tools.detect_cue_points()
                
                result_text = f"Cue Points: {os.path.basename(file_path)}\n"
                result_text += "=" * 50 + "\n\n"
                
                for i, cue in enumerate(cue_points[:10], 1):
                    result_text += f"{i}. {cue['time']:.1f}s - {cue['type']} (Strength: {cue['strength']:.2f})\n"
                
                self.dj_tools_results.delete(1.0, tk.END)
                self.dj_tools_results.insert(1.0, result_text)
                self.update_status("Cue points detected")
            except Exception as e:
                messagebox.showerror("Error", f"Cue point detection failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def suggest_loops(self):
        """Suggest loops"""
        file_path = self.dj_tools_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Suggesting loops...")
                dj_tools = DJTools(file_path)
                loops = dj_tools.suggest_loops()
                
                result_text = f"Loop Suggestions: {os.path.basename(file_path)}\n"
                result_text += "=" * 50 + "\n\n"
                
                for i, loop in enumerate(loops[:10], 1):
                    result_text += f"{i}. {loop['start_time']:.1f}s - {loop['end_time']:.1f}s "
                    result_text += f"({loop['duration']:.1f}s)\n"
                    result_text += f"   Type: {loop['type']}\n"
                    result_text += f"   Energy Stability: {loop['energy_stability']:.2f}\n\n"
                
                self.dj_tools_results.delete(1.0, tk.END)
                self.dj_tools_results.insert(1.0, result_text)
                self.update_status("Loops suggested")
            except Exception as e:
                messagebox.showerror("Error", f"Loop suggestion failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_zones(self):
        """Analyze performance zones"""
        file_path = self.dj_tools_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Analyzing zones...")
                dj_tools = DJTools(file_path)
                zones = dj_tools.analyze_performance_zones()
                
                result_text = f"Performance Zones: {os.path.basename(file_path)}\n"
                result_text += "=" * 50 + "\n\n"
                
                for zone_name, zone_data in zones.items():
                    if zone_data['start'] > 0:
                        result_text += f"{zone_name.title()}:\n"
                        result_text += f"  Start: {zone_data['start']:.1f}s\n"
                        result_text += f"  End: {zone_data['end']:.1f}s\n"
                        result_text += f"  Energy: {zone_data['energy']:.4f}\n"
                        result_text += f"  Complexity: {zone_data['complexity']:.4f}\n\n"
                
                self.dj_tools_results.delete(1.0, tk.END)
                self.dj_tools_results.insert(1.0, result_text)
                self.update_status("Zones analyzed")
            except Exception as e:
                messagebox.showerror("Error", f"Zone analysis failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def generate_dj_notes(self):
        """Generate DJ notes"""
        file_path = self.dj_tools_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Generating DJ notes...")
                dj_tools = DJTools(file_path)
                notes = dj_tools.generate_dj_notes()
                
                self.dj_tools_results.delete(1.0, tk.END)
                self.dj_tools_results.insert(1.0, notes)
                self.update_status("DJ notes generated")
            except Exception as e:
                messagebox.showerror("Error", f"DJ notes generation failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def batch_analyze(self):
        """Batch analyze directory"""
        directory = filedialog.askdirectory(title="Select Directory for Batch Analysis")
        if not directory:
            return
        
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        def analyze():
            try:
                self.update_status("Batch analyzing...")
                batch_analyze_tracks(directory, output_dir)
                self.update_status("Batch analysis complete")
                messagebox.showinfo("Success", f"Batch analysis complete!\nResults saved to: {output_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"Batch analysis failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def analyze_effects(self):
        """Analyze audio effects"""
        file_path = self.effects_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid audio file")
            return
        
        def analyze():
            try:
                self.update_status("Analyzing audio effects...")
                effects = AudioEffects(file_path)
                analysis = effects.get_comprehensive_effects_analysis()
                
                result_text = f"Audio Effects Analysis: {os.path.basename(file_path)}\n"
                result_text += "=" * 50 + "\n\n"
                
                # Dynamics
                result_text += "Dynamics:\n"
                dynamics = analysis['dynamics']
                result_text += f"  Peak Level: {dynamics['peak_level']:.4f}\n"
                result_text += f"  RMS Level: {dynamics['rms_level']:.4f}\n"
                result_text += f"  Dynamic Range: {dynamics['dynamic_range_db']:.2f} dB\n"
                result_text += f"  Compression Ratio: {dynamics['compression_ratio']:.2f}\n"
                result_text += f"  Crest Factor: {dynamics['crest_factor']:.2f}\n"
                result_text += f"  Is Compressed: {dynamics['is_compressed']}\n\n"
                
                # Frequency spectrum
                result_text += "Frequency Spectrum:\n"
                freq = analysis['frequency_spectrum']
                result_text += f"  Spectral Centroid: {freq['spectral_centroid']:.2f} Hz\n"
                result_text += f"  Spectral Rolloff: {freq['spectral_rolloff']:.2f} Hz\n"
                result_text += f"  Zero Crossing Rate: {freq['zero_crossing_rate']:.4f}\n"
                result_text += f"  Bass: {freq['bass_percentage']:.1f}%\n"
                result_text += f"  Mid: {freq['mid_percentage']:.1f}%\n"
                result_text += f"  Treble: {freq['treble_percentage']:.1f}%\n\n"
                
                # Transient response
                result_text += "Transient Response:\n"
                transient = analysis['transient_response']
                result_text += f"  Onset Count: {transient['onset_count']}\n"
                result_text += f"  Avg Attack Time: {transient['avg_attack_time']:.3f}s\n"
                result_text += f"  Max Attack Time: {transient['max_attack_time']:.3f}s\n"
                result_text += f"  Min Attack Time: {transient['min_attack_time']:.3f}s\n"
                
                if analysis['clipping_points']:
                    result_text += f"\n⚠️  Clipping detected at: {analysis['clipping_points'][:5]}\n"
                
                self.effects_results.delete(1.0, tk.END)
                self.effects_results.insert(1.0, result_text)
                self.update_status("Effects analysis complete")
            except Exception as e:
                messagebox.showerror("Error", f"Effects analysis failed: {str(e)}")
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def export_analysis(self):
        """Export analysis results"""
        if not self.analysis_results:
            messagebox.showwarning("Warning", "No analysis results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Analysis",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("CSV", "*.csv"), ("Text", "*.txt"), ("All", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            format_type = self.export_format_var.get().lower()
            
            if format_type == "json":
                ExportTools.export_to_json(self.analysis_results, filename)
            elif format_type == "csv":
                # Convert to list format for CSV
                if isinstance(self.analysis_results, dict):
                    ExportTools.export_to_csv([self.analysis_results], filename)
            elif format_type == "txt":
                ExportTools.export_analysis_report(self.analysis_results, filename, format='txt')
            
            self.export_log.insert(tk.END, f"Exported analysis to: {filename}\n")
            self.update_status("Export complete")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def export_playlist(self):
        """Export playlist"""
        if not hasattr(self, 'current_set_list') and not hasattr(self, 'playlist_manager'):
            messagebox.showwarning("Warning", "No playlist to export")
            return
        
        playlist = getattr(self, 'current_set_list', None)
        if not playlist and hasattr(self, 'playlist_manager'):
            playlist = self.playlist_manager.tracks
        
        if not playlist:
            messagebox.showwarning("Warning", "No playlist data available")
            return
        
        format_type = self.export_format_var.get().lower()
        
        if format_type == "m3u":
            filename = filedialog.asksaveasfilename(
                title="Export Playlist",
                defaultextension=".m3u",
                filetypes=[("M3U", "*.m3u"), ("All", "*.*")]
            )
            if filename:
                ExportTools.export_to_m3u(playlist, filename)
        elif format_type == "rekordbox xml":
            filename = filedialog.asksaveasfilename(
                title="Export Playlist",
                defaultextension=".xml",
                filetypes=[("XML", "*.xml"), ("All", "*.*")]
            )
            if filename:
                ExportTools.export_to_rekordbox_xml(playlist, filename)
        elif format_type == "traktor nml":
            filename = filedialog.asksaveasfilename(
                title="Export Playlist",
                defaultextension=".nml",
                filetypes=[("NML", "*.nml"), ("All", "*.*")]
            )
            if filename:
                ExportTools.export_to_traktor_nml(playlist, filename)
        elif format_type == "json":
            filename = filedialog.asksaveasfilename(
                title="Export Playlist",
                defaultextension=".json",
                filetypes=[("JSON", "*.json"), ("All", "*.*")]
            )
            if filename:
                ExportTools.export_to_json(playlist, filename)
        elif format_type == "csv":
            filename = filedialog.asksaveasfilename(
                title="Export Playlist",
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv"), ("All", "*.*")]
            )
            if filename:
                ExportTools.export_to_csv(playlist, filename)
        
        if filename:
            self.export_log.insert(tk.END, f"Exported playlist to: {filename}\n")
            self.update_status("Playlist export complete")


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = DynaMixGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

