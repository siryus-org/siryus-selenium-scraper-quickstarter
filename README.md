# Selenium Scraper Starter

This repository provides a foundation for building robust and scalable web scrapers using Selenium and Flask. It emphasizes best practices including environment management, configuration with Docker, and a well-structured project layout.

## Key Features

- **Selenium Automation:** Efficiently interact with dynamic webpages using Selenium's browser automation capabilities.
- **Flask Backend:** Create a RESTful API with Flask to manage scraper execution, authorization, and logging.
- **Bearer Authentication:** Implement a secure mechanism for API access using bearer tokens.
- **Environment Management:** Facilitate deployment across different environments (production, staging) using environment variables.
- **Docker Configuration:** Streamline containerization for a consistent and portable development experience.
- **Logging System:** Track scraper activities and errors for debugging and monitoring.

## Local Setup

### Prerequisites

Before diving in, ensure you have the following tools installed:

- **Python (version 3.x recommended):** Download and install from https://www.python.org/downloads/.
- **.env file:** Create a `.env` file to store environment variables (refer to `.env.example` for guidance).
- **HTTP Client (Postman recommended):** Use an HTTP client like https://www.postman.com/ to send requests to the Flask API.
- **Chrome Browser:** Download and install the latest version from https://www.google.com/chrome/.

### Create a Virtual Environment

We use a module named virtualenv which is a tool to create **isolated Python environments**. Virtualenv creates a folder that contains all the necessary executables to use the packages that a Python project would need.

```bash
python -m venv <whatever_virtual_environment_name>
```

### Activate virtual environment

```bash
source <whatever_virtual_environment_name>/bin/activate   # for Unix/Linux
.\<whatever_virtual_environment_name>\Scripts\activate    # for Windows
```

### Install project libraries

```bash
python -r .\requirements.txt
```

### Run main file

```bash
py .\main.py
```

Now, the server is accessible at `http://localhost3000`

## Project Structure

```bash
├─── main.py                   # Entry point for the Flask application
├─── .vscode                   # Configuration for Visual Studio Code (optional)
├─── actions                   # Contains scraper actions (logic for data extraction)
├─── controller                # Functions handling API requests
├─── temp_downloads            # Temporary files created during scraping
└─── utils                     # Reusable helper functions
```

## Bibliography

- [Selenium Web Page](https://selenium-python.readthedocs.io/): Main bot technology
- [Selenium Tutorial](https://youtube.com/playlist?list=PLheIVUbpfWZ17lCcHnoaa1RD59juFR06C&si=TTyB-dQQFl38tXO2)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/): Core technology for creating a REST API server
