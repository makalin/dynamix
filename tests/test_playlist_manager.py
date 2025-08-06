#!/usr/bin/env python3
"""
Unit tests for playlist_manager module
Tests the PlaylistManager class and playlist analysis functions
"""

import unittest
import tempfile
import os
import sys
import json
import pandas as pd
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playlist_manager import PlaylistManager, create_energy_based_set

class TestPlaylistManager(unittest.TestCase):
    """Test cases for PlaylistManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = PlaylistManager(self.temp_dir)
        
        # Create mock audio files
        self.mock_audio_files = [
            os.path.join(self.temp_dir, "track1.mp3"),
            os.path.join(self.temp_dir, "track2.wav"),
            os.path.join(self.temp_dir, "track3.flac"),
            os.path.join(self.temp_dir, "subfolder", "track4.m4a"),
            os.path.join(self.temp_dir, "document.txt"),  # Non-audio file
        ]
        
        # Create directories and files
        os.makedirs(os.path.join(self.temp_dir, "subfolder"), exist_ok=True)
        for file_path in self.mock_audio_files:
            if file_path.endswith(('.mp3', '.wav', '.flac', '.m4a')):
                with open(file_path, 'w') as f:
                    f.write("mock audio content")
            elif file_path.endswith('.txt'):
                with open(file_path, 'w') as f:
                    f.write("document content")
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scan_directory(self):
        """Test directory scanning for audio files"""
        audio_files = self.manager.scan_directory()
        
        # Should find 4 audio files
        self.assertEqual(len(audio_files), 4)
        
        # Check that all found files are audio files
        audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'}
        for file_path in audio_files:
            ext = os.path.splitext(file_path)[1].lower()
            self.assertIn(ext, audio_extensions)
        
        # Check that non-audio files are not included
        txt_files = [f for f in audio_files if f.endswith('.txt')]
        self.assertEqual(len(txt_files), 0)
    
    def test_scan_empty_directory(self):
        """Test scanning empty directory"""
        empty_dir = tempfile.mkdtemp()
        try:
            manager = PlaylistManager(empty_dir)
            audio_files = manager.scan_directory()
            self.assertEqual(len(audio_files), 0)
        finally:
            import shutil
            shutil.rmtree(empty_dir)
    
    def test_scan_nonexistent_directory(self):
        """Test scanning nonexistent directory"""
        manager = PlaylistManager("/nonexistent/path")
        audio_files = manager.scan_directory()
        self.assertEqual(len(audio_files), 0)
    
    def test_analyze_playlist(self):
        """Test playlist analysis"""
        # Mock AudioAnalyzer
        mock_analyzer = Mock()
        mock_analyzer.get_audio_features.return_value = {
            'duration': 240.0,
            'bpm': 128.0,
            'bpm_confidence': 0.8,
            'key': 'C major',
            'key_confidence': 0.7,
            'avg_energy': 0.5,
            'max_energy': 0.8,
            'energy_std': 0.2,
            'beat_count': 480,
            'section_count': 5,
            'drop_count': 2
        }
        
        with patch('playlist_manager.AudioAnalyzer') as mock_audio_analyzer:
            mock_audio_analyzer.return_value = mock_analyzer
            
            # Get audio files
            audio_files = self.manager.scan_directory()
            
            # Analyze playlist
            df = self.manager.analyze_playlist(audio_files)
            
            # Check DataFrame structure
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(len(df), len(audio_files))
            
            # Check required columns
            required_columns = [
                'file_path', 'filename', 'duration', 'bpm', 'bpm_confidence',
                'key', 'key_confidence', 'avg_energy', 'max_energy', 'energy_std',
                'beat_count', 'section_count', 'drop_count'
            ]
            
            for col in required_columns:
                self.assertIn(col, df.columns)
            
            # Check data types
            self.assertIsInstance(df['duration'].iloc[0], float)
            self.assertIsInstance(df['bpm'].iloc[0], float)
            self.assertIsInstance(df['key'].iloc[0], str)
    
    def test_suggest_playlist_order_build(self):
        """Test playlist order suggestion with build energy curve"""
        # Create mock tracks
        self.manager.tracks = [
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            },
            {
                'file_path': 'track2.mp3',
                'filename': 'track2.mp3',
                'duration': 245.0,
                'bpm': 128.0,
                'key': 'F major',
                'avg_energy': 0.6
            },
            {
                'file_path': 'track3.mp3',
                'filename': 'track3.mp3',
                'duration': 242.0,
                'bpm': 130.0,
                'key': 'G major',
                'avg_energy': 0.8
            }
        ]
        
        # Test build energy curve
        ordered_tracks = self.manager.suggest_playlist_order(energy_curve='build')
        
        self.assertEqual(len(ordered_tracks), 3)
        
        # Check that energy increases (build curve)
        energies = [track['avg_energy'] for track in ordered_tracks]
        self.assertEqual(energies, sorted(energies))
    
    def test_suggest_playlist_order_wave(self):
        """Test playlist order suggestion with wave energy curve"""
        # Create mock tracks
        self.manager.tracks = [
            {'filename': 'track1.mp3', 'avg_energy': 0.3},
            {'filename': 'track2.mp3', 'avg_energy': 0.8},
            {'filename': 'track3.mp3', 'avg_energy': 0.2},
            {'filename': 'track4.mp3', 'avg_energy': 0.9},
        ]
        
        # Test wave energy curve
        ordered_tracks = self.manager.suggest_playlist_order(energy_curve='wave')
        
        self.assertEqual(len(ordered_tracks), 4)
        
        # Check alternating pattern (high-low-high-low)
        energies = [track['avg_energy'] for track in ordered_tracks]
        self.assertGreater(energies[1], energies[0])  # Second > First
        self.assertLess(energies[2], energies[1])     # Third < Second
        self.assertGreater(energies[3], energies[2])  # Fourth > Third
    
    def test_create_set_list(self):
        """Test set list creation"""
        # Create mock tracks
        self.manager.tracks = [
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            },
            {
                'file_path': 'track2.mp3',
                'filename': 'track2.mp3',
                'duration': 245.0,
                'bpm': 128.0,
                'key': 'F major',
                'avg_energy': 0.6
            },
            {
                'file_path': 'track3.mp3',
                'filename': 'track3.mp3',
                'duration': 242.0,
                'bpm': 130.0,
                'key': 'G major',
                'avg_energy': 0.8
            }
        ]
        
        # Create 10-minute set (600 seconds)
        set_list = self.manager.create_set_list(duration_minutes=10)
        
        self.assertIsInstance(set_list, list)
        
        # Check total duration doesn't exceed target
        total_duration = sum(track['duration'] for track in set_list)
        self.assertLessEqual(total_duration, 600)
        
        # Check that tracks are ordered by energy (build curve)
        if len(set_list) > 1:
            energies = [track['avg_energy'] for track in set_list]
            self.assertEqual(energies, sorted(energies))
    
    def test_export_playlist_json(self):
        """Test playlist export to JSON"""
        # Create mock tracks
        self.manager.tracks = [
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            }
        ]
        
        # Export to JSON
        output_file = os.path.join(self.temp_dir, "playlist.json")
        self.manager.export_playlist(output_file, format='json')
        
        # Check file exists
        self.assertTrue(os.path.exists(output_file))
        
        # Check JSON content
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['filename'], 'track1.mp3')
    
    def test_export_playlist_csv(self):
        """Test playlist export to CSV"""
        # Create mock tracks
        self.manager.tracks = [
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            }
        ]
        
        # Export to CSV
        output_file = os.path.join(self.temp_dir, "playlist.csv")
        self.manager.export_playlist(output_file, format='csv')
        
        # Check file exists
        self.assertTrue(os.path.exists(output_file))
        
        # Check CSV content
        df = pd.read_csv(output_file)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['filename'], 'track1.mp3')
    
    def test_export_invalid_format(self):
        """Test export with invalid format"""
        self.manager.tracks = [{'filename': 'track1.mp3'}]
        
        with self.assertRaises(ValueError):
            self.manager.export_playlist("output.txt", format='invalid')
    
    def test_load_playlist_json(self):
        """Test loading playlist from JSON"""
        # Create test JSON file
        test_data = [
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            }
        ]
        
        json_file = os.path.join(self.temp_dir, "test_playlist.json")
        with open(json_file, 'w') as f:
            json.dump(test_data, f)
        
        # Load playlist
        self.manager.load_playlist(json_file)
        
        self.assertEqual(len(self.manager.tracks), 1)
        self.assertEqual(self.manager.tracks[0]['filename'], 'track1.mp3')
    
    def test_load_playlist_csv(self):
        """Test loading playlist from CSV"""
        # Create test CSV file
        test_data = pd.DataFrame([
            {
                'file_path': 'track1.mp3',
                'filename': 'track1.mp3',
                'duration': 240.0,
                'bpm': 125.0,
                'key': 'C major',
                'avg_energy': 0.3
            }
        ])
        
        csv_file = os.path.join(self.temp_dir, "test_playlist.csv")
        test_data.to_csv(csv_file, index=False)
        
        # Load playlist
        self.manager.load_playlist(csv_file)
        
        self.assertEqual(len(self.manager.tracks), 1)
        self.assertEqual(self.manager.tracks[0]['filename'], 'track1.mp3')
    
    def test_load_invalid_file(self):
        """Test loading invalid file format"""
        with self.assertRaises(ValueError):
            self.manager.load_playlist("invalid.txt")

class TestEnergyBasedSet(unittest.TestCase):
    """Test cases for energy-based set creation"""
    
    def test_create_energy_based_set_peak_middle(self):
        """Test energy-based set creation with peak_middle profile"""
        # Create mock playlist manager
        manager = Mock()
        manager.tracks = [
            {'duration': 240.0, 'avg_energy': 0.3},
            {'duration': 245.0, 'avg_energy': 0.6},
            {'duration': 242.0, 'avg_energy': 0.8},
            {'duration': 238.0, 'avg_energy': 0.4},
            {'duration': 246.0, 'avg_energy': 0.9},
        ]
        
        # Create set with peak_middle profile
        set_list = create_energy_based_set(manager, target_duration=10, energy_profile='peak_middle')
        
        self.assertIsInstance(set_list, list)
        
        # Check total duration doesn't exceed target
        total_duration = sum(track['duration'] for track in set_list)
        self.assertLessEqual(total_duration, 600)  # 10 minutes = 600 seconds
    
    def test_create_energy_based_set_build_up(self):
        """Test energy-based set creation with build_up profile"""
        manager = Mock()
        manager.tracks = [
            {'duration': 240.0, 'avg_energy': 0.3},
            {'duration': 245.0, 'avg_energy': 0.6},
            {'duration': 242.0, 'avg_energy': 0.8},
        ]
        
        set_list = create_energy_based_set(manager, target_duration=10, energy_profile='build_up')
        
        self.assertIsInstance(set_list, list)
        
        # Check that energy increases (build_up profile)
        if len(set_list) > 1:
            energies = [track['avg_energy'] for track in set_list]
            self.assertEqual(energies, sorted(energies))
    
    def test_create_energy_based_set_wave(self):
        """Test energy-based set creation with wave profile"""
        manager = Mock()
        manager.tracks = [
            {'duration': 240.0, 'avg_energy': 0.3},
            {'duration': 245.0, 'avg_energy': 0.8},
            {'duration': 242.0, 'avg_energy': 0.2},
            {'duration': 238.0, 'avg_energy': 0.9},
        ]
        
        set_list = create_energy_based_set(manager, target_duration=10, energy_profile='wave')
        
        self.assertIsInstance(set_list, list)
        
        # Check alternating pattern
        if len(set_list) > 1:
            energies = [track['avg_energy'] for track in set_list]
            self.assertGreater(energies[1], energies[0])  # Second > First
            if len(energies) > 2:
                self.assertLess(energies[2], energies[1])  # Third < Second

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def test_analyze_playlist_without_tracks(self):
        """Test analyzing playlist without tracks"""
        manager = PlaylistManager()
        
        with self.assertRaises(ValueError):
            manager.suggest_playlist_order()
    
    def test_export_playlist_without_tracks(self):
        """Test exporting playlist without tracks"""
        manager = PlaylistManager()
        
        with self.assertRaises(ValueError):
            manager.export_playlist("output.json")
    
    def test_create_set_list_without_tracks(self):
        """Test creating set list without tracks"""
        manager = PlaylistManager()
        
        with self.assertRaises(ValueError):
            manager.create_set_list()

if __name__ == '__main__':
    unittest.main() 