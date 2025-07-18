
# Sample Audio Directory

Place your audio files here for voice cloning training.

## Requirements:
- At least 3-5 audio files of your voice
- Total duration: 30 seconds to 5 minutes
- Supported formats: WAV, MP3, FLAC, OGG, M4A
- Clear recordings without background noise

## Example files to add:
- my_voice_1.wav
- my_voice_2.mp3
- reading_text.flac

## Training command:
python demo_voice_cloning.py --train --model-name my_voice --audio-dir ./sample_audio/

## After training, synthesize:
python demo_voice_cloning.py --synthesize --model-name my_voice --text "Hallo, das ist meine geklonte Stimme!"
