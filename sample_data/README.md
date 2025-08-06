# Sample Data Directory

This directory is intended for storing sample audio files for testing and demonstration purposes.

## Purpose

- **Testing**: Audio files for running unit tests and integration tests
- **Demonstration**: Sample tracks for showcasing DynaMix features
- **Development**: Files for development and debugging

## Recommended Structure

```
sample_data/
├── README.md                    # This file
├── test_tracks/                 # Small test files for unit tests
│   ├── short_test.mp3          # 10-30 second test file
│   ├── medium_test.mp3         # 1-2 minute test file
│   └── long_test.mp3           # 3-5 minute test file
├── demo_tracks/                 # Demo files for showcasing features
│   ├── track1.mp3              # Demo track 1
│   ├── track2.mp3              # Demo track 2
│   └── track3.mp3              # Demo track 3
└── playlists/                   # Sample playlists
    ├── house_playlist/          # House music playlist
    ├── techno_playlist/         # Techno music playlist
    └── mixed_playlist/          # Mixed genre playlist
```

## File Requirements

### For Testing
- **Format**: MP3, WAV, FLAC, M4A, AAC, OGG
- **Duration**: 10 seconds to 5 minutes
- **Quality**: 128kbps minimum (for testing)
- **Size**: Keep under 10MB per file for testing

### For Demos
- **Format**: MP3, WAV, FLAC
- **Duration**: 2-5 minutes
- **Quality**: 192kbps or higher
- **Size**: Reasonable file sizes for demonstrations

## Usage Examples

### Running Tests with Sample Data
```bash
# Test with sample tracks
python tests/run_tests.py

# Test specific module
python tests/run_tests.py --module audio_utils

# Run examples with sample data
python examples.py
```

### Demo with Sample Data
```bash
# Analyze two tracks
python mix_enhanced.py sample_data/demo_tracks/track1.mp3 sample_data/demo_tracks/track2.mp3 --visualize

# Analyze playlist
python mix_enhanced.py --playlist sample_data/playlists/house_playlist --visualize

# Generate DJ notes
python dj_tools.py sample_data/demo_tracks/track1.mp3 --export dj_notes.txt
```

## Important Notes

1. **Do not commit large audio files** to version control
2. **Use small test files** for automated testing
3. **Keep demo files reasonable** in size
4. **Respect copyright** - only use files you have permission to use
5. **Document sources** if using third-party audio files

## Adding Your Own Files

1. Create appropriate subdirectories
2. Add files in supported formats
3. Update this README if adding new categories
4. Consider file sizes and licensing

## Supported Audio Formats

- **MP3** (.mp3) - Most common, good compression
- **WAV** (.wav) - Uncompressed, high quality
- **FLAC** (.flac) - Lossless compression
- **M4A** (.m4a) - Apple format
- **AAC** (.aac) - Advanced audio coding
- **OGG** (.ogg) - Open source format

## File Naming Convention

Use descriptive names that indicate:
- **Genre**: house_track.mp3, techno_track.mp3
- **BPM**: track_128bpm.mp3, track_140bpm.mp3
- **Key**: track_cmajor.mp3, track_aminor.mp3
- **Energy**: low_energy_track.mp3, high_energy_track.mp3 