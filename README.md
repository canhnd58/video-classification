# Video Classification

### Installation
- [openCV](http://opencv.org/): `sudo apt-get install python-opencv`. Should be in version 3.1.0.
- [ffmpeg](https://ffmpeg.org/download.html): `sudo apt-get install ffmpeg`
- [pytube](https://github.com/nficano/pytube): `pip install pytube`
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis): Follow the instruction on [this](https://github.com/tyiannak/pyAudioAnalysis/wiki/2.-General).

### Usage
- Build to csv files: `python src/combine.py path_to_id_text_file number_of_id`. Example: `python src/combine.py data/id2games.txt 200`.
- `path_to_id_text_file` should be in format `data/*.txt`.

### References
- [YouTube-8M: A Large-Scale Video Classification Benchmark](http://static.googleusercontent.com/media/research.google.com/vi//youtube8m/youtube8m-paper.pdf)
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis)
