import librosa
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional, List
import warnings
warnings.filterwarnings('ignore')

class AudioAnalyzer:
    """Advanced audio analysis utilities for DJ mixing"""
    
    def __init__(self, file_path: str):
        """Initialize analyzer with audio file"""
        self.file_path = file_path
        self.y, self.sr = librosa.load(file_path, sr=None)
        self.duration = librosa.get_duration(y=self.y, sr=self.sr)
        
    def detect_bpm(self) -> Tuple[float, float]:
        """
        Detect BPM using multiple methods and return the most reliable result
        Returns: (bpm, confidence)
        """
        # Method 1: Using librosa's beat_track
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        
        # Method 2: Using onset detection
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempo_onset = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sr)
        
        # Method 3: Using dynamic programming
        tempo_dp = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sr, aggregate=None)
        
        # Return the most consistent result
        tempos = [tempo, tempo_onset[0], np.median(tempo_dp)]
        final_bpm = np.median(tempos)
        
        # Calculate confidence based on consistency
        confidence = 1.0 - (np.std(tempos) / np.mean(tempos))
        
        return final_bpm, confidence
    
    def detect_key(self) -> Tuple[str, float]:
        """
        Detect musical key using chromagram analysis
        Returns: (key, confidence)
        """
        # Extract chromagram
        chroma = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
        
        # Get key using librosa's key detection
        key_raw = librosa.feature.key_mode(chroma)
        
        # Map to readable key names
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key = key_names[key_raw[0]]
        mode = 'major' if key_raw[1] == 1 else 'minor'
        
        # Calculate confidence
        chroma_avg = np.mean(chroma, axis=1)
        confidence = np.max(chroma_avg) / np.sum(chroma_avg)
        
        return f"{key} {mode}", confidence
    
    def analyze_beat_grid(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Analyze beat grid and return beat times and strengths
        Returns: (beat_times, beat_strengths)
        """
        # Get onset strength
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        
        # Detect beats
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sr)
        
        # Get beat times
        beat_times = librosa.frames_to_time(beats, sr=self.sr)
        
        # Get beat strengths
        beat_strengths = onset_env[beats]
        
        return beat_times, beat_strengths
    
    def detect_sections(self) -> List[Tuple[str, float, float]]:
        """
        Detect song sections (intro, verse, chorus, etc.)
        Returns: List of (section_name, start_time, end_time)
        """
        # Compute MFCC features
        mfcc = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
        
        # Compute similarity matrix
        sim_matrix = librosa.segment.recurrence_matrix(mfcc, mode='affinity')
        
        # Detect segments
        segments = librosa.segment.detect_segments(sim_matrix)
        
        # Convert to time
        segment_times = librosa.frames_to_time(segments, sr=self.sr)
        
        # Label sections (simplified)
        section_names = ['Intro', 'Verse', 'Chorus', 'Bridge', 'Outro']
        sections = []
        
        for i, (start, end) in enumerate(segment_times):
            if i < len(section_names):
                sections.append((section_names[i], start, end))
            else:
                sections.append((f'Section {i+1}', start, end))
        
        return sections
    
    def analyze_energy_profile(self, window_size: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Analyze energy profile with customizable window size
        Returns: (times, energy_values)
        """
        # Calculate RMS energy
        hop_length = int(self.sr * window_size / 4)  # 25% overlap
        rms = librosa.feature.rms(y=self.y, hop_length=hop_length)[0]
        
        # Convert to time
        times = librosa.frames_to_time(np.arange(len(rms)), sr=self.sr, hop_length=hop_length)
        
        return times, rms
    
    def detect_drops(self, threshold_factor: float = 1.5) -> List[float]:
        """
        Detect energy drops (breakdowns) in the track
        Returns: List of drop times
        """
        times, rms = self.analyze_energy_profile()
        
        # Calculate rolling average
        window = int(len(rms) * 0.1)  # 10% of track length
        rolling_avg = np.convolve(rms, np.ones(window)/window, mode='same')
        
        # Find drops (energy significantly below rolling average)
        drops = []
        for i, (time, energy, avg) in enumerate(zip(times, rms, rolling_avg)):
            if energy < avg / threshold_factor and i > window:
                drops.append(time)
        
        # Remove duplicates (drops within 5 seconds of each other)
        filtered_drops = []
        for drop in drops:
            if not any(abs(drop - existing) < 5 for existing in filtered_drops):
                filtered_drops.append(drop)
        
        return filtered_drops
    
    def get_audio_features(self) -> dict:
        """
        Get comprehensive audio features
        Returns: Dictionary with all analyzed features
        """
        features = {}
        
        # Basic features
        features['duration'] = self.duration
        features['sample_rate'] = self.sr
        
        # BPM and key
        features['bpm'], features['bpm_confidence'] = self.detect_bpm()
        features['key'], features['key_confidence'] = self.detect_key()
        
        # Energy analysis
        times, rms = self.analyze_energy_profile()
        features['avg_energy'] = np.mean(rms)
        features['max_energy'] = np.max(rms)
        features['energy_std'] = np.std(rms)
        
        # Beat analysis
        beat_times, beat_strengths = self.analyze_beat_grid()
        features['beat_count'] = len(beat_times)
        features['avg_beat_strength'] = np.mean(beat_strengths)
        
        # Section analysis
        sections = self.detect_sections()
        features['section_count'] = len(sections)
        features['sections'] = sections
        
        # Drop detection
        drops = self.detect_drops()
        features['drop_count'] = len(drops)
        features['drops'] = drops
        
        return features
    
    def plot_comprehensive_analysis(self):
        """Create a comprehensive visualization of all analyses"""
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # Energy profile
        times, rms = self.analyze_energy_profile()
        axes[0].plot(times, rms, label='RMS Energy')
        axes[0].set_title('Energy Profile')
        axes[0].set_ylabel('Energy')
        axes[0].legend()
        
        # Beat grid
        beat_times, beat_strengths = self.analyze_beat_grid()
        axes[1].vlines(beat_times, 0, beat_strengths, alpha=0.5, label='Beats')
        axes[1].set_title('Beat Grid')
        axes[1].set_ylabel('Beat Strength')
        axes[1].legend()
        
        # Chromagram (key analysis)
        chroma = librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
        librosa.display.specshow(chroma, sr=self.sr, x_axis='time', y_axis='chroma', ax=axes[2])
        axes[2].set_title('Chroma Features (Key Analysis)')
        
        # Sections
        sections = self.detect_sections()
        for section_name, start, end in sections:
            axes[3].axvspan(start, end, alpha=0.3, label=section_name)
        axes[3].set_title('Detected Sections')
        axes[3].set_xlabel('Time (s)')
        axes[3].legend()
        
        plt.tight_layout()
        plt.show()

def analyze_track_compatibility(track1_path: str, track2_path: str) -> dict:
    """
    Analyze compatibility between two tracks for mixing
    Returns: Dictionary with compatibility metrics
    """
    analyzer1 = AudioAnalyzer(track1_path)
    analyzer2 = AudioAnalyzer(track2_path)
    
    features1 = analyzer1.get_audio_features()
    features2 = analyzer2.get_audio_features()
    
    compatibility = {}
    
    # BPM compatibility
    bpm_diff = abs(features1['bpm'] - features2['bpm'])
    compatibility['bpm_compatibility'] = max(0, 100 - (bpm_diff * 2))
    compatibility['bpm_difference'] = bpm_diff
    
    # Key compatibility
    key1, key2 = features1['key'], features2['key']
    # Simple key compatibility (can be enhanced with music theory)
    if key1 == key2:
        compatibility['key_compatibility'] = 100
    elif key1.split()[0] == key2.split()[0]:  # Same root note
        compatibility['key_compatibility'] = 80
    else:
        compatibility['key_compatibility'] = 50
    
    # Energy compatibility
    energy_diff = abs(features1['avg_energy'] - features2['avg_energy'])
    max_energy = max(features1['avg_energy'], features2['avg_energy'])
    compatibility['energy_compatibility'] = max(0, 100 - (energy_diff / max_energy * 100))
    
    # Overall compatibility score
    compatibility['overall_score'] = (
        compatibility['bpm_compatibility'] * 0.4 +
        compatibility['key_compatibility'] * 0.3 +
        compatibility['energy_compatibility'] * 0.3
    )
    
    return compatibility

def suggest_mix_points(track1_path: str, track2_path: str) -> dict:
    """
    Suggest optimal mix points for two tracks
    Returns: Dictionary with mix suggestions
    """
    analyzer1 = AudioAnalyzer(track1_path)
    analyzer2 = AudioAnalyzer(track2_path)
    
    # Get features
    features1 = analyzer1.get_audio_features()
    features2 = analyzer2.get_audio_features()
    
    # Analyze energy profiles
    times1, rms1 = analyzer1.analyze_energy_profile()
    times2, rms2 = analyzer2.analyze_energy_profile()
    
    # Find energy valleys in track 1 (good exit points)
    rolling_avg1 = np.convolve(rms1, np.ones(20)/20, mode='same')
    valleys1 = []
    for i, (time, energy, avg) in enumerate(zip(times1, rms1, rolling_avg1)):
        if energy < avg * 0.8 and time > 30:  # Avoid very early valleys
            valleys1.append(time)
    
    # Find energy peaks in track 2 (good entry points)
    rolling_avg2 = np.convolve(rms2, np.ones(20)/20, mode='same')
    peaks2 = []
    for i, (time, energy, avg) in enumerate(zip(times2, rms2, rolling_avg2)):
        if energy > avg * 1.2 and time < features2['duration'] - 30:  # Avoid very late peaks
            peaks2.append(time)
    
    suggestions = {
        'track1_exit_points': valleys1[:5],  # Top 5 exit points
        'track2_entry_points': peaks2[:5],   # Top 5 entry points
        'recommended_mix_duration': min(16, features1['duration'] * 0.1),  # 10% of track or 16 bars
        'bpm_sync_required': abs(features1['bpm'] - features2['bpm']) > 5
    }
    
    return suggestions 