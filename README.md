# DynaMix

**DynaMix** is an advanced audio transition analysis tool designed for DJs and music enthusiasts to ensure smooth and energetic transitions between tracks. By analyzing the RMS (Root Mean Square) energy levels, BPM, musical key, and other audio features of MP3 files, DynaMix helps you identify the optimal mixing points so that the energy flow on the dance floor remains consistent.

[🇹🇷 Türkçe - Benioku](BENIOKU.md)

## 🚀 New Features

### Enhanced Analysis Tools
- **BPM Detection:** Accurate tempo analysis with confidence scoring
- **Key Detection:** Musical key identification for harmonic mixing
- **Beat Grid Analysis:** Precise beat timing and strength analysis
- **Section Detection:** Automatic identification of intro, verse, chorus, bridge, outro
- **Drop Detection:** Energy breakdown and build-up point identification

### Playlist Management
- **Playlist Analysis:** Analyze entire music collections
- **Set List Generation:** Create optimal track sequences for DJ sets
- **Energy Curve Optimization:** Build-up, wave, or custom energy patterns
- **Compatibility Matrix:** Track-to-track compatibility scoring
- **Export/Import:** Save and load playlist analyses

### DJ Performance Tools
- **Cue Point Detection:** Optimal cue points for DJ performance
- **Loop Suggestions:** Musical phrase and section-based loop recommendations
- **Performance Zones:** Intro, build, drop, breakdown, outro analysis
- **DJ Notes Generation:** Comprehensive performance notes for each track
- **Batch Analysis:** Process entire directories automatically

### Advanced Visualization
- **Comprehensive Charts:** Energy profiles, beat grids, chromagrams
- **Compatibility Radar:** Visual compatibility scoring
- **Performance Zones:** Color-coded track sections
- **Cue Point Visualization:** Onset strength and timing analysis

## 📋 Requirements

- **Python 3.8+**
- [Librosa](https://librosa.org/) for audio processing
- [NumPy](https://numpy.org/) for numerical operations
- [Matplotlib](https://matplotlib.org/) for visualization
- [Pandas](https://pandas.pydata.org/) for data analysis
- [Seaborn](https://seaborn.pydata.org/) for enhanced plotting
- **FFmpeg** or **AVbin** (if required) to support MP3 file decoding

## 🛠️ Installation

1. **Clone or Download the Repository:**

   ```bash
   git clone https://github.com/makalin/dynamix.git
   cd dynamix
   ```

2. **Install the Required Python Packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg (if not already installed):**

   - **FFmpeg Download:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Alternatively, you can use package managers like `apt`, `brew`, or `chocolatey` depending on your OS.

## 🎵 Usage

### Basic Two-Track Analysis

Run the original DynaMix tool for basic energy analysis:

```bash
python mix_analiz.py path/to/track1.mp3 path/to/track2.mp3 --gecis_suresi 10 --threshold_factor 1.2
```

### Enhanced Analysis

Use the enhanced version for comprehensive analysis:

```bash
python mix_enhanced.py track1.mp3 track2.mp3 --visualize
```

### Playlist Analysis

Analyze entire music collections:

```bash
python mix_enhanced.py --playlist /path/to/music/folder --set-duration 90 --visualize
```

### DJ Performance Tools

Generate DJ notes for individual tracks:

```bash
python dj_tools.py track.mp3 --export dj_notes.txt --visualize
```

Batch analyze entire directories:

```bash
python dj_tools.py --batch /path/to/music/folder --output-dir /path/to/notes
```

## 📊 Command-Line Arguments

### Enhanced Mix Analysis (`mix_enhanced.py`)

- **`track1`** - First MP3 file path
- **`track2`** - Second MP3 file path
- **`--visualize`** - Show enhanced visualizations
- **`--playlist`** - Analyze entire playlist directory
- **`--export`** - Export analysis to file (JSON/CSV)
- **`--set-duration`** - Set duration in minutes for playlist analysis

### DJ Tools (`dj_tools.py`)

- **`audio_file`** - Audio file to analyze
- **`--export`** - Export DJ notes to file
- **`--visualize`** - Show performance visualization
- **`--batch`** - Batch analyze directory
- **`--output-dir`** - Output directory for batch analysis

## 🔧 Advanced Features

### Audio Analysis (`audio_utils.py`)

```python
from audio_utils import AudioAnalyzer

# Initialize analyzer
analyzer = AudioAnalyzer("track.mp3")

# Get comprehensive features
features = analyzer.get_audio_features()
print(f"BPM: {features['bpm']}")
print(f"Key: {features['key']}")

# Detect sections
sections = analyzer.detect_sections()

# Analyze beat grid
beat_times, beat_strengths = analyzer.analyze_beat_grid()

# Create comprehensive visualization
analyzer.plot_comprehensive_analysis()
```

### Playlist Management (`playlist_manager.py`)

```python
from playlist_manager import PlaylistManager

# Initialize playlist manager
manager = PlaylistManager("/path/to/music")

# Analyze playlist
df = manager.analyze_playlist()

# Create optimized set list
set_list = manager.create_set_list(duration_minutes=60, energy_curve='build')

# Export analysis
manager.export_playlist("playlist_analysis.json", format='json')
```

### DJ Performance Tools (`dj_tools.py`)

```python
from dj_tools import DJTools

# Initialize DJ tools
dj_tools = DJTools("track.mp3")

# Detect cue points
cue_points = dj_tools.detect_cue_points(sensitivity=0.7)

# Suggest loops
loops = dj_tools.suggest_loops(min_duration=4.0, max_duration=16.0)

# Generate DJ notes
notes = dj_tools.generate_dj_notes()

# Create performance visualization
dj_tools.create_performance_visualization()
```

## 📈 Analysis Output

### Track Information
- **Duration:** Track length in seconds
- **BPM:** Tempo with confidence score
- **Key:** Musical key with confidence score
- **Energy Profile:** Average, maximum, and standard deviation
- **Sections:** Number and timing of detected sections
- **Drops:** Number and timing of energy drops

### Compatibility Analysis
- **BPM Compatibility:** Percentage based on tempo difference
- **Key Compatibility:** Harmonic compatibility score
- **Energy Compatibility:** Energy level matching
- **Overall Score:** Weighted combination of all factors

### Mix Recommendations
- **Mix Duration:** Recommended transition length
- **Exit Points:** Optimal points to exit from track 1
- **Entry Points:** Optimal points to enter track 2
- **BPM Sync:** Whether tempo synchronization is required
- **Mixing Strategy:** Detailed technique recommendations

## 🎯 Use Cases

### DJ Performance
- **Set Planning:** Create optimal track sequences
- **Cue Point Preparation:** Identify best mixing points
- **Harmonic Mixing:** Ensure key compatibility
- **Energy Management:** Maintain dance floor energy

### Music Production
- **Reference Analysis:** Analyze reference tracks
- **Structure Analysis:** Understand song sections
- **Energy Mapping:** Visualize track dynamics

### Music Discovery
- **Playlist Optimization:** Create better playlists
- **Compatibility Testing:** Test track combinations
- **Genre Analysis:** Understand musical characteristics

## 🔄 How It Works

1. **Audio Loading:** Each MP3 file is loaded and converted to a mono audio signal using Librosa.

2. **Feature Extraction:** Multiple audio features are extracted:
   - RMS energy levels
   - BPM detection using multiple algorithms
   - Musical key analysis via chromagram
   - Beat grid analysis
   - Section detection using MFCC features

3. **Compatibility Analysis:** Tracks are compared across multiple dimensions:
   - BPM difference and compatibility
   - Key compatibility using music theory
   - Energy level matching
   - Overall compatibility scoring

4. **Mix Point Detection:** Optimal mixing points are identified:
   - Energy valleys in track 1 (exit points)
   - Energy peaks in track 2 (entry points)
   - Beat-synchronized points
   - Section boundaries

5. **Visualization:** Comprehensive charts show:
   - Energy profiles over time
   - Beat grids and timing
   - Chromagram for key analysis
   - Performance zones and sections

6. **Recommendations:** Detailed mixing advice including:
   - Recommended mix duration
   - Specific timing suggestions
   - Technique recommendations
   - Potential challenges and solutions

## 🎨 Customization

You can fine-tune the following parameters to suit your mixing style:

### Energy Analysis
- **`--gecis_suresi`:** Adjust the duration of track 1's tail end used for analysis
- **`--threshold_factor`:** Modify the sensitivity of energy increase detection in track 2

### Cue Point Detection
- **`sensitivity`:** Adjust cue point detection sensitivity (0.0-1.0)

### Loop Suggestions
- **`min_duration`:** Minimum loop duration in seconds
- **`max_duration`:** Maximum loop duration in seconds

### Playlist Analysis
- **`energy_curve`:** Choose from 'build', 'wave', 'peak_middle', 'constant'
- **`key_compatibility`:** Enable/disable key-based optimization
- **`bpm_transitions`:** Enable/disable BPM-based optimization

## 📁 File Structure

```
dynamix/
├── mix_analiz.py          # Original basic analysis tool
├── mix_enhanced.py        # Enhanced analysis with all features
├── audio_utils.py         # Core audio analysis utilities
├── playlist_manager.py    # Playlist and set list management
├── dj_tools.py           # DJ performance tools
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── BENIOKU.md           # Turkish documentation
└── LICENSE              # MIT License
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙏 Acknowledgements

- [Librosa](https://librosa.org/) - Audio and music signal processing
- [NumPy](https://numpy.org/) - Numerical computing
- [Matplotlib](https://matplotlib.org/) - Plotting and visualization
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis
- [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization

---

🎵 **Enjoy seamless transitions and keep the energy high with DynaMix!** 🎵
