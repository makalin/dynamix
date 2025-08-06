#!/usr/bin/env python3
"""
Enhanced DynaMix - Advanced Audio Transition Analysis Tool
Enhanced version with BPM detection, key analysis, and comprehensive mixing recommendations
"""

import argparse
import sys
import os
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import numpy as np

from audio_utils import AudioAnalyzer, analyze_track_compatibility, suggest_mix_points
from playlist_manager import PlaylistManager

class EnhancedMixAnalyzer:
    """Enhanced mixing analysis with comprehensive features"""
    
    def __init__(self):
        self.analyzer1 = None
        self.analyzer2 = None
        
    def analyze_tracks(self, track1_path: str, track2_path: str) -> Dict:
        """
        Perform comprehensive analysis of two tracks
        Returns: Dictionary with all analysis results
        """
        print("🔍 Analyzing Track 1...")
        self.analyzer1 = AudioAnalyzer(track1_path)
        features1 = self.analyzer1.get_audio_features()
        
        print("🔍 Analyzing Track 2...")
        self.analyzer2 = AudioAnalyzer(track2_path)
        features2 = self.analyzer2.get_audio_features()
        
        # Analyze compatibility
        print("🔗 Analyzing compatibility...")
        compatibility = analyze_track_compatibility(track1_path, track2_path)
        
        # Get mix suggestions
        print("🎯 Generating mix suggestions...")
        mix_suggestions = suggest_mix_points(track1_path, track2_path)
        
        return {
            'track1': features1,
            'track2': features2,
            'compatibility': compatibility,
            'mix_suggestions': mix_suggestions
        }
    
    def print_analysis_report(self, analysis_results: Dict):
        """Print comprehensive analysis report"""
        track1 = analysis_results['track1']
        track2 = analysis_results['track2']
        compatibility = analysis_results['compatibility']
        mix_suggestions = analysis_results['mix_suggestions']
        
        print("\n" + "="*60)
        print("🎵 ENHANCED DYNAMIX ANALYSIS REPORT")
        print("="*60)
        
        # Track Information
        print("\n📊 TRACK INFORMATION:")
        print("-" * 40)
        print(f"Track 1: {os.path.basename(self.analyzer1.file_path)}")
        print(f"  • Duration: {track1['duration']:.1f}s")
        print(f"  • BPM: {track1['bpm']:.1f} (confidence: {track1['bpm_confidence']:.2f})")
        print(f"  • Key: {track1['key']} (confidence: {track1['key_confidence']:.2f})")
        print(f"  • Avg Energy: {track1['avg_energy']:.4f}")
        print(f"  • Sections: {track1['section_count']}")
        print(f"  • Drops: {track1['drop_count']}")
        
        print(f"\nTrack 2: {os.path.basename(self.analyzer2.file_path)}")
        print(f"  • Duration: {track2['duration']:.1f}s")
        print(f"  • BPM: {track2['bpm']:.1f} (confidence: {track2['bpm_confidence']:.2f})")
        print(f"  • Key: {track2['key']} (confidence: {track2['key_confidence']:.2f})")
        print(f"  • Avg Energy: {track2['avg_energy']:.4f}")
        print(f"  • Sections: {track2['section_count']}")
        print(f"  • Drops: {track2['drop_count']}")
        
        # Compatibility Analysis
        print("\n🔗 COMPATIBILITY ANALYSIS:")
        print("-" * 40)
        print(f"BPM Compatibility: {compatibility['bpm_compatibility']:.1f}%")
        print(f"  • BPM Difference: {compatibility['bpm_difference']:.1f}")
        print(f"Key Compatibility: {compatibility['key_compatibility']:.1f}%")
        print(f"Energy Compatibility: {compatibility['energy_compatibility']:.1f}%")
        print(f"Overall Score: {compatibility['overall_score']:.1f}%")
        
        # Mix Recommendations
        print("\n🎯 MIX RECOMMENDATIONS:")
        print("-" * 40)
        
        if compatibility['overall_score'] >= 80:
            print("✅ EXCELLENT compatibility! These tracks should mix very well.")
        elif compatibility['overall_score'] >= 60:
            print("✅ GOOD compatibility! These tracks should mix well with some adjustments.")
        elif compatibility['overall_score'] >= 40:
            print("⚠️  MODERATE compatibility. Consider BPM matching or key adjustment.")
        else:
            print("❌ LOW compatibility. These tracks may be challenging to mix.")
        
        print(f"\nRecommended Mix Duration: {mix_suggestions['recommended_mix_duration']:.1f} seconds")
        
        if mix_suggestions['bpm_sync_required']:
            print("⚠️  BPM synchronization required for smooth transition")
        
        # Exit/Entry Points
        if mix_suggestions['track1_exit_points']:
            print(f"\nTrack 1 Exit Points (seconds): {[f'{t:.1f}s' for t in mix_suggestions['track1_exit_points'][:3]]}")
        
        if mix_suggestions['track2_entry_points']:
            print(f"Track 2 Entry Points (seconds): {[f'{t:.1f}s' for t in mix_suggestions['track2_entry_points'][:3]]}")
        
        # Detailed Mixing Strategy
        print("\n🎚️  MIXING STRATEGY:")
        print("-" * 40)
        
        if compatibility['bpm_difference'] > 10:
            print("• Use pitch shifting to match BPMs")
            print("• Consider using sync features on your DJ equipment")
        elif compatibility['bpm_difference'] > 5:
            print("• Use tempo adjustment for smooth transition")
            print("• Monitor BPM drift during the mix")
        else:
            print("• BPMs are well-matched for natural mixing")
        
        if compatibility['key_compatibility'] < 70:
            print("• Consider harmonic mixing techniques")
            print("• Use key detection to find compatible sections")
        
        # Energy Management
        energy_diff = abs(track1['avg_energy'] - track2['avg_energy'])
        if energy_diff > 0.1:
            print("• Use EQ to balance energy levels")
            print("• Consider using filters during transition")
        
        print("\n" + "="*60)
    
    def create_enhanced_visualization(self, analysis_results: Dict):
        """Create comprehensive visualization"""
        track1 = analysis_results['track1']
        track2 = analysis_results['track2']
        
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle('Enhanced DynaMix Analysis', fontsize=16, fontweight='bold')
        
        # Energy profiles
        times1, rms1 = self.analyzer1.analyze_energy_profile()
        times2, rms2 = self.analyzer2.analyze_energy_profile()
        
        axes[0, 0].plot(times1, rms1, label='Track 1', color='blue', alpha=0.7)
        axes[0, 0].set_title('Track 1 Energy Profile')
        axes[0, 0].set_ylabel('RMS Energy')
        axes[0, 0].legend()
        
        axes[0, 1].plot(times2, rms2, label='Track 2', color='red', alpha=0.7)
        axes[0, 1].set_title('Track 2 Energy Profile')
        axes[0, 1].set_ylabel('RMS Energy')
        axes[0, 1].legend()
        
        # Beat grids
        beat_times1, beat_strengths1 = self.analyzer1.analyze_beat_grid()
        beat_times2, beat_strengths2 = self.analyzer2.analyze_beat_grid()
        
        axes[1, 0].vlines(beat_times1, 0, beat_strengths1, alpha=0.6, color='blue', label='Beats')
        axes[1, 0].set_title('Track 1 Beat Grid')
        axes[1, 0].set_ylabel('Beat Strength')
        axes[1, 0].legend()
        
        axes[1, 1].vlines(beat_times2, 0, beat_strengths2, alpha=0.6, color='red', label='Beats')
        axes[1, 1].set_title('Track 2 Beat Grid')
        axes[1, 1].set_ylabel('Beat Strength')
        axes[1, 1].legend()
        
        # Compatibility radar chart
        compatibility = analysis_results['compatibility']
        categories = ['BPM', 'Key', 'Energy']
        values = [
            compatibility['bpm_compatibility'],
            compatibility['key_compatibility'],
            compatibility['energy_compatibility']
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Complete the circle
        angles += angles[:1]
        
        axes[2, 0].plot(angles, values, 'o-', linewidth=2, label='Compatibility')
        axes[2, 0].fill(angles, values, alpha=0.25)
        axes[2, 0].set_xticks(angles[:-1])
        axes[2, 0].set_xticklabels(categories)
        axes[2, 0].set_ylim(0, 100)
        axes[2, 0].set_title('Compatibility Radar')
        axes[2, 0].grid(True)
        
        # Feature comparison
        features = ['BPM', 'Duration', 'Avg Energy', 'Sections']
        track1_values = [track1['bpm'], track1['duration']/60, track1['avg_energy'], track1['section_count']]
        track2_values = [track2['bpm'], track2['duration']/60, track2['avg_energy'], track2['section_count']]
        
        x = np.arange(len(features))
        width = 0.35
        
        axes[2, 1].bar(x - width/2, track1_values, width, label='Track 1', alpha=0.7)
        axes[2, 1].bar(x + width/2, track2_values, width, label='Track 2', alpha=0.7)
        axes[2, 1].set_title('Feature Comparison')
        axes[2, 1].set_xticks(x)
        axes[2, 1].set_xticklabels(features)
        axes[2, 1].legend()
        
        plt.tight_layout()
        plt.show()

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced DynaMix - Advanced Audio Transition Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mix_enhanced.py track1.mp3 track2.mp3
  python mix_enhanced.py track1.mp3 track2.mp3 --visualize
  python mix_enhanced.py --playlist /path/to/music/folder
        """
    )
    
    parser.add_argument("track1", nargs='?', help="First MP3 file path")
    parser.add_argument("track2", nargs='?', help="Second MP3 file path")
    parser.add_argument("--visualize", action="store_true", help="Show enhanced visualizations")
    parser.add_argument("--playlist", type=str, help="Analyze entire playlist directory")
    parser.add_argument("--export", type=str, help="Export analysis to file (JSON/CSV)")
    parser.add_argument("--set-duration", type=int, default=60, help="Set duration in minutes for playlist analysis")
    
    args = parser.parse_args()
    
    if args.playlist:
        # Playlist analysis mode
        print("🎵 Playlist Analysis Mode")
        print("=" * 40)
        
        if not os.path.exists(args.playlist):
            print(f"❌ Directory not found: {args.playlist}")
            sys.exit(1)
        
        manager = PlaylistManager(args.playlist)
        audio_files = manager.scan_directory()
        
        if not audio_files:
            print(f"❌ No audio files found in {args.playlist}")
            sys.exit(1)
        
        print(f"📁 Found {len(audio_files)} audio files")
        
        # Analyze playlist
        df = manager.analyze_playlist(audio_files)
        print(f"\n✅ Analyzed {len(df)} tracks")
        
        # Create set list
        set_list = manager.create_set_list(duration_minutes=args.set_duration)
        print(f"\n🎯 Created {len(set_list)} track set ({args.set_duration} minutes)")
        
        # Print set list
        print("\n📋 RECOMMENDED SET LIST:")
        print("-" * 40)
        total_duration = 0
        for i, track in enumerate(set_list, 1):
            duration_min = track['duration'] / 60
            total_duration += track['duration']
            print(f"{i:2d}. {track['filename']}")
            print(f"    BPM: {track['bpm']:.1f} | Key: {track['key']} | Duration: {duration_min:.1f}min")
        
        print(f"\nTotal Duration: {total_duration/60:.1f} minutes")
        
        # Export if requested
        if args.export:
            manager.export_playlist(args.export)
        
        # Show playlist analysis
        if args.visualize:
            manager.plot_playlist_analysis()
    
    elif args.track1 and args.track2:
        # Two-track analysis mode
        if not os.path.exists(args.track1):
            print(f"❌ Track 1 not found: {args.track1}")
            sys.exit(1)
        
        if not os.path.exists(args.track2):
            print(f"❌ Track 2 not found: {args.track2}")
            sys.exit(1)
        
        analyzer = EnhancedMixAnalyzer()
        analysis_results = analyzer.analyze_tracks(args.track1, args.track2)
        
        # Print report
        analyzer.print_analysis_report(analysis_results)
        
        # Show visualizations
        if args.visualize:
            analyzer.create_enhanced_visualization(analysis_results)
        
        # Export if requested
        if args.export:
            import json
            with open(args.export, 'w') as f:
                json.dump(analysis_results, f, indent=2, default=str)
            print(f"\n📄 Analysis exported to {args.export}")
    
    else:
        parser.print_help()
        print("\n❌ Please provide either two track files or a playlist directory")

if __name__ == "__main__":
    main() 