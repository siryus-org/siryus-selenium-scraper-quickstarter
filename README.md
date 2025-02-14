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
python3 -m venv <whatever_virtual_environment_name>
```

### Activate virtual environment

```bash
source <whatever_virtual_environment_name>/bin/activate   # for Unix/Linux
.\<whatever_virtual_environment_name>\Scripts\activate    # for Windows
```

### Install project libraries

```bash
pip install -r requirements.txt  # Works for both Unix/Linux and Windows
```

### Run main file

```bash
python3 main.py  # for Unix/Linux
python main.py   # for Windows
```

Now, the server is accessible at `http://localhost3000`

### First Call

![First Call](./readmeImages/firstcall.png)

![Auth Call](./readmeImages/authcall.png)

### Make your firsts changes

1. The first thing is to add your .env file. You can add a invented bearer token to get started

2. Then configure the base url in the utils/config.py file

3. In order to work on your project, you must add an endpoint to main.py.

4. Next, create a controller, and add the different web actions on the controller. It is recommended to do actions with few steps, to be able to modularize your code, and not repeat code in the future.

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

## Commond Errors

```bash
ERROR: local variable 'driver' referenced before assignment
```

`It may be because the script are taking the chromedriver from the wrong place. Every time Chrome and Chromedriver's versions are not in harmony, this error occurs`

### Steps

#### 1. Check this script. In python terminal, paste the content. If there are any errors, continue to the next step

```bash
# To run this file you must have followed the initial steps of the Readme. (Install dependencies in Virtual Enviroment)
from actions.web_driver import get_wait
from dotenv import load_dotenv
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.config import download_dir
load_dotenv()
stage = os.getenv("STAGE")
route = ChromeDriverManager().install()
options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-web-security")
options.add_argument("--disable-extension")
options.add_argument("--disable-notifications")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--password-store=basic")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--no-default-browser-check")
options.add_argument("--no-first-run")
options.add_argument("--no-proxy-server")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-popup-blocking")
options.add_argument("--start-maximized")
options.add_argument("--disable-cache")
options.add_argument("--disable-translate")
exp_opt = [
    # Disable possible errors
    "enable_automation",
    "ignore-certificate-errors",
    "enable-logging"
]
options.add_experimental_option("excludeSwitches", exp_opt)
pref_opt = {
    # Disable all type of popups
    "profile.default_content_setting_values.notifications": 2,
    "profile.password_manager_enabled": False,
    "intl.accept_languages": ["es-Es", "es"],
    "credentials_enable_service": False,
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", pref_opt)
service = Service(route)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.google.com')
wait = get_wait(driver)
wait = WebDriverWait(driver, 4)
driver.quit()

```

#### 2. To have the python script install the chromedriver again, delete this folder. In this folder is where the files that installs Python del Chromedriver are saved

```bash
rm -rf ~/.wdm
```
