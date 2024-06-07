# Selenium Scraper Starter

This repository has a quick start to create a scrapper with selenium. Flask is used to create calls that execute functions in the scrapper, in addition to bearer authorization. It has a log system, environment management (production, staging, etc.) and a configuration with docker

## `Local Deploy`

### 1. Prerequisites

To build and run this application locally, ensure you have the following:

- Install [Python](https://www.python.org/)
- .env file **_(you can use .env.example to create this file)_**
- [Postman](https://www.postman.com/) to be able to send requests to the server
- [Chrome](https://www.google.com/intl/en_en/chrome)

### 2. Versions

- **Python**: 3.12.2

### 3. Create virtual environment

We use a module named virtualenv which is a tool to create **isolated Python environments**. Virtualenv creates a folder that contains all the necessary executables to use the packages that a Python project would need.

```bash
python -m venv <whatever_virtual_environment_name>
```

### 4. Activate virtual environment

```bash
source <whatever_virtual_environment_name>/bin/activate   # for Unix/Linux
.\<whatever_virtual_environment_name>\Scripts\activate    # for Windows
```

### 5. Install project libraries

```bash
python -r .\requirements.txt
```

### 6. Run main file

```bash
py .\main.py
```

Now, the server is accessible at `http://localhost3000`

## `Project Structure`

```bash
├───main.py # Main file that raises the server. Contains the endpoints
├───.vscode # Visual Studio Code specific configuration folder
├───actions # Folder that contains the files related to the actions carried out by the bot. Each file in it is an action
├───controller # It contains the functions that are executed on each endpoint
├───temp_downloads # Folder containing temporary files downloaded during project execution
└───utils # It contains the functions that are executed on each endpoint
```

## `Bibliography`

- [Selenium Web Page](https://selenium-python.readthedocs.io/): Main bot technology
- [Selenium Tutorial](https://youtube.com/playlist?list=PLheIVUbpfWZ17lCcHnoaa1RD59juFR06C&si=TTyB-dQQFl38tXO2)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/): Core technology for creating a REST API server
