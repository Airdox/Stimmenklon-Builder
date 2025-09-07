#!/usr/bin/env python3
"""
Demo script for Stimmenklon-Builder Voice Cloning
=================================================

This script demonstrates the voice cloning functionality without requiring
the full Android GUI. Useful for testing and development.

Usage:
    python demo_voice_cloning.py --help
    python demo_voice_cloning.py --train --model-name my_voice --audio-dir ./audio_samples/
    python demo_voice_cloning.py --synthesize --model-name my_voice --text "Hallo Welt"
"""

import argparse
import os
import sys
from pathlib import Path

def setup_path():
    """Add current directory to Python path"""
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))

def train_voice_model(model_name, audio_dir, verbose=True):
    """Train a voice model from audio files"""
    setup_path()
    
    try:
        from voice_model import ZonosVoiceModel, check_zonos_installation
        
        if verbose:
            print(f"🎙️ Training voice model: {model_name}")
            print(f"📁 Audio directory: {audio_dir}")
        
        # Check Zonos availability
        if not check_zonos_installation():
            print("⚠️ Zonos TTS not installed. Install with: pip install zonos")
            print("📝 For demo purposes, using placeholder functionality.")
        
        # Find audio files
        audio_dir = Path(audio_dir)
        if not audio_dir.exists():
            print(f"❌ Audio directory not found: {audio_dir}")
            return False
        
        audio_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(audio_dir.glob(f'*{ext}'))
            audio_files.extend(audio_dir.glob(f'*{ext.upper()}'))
        
        if not audio_files:
            print(f"❌ No audio files found in {audio_dir}")
            print(f"📝 Supported formats: {', '.join(audio_extensions)}")
            return False
        
        if verbose:
            print(f"🔍 Found {len(audio_files)} audio files:")
            for audio_file in audio_files:
                print(f"   - {audio_file.name}")
        
        # Create and train model
        voice_model = ZonosVoiceModel(model_name)
        
        def progress_callback(progress):
            if verbose:
                print(f"📊 Training progress: {progress:.1f}%")
        
        if verbose:
            print("🚀 Starting training...")
        
        success = voice_model.train_voice_model(
            [str(f) for f in audio_files], 
            progress_callback
        )
        
        if success:
            if verbose:
                print(f"✅ Training completed successfully!")
                print(f"💾 Model saved as: {model_name}")
            return True
        else:
            print("❌ Training failed")
            return False
            
    except Exception as e:
        print(f"❌ Training error: {e}")
        return False

def synthesize_speech(model_name, text, output_file=None, verbose=True):
    """Synthesize speech using a trained model"""
    setup_path()
    
    try:
        from voice_model import ZonosVoiceModel, check_zonos_installation
        
        if verbose:
            print(f"🎙️ Using voice model: {model_name}")
            print(f"📝 Text: {text}")
        
        # Check Zonos availability
        if not check_zonos_installation():
            print("⚠️ Zonos TTS not installed. Using demo functionality.")
        
        # Load model
        voice_model = ZonosVoiceModel(model_name)
        
        if not voice_model.load_voice_model():
            print(f"❌ Could not load model: {model_name}")
            print("💡 Train a model first with: --train")
            return False
        
        if verbose:
            print("🚀 Starting speech synthesis...")
        
        # Generate speech
        result_path = voice_model.synthesize_speech(text, output_file)
        
        if result_path and os.path.exists(result_path):
            if verbose:
                print(f"✅ Speech synthesis completed!")
                print(f"🔊 Audio file: {result_path}")
            return result_path
        else:
            print("❌ Speech synthesis failed")
            return None
            
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return None

def list_models(verbose=True):
    """List all available trained models"""
    setup_path()
    
    try:
        from voice_model import ZonosVoiceModel
        
        models = ZonosVoiceModel.list_available_models()
        
        if verbose:
            print(f"📋 Available voice models ({len(models)}):")
        
        if models:
            for model in models:
                print(f"   - {model}")
        else:
            print("   (No trained models found)")
        
        return models
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return []

def create_sample_audio_dir():
    """Create a sample audio directory with instructions"""
    sample_dir = Path("./sample_audio")
    sample_dir.mkdir(exist_ok=True)
    
    readme_text = """
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
"""
    
    readme_file = sample_dir / "README.md"
    readme_file.write_text(readme_text)
    
    print(f"📁 Created sample audio directory: {sample_dir}")
    print(f"📝 Instructions written to: {readme_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Stimmenklon-Builder Voice Cloning Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available models
  python demo_voice_cloning.py --list
  
  # Train a new voice model
  python demo_voice_cloning.py --train --model-name my_voice --audio-dir ./audio_samples/
  
  # Synthesize speech with trained model
  python demo_voice_cloning.py --synthesize --model-name my_voice --text "Hallo Welt!"
  
  # Create sample directory structure
  python demo_voice_cloning.py --setup
        """
    )
    
    parser.add_argument('--train', action='store_true',
                       help='Train a new voice model')
    parser.add_argument('--synthesize', action='store_true',
                       help='Synthesize speech using trained model')
    parser.add_argument('--list', action='store_true',
                       help='List available trained models')
    parser.add_argument('--setup', action='store_true',
                       help='Create sample audio directory structure')
    
    parser.add_argument('--model-name', type=str,
                       help='Name of the voice model')
    parser.add_argument('--audio-dir', type=str,
                       help='Directory containing audio files for training')
    parser.add_argument('--text', type=str,
                       help='Text to synthesize')
    parser.add_argument('--output', type=str,
                       help='Output audio file path')
    
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress verbose output')
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    if verbose:
        print("🎯 Stimmenklon-Builder Voice Cloning Demo")
        print("=" * 50)
    
    # Setup sample directory
    if args.setup:
        create_sample_audio_dir()
        return 0
    
    # List models
    if args.list:
        list_models(verbose)
        return 0
    
    # Training
    if args.train:
        if not args.model_name:
            print("❌ --model-name required for training")
            return 1
        
        if not args.audio_dir:
            print("❌ --audio-dir required for training")
            return 1
        
        success = train_voice_model(args.model_name, args.audio_dir, verbose)
        return 0 if success else 1
    
    # Synthesis
    if args.synthesize:
        if not args.model_name:
            print("❌ --model-name required for synthesis")
            return 1
        
        if not args.text:
            print("❌ --text required for synthesis")
            return 1
        
        result = synthesize_speech(args.model_name, args.text, args.output, verbose)
        return 0 if result else 1
    
    # No action specified
    parser.print_help()
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)