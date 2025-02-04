# DynaMix

**DynaMix** is an audio transition analysis tool designed for DJs and music enthusiasts to ensure smooth and energetic transitions between tracks. By analyzing the RMS (Root Mean Square) energy levels of two MP3 files, DynaMix helps you identify the optimal mixing points so that the energy flow on the dance floor remains consistent.

## Features

- **Audio Energy Analysis:** Computes RMS energy levels for each track.
- **Transition Point Detection:** Identifies the moment in the second track where energy increases significantly.
- **Mixing Recommendations:** Suggests how long to extend the energetic part of the first track to create a seamless blend.
- **Visualization:** Provides plots of energy curves for both tracks to help you visualize the transition.

## Requirements

- **Python 3.x**
- [Librosa](https://librosa.org/) for audio processing.
- [NumPy](https://numpy.org/) for numerical operations.
- [Matplotlib](https://matplotlib.org/) for visualization.
- **FFmpeg** or **AVbin** (if required) to support MP3 file decoding.

## Installation

1. **Clone or Download the Repository:**

   ```bash
   git clone https://github.com/makalin/dynamix.git
   cd dynamix
   ```

2. **Install the Required Python Packages:**

   ```bash
   pip install librosa numpy matplotlib
   ```

3. **Install FFmpeg (if not already installed):**

   - **FFmpeg Download:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Alternatively, you can use package managers like `apt`, `brew`, or `chocolatey` depending on your OS.

## Usage

Run the DynaMix tool from the command line by providing the paths to the two MP3 files you want to analyze:

```bash
python mix_analiz.py path/to/track1.mp3 path/to/track2.mp3 --gecis_suresi 10 --threshold_factor 1.2
```

### Command-Line Arguments

- **`path/to/track1.mp3`**  
  The path to the first MP3 file (e.g., Tarkan's "Öp").

- **`path/to/track2.mp3`**  
  The path to the second MP3 file (e.g., Ajda Pekkan's "Harika").

- **`--gecis_suresi`** (Optional)  
  The duration (in seconds) of the end section of track 1 to analyze.  
  _Default: 10 seconds_

- **`--threshold_factor`** (Optional)  
  The multiplier used to determine the energy increase threshold in track 2.  
  _Default: 1.2_

## How It Works

1. **Audio Loading:**  
   Each MP3 file is loaded and converted to a mono audio signal using Librosa.

2. **Energy Calculation:**  
   The RMS energy is computed frame-by-frame for both tracks to quantify their dynamic levels.

3. **Transition Analysis:**  
   - The tool computes the average energy in the last few seconds of track 1.
   - For track 2, it identifies the point where the energy surpasses a threshold (a multiple of the initial low-energy baseline).

4. **Visualization:**  
   Energy curves for both tracks are plotted, with markers indicating:
   - The start of the transition section in track 1.
   - The detected energy increase point in track 2.

5. **Mixing Recommendation:**  
   Based on the analysis, DynaMix suggests how long to use the energetic section of track 1 during the transition.

## Customization

You can fine-tune the following parameters to suit your mixing style:
- **`--gecis_suresi`:** Adjust the duration of track 1's tail end used for analysis.
- **`--threshold_factor`:** Modify the sensitivity of energy increase detection in track 2.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Librosa](https://librosa.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

---

Enjoy seamless transitions and keep the energy high with DynaMix!
