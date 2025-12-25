# DynaMix GUI - Quick Start Guide

## Launching the GUI

To start the DynaMix graphical user interface:

```bash
python gui.py
```

## GUI Tabs Overview

### 1. Track Analysis Tab
- **Purpose**: Analyze individual audio tracks
- **Features**:
  - Browse and select audio files
  - View comprehensive track analysis (BPM, key, energy, sections, etc.)
  - Visualize energy profiles and beat grids
  - Export analysis results

### 2. Two-Track Analysis Tab
- **Purpose**: Compare and analyze compatibility between two tracks
- **Features**:
  - Select two tracks for comparison
  - View compatibility scores (BPM, key, energy)
  - Get mix recommendations
  - See optimal exit/entry points

### 3. Playlist Manager Tab
- **Purpose**: Manage and analyze entire music collections
- **Features**:
  - Scan directories for audio files
  - Analyze entire playlists
  - Create optimized set lists
  - Configure energy curves and duration
  - View playlist in table format

### 4. DJ Tools Tab
- **Purpose**: Access DJ performance tools
- **Features**:
  - Detect cue points
  - Suggest loops
  - Analyze performance zones
  - Generate DJ notes
  - Batch analyze directories

### 5. Audio Effects Tab
- **Purpose**: Advanced audio effects analysis
- **Features**:
  - Analyze dynamics (compression, dynamic range)
  - Frequency spectrum analysis
  - Transient response analysis
  - Detect clipping and phasing issues

### 6. Export Tools Tab
- **Purpose**: Export analysis results in various formats
- **Features**:
  - Export to JSON, CSV, M3U
  - Export to Rekordbox XML
  - Export to Traktor NML
  - Export text reports
  - View export log

## Usage Tips

1. **File Selection**: Use the "Browse" buttons to select audio files or directories
2. **Analysis**: Click "Analyze" buttons to start processing (may take time for large files)
3. **Visualizations**: Charts and graphs appear automatically after analysis
4. **Export**: Use the Export Tools tab to save results in your preferred format
5. **Status Bar**: Check the bottom status bar for current operation status

## Keyboard Shortcuts

- **Ctrl+O**: Open file (in file selection dialogs)
- **Ctrl+S**: Save (in export dialogs)
- **Esc**: Close dialogs

## Troubleshooting

### GUI Won't Start
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify tkinter is available (usually included with Python)

### Analysis Takes Too Long
- Large audio files take longer to process
- Use batch analysis for multiple files
- Check the status bar for progress

### No Visualizations Appearing
- Ensure matplotlib is properly installed
- Check that analysis completed successfully
- Try resizing the window

## System Requirements

- Python 3.8 or higher
- All dependencies from requirements.txt
- Tkinter (usually included with Python)
- Sufficient RAM for large playlists (recommended: 4GB+)

## Notes

- The GUI runs analysis in background threads to keep the interface responsive
- Large playlists may take several minutes to analyze
- Export formats are optimized for compatibility with popular DJ software

