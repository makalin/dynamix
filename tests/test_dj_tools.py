#!/usr/bin/env python3
"""
Unit tests for dj_tools module
Tests the DJTools class and DJ performance analysis functions
"""

import unittest
import tempfile
import os
import sys
import numpy as np
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dj_tools import DJTools, batch_analyze_tracks

class TestDJTools(unittest.TestCase):
    """Test cases for DJTools class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_audio_data = np.random.rand(44100 * 10)  # 10 seconds of random audio
        self.sample_rate = 44100
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_dj_tools_initialization(self):
        """Test DJTools initialization"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                dj_tools = DJTools("test_file.mp3")
                
                self.assertEqual(dj_tools.file_path, "test_file.mp3")
                self.assertIsNotNone(dj_tools.analyzer)
    
    def test_detect_cue_points(self):
        """Test cue point detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock onset detection
                with patch('librosa.onset.onset_strength') as mock_onset_strength:
                    mock_onset_strength.return_value = np.random.rand(100)
                    
                    with patch('librosa.onset.onset_detect') as mock_onset_detect:
                        mock_onset_detect.return_value = np.array([10, 20, 30, 40, 50])
                        
                        with patch('librosa.frames_to_time') as mock_frames_to_time:
                            mock_frames_to_time.return_value = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
                            
                            with patch.object(DJTools, 'analyze_beat_grid') as mock_beat_grid:
                                mock_beat_grid.return_value = (np.array([0, 0.5, 1.0]), np.array([0.8, 0.9, 0.7]))
                                
                                dj_tools = DJTools("test_file.mp3")
                                cue_points = dj_tools.detect_cue_points(sensitivity=0.7)
                                
                                self.assertIsInstance(cue_points, list)
                                self.assertGreater(len(cue_points), 0)
                                
                                # Check cue point structure
                                for cue in cue_points:
                                    self.assertIn('time', cue)
                                    self.assertIn('type', cue)
                                    self.assertIn('strength', cue)
                                    self.assertIn('nearest_beat', cue)
                                    self.assertIn('beat_distance', cue)
                                    
                                    self.assertIsInstance(cue['time'], float)
                                    self.assertIsInstance(cue['type'], str)
                                    self.assertIsInstance(cue['strength'], float)
                                    self.assertIsInstance(cue['nearest_beat'], float)
                                    self.assertIsInstance(cue['beat_distance'], float)
    
    def test_suggest_loops(self):
        """Test loop suggestions"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock beat grid
                with patch.object(DJTools, 'analyze_beat_grid') as mock_beat_grid:
                    mock_beat_grid.return_value = (np.array([0, 0.5, 1.0, 1.5, 2.0]), np.array([0.8, 0.9, 0.7, 0.8, 0.9]))
                    
                    # Mock sections
                    with patch.object(DJTools, 'detect_sections') as mock_sections:
                        mock_sections.return_value = [("Intro", 0, 2), ("Verse", 2, 5), ("Chorus", 5, 8)]
                        
                        # Mock energy profile
                        with patch.object(DJTools, 'analyze_energy_profile') as mock_energy:
                            mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                            
                            dj_tools = DJTools("test_file.mp3")
                            loops = dj_tools.suggest_loops(min_duration=4.0, max_duration=16.0)
                            
                            self.assertIsInstance(loops, list)
                            
                            # Check loop structure
                            for loop in loops:
                                self.assertIn('start_time', loop)
                                self.assertIn('end_time', loop)
                                self.assertIn('duration', loop)
                                self.assertIn('type', loop)
                                self.assertIn('energy_stability', loop)
                                self.assertIn('avg_energy', loop)
                                
                                self.assertIsInstance(loop['start_time'], float)
                                self.assertIsInstance(loop['end_time'], float)
                                self.assertIsInstance(loop['duration'], float)
                                self.assertIsInstance(loop['type'], str)
                                self.assertIsInstance(loop['energy_stability'], float)
                                self.assertIsInstance(loop['avg_energy'], float)
                                
                                # Check duration constraints
                                self.assertGreaterEqual(loop['duration'], 4.0)
                                self.assertLessEqual(loop['duration'], 16.0)
    
    def test_analyze_performance_zones(self):
        """Test performance zone analysis"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock sections
                with patch.object(DJTools, 'detect_sections') as mock_sections:
                    mock_sections.return_value = [
                        ("Intro", 0, 2),
                        ("Build", 2, 4),
                        ("Drop", 4, 6),
                        ("Breakdown", 6, 8),
                        ("Outro", 8, 10)
                    ]
                    
                    # Mock energy profile
                    with patch.object(DJTools, 'analyze_energy_profile') as mock_energy:
                        mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                        
                        dj_tools = DJTools("test_file.mp3")
                        zones = dj_tools.analyze_performance_zones()
                        
                        self.assertIsInstance(zones, dict)
                        
                        # Check required zones
                        required_zones = ['intro', 'build', 'drop', 'breakdown', 'outro']
                        for zone in required_zones:
                            self.assertIn(zone, zones)
                            
                            zone_data = zones[zone]
                            self.assertIn('start', zone_data)
                            self.assertIn('end', zone_data)
                            self.assertIn('energy', zone_data)
                            self.assertIn('complexity', zone_data)
                            
                            self.assertIsInstance(zone_data['start'], float)
                            self.assertIsInstance(zone_data['end'], float)
                            self.assertIsInstance(zone_data['energy'], float)
                            self.assertIsInstance(zone_data['complexity'], float)
    
    def test_generate_dj_notes(self):
        """Test DJ notes generation"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock all analysis methods
                with patch.object(DJTools, 'detect_cue_points') as mock_cue_points:
                    mock_cue_points.return_value = [
                        {'time': 1.0, 'type': 'Beat Sync', 'strength': 0.8},
                        {'time': 3.0, 'type': 'Strong Onset', 'strength': 0.9}
                    ]
                    
                    with patch.object(DJTools, 'suggest_loops') as mock_loops:
                        mock_loops.return_value = [
                            {'start_time': 2.0, 'end_time': 6.0, 'duration': 4.0, 'type': 'Section: Verse', 'energy_stability': 0.8, 'avg_energy': 0.6}
                        ]
                        
                        with patch.object(DJTools, 'analyze_performance_zones') as mock_zones:
                            mock_zones.return_value = {
                                'intro': {'start': 0, 'end': 2, 'energy': 0.3, 'complexity': 0.2},
                                'build': {'start': 2, 'end': 4, 'energy': 0.5, 'complexity': 0.4},
                                'drop': {'start': 4, 'end': 6, 'energy': 0.8, 'complexity': 0.6},
                                'breakdown': {'start': 6, 'end': 8, 'energy': 0.4, 'complexity': 0.3},
                                'outro': {'start': 8, 'end': 10, 'energy': 0.2, 'complexity': 0.1}
                            }
                            
                            with patch.object(DJTools, '_get_compatible_keys') as mock_keys:
                                mock_keys.return_value = 'F, G, Am'
                                
                                with patch.object(DJTools, '_find_energy_peaks') as mock_peaks:
                                    mock_peaks.return_value = 5.0
                                    
                                    with patch.object(DJTools, '_find_mix_points') as mock_mix:
                                        mock_mix.return_value = [3.0, 7.0]
                                        
                                        # Mock analyzer features
                                        with patch.object(DJTools, 'analyzer') as mock_analyzer:
                                            mock_analyzer.get_audio_features.return_value = {
                                                'duration': 240.0,
                                                'bpm': 128.0,
                                                'key': 'C major',
                                                'avg_energy': 0.5
                                            }
                                            
                                            dj_tools = DJTools("test_file.mp3")
                                            notes = dj_tools.generate_dj_notes()
                                            
                                            self.assertIsInstance(notes, str)
                                            self.assertGreater(len(notes), 0)
                                            
                                            # Check for key information in notes
                                            self.assertIn('BPM', notes)
                                            self.assertIn('Key', notes)
                                            self.assertIn('Cue Points', notes)
                                            self.assertIn('Loop Suggestions', notes)
                                            self.assertIn('Performance Zones', notes)
    
    def test_export_dj_notes(self):
        """Test DJ notes export"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock generate_dj_notes
                with patch.object(DJTools, 'generate_dj_notes') as mock_generate:
                    mock_generate.return_value = "Mock DJ notes content"
                    
                    dj_tools = DJTools("test_file.mp3")
                    output_file = os.path.join(self.temp_dir, "dj_notes.txt")
                    
                    dj_tools.export_dj_notes(output_file)
                    
                    # Check file exists
                    self.assertTrue(os.path.exists(output_file))
                    
                    # Check file content
                    with open(output_file, 'r') as f:
                        content = f.read()
                    
                    self.assertEqual(content, "Mock DJ notes content")
    
    def test_create_performance_visualization(self):
        """Test performance visualization creation"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock all analysis methods
                with patch.object(DJTools, 'analyze_energy_profile') as mock_energy:
                    mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                    
                    with patch.object(DJTools, 'analyze_performance_zones') as mock_zones:
                        mock_zones.return_value = {
                            'intro': {'start': 0, 'end': 2, 'energy': 0.3, 'complexity': 0.2},
                            'build': {'start': 2, 'end': 4, 'energy': 0.5, 'complexity': 0.4},
                            'drop': {'start': 4, 'end': 6, 'energy': 0.8, 'complexity': 0.6},
                            'breakdown': {'start': 6, 'end': 8, 'energy': 0.4, 'complexity': 0.3},
                            'outro': {'start': 8, 'end': 10, 'energy': 0.2, 'complexity': 0.1}
                        }
                        
                        with patch.object(DJTools, 'detect_cue_points') as mock_cue_points:
                            mock_cue_points.return_value = [
                                {'time': 1.0, 'strength': 0.8},
                                {'time': 3.0, 'strength': 0.9},
                                {'time': 5.0, 'strength': 0.7}
                            ]
                            
                            with patch.object(DJTools, 'suggest_loops') as mock_loops:
                                mock_loops.return_value = [
                                    {'start_time': 2.0, 'end_time': 6.0, 'type': 'Section: Verse'},
                                    {'start_time': 4.0, 'end_time': 8.0, 'type': 'Beat Loop: 8 beats'}
                                ]
                                
                                # Mock matplotlib
                                with patch('matplotlib.pyplot.show') as mock_show:
                                    dj_tools = DJTools("test_file.mp3")
                                    dj_tools.create_performance_visualization()
                                    
                                    # Check that show was called
                                    mock_show.assert_called_once()

class TestBatchAnalysis(unittest.TestCase):
    """Test cases for batch analysis functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create mock audio files
        self.mock_audio_files = [
            os.path.join(self.temp_dir, "track1.mp3"),
            os.path.join(self.temp_dir, "track2.wav"),
            os.path.join(self.temp_dir, "track3.flac"),
        ]
        
        for file_path in self.mock_audio_files:
            with open(file_path, 'w') as f:
                f.write("mock audio content")
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_batch_analyze_tracks(self):
        """Test batch analysis of tracks"""
        # Mock DJTools
        mock_dj_tools = Mock()
        mock_dj_tools.export_dj_notes = Mock()
        
        with patch('dj_tools.DJTools') as mock_dj_tools_class:
            mock_dj_tools_class.return_value = mock_dj_tools
            
            # Run batch analysis
            batch_analyze_tracks(self.temp_dir, self.temp_dir)
            
            # Check that DJTools was called for each audio file
            self.assertEqual(mock_dj_tools_class.call_count, 3)
            
            # Check that export_dj_notes was called for each file
            self.assertEqual(mock_dj_tools.export_dj_notes.call_count, 3)
    
    def test_batch_analyze_tracks_with_error(self):
        """Test batch analysis with error handling"""
        # Mock DJTools to raise an exception
        with patch('dj_tools.DJTools') as mock_dj_tools_class:
            mock_dj_tools_class.side_effect = Exception("Test error")
            
            # Run batch analysis - should not raise exception
            try:
                batch_analyze_tracks(self.temp_dir, self.temp_dir)
            except Exception as e:
                self.fail(f"Batch analysis should handle errors gracefully: {e}")
    
    def test_batch_analyze_empty_directory(self):
        """Test batch analysis of empty directory"""
        empty_dir = tempfile.mkdtemp()
        try:
            # Run batch analysis on empty directory
            batch_analyze_tracks(empty_dir, empty_dir)
            # Should complete without errors
        finally:
            import shutil
            shutil.rmtree(empty_dir)

class TestHelperMethods(unittest.TestCase):
    """Test cases for helper methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_audio_data = np.random.rand(44100 * 10)
        self.sample_rate = 44100
    
    def test_get_compatible_keys(self):
        """Test compatible keys lookup"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                dj_tools = DJTools("test_file.mp3")
                
                # Test known keys
                compatible = dj_tools._get_compatible_keys("C major")
                self.assertIsInstance(compatible, str)
                self.assertIn("F", compatible)
                self.assertIn("G", compatible)
                
                compatible = dj_tools._get_compatible_keys("A minor")
                self.assertIsInstance(compatible, str)
                self.assertIn("D", compatible)
                self.assertIn("E", compatible)
                
                # Test unknown key
                compatible = dj_tools._get_compatible_keys("Unknown key")
                self.assertEqual(compatible, "Check music theory")
    
    def test_find_energy_peaks(self):
        """Test energy peak detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock energy profile
                with patch.object(DJTools, 'analyze_energy_profile') as mock_energy:
                    mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                    
                    dj_tools = DJTools("test_file.mp3")
                    peak_time = dj_tools._find_energy_peaks()
                    
                    self.assertIsInstance(peak_time, float)
                    self.assertGreaterEqual(peak_time, 0)
                    self.assertLessEqual(peak_time, 10.0)
    
    def test_find_mix_points(self):
        """Test mix point detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock energy profile
                with patch.object(DJTools, 'analyze_energy_profile') as mock_energy:
                    mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                    
                    dj_tools = DJTools("test_file.mp3")
                    mix_points = dj_tools._find_mix_points()
                    
                    self.assertIsInstance(mix_points, list)
                    
                    for point in mix_points:
                        self.assertIsInstance(point, float)
                        self.assertGreaterEqual(point, 0)

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def test_invalid_file_path(self):
        """Test handling of invalid file paths"""
        with self.assertRaises(Exception):
            DJTools("nonexistent_file.mp3")
    
    def test_empty_audio_file(self):
        """Test handling of empty audio files"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (np.array([]), 44100)
            
            with self.assertRaises(Exception):
                dj_tools = DJTools("empty_file.mp3")
                dj_tools.detect_cue_points()

if __name__ == '__main__':
    unittest.main() 