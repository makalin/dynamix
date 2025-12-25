"""
Audio Effects and Processing Tools
Additional utilities for audio manipulation and effects analysis
"""

import librosa
import numpy as np
from typing import List, Dict, Tuple, Optional
from audio_utils import AudioAnalyzer


class AudioEffects:
    """Audio effects analysis and processing tools"""
    
    def __init__(self, audio_file: str):
        """Initialize with audio file"""
        self.analyzer = AudioAnalyzer(audio_file)
        self.file_path = audio_file
        
    def analyze_dynamics(self) -> Dict:
        """
        Analyze dynamic range and compression characteristics
        Returns: Dictionary with dynamics analysis
        """
        y = self.analyzer.y
        sr = self.analyzer.sr
        
        # Calculate RMS energy
        rms = librosa.feature.rms(y=y)[0]
        
        # Calculate peak levels
        peak = np.max(np.abs(y))
        
        # Calculate dynamic range
        dynamic_range = 20 * np.log10(peak / (np.mean(rms) + 1e-10))
        
        # Detect compression (low dynamic range = more compressed)
        compression_ratio = 1.0 - (dynamic_range / 60.0)  # Normalize to 0-1
        
        # Analyze crest factor (peak to RMS ratio)
        crest_factor = peak / (np.mean(rms) + 1e-10)
        
        return {
            'peak_level': float(peak),
            'rms_level': float(np.mean(rms)),
            'dynamic_range_db': float(dynamic_range),
            'compression_ratio': float(compression_ratio),
            'crest_factor': float(crest_factor),
            'is_compressed': compression_ratio > 0.5
        }
    
    def detect_phasing(self, window_size: float = 0.1) -> List[float]:
        """
        Detect potential phasing issues in stereo audio
        Returns: List of time positions with potential phasing
        """
        # Load as stereo
        y, sr = librosa.load(self.file_path, sr=None, mono=False)
        
        if y.ndim == 1:
            return []  # Mono audio, no phasing possible
        
        # Calculate correlation between channels
        window_samples = int(sr * window_size)
        phasing_points = []
        
        for i in range(0, len(y[0]) - window_samples, window_samples):
            left = y[0][i:i+window_samples]
            right = y[1][i:i+window_samples]
            
            # Calculate cross-correlation
            correlation = np.corrcoef(left, right)[0, 1]
            
            # Low correlation indicates potential phasing
            if correlation < 0.3:
                time_pos = i / sr
                phasing_points.append(time_pos)
        
        return phasing_points
    
    def analyze_frequency_spectrum(self) -> Dict:
        """
        Analyze frequency spectrum characteristics
        Returns: Dictionary with frequency analysis
        """
        y = self.analyzer.y
        sr = self.analyzer.sr
        
        # Compute spectral centroid (brightness)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        avg_centroid = np.mean(spectral_centroids)
        
        # Compute spectral rolloff (high frequency content)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        avg_rolloff = np.mean(spectral_rolloff)
        
        # Compute zero crossing rate (noisiness)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        avg_zcr = np.mean(zcr)
        
        # Compute spectral bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        avg_bandwidth = np.mean(spectral_bandwidth)
        
        # Analyze frequency bands
        stft = librosa.stft(y)
        magnitude = np.abs(stft)
        
        # Frequency bands (Hz)
        freqs = librosa.fft_frequencies(sr=sr)
        bass_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 4000)
        treble_mask = freqs >= 4000
        
        bass_energy = np.mean(magnitude[bass_mask, :])
        mid_energy = np.mean(magnitude[mid_mask, :])
        treble_energy = np.mean(magnitude[treble_mask, :])
        
        total_energy = bass_energy + mid_energy + treble_energy
        
        return {
            'spectral_centroid': float(avg_centroid),
            'spectral_rolloff': float(avg_rolloff),
            'zero_crossing_rate': float(avg_zcr),
            'spectral_bandwidth': float(avg_bandwidth),
            'bass_percentage': float(bass_energy / total_energy * 100),
            'mid_percentage': float(mid_energy / total_energy * 100),
            'treble_percentage': float(treble_energy / total_energy * 100)
        }
    
    def detect_clipping(self, threshold: float = 0.98) -> List[float]:
        """
        Detect potential clipping/overload in audio
        Returns: List of time positions with clipping
        """
        y = self.analyzer.y
        sr = self.analyzer.sr
        
        # Find samples near maximum
        clipping_samples = np.where(np.abs(y) > threshold)[0]
        
        if len(clipping_samples) == 0:
            return []
        
        # Convert to time positions
        clipping_times = librosa.samples_to_time(clipping_samples, sr=sr)
        
        # Group nearby clipping points
        grouped_times = []
        current_group = [clipping_times[0]]
        
        for time in clipping_times[1:]:
            if time - current_group[-1] < 0.1:  # Within 100ms
                current_group.append(time)
            else:
                if len(current_group) > 10:  # Significant clipping
                    grouped_times.append(current_group[0])
                current_group = [time]
        
        if len(current_group) > 10:
            grouped_times.append(current_group[0])
        
        return grouped_times
    
    def analyze_transient_response(self) -> Dict:
        """
        Analyze transient response and attack characteristics
        Returns: Dictionary with transient analysis
        """
        y = self.analyzer.y
        sr = self.analyzer.sr
        
        # Calculate onset strength
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Detect onsets
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        onset_times = librosa.frames_to_time(onsets, sr=sr)
        
        # Calculate attack times (time to reach peak from onset)
        attack_times = []
        for onset_frame in onsets:
            onset_sample = librosa.frames_to_samples(onset_frame, sr=sr)
            window = y[onset_sample:onset_sample + int(sr * 0.1)]  # 100ms window
            
            if len(window) > 0:
                peak_idx = np.argmax(np.abs(window))
                attack_time = peak_idx / sr
                attack_times.append(attack_time)
        
        return {
            'onset_count': len(onsets),
            'avg_attack_time': float(np.mean(attack_times)) if attack_times else 0.0,
            'max_attack_time': float(np.max(attack_times)) if attack_times else 0.0,
            'min_attack_time': float(np.min(attack_times)) if attack_times else 0.0,
            'onset_strength_avg': float(np.mean(onset_env)),
            'onset_strength_max': float(np.max(onset_env))
        }
    
    def get_comprehensive_effects_analysis(self) -> Dict:
        """Get comprehensive effects analysis"""
        return {
            'dynamics': self.analyze_dynamics(),
            'frequency_spectrum': self.analyze_frequency_spectrum(),
            'transient_response': self.analyze_transient_response(),
            'clipping_points': self.detect_clipping(),
            'phasing_points': self.detect_phasing()
        }


class TrackComparer:
    """Compare multiple tracks for mixing compatibility"""
    
    def __init__(self):
        self.tracks = []
        
    def add_track(self, audio_file: str):
        """Add a track to comparison"""
        analyzer = AudioAnalyzer(audio_file)
        features = analyzer.get_audio_features()
        effects = AudioEffects(audio_file)
        effects_data = effects.get_comprehensive_effects_analysis()
        
        self.tracks.append({
            'file_path': audio_file,
            'analyzer': analyzer,
            'features': features,
            'effects': effects_data
        })
    
    def compare_all_tracks(self) -> Dict:
        """Compare all tracks and return compatibility matrix"""
        if len(self.tracks) < 2:
            return {}
        
        from audio_utils import analyze_track_compatibility
        
        comparison = {}
        
        for i, track1 in enumerate(self.tracks):
            for j, track2 in enumerate(self.tracks):
                if i != j:
                    key = f"{i}_{j}"
                    compatibility = analyze_track_compatibility(
                        track1['file_path'],
                        track2['file_path']
                    )
                    
                    # Add additional comparisons
                    bpm_diff = abs(track1['features']['bpm'] - track2['features']['bpm'])
                    energy_diff = abs(track1['features']['avg_energy'] - track2['features']['avg_energy'])
                    
                    comparison[key] = {
                        'track1_index': i,
                        'track2_index': j,
                        'compatibility': compatibility,
                        'bpm_difference': bpm_diff,
                        'energy_difference': energy_diff,
                        'frequency_match': abs(
                            track1['effects']['frequency_spectrum']['spectral_centroid'] -
                            track2['effects']['frequency_spectrum']['spectral_centroid']
                        ) < 500  # Within 500 Hz
                    }
        
        return comparison
    
    def find_best_mix_sequence(self, max_tracks: int = None) -> List[int]:
        """
        Find optimal sequence for mixing multiple tracks
        Returns: List of track indices in optimal order
        """
        if len(self.tracks) < 2:
            return list(range(len(self.tracks)))
        
        comparison = self.compare_all_tracks()
        
        # Build compatibility graph
        compatibility_scores = {}
        for key, data in comparison.items():
            i, j = data['track1_index'], data['track2_index']
            score = data['compatibility']['overall_score']
            compatibility_scores[(i, j)] = score
        
        # Greedy algorithm to find best sequence
        sequence = [0]  # Start with first track
        remaining = set(range(1, len(self.tracks)))
        
        while remaining:
            current = sequence[-1]
            best_next = None
            best_score = -1
            
            for next_track in remaining:
                score = compatibility_scores.get((current, next_track), 0)
                if score > best_score:
                    best_score = score
                    best_next = next_track
            
            if best_next is not None:
                sequence.append(best_next)
                remaining.remove(best_next)
            else:
                # If no good match, just add any remaining track
                sequence.append(remaining.pop())
        
        if max_tracks:
            sequence = sequence[:max_tracks]
        
        return sequence

