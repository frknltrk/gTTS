# TXT To Audio

Convert your text into audio files effortlessly.
This Python script harnesses the power of Google's Text-to-Speech (gTTS) service to transform written content into spoken words. Ideal for accessibility, auditory learning, or enjoying documents on-the-go.

## 🌟 Features

- **Text-to-Speech**: Leverages Google's gTTS API for high-quality audio output.
- **Parallel Processing**: Option for faster processing of multiple documents.
- **Rate Limit Management**: Smart retry logic with exponential backoff.
- **Flexible CLI**: Command-line interface for customizable configurations.

## 📋 Installation

Get started with these simple steps:

### Prerequisites

- Python 3.x
- Required packages: `gtts`

### Install Python Packages

```bash
pip install gtts
```

## 🚀 Usage

## Command Syntax

```bash
python main.py <input_files> [--output_folder OUTPUT_FOLDER] [options]
```

### Arguments

- input_files: Paths to txt files (>= 1)
- output_folder (optional): Folder for saving audio files (defaults to script directory).

### Options

- --language: Language for conversion (default: 'en').
- --parallel: Enable parallel processing (sequential by default).
- --retry_delay: Delay in seconds for retrying conversion (default: 5).
- --max_retries: Max retries for conversion (default: 10).

## Example

```bash
python main.py ./input/aaa.txt ./input/bbb.txt ./input/ccc.txt --output_folder ./audios --language de --parallel --retry_delay 2 --max_retries 3
```

## 🤝 Contributing

Your contributions are welcome! Feel free to submit bug fixes, feature requests, or documentation improvements.
Check out the issues and pull requests sections.

## 📄 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.
