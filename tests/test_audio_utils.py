#!/usr/bin/env python3
"""
Unit tests for audio_utils module
Tests the AudioAnalyzer class and utility functions
"""

import unittest
import numpy as np
import tempfile
import os
import sys
from unittest.mock import Mock, patch

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio_utils import AudioAnalyzer, analyze_track_compatibility, suggest_mix_points

class TestAudioAnalyzer(unittest.TestCase):
    """Test cases for AudioAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a mock audio file for testing
        self.mock_audio_data = np.random.rand(44100 * 10)  # 10 seconds of random audio
        self.sample_rate = 44100
        
    def test_audio_analyzer_initialization(self):
        """Test AudioAnalyzer initialization"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            # Mock librosa.get_duration
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                analyzer = AudioAnalyzer("test_file.mp3")
                
                self.assertEqual(analyzer.file_path, "test_file.mp3")
                self.assertEqual(analyzer.sr, self.sample_rate)
                self.assertEqual(analyzer.duration, 10.0)
    
    def test_detect_bpm(self):
        """Test BPM detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock beat detection functions
                with patch('librosa.beat.beat_track') as mock_beat_track:
                    mock_beat_track.return_value = (128.0, np.array([0, 512, 1024]))
                    
                    with patch('librosa.onset.onset_strength') as mock_onset_strength:
                        mock_onset_strength.return_value = np.random.rand(100)
                        
                        with patch('librosa.beat.tempo') as mock_tempo:
                            mock_tempo.return_value = np.array([130.0])
                            
                            analyzer = AudioAnalyzer("test_file.mp3")
                            bpm, confidence = analyzer.detect_bpm()
                            
                            self.assertIsInstance(bpm, float)
                            self.assertIsInstance(confidence, float)
                            self.assertGreater(bpm, 0)
                            self.assertGreaterEqual(confidence, 0)
                            self.assertLessEqual(confidence, 1)
    
    def test_detect_key(self):
        """Test key detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock chromagram and key detection
                with patch('librosa.feature.chroma_cqt') as mock_chroma:
                    mock_chroma.return_value = np.random.rand(12, 100)
                    
                    with patch('librosa.feature.key_mode') as mock_key_mode:
                        mock_key_mode.return_value = (0, 1)  # C major
                        
                        analyzer = AudioAnalyzer("test_file.mp3")
                        key, confidence = analyzer.detect_key()
                        
                        self.assertIsInstance(key, str)
                        self.assertIsInstance(confidence, float)
                        self.assertGreaterEqual(confidence, 0)
                        self.assertLessEqual(confidence, 1)
    
    def test_analyze_beat_grid(self):
        """Test beat grid analysis"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock beat detection
                with patch('librosa.onset.onset_strength') as mock_onset_strength:
                    mock_onset_strength.return_value = np.random.rand(100)
                    
                    with patch('librosa.beat.beat_track') as mock_beat_track:
                        mock_beat_track.return_value = (128.0, np.array([0, 512, 1024]))
                        
                        analyzer = AudioAnalyzer("test_file.mp3")
                        beat_times, beat_strengths = analyzer.analyze_beat_grid()
                        
                        self.assertIsInstance(beat_times, np.ndarray)
                        self.assertIsInstance(beat_strengths, np.ndarray)
                        self.assertEqual(len(beat_times), len(beat_strengths))
    
    def test_detect_sections(self):
        """Test section detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock MFCC and section detection
                with patch('librosa.feature.mfcc') as mock_mfcc:
                    mock_mfcc.return_value = np.random.rand(13, 100)
                    
                    with patch('librosa.segment.recurrence_matrix') as mock_recurrence:
                        mock_recurrence.return_value = np.random.rand(100, 100)
                        
                        with patch('librosa.segment.detect_segments') as mock_detect:
                            mock_detect.return_value = np.array([[0, 50], [50, 100]])
                            
                            analyzer = AudioAnalyzer("test_file.mp3")
                            sections = analyzer.detect_sections()
                            
                            self.assertIsInstance(sections, list)
                            for section in sections:
                                self.assertIsInstance(section, tuple)
                                self.assertEqual(len(section), 3)
    
    def test_analyze_energy_profile(self):
        """Test energy profile analysis"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock RMS calculation
                with patch('librosa.feature.rms') as mock_rms:
                    mock_rms.return_value = np.random.rand(1, 100)
                    
                    with patch('librosa.frames_to_time') as mock_frames_to_time:
                        mock_frames_to_time.return_value = np.linspace(0, 10, 100)
                        
                        analyzer = AudioAnalyzer("test_file.mp3")
                        times, rms = analyzer.analyze_energy_profile()
                        
                        self.assertIsInstance(times, np.ndarray)
                        self.assertIsInstance(rms, np.ndarray)
                        self.assertEqual(len(times), len(rms))
    
    def test_detect_drops(self):
        """Test drop detection"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock energy profile
                with patch.object(AudioAnalyzer, 'analyze_energy_profile') as mock_energy:
                    mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                    
                    analyzer = AudioAnalyzer("test_file.mp3")
                    drops = analyzer.detect_drops()
                    
                    self.assertIsInstance(drops, list)
                    for drop in drops:
                        self.assertIsInstance(drop, float)
                        self.assertGreaterEqual(drop, 0)
    
    def test_get_audio_features(self):
        """Test comprehensive audio features extraction"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (self.mock_audio_data, self.sample_rate)
            
            with patch('librosa.get_duration') as mock_duration:
                mock_duration.return_value = 10.0
                
                # Mock all analysis methods
                with patch.object(AudioAnalyzer, 'detect_bpm') as mock_bpm:
                    mock_bpm.return_value = (128.0, 0.8)
                    
                    with patch.object(AudioAnalyzer, 'detect_key') as mock_key:
                        mock_key.return_value = ("C major", 0.7)
                        
                        with patch.object(AudioAnalyzer, 'analyze_energy_profile') as mock_energy:
                            mock_energy.return_value = (np.linspace(0, 10, 100), np.random.rand(100))
                            
                            with patch.object(AudioAnalyzer, 'analyze_beat_grid') as mock_beat:
                                mock_beat.return_value = (np.array([0, 0.5, 1.0]), np.array([0.8, 0.9, 0.7]))
                                
                                with patch.object(AudioAnalyzer, 'detect_sections') as mock_sections:
                                    mock_sections.return_value = [("Intro", 0, 2), ("Verse", 2, 5)]
                                    
                                    with patch.object(AudioAnalyzer, 'detect_drops') as mock_drops:
                                        mock_drops.return_value = [3.0, 7.0]
                                        
                                        analyzer = AudioAnalyzer("test_file.mp3")
                                        features = analyzer.get_audio_features()
                                        
                                        # Check required keys
                                        required_keys = [
                                            'duration', 'sample_rate', 'bpm', 'bpm_confidence',
                                            'key', 'key_confidence', 'avg_energy', 'max_energy',
                                            'energy_std', 'beat_count', 'avg_beat_strength',
                                            'section_count', 'drop_count'
                                        ]
                                        
                                        for key in required_keys:
                                            self.assertIn(key, features)
                                        
                                        # Check data types
                                        self.assertIsInstance(features['duration'], float)
                                        self.assertIsInstance(features['bpm'], float)
                                        self.assertIsInstance(features['key'], str)
                                        self.assertIsInstance(features['sections'], list)

class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_analyze_track_compatibility(self):
        """Test track compatibility analysis"""
        # Mock two analyzers
        mock_analyzer1 = Mock()
        mock_analyzer1.get_audio_features.return_value = {
            'bpm': 128.0,
            'key': 'C major',
            'avg_energy': 0.5
        }
        
        mock_analyzer2 = Mock()
        mock_analyzer2.get_audio_features.return_value = {
            'bpm': 130.0,
            'key': 'F major',
            'avg_energy': 0.6
        }
        
        with patch('audio_utils.AudioAnalyzer') as mock_audio_analyzer:
            mock_audio_analyzer.side_effect = [mock_analyzer1, mock_analyzer2]
            
            compatibility = analyze_track_compatibility("track1.mp3", "track2.mp3")
            
            # Check required keys
            required_keys = [
                'bpm_compatibility', 'bpm_difference', 'key_compatibility',
                'energy_compatibility', 'overall_score'
            ]
            
            for key in required_keys:
                self.assertIn(key, compatibility)
            
            # Check data types and ranges
            self.assertIsInstance(compatibility['bpm_compatibility'], float)
            self.assertIsInstance(compatibility['overall_score'], float)
            self.assertGreaterEqual(compatibility['bpm_compatibility'], 0)
            self.assertLessEqual(compatibility['bpm_compatibility'], 100)
            self.assertGreaterEqual(compatibility['overall_score'], 0)
            self.assertLessEqual(compatibility['overall_score'], 100)
    
    def test_suggest_mix_points(self):
        """Test mix point suggestions"""
        # Mock analyzers
        mock_analyzer1 = Mock()
        mock_analyzer1.get_audio_features.return_value = {
            'bpm': 128.0,
            'duration': 240.0
        }
        mock_analyzer1.analyze_energy_profile.return_value = (
            np.linspace(0, 240, 1000),
            np.random.rand(1000)
        )
        
        mock_analyzer2 = Mock()
        mock_analyzer2.get_audio_features.return_value = {
            'bpm': 130.0,
            'duration': 245.0
        }
        mock_analyzer2.analyze_energy_profile.return_value = (
            np.linspace(0, 245, 1000),
            np.random.rand(1000)
        )
        
        with patch('audio_utils.AudioAnalyzer') as mock_audio_analyzer:
            mock_audio_analyzer.side_effect = [mock_analyzer1, mock_analyzer2]
            
            suggestions = suggest_mix_points("track1.mp3", "track2.mp3")
            
            # Check required keys
            required_keys = [
                'track1_exit_points', 'track2_entry_points',
                'recommended_mix_duration', 'bpm_sync_required'
            ]
            
            for key in required_keys:
                self.assertIn(key, suggestions)
            
            # Check data types
            self.assertIsInstance(suggestions['track1_exit_points'], list)
            self.assertIsInstance(suggestions['track2_entry_points'], list)
            self.assertIsInstance(suggestions['recommended_mix_duration'], float)
            self.assertIsInstance(suggestions['bpm_sync_required'], bool)

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios"""
    
    def test_invalid_file_path(self):
        """Test handling of invalid file paths"""
        with self.assertRaises(Exception):
            AudioAnalyzer("nonexistent_file.mp3")
    
    def test_empty_audio_file(self):
        """Test handling of empty audio files"""
        with patch('librosa.load') as mock_load:
            mock_load.return_value = (np.array([]), 44100)
            
            with self.assertRaises(Exception):
                analyzer = AudioAnalyzer("empty_file.mp3")
                analyzer.get_audio_features()

if __name__ == '__main__':
    unittest.main() 