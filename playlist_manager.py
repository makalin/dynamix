import os
import json
import pandas as pd
from typing import List, Dict, Tuple
from audio_utils import AudioAnalyzer, analyze_track_compatibility
import matplotlib.pyplot as plt
import seaborn as sns

class PlaylistManager:
    """Manage and analyze playlists for optimal DJ mixing"""
    
    def __init__(self, playlist_directory: str = None):
        """Initialize playlist manager"""
        self.playlist_directory = playlist_directory
        self.tracks = []
        self.analysis_cache = {}
        
    def scan_directory(self, directory: str = None) -> List[str]:
        """
        Scan directory for audio files
        Returns: List of audio file paths
        """
        if directory is None:
            directory = self.playlist_directory
            
        if not directory or not os.path.exists(directory):
            return []
            
        audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
        audio_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    audio_files.append(os.path.join(root, file))
                    
        return audio_files
    
    def analyze_playlist(self, file_paths: List[str] = None) -> pd.DataFrame:
        """
        Analyze all tracks in playlist
        Returns: DataFrame with track analysis
        """
        if file_paths is None:
            file_paths = self.scan_directory()
            
        self.tracks = []
        
        for i, file_path in enumerate(file_paths):
            print(f"Analyzing track {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
            
            try:
                analyzer = AudioAnalyzer(file_path)
                features = analyzer.get_audio_features()
                
                track_info = {
                    'file_path': file_path,
                    'filename': os.path.basename(file_path),
                    'duration': features['duration'],
                    'bpm': features['bpm'],
                    'bpm_confidence': features['bpm_confidence'],
                    'key': features['key'],
                    'key_confidence': features['key_confidence'],
                    'avg_energy': features['avg_energy'],
                    'max_energy': features['max_energy'],
                    'energy_std': features['energy_std'],
                    'beat_count': features['beat_count'],
                    'section_count': features['section_count'],
                    'drop_count': features['drop_count']
                }
                
                self.tracks.append(track_info)
                self.analysis_cache[file_path] = features
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                continue
                
        return pd.DataFrame(self.tracks)
    
    def suggest_playlist_order(self, energy_curve: str = 'build', 
                             key_compatibility: bool = True,
                             bpm_transitions: bool = True) -> List[Dict]:
        """
        Suggest optimal playlist order based on various criteria
        
        Args:
            energy_curve: 'build' (low to high), 'wave' (alternating), 'custom'
            key_compatibility: Consider musical key compatibility
            bpm_transitions: Consider BPM transitions
            
        Returns: List of track dictionaries in suggested order
        """
        if not self.tracks:
            raise ValueError("No tracks analyzed. Run analyze_playlist() first.")
            
        df = pd.DataFrame(self.tracks)
        
        # Sort by energy for build curve
        if energy_curve == 'build':
            df_sorted = df.sort_values('avg_energy')
        elif energy_curve == 'wave':
            # Create alternating high/low energy pattern
            df_high = df[df['avg_energy'] > df['avg_energy'].median()].sort_values('avg_energy', ascending=False)
            df_low = df[df['avg_energy'] <= df['avg_energy'].median()].sort_values('avg_energy')
            
            # Interleave high and low energy tracks
            min_len = min(len(df_high), len(df_low))
            df_sorted = pd.concat([
                df_high.iloc[:min_len].reset_index(drop=True),
                df_low.iloc[:min_len].reset_index(drop=True)
            ], axis=1).T.melt()['value'].dropna()
        else:
            df_sorted = df
            
        # Apply key compatibility if requested
        if key_compatibility and len(df_sorted) > 1:
            df_sorted = self._optimize_key_transitions(df_sorted)
            
        # Apply BPM transitions if requested
        if bpm_transitions and len(df_sorted) > 1:
            df_sorted = self._optimize_bpm_transitions(df_sorted)
            
        return df_sorted.to_dict('records')
    
    def _optimize_key_transitions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize playlist for smooth key transitions"""
        # Simple key compatibility matrix
        key_compatibility = {
            'C': ['C', 'F', 'G', 'Am'],
            'C#': ['C#', 'F#', 'G#', 'A#m'],
            'D': ['D', 'G', 'A', 'Bm'],
            'D#': ['D#', 'G#', 'A#', 'Cm'],
            'E': ['E', 'A', 'B', 'C#m'],
            'F': ['F', 'Bb', 'C', 'Dm'],
            'F#': ['F#', 'B', 'C#', 'D#m'],
            'G': ['G', 'C', 'D', 'Em'],
            'G#': ['G#', 'C#', 'D#', 'Fm'],
            'A': ['A', 'D', 'E', 'F#m'],
            'A#': ['A#', 'D#', 'F', 'Gm'],
            'B': ['B', 'E', 'F#', 'G#m']
        }
        
        # Extract root notes
        def get_root_note(key_str):
            return key_str.split()[0]
            
        df['root_note'] = df['key'].apply(get_root_note)
        
        # Reorder for better key transitions
        optimized_order = []
        remaining_tracks = df.copy()
        
        # Start with first track
        current_track = remaining_tracks.iloc[0]
        optimized_order.append(current_track)
        remaining_tracks = remaining_tracks.drop(current_track.name)
        
        while not remaining_tracks.empty:
            current_key = current_track['root_note']
            compatible_keys = key_compatibility.get(current_key, [current_key])
            
            # Find tracks with compatible keys
            compatible_tracks = remaining_tracks[
                remaining_tracks['root_note'].isin(compatible_keys)
            ]
            
            if not compatible_tracks.empty:
                # Choose the most compatible track
                current_track = compatible_tracks.iloc[0]
            else:
                # If no compatible key, choose any track
                current_track = remaining_tracks.iloc[0]
                
            optimized_order.append(current_track)
            remaining_tracks = remaining_tracks.drop(current_track.name)
            
        return pd.DataFrame(optimized_order)
    
    def _optimize_bpm_transitions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize playlist for smooth BPM transitions"""
        # Sort by BPM for gradual transitions
        return df.sort_values('bpm')
    
    def create_set_list(self, duration_minutes: int = 60, 
                       energy_curve: str = 'build') -> List[Dict]:
        """
        Create a set list with specified duration
        
        Args:
            duration_minutes: Target set duration in minutes
            energy_curve: Energy curve type
            
        Returns: List of tracks for the set
        """
        if not self.tracks:
            raise ValueError("No tracks analyzed. Run analyze_playlist() first.")
            
        target_duration = duration_minutes * 60  # Convert to seconds
        suggested_order = self.suggest_playlist_order(energy_curve=energy_curve)
        
        set_list = []
        current_duration = 0
        
        for track in suggested_order:
            if current_duration + track['duration'] <= target_duration:
                set_list.append(track)
                current_duration += track['duration']
            else:
                break
                
        return set_list
    
    def analyze_playlist_compatibility(self) -> pd.DataFrame:
        """
        Analyze compatibility between all track pairs in playlist
        Returns: DataFrame with compatibility matrix
        """
        if not self.tracks:
            raise ValueError("No tracks analyzed. Run analyze_playlist() first.")
            
        compatibility_matrix = []
        
        for i, track1 in enumerate(self.tracks):
            for j, track2 in enumerate(self.tracks):
                if i != j:
                    try:
                        compatibility = analyze_track_compatibility(
                            track1['file_path'], 
                            track2['file_path']
                        )
                        
                        compatibility_matrix.append({
                            'track1': track1['filename'],
                            'track2': track2['filename'],
                            'bpm_compatibility': compatibility['bpm_compatibility'],
                            'key_compatibility': compatibility['key_compatibility'],
                            'energy_compatibility': compatibility['energy_compatibility'],
                            'overall_score': compatibility['overall_score']
                        })
                    except Exception as e:
                        print(f"Error analyzing compatibility: {e}")
                        continue
                        
        return pd.DataFrame(compatibility_matrix)
    
    def plot_playlist_analysis(self):
        """Create comprehensive playlist analysis visualization"""
        if not self.tracks:
            raise ValueError("No tracks analyzed. Run analyze_playlist() first.")
            
        df = pd.DataFrame(self.tracks)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # BPM distribution
        axes[0, 0].hist(df['bpm'], bins=20, alpha=0.7, edgecolor='black')
        axes[0, 0].set_title('BPM Distribution')
        axes[0, 0].set_xlabel('BPM')
        axes[0, 0].set_ylabel('Number of Tracks')
        
        # Energy distribution
        axes[0, 1].hist(df['avg_energy'], bins=20, alpha=0.7, edgecolor='black')
        axes[0, 1].set_title('Energy Distribution')
        axes[0, 1].set_xlabel('Average Energy')
        axes[0, 1].set_ylabel('Number of Tracks')
        
        # Key distribution
        key_counts = df['key'].value_counts()
        axes[1, 0].bar(range(len(key_counts)), key_counts.values)
        axes[1, 0].set_title('Key Distribution')
        axes[1, 0].set_xlabel('Musical Key')
        axes[1, 0].set_ylabel('Number of Tracks')
        axes[1, 0].set_xticks(range(len(key_counts)))
        axes[1, 0].set_xticklabels(key_counts.index, rotation=45)
        
        # Duration vs Energy scatter
        axes[1, 1].scatter(df['duration'], df['avg_energy'], alpha=0.6)
        axes[1, 1].set_title('Duration vs Energy')
        axes[1, 1].set_xlabel('Duration (seconds)')
        axes[1, 1].set_ylabel('Average Energy')
        
        plt.tight_layout()
        plt.show()
    
    def export_playlist(self, output_path: str, format: str = 'json'):
        """
        Export playlist analysis to file
        
        Args:
            output_path: Output file path
            format: 'json' or 'csv'
        """
        if not self.tracks:
            raise ValueError("No tracks analyzed. Run analyze_playlist() first.")
            
        df = pd.DataFrame(self.tracks)
        
        if format.lower() == 'json':
            df.to_json(output_path, orient='records', indent=2)
        elif format.lower() == 'csv':
            df.to_csv(output_path, index=False)
        else:
            raise ValueError("Format must be 'json' or 'csv'")
            
        print(f"Playlist exported to {output_path}")
    
    def load_playlist(self, file_path: str):
        """Load playlist from exported file"""
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                self.tracks = json.load(f)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            self.tracks = df.to_dict('records')
        else:
            raise ValueError("File must be .json or .csv")
            
        print(f"Loaded {len(self.tracks)} tracks from {file_path}")

def create_energy_based_set(playlist_manager: PlaylistManager, 
                           target_duration: int = 60,
                           energy_profile: str = 'peak_middle') -> List[Dict]:
    """
    Create a set list with specific energy profile
    
    Args:
        playlist_manager: Initialized playlist manager
        target_duration: Set duration in minutes
        energy_profile: 'peak_middle', 'build_up', 'wave', 'constant'
        
    Returns: List of tracks for the set
    """
    if not playlist_manager.tracks:
        raise ValueError("No tracks analyzed")
        
    df = pd.DataFrame(playlist_manager.tracks)
    target_seconds = target_duration * 60
    
    if energy_profile == 'peak_middle':
        # Sort by energy, peak in middle
        df_sorted = df.sort_values('avg_energy')
        n_tracks = len(df_sorted)
        mid_point = n_tracks // 2
        
        # Reorder: low -> high -> low
        first_half = df_sorted.iloc[:mid_point]
        second_half = df_sorted.iloc[mid_point:].sort_values('avg_energy', ascending=False)
        
        set_tracks = pd.concat([first_half, second_half])
        
    elif energy_profile == 'build_up':
        # Gradual energy increase
        set_tracks = df.sort_values('avg_energy')
        
    elif energy_profile == 'wave':
        # Alternating high/low energy
        high_energy = df[df['avg_energy'] > df['avg_energy'].median()].sort_values('avg_energy', ascending=False)
        low_energy = df[df['avg_energy'] <= df['avg_energy'].median()].sort_values('avg_energy')
        
        min_len = min(len(high_energy), len(low_energy))
        set_tracks = pd.concat([
            high_energy.iloc[:min_len].reset_index(drop=True),
            low_energy.iloc[:min_len].reset_index(drop=True)
        ], axis=1).T.melt()['value'].dropna()
        
    else:  # constant
        set_tracks = df
        
    # Select tracks to fit duration
    selected_tracks = []
    current_duration = 0
    
    for _, track in set_tracks.iterrows():
        if current_duration + track['duration'] <= target_seconds:
            selected_tracks.append(track.to_dict())
            current_duration += track['duration']
        else:
            break
            
    return selected_tracks 