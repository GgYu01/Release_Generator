# Release Note Generator

## Overview

The Release Note Generator is a Python-based tool designed to automatically generate and populate release notes by extracting commit information and patch files from various Git-managed repositories. It supports repositories managed by `git`, `repo`, and `jiri`, and integrates with FastAPI for task and file management.

## Features

- **Automated Tag Retrieval**: Fetches the latest and second latest tags from specified repositories.
- **Commit Extraction**: Retrieves commits between two tags.
- **Patch Generation**: Creates patch files for commits and manages special commit patterns.
- **Excel Integration**: Populates an existing Excel spreadsheet with release notes.
- **FastAPI Interface**: Provides HTTP endpoints for file and task management.
- **Task Management**: Handles task queues and execution statuses.
- **Logging and Exception Handling**: Comprehensive logging and error handling mechanisms.

## Project Structure
release_note_generator/
├── config/
│ ├── init.py
│ └── settings.py
├── core/
│ ├── init.py
│ ├── git_handler.py
│ ├── manifest_parser.py
│ ├── commit_processor.py
│ ├── patch_manager.py
│ └── release_note_writer.py
├── api/
│ ├── init.py
│ ├── file_manager.py
│ ├── task_manager.py
│ └── main.py
├── tasks/
│ ├── init.py
│ ├── task_queue.py
│ └── task_executor.py
├── utils/
│ ├── init.py
│ ├── logger.py
│ ├── exception_handler.py
│ ├── file_utils.py
│ └── common.py
├── main.py
├── README.md
└── requirements.txt

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://your-repo-url.git
   cd release_note_generator
Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate
Install Dependencies

pip install -r requirements.txt
Configuration
All configurations are managed in config/settings.py. Adjust the paths, repository information, and other settings as needed.

Usage
Running the Script
To execute the release note generation process:

python3 main.py
Starting the FastAPI Server
To start the FastAPI server for handling file and task management:

uvicorn api.main:app --host 0.0.0.0 --port 8000
Access the API documentation at http://localhost:8000/docs.

Dependencies
Python 3.8.10
FastAPI
Uvicorn
openpyxl
Refer to requirements.txt for the complete list of dependencies.

Logging
Logs are stored in release_note_generator.log with rotating file handling to manage log sizes.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

License
This project is licensed under the MIT License.


### `requirements.txt`

```plaintext
fastapi==0.95.1
uvicorn==0.22.0
openpyxl==3.1.2