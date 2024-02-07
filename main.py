import argparse
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from gtts import gTTS, gTTSError

# Function to convert text to speech
def convert_text_to_speech(text, filename_without_extension, cache_folder_path, language='en', retry_delay=5,
                           max_retries=10):
    """Convert text to speech using Google's Text-to-Speech API.

    Args:
        text (str): Text to be converted to speech.
        filename_without_extension (str): Filename for the output audio file without extension.
        cache_folder_path (Path): Path to the folder where the audio file will be saved.
        language (str, optional): Language for text-to-speech conversion. Defaults to 'en'.
        retry_delay (int, optional): Initial delay in seconds for retrying conversion. Defaults to 5.
        max_retries (int, optional): Maximum number of retries for conversion. Defaults to 10.

    Returns:
        Path: The path to the saved audio file.

    Raises:
        RuntimeError: If conversion fails after maximum retries.
    """
    audio_file_path = cache_folder_path / f"{filename_without_extension}.mp3"

    if audio_file_path.exists():
        print(f"Using existing audio file for {filename_without_extension}")
        return audio_file_path

    for attempt in range(max_retries):
        try:
            tts = gTTS(text, lang=language)
            tts.save(audio_file_path)
            return audio_file_path
        except gTTSError as e:
            if "429 (Too Many Requests)" in str(e):
                print(f"Rate limit hit, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                raise
        except Exception as e:
            raise  # Re-raise any other exceptions

    raise RuntimeError("Failed to convert text to speech after retries")

# Main function to process each txt
def process_txt(file_path: Path, output_dir_path, language='en', retry_delay=5, max_retries=10):
    """Process a single PDF file: extract text, convert to speech, and save.

    Args:
        file_path (Path): Path to the txt file.
        output_folder_path (Path): Path to the folder for saving extracted text files.
        output_dir_path (Path): Path to the folder for saving audio files.
        language (str, optional): Language for text-to-speech conversion. Defaults to 'en'.
        retry_delay (int, optional): Initial delay for retrying conversion. Defaults to 5.
        max_retries (int, optional): Maximum number of retries for conversion. Defaults to 10.
    """
    start_time = time.time()
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    filename_without_extension = file_path.stem
    convert_text_to_speech(text, filename_without_extension, output_dir_path, language, retry_delay, max_retries)
    end_time = time.time()
    print(f"Processed {file_path.name} in {end_time - start_time:.2f} seconds.")

# Entry point for the script
def main():
    """Main function to handle command-line arguments and process TXT files."""
    parser = argparse.ArgumentParser(description="Convert TXT files to audio.")
    parser.add_argument("input_files", nargs='+', help="Paths to the input TXT files")
    parser.add_argument("--output_dir", default=None, help="Path to the folder for saving audio files")
    parser.add_argument("--language", default='en', help="Language for text-to-speech conversion")
    parser.add_argument("--parallel", action='store_true', help="Process files in parallel")
    parser.add_argument("--retry_delay", type=int, default=5, help="Initial delay for retrying conversion")
    parser.add_argument("--max_retries", type=int, default=10, help="Maximum retries for conversion")

    args = parser.parse_args()

    script_directory = Path(__file__).parent
    output_dir_path = Path(args.output_dir) if args.output_dir else script_directory / "audio"

    output_dir_path.mkdir(parents=True, exist_ok=True)

    if args.parallel:
        num_workers = os.cpu_count()
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(process_txt, Path(txt_path), output_dir_path, args.language,
                                       args.retry_delay, args.max_retries) for txt_path in args.input_files]
            for future in as_completed(futures):
                future.result()
    else:
        for txt_path in args.input_files:
            process_txt(Path(txt_path), output_dir_path, args.language, args.retry_delay,
                        args.max_retries)

if __name__ == "__main__":
    main()
