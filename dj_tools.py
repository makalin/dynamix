import librosa
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
from audio_utils import AudioAnalyzer
import json
import os

class DJTools:
    """Collection of DJ-specific analysis and utility tools"""
    
    def __init__(self, audio_file: str):
        """Initialize DJ tools with audio file"""
        self.analyzer = AudioAnalyzer(audio_file)
        self.file_path = audio_file
        
    def detect_cue_points(self, sensitivity: float = 0.7) -> List[Dict]:
        """
        Detect optimal cue points for DJ performance
        
        Args:
            sensitivity: Detection sensitivity (0.0-1.0)
            
        Returns: List of cue point dictionaries
        """
        # Get onset strength
        onset_env = librosa.onset.onset_strength(y=self.analyzer.y, sr=self.analyzer.sr)
        
        # Detect onsets
        onset_frames = librosa.onset.onset_detect(
            onset_envelope=onset_env, 
            sr=self.analyzer.sr,
            threshold=sensitivity
        )
        
        # Convert to time
        onset_times = librosa.frames_to_time(onset_frames, sr=self.analyzer.sr)
        
        # Get beat times for reference
        beat_times, beat_strengths = self.analyzer.analyze_beat_grid()
        
        cue_points = []
        for i, onset_time in enumerate(onset_times):
            # Find nearest beat
            nearest_beat_idx = np.argmin(np.abs(beat_times - onset_time))
            nearest_beat = beat_times[nearest_beat_idx]
            beat_distance = abs(onset_time - nearest_beat)
            
            # Calculate onset strength
            onset_frame = librosa.time_to_frames(onset_time, sr=self.analyzer.sr)
            strength = onset_env[onset_frame] if onset_frame < len(onset_env) else 0
            
            # Determine cue point type
            if beat_distance < 0.1:  # Very close to beat
                cue_type = "Beat Sync"
            elif strength > np.percentile(onset_env, 80):
                cue_type = "Strong Onset"
            else:
                cue_type = "Onset"
            
            cue_points.append({
                'time': onset_time,
                'type': cue_type,
                'strength': float(strength),
                'nearest_beat': nearest_beat,
                'beat_distance': beat_distance
            })
        
        # Sort by strength and remove duplicates
        cue_points.sort(key=lambda x: x['strength'], reverse=True)
        
        # Remove cue points too close to each other (within 2 seconds)
        filtered_cues = []
        for cue in cue_points:
            if not any(abs(cue['time'] - existing['time']) < 2 for existing in filtered_cues):
                filtered_cues.append(cue)
        
        return filtered_cues[:20]  # Return top 20 cue points
    
    def suggest_loops(self, min_duration: float = 4.0, max_duration: float = 16.0) -> List[Dict]:
        """
        Suggest loop points for DJ performance
        
        Args:
            min_duration: Minimum loop duration in seconds
            max_duration: Maximum loop duration in seconds
            
        Returns: List of loop suggestions
        """
        # Get beat times
        beat_times, beat_strengths = self.analyzer.analyze_beat_grid()
        
        # Get sections
        sections = self.analyzer.detect_sections()
        
        # Get energy profile
        times, rms = self.analyzer.analyze_energy_profile()
        
        loop_suggestions = []
        
        # Suggest loops based on sections
        for section_name, start_time, end_time in sections:
            section_duration = end_time - start_time
            
            if min_duration <= section_duration <= max_duration:
                # Calculate section energy stability
                section_mask = (times >= start_time) & (times <= end_time)
                section_energy = rms[section_mask]
                energy_stability = 1.0 - (np.std(section_energy) / np.mean(section_energy))
                
                loop_suggestions.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': section_duration,
                    'type': f"Section: {section_name}",
                    'energy_stability': energy_stability,
                    'avg_energy': np.mean(section_energy)
                })
        
        # Suggest loops based on beat patterns
        for i in range(len(beat_times) - 1):
            for j in range(i + 1, len(beat_times)):
                loop_duration = beat_times[j] - beat_times[i]
                
                if min_duration <= loop_duration <= max_duration:
                    # Check if this is a musical phrase (4, 8, 16 beats)
                    beat_count = j - i
                    if beat_count in [4, 8, 16, 32]:
                        # Calculate loop energy
                        loop_mask = (times >= beat_times[i]) & (times <= beat_times[j])
                        loop_energy = rms[loop_mask]
                        
                        loop_suggestions.append({
                            'start_time': beat_times[i],
                            'end_time': beat_times[j],
                            'duration': loop_duration,
                            'type': f"Beat Loop: {beat_count} beats",
                            'energy_stability': 1.0 - (np.std(loop_energy) / np.mean(loop_energy)),
                            'avg_energy': np.mean(loop_energy)
                        })
        
        # Sort by energy stability and remove duplicates
        loop_suggestions.sort(key=lambda x: x['energy_stability'], reverse=True)
        
        # Remove overlapping loops
        filtered_loops = []
        for loop in loop_suggestions:
            overlapping = False
            for existing in filtered_loops:
                if (loop['start_time'] < existing['end_time'] and 
                    loop['end_time'] > existing['start_time']):
                    overlapping = True
                    break
            
            if not overlapping:
                filtered_loops.append(loop)
        
        return filtered_loops[:10]  # Return top 10 loops
    
    def analyze_performance_zones(self) -> Dict:
        """
        Analyze different performance zones in the track
        
        Returns: Dictionary with performance zone analysis
        """
        # Get sections
        sections = self.analyzer.detect_sections()
        
        # Get energy profile
        times, rms = self.analyzer.analyze_energy_profile()
        
        # Get drops
        drops = self.analyzer.detect_drops()
        
        zones = {
            'intro': {'start': 0, 'end': 0, 'energy': 0, 'complexity': 0},
            'build': {'start': 0, 'end': 0, 'energy': 0, 'complexity': 0},
            'drop': {'start': 0, 'end': 0, 'energy': 0, 'complexity': 0},
            'breakdown': {'start': 0, 'end': 0, 'energy': 0, 'complexity': 0},
            'outro': {'start': 0, 'end': 0, 'energy': 0, 'complexity': 0}
        }
        
        # Analyze each section
        for section_name, start_time, end_time in sections:
            section_mask = (times >= start_time) & (times <= end_time)
            section_energy = rms[section_mask]
            avg_energy = np.mean(section_energy)
            
            # Determine zone type based on energy and position
            if start_time < self.analyzer.duration * 0.2:
                zone_type = 'intro'
            elif start_time < self.analyzer.duration * 0.4:
                zone_type = 'build'
            elif start_time < self.analyzer.duration * 0.7:
                zone_type = 'drop'
            elif start_time < self.analyzer.duration * 0.9:
                zone_type = 'breakdown'
            else:
                zone_type = 'outro'
            
            # Update zone if this section has higher energy
            if avg_energy > zones[zone_type]['energy']:
                zones[zone_type].update({
                    'start': start_time,
                    'end': end_time,
                    'energy': avg_energy,
                    'complexity': np.std(section_energy)
                })
        
        return zones
    
    def generate_dj_notes(self) -> str:
        """
        Generate DJ performance notes for the track
        
        Returns: Formatted string with DJ notes
        """
        features = self.analyzer.get_audio_features()
        cue_points = self.detect_cue_points()
        loops = self.suggest_loops()
        zones = self.analyze_performance_zones()
        
        notes = f"""
🎵 DJ PERFORMANCE NOTES
Track: {os.path.basename(self.file_path)}
{'='*50}

📊 TRACK INFO:
• BPM: {features['bpm']:.1f}
• Key: {features['key']}
• Duration: {features['duration']:.1f}s
• Energy Level: {'High' if features['avg_energy'] > 0.1 else 'Medium' if features['avg_energy'] > 0.05 else 'Low'}

🎯 TOP CUE POINTS:
"""
        
        for i, cue in enumerate(cue_points[:5], 1):
            notes += f"{i}. {cue['time']:.1f}s - {cue['type']} (Strength: {cue['strength']:.2f})\n"
        
        notes += f"""
🔄 LOOP SUGGESTIONS:
"""
        
        for i, loop in enumerate(loops[:3], 1):
            notes += f"{i}. {loop['start_time']:.1f}s - {loop['end_time']:.1f}s ({loop['duration']:.1f}s)\n"
            notes += f"   Type: {loop['type']}\n"
        
        notes += f"""
🎚️ PERFORMANCE ZONES:
• Intro: {zones['intro']['start']:.1f}s - {zones['intro']['end']:.1f}s
• Build: {zones['build']['start']:.1f}s - {zones['build']['end']:.1f}s  
• Drop: {zones['drop']['start']:.1f}s - {zones['drop']['end']:.1f}s
• Breakdown: {zones['breakdown']['start']:.1f}s - {zones['breakdown']['end']:.1f}s
• Outro: {zones['outro']['start']:.1f}s - {zones['outro']['end']:.1f}s

💡 MIXING TIPS:
• Use {features['bpm']:.1f} BPM for tempo matching
• Key: {features['key']} - compatible with {self._get_compatible_keys(features['key'])}
• Energy peaks at {self._find_energy_peaks():.1f}s
• Best mixing points: {', '.join([f'{t:.1f}s' for t in self._find_mix_points()])}
"""
        
        return notes
    
    def _get_compatible_keys(self, key: str) -> str:
        """Get compatible musical keys"""
        key_compatibility = {
            'C major': 'F, G, Am',
            'C minor': 'F, G, Bb',
            'D major': 'G, A, Bm',
            'D minor': 'G, A, C',
            'E major': 'A, B, C#m',
            'E minor': 'A, B, D',
            'F major': 'Bb, C, Dm',
            'F minor': 'Bb, C, Eb',
            'G major': 'C, D, Em',
            'G minor': 'C, D, F',
            'A major': 'D, E, F#m',
            'A minor': 'D, E, G',
            'B major': 'E, F#, G#m',
            'B minor': 'E, F#, A'
        }
        return key_compatibility.get(key, 'Check music theory')
    
    def _find_energy_peaks(self) -> float:
        """Find the time of maximum energy"""
        times, rms = self.analyzer.analyze_energy_profile()
        peak_idx = np.argmax(rms)
        return times[peak_idx]
    
    def _find_mix_points(self) -> List[float]:
        """Find optimal mixing points"""
        times, rms = self.analyzer.analyze_energy_profile()
        
        # Find energy valleys (good exit points)
        rolling_avg = np.convolve(rms, np.ones(20)/20, mode='same')
        valleys = []
        
        for i, (time, energy, avg) in enumerate(zip(times, rms, rolling_avg)):
            if energy < avg * 0.8 and time > 30:
                valleys.append(time)
        
        return valleys[:3]  # Return top 3 mix points
    
    def export_dj_notes(self, output_file: str):
        """Export DJ notes to file"""
        notes = self.generate_dj_notes()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(notes)
        
        print(f"DJ notes exported to {output_file}")
    
    def create_performance_visualization(self):
        """Create visualization for DJ performance analysis"""
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Energy profile with zones
        times, rms = self.analyzer.analyze_energy_profile()
        axes[0].plot(times, rms, label='Energy', color='blue', alpha=0.7)
        
        zones = self.analyze_performance_zones()
        colors = ['green', 'orange', 'red', 'purple', 'brown']
        
        for (zone_name, zone_data), color in zip(zones.items(), colors):
            if zone_data['start'] > 0:
                axes[0].axvspan(zone_data['start'], zone_data['end'], 
                              alpha=0.3, color=color, label=zone_name.title())
        
        axes[0].set_title('Performance Zones')
        axes[0].set_ylabel('Energy')
        axes[0].legend()
        
        # Cue points
        cue_points = self.detect_cue_points()
        cue_times = [cue['time'] for cue in cue_points[:10]]
        cue_strengths = [cue['strength'] for cue in cue_points[:10]]
        
        axes[1].vlines(cue_times, 0, cue_strengths, alpha=0.7, color='red', label='Cue Points')
        axes[1].set_title('Cue Points')
        axes[1].set_ylabel('Strength')
        axes[1].legend()
        
        # Loop suggestions
        loops = self.suggest_loops()
        for i, loop in enumerate(loops[:5]):
            axes[2].axvspan(loop['start_time'], loop['end_time'], 
                          alpha=0.5, label=f"Loop {i+1}: {loop['type']}")
        
        axes[2].set_title('Loop Suggestions')
        axes[2].set_xlabel('Time (s)')
        axes[2].legend()
        
        plt.tight_layout()
        plt.show()

def batch_analyze_tracks(directory: str, output_dir: str = None):
    """
    Batch analyze all tracks in a directory and generate DJ notes
    
    Args:
        directory: Directory containing audio files
        output_dir: Output directory for DJ notes (optional)
    """
    if output_dir is None:
        output_dir = directory
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
    audio_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))
    
    print(f"Found {len(audio_files)} audio files")
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"Analyzing {i}/{len(audio_files)}: {os.path.basename(audio_file)}")
        
        try:
            dj_tools = DJTools(audio_file)
            
            # Generate filename for output
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_dj_notes.txt")
            
            # Export DJ notes
            dj_tools.export_dj_notes(output_file)
            
        except Exception as e:
            print(f"Error analyzing {audio_file}: {e}")
            continue
    
    print(f"Analysis complete! DJ notes saved to {output_dir}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DJ Tools - Performance Analysis")
    parser.add_argument("audio_file", help="Audio file to analyze")
    parser.add_argument("--export", help="Export DJ notes to file")
    parser.add_argument("--visualize", action="store_true", help="Show performance visualization")
    parser.add_argument("--batch", help="Batch analyze directory")
    parser.add_argument("--output-dir", help="Output directory for batch analysis")
    
    args = parser.parse_args()
    
    if args.batch:
        batch_analyze_tracks(args.batch, args.output_dir)
    else:
        dj_tools = DJTools(args.audio_file)
        
        # Print DJ notes
        print(dj_tools.generate_dj_notes())
        
        # Export if requested
        if args.export:
            dj_tools.export_dj_notes(args.export)
        
        # Show visualization if requested
        if args.visualize:
            dj_tools.create_performance_visualization() 