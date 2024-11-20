# Release Note Generator

A professional, modular, and extensible Python script for automatically generating Release Notes on Linux.

## Features

- Modular design with clear separation of concerns.
- Supports Git operations across multiple repositories.
- Parses Manifest files to retrieve repository information.
- Processes commit information between tags.
- Generates and fills Release Note Excel sheets.
- Manages patch files, including generation and cleanup.
- Provides FastAPI interfaces for file and task management.
- Task queue management with sequential execution.
- Extensive logging and exception handling.

## Requirements

- Python 3.8.10
- Linux operating system
- Install dependencies using:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

- Execute the script directly:

  ```bash
  python main.py
  ```

- Start the FastAPI application:

  ```bash
  python api/main.py
  ```
