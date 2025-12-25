#!/usr/bin/env python3
"""
DynaMix Examples - Demonstration of all features and tools
This file contains practical examples of how to use DynaMix for various scenarios
"""

import os
import sys
import numpy as np
from audio_utils import AudioAnalyzer, analyze_track_compatibility, suggest_mix_points
from playlist_manager import PlaylistManager, create_energy_based_set
from dj_tools import DJTools, batch_analyze_tracks

def example_basic_analysis():
    """Example 1: Basic track analysis"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Track Analysis")
    print("=" * 60)
    
    # This is a demonstration - replace with actual file paths
    track_path = "example_track.mp3"
    
    if os.path.exists(track_path):
        # Initialize analyzer
        analyzer = AudioAnalyzer(track_path)
        
        # Get comprehensive features
        features = analyzer.get_audio_features()
        
        print(f"Track: {os.path.basename(track_path)}")
        print(f"Duration: {features['duration']:.1f} seconds")
        print(f"BPM: {features['bpm']:.1f} (confidence: {features['bpm_confidence']:.2f})")
        print(f"Key: {features['key']} (confidence: {features['key_confidence']:.2f})")
        print(f"Average Energy: {features['avg_energy']:.4f}")
        print(f"Sections: {features['section_count']}")
        print(f"Drops: {features['drop_count']}")
        
        # Detect sections
        sections = analyzer.detect_sections()
        print("\nDetected Sections:")
        for section_name, start, end in sections:
            print(f"  {section_name}: {start:.1f}s - {end:.1f}s")
        
        # Analyze beat grid
        beat_times, beat_strengths = analyzer.analyze_beat_grid()
        print(f"\nBeat Analysis: {len(beat_times)} beats detected")
        print(f"Average beat strength: {np.mean(beat_strengths):.3f}")
        
    else:
        print(f"Example file {track_path} not found. Skipping basic analysis example.")

def example_two_track_compatibility():
    """Example 2: Two-track compatibility analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Two-Track Compatibility Analysis")
    print("=" * 60)
    
    # This is a demonstration - replace with actual file paths
    track1_path = "track1.mp3"
    track2_path = "track2.mp3"
    
    if os.path.exists(track1_path) and os.path.exists(track2_path):
        # Analyze compatibility
        compatibility = analyze_track_compatibility(track1_path, track2_path)
        
        print("Compatibility Analysis:")
        print(f"BPM Compatibility: {compatibility['bpm_compatibility']:.1f}%")
        print(f"BPM Difference: {compatibility['bpm_difference']:.1f}")
        print(f"Key Compatibility: {compatibility['key_compatibility']:.1f}%")
        print(f"Energy Compatibility: {compatibility['energy_compatibility']:.1f}%")
        print(f"Overall Score: {compatibility['overall_score']:.1f}%")
        
        # Get mix suggestions
        suggestions = suggest_mix_points(track1_path, track2_path)
        
        print(f"\nMix Suggestions:")
        print(f"Recommended mix duration: {suggestions['recommended_mix_duration']:.1f} seconds")
        print(f"BPM sync required: {suggestions['bpm_sync_required']}")
        
        if suggestions['track1_exit_points']:
            print(f"Track 1 exit points: {[f'{t:.1f}s' for t in suggestions['track1_exit_points'][:3]]}")
        
        if suggestions['track2_entry_points']:
            print(f"Track 2 entry points: {[f'{t:.1f}s' for t in suggestions['track2_entry_points'][:3]]}")
        
    else:
        print("Example files not found. Skipping compatibility analysis example.")

def example_playlist_management():
    """Example 3: Playlist management and set creation"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Playlist Management and Set Creation")
    print("=" * 60)
    
    # This is a demonstration - replace with actual directory path
    music_directory = "music_folder"
    
    if os.path.exists(music_directory):
        # Initialize playlist manager
        manager = PlaylistManager(music_directory)
        
        # Scan for audio files
        audio_files = manager.scan_directory()
        print(f"Found {len(audio_files)} audio files")
        
        if audio_files:
            # Analyze playlist (this would take some time with real files)
            print("Analyzing playlist...")
            # df = manager.analyze_playlist(audio_files)  # Uncomment for real analysis
            
            # Create set list
            print("Creating 60-minute set list...")
            # set_list = manager.create_set_list(duration_minutes=60, energy_curve='build')
            
            # Example set list structure
            set_list = [
                {'filename': 'Track 1.mp3', 'bpm': 128.0, 'key': 'C major', 'duration': 240.0},
                {'filename': 'Track 2.mp3', 'bpm': 130.0, 'key': 'F major', 'duration': 245.0},
                {'filename': 'Track 3.mp3', 'bpm': 132.0, 'key': 'G major', 'duration': 238.0},
            ]
            
            print("\nRecommended Set List:")
            total_duration = 0
            for i, track in enumerate(set_list, 1):
                duration_min = track['duration'] / 60
                total_duration += track['duration']
                print(f"{i:2d}. {track['filename']}")
                print(f"    BPM: {track['bpm']:.1f} | Key: {track['key']} | Duration: {duration_min:.1f}min")
            
            print(f"\nTotal Duration: {total_duration/60:.1f} minutes")
            
            # Export analysis
            # manager.export_playlist("playlist_analysis.json", format='json')
            print("\nPlaylist analysis can be exported to JSON/CSV format")
            
    else:
        print(f"Example directory {music_directory} not found. Skipping playlist management example.")

def example_dj_tools():
    """Example 4: DJ performance tools"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: DJ Performance Tools")
    print("=" * 60)
    
    # This is a demonstration - replace with actual file path
    track_path = "example_track.mp3"
    
    if os.path.exists(track_path):
        # Initialize DJ tools
        dj_tools = DJTools(track_path)
        
        # Detect cue points
        cue_points = dj_tools.detect_cue_points(sensitivity=0.7)
        print(f"Detected {len(cue_points)} cue points")
        
        print("\nTop 5 Cue Points:")
        for i, cue in enumerate(cue_points[:5], 1):
            print(f"{i}. {cue['time']:.1f}s - {cue['type']} (Strength: {cue['strength']:.2f})")
        
        # Suggest loops
        loops = dj_tools.suggest_loops(min_duration=4.0, max_duration=16.0)
        print(f"\nSuggested {len(loops)} loops")
        
        print("\nTop 3 Loop Suggestions:")
        for i, loop in enumerate(loops[:3], 1):
            print(f"{i}. {loop['start_time']:.1f}s - {loop['end_time']:.1f}s ({loop['duration']:.1f}s)")
            print(f"   Type: {loop['type']}")
            print(f"   Energy Stability: {loop['energy_stability']:.2f}")
        
        # Analyze performance zones
        zones = dj_tools.analyze_performance_zones()
        print(f"\nPerformance Zones:")
        for zone_name, zone_data in zones.items():
            if zone_data['start'] > 0:
                print(f"  {zone_name.title()}: {zone_data['start']:.1f}s - {zone_data['end']:.1f}s")
        
        # Generate DJ notes
        notes = dj_tools.generate_dj_notes()
        print(f"\nDJ Notes Preview:")
        print(notes[:500] + "..." if len(notes) > 500 else notes)
        
    else:
        print(f"Example file {track_path} not found. Skipping DJ tools example.")

def example_batch_analysis():
    """Example 5: Batch analysis of multiple tracks"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Batch Analysis")
    print("=" * 60)
    
    # This is a demonstration - replace with actual directory path
    music_directory = "music_folder"
    output_directory = "dj_notes"
    
    if os.path.exists(music_directory):
        print(f"Batch analyzing tracks in {music_directory}")
        print("This would process all audio files and generate DJ notes for each")
        
        # Create output directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Example of what batch analysis would do
        audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
        audio_files = []
        
        for root, dirs, files in os.walk(music_directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    audio_files.append(os.path.join(root, file))
        
        print(f"Would analyze {len(audio_files)} audio files")
        print(f"DJ notes would be saved to {output_directory}/")
        
        # Example output files
        example_files = [
            "track1_dj_notes.txt",
            "track2_dj_notes.txt", 
            "track3_dj_notes.txt"
        ]
        
        print("\nExample output files:")
        for file in example_files:
            print(f"  {output_directory}/{file}")
        
    else:
        print(f"Example directory {music_directory} not found. Skipping batch analysis example.")

def example_advanced_visualization():
    """Example 6: Advanced visualization features"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Advanced Visualization")
    print("=" * 60)
    
    # This is a demonstration - replace with actual file path
    track_path = "example_track.mp3"
    
    if os.path.exists(track_path):
        analyzer = AudioAnalyzer(track_path)
        
        print("Available visualization features:")
        print("1. Comprehensive Analysis Plot:")
        print("   - Energy profile over time")
        print("   - Beat grid with timing")
        print("   - Chromagram for key analysis")
        print("   - Detected sections")
        
        print("\n2. DJ Performance Visualization:")
        print("   - Performance zones (intro, build, drop, etc.)")
        print("   - Cue points with strength indicators")
        print("   - Loop suggestions")
        
        print("\n3. Playlist Analysis Charts:")
        print("   - BPM distribution histogram")
        print("   - Energy distribution")
        print("   - Key distribution")
        print("   - Duration vs Energy scatter plot")
        
        print("\n4. Compatibility Radar Chart:")
        print("   - BPM compatibility")
        print("   - Key compatibility")
        print("   - Energy compatibility")
        
        print("\nTo see these visualizations, run:")
        print("  python mix_enhanced.py track1.mp3 track2.mp3 --visualize")
        print("  python dj_tools.py track.mp3 --visualize")
        print("  python mix_enhanced.py --playlist /path/to/music --visualize")
        
    else:
        print(f"Example file {track_path} not found. Skipping visualization example.")

def example_custom_analysis():
    """Example 7: Custom analysis workflow"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Custom Analysis Workflow")
    print("=" * 60)
    
    print("Custom analysis workflow example:")
    print("\n1. Load and analyze multiple tracks:")
    print("   analyzer1 = AudioAnalyzer('track1.mp3')")
    print("   analyzer2 = AudioAnalyzer('track2.mp3')")
    print("   analyzer3 = AudioAnalyzer('track3.mp3')")
    
    print("\n2. Compare specific features:")
    print("   features1 = analyzer1.get_audio_features()")
    print("   features2 = analyzer2.get_audio_features()")
    print("   bpm_diff = abs(features1['bpm'] - features2['bpm'])")
    
    print("\n3. Create custom compatibility matrix:")
    print("   tracks = [analyzer1, analyzer2, analyzer3]")
    print("   for i, track1 in enumerate(tracks):")
    print("       for j, track2 in enumerate(tracks):")
    print("           if i != j:")
    print("               compatibility = analyze_track_compatibility(...)")
    
    print("\n4. Generate custom set lists:")
    print("   # Filter tracks by BPM range")
    print("   bpm_filtered = [t for t in tracks if 125 <= t.get_audio_features()['bpm'] <= 135]")
    print("   # Sort by energy")
    print("   energy_sorted = sorted(bpm_filtered, key=lambda x: x.get_audio_features()['avg_energy'])")
    
    print("\n5. Export custom analysis:")
    print("   import json")
    print("   with open('custom_analysis.json', 'w') as f:")
    print("       json.dump(analysis_results, f, indent=2)")

def main():
    """Run all examples"""
    print("🎵 DynaMix Examples - Feature Demonstration")
    print("Note: These examples use placeholder file paths.")
    print("Replace with actual audio files to see real results.\n")
    
    try:
        example_basic_analysis()
        example_two_track_compatibility()
        example_playlist_management()
        example_dj_tools()
        example_batch_analysis()
        example_advanced_visualization()
        example_custom_analysis()
        
        print("\n" + "=" * 60)
        print("EXAMPLES COMPLETE")
        print("=" * 60)
        print("\nTo run with real audio files:")
        print("1. Replace placeholder paths with actual audio files")
        print("2. Uncomment the analysis code in each example")
        print("3. Run: python examples.py")
        
        print("\nFor more information, see the README.md file")
        print("or run: python mix_enhanced.py --help")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    main() 