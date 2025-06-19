# 🚀 Selenium Scraper Quickstarter

**Selenium Scraper Quickstarter** is a professional template for building robust and scalable web scrapers using Selenium and Flask, ready for local development, Docker containers, and cloud deployment.

---

## ✨ Main Features

- **Selenium Automation:** Advanced interaction with dynamic web pages.
- **RESTful API with Flask:** Secure and customizable endpoint exposure.
- **Bearer Authentication:** Security via configurable tokens.
- **Environment Management:** Environment variables for production, testing, and staging.
- **Docker & Codespaces Support:** Ready for containers and cloud development.
- **Logging System:** Activity and error logging for auditing and debugging.
- **Automated Downloads:** File and temporary directory management.
- **Extensible & Modular:** Clean architecture for easily adding actions and endpoints.

---

## 📁 Project Structure

```bash
├── main.py                   # Flask entry point
├── actions/                  # Scraping and automation logic
├── controller/               # Endpoint controllers
├── temp_downloads/           # Temporary downloads
├── utils/                    # Utilities and configuration
├── requirements.txt          # Python dependencies
├── Dockerfile                # Production-ready Docker image
├── .env.example              # Example environment configuration
└── README.md                 # This file
```

---

## ⚙️ Environment Variables

Configure scraper behavior via variables in the `.env` file. Copy `.env.example` to `.env` and customize as needed.

| Variable           | Required | Possible Values / Example                | Description                                                        |
|--------------------|----------|------------------------------------------|--------------------------------------------------------------------|
| `STAGE`            | Yes      | `production`, `testing`, `staging`       | Execution environment (affects visibility and real actions)        |
| `VALID_TOKEN`      | Yes      | `sample`                                 | Bearer token to authenticate requests                              |
| `URL`              | Yes      | `https://www.google.com/`                | Base URL the scraper connects to                                   |
| `HEADLESS_MODE`    | Optional | `auto`, `True`, `False`                  | Controls if the browser is visible or headless                     |
| `AUTO_DELETE_LOGS` | Optional | `True`, `False`                          | Automatically deletes old logs                                     |

> **Note:** See `.env.example` for more details and recommendations.

---

## 🏁 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Ismola/selenium-scraper-quickstarter.git
cd selenium-scraper-quickstarter
```

### 2. Set up your environment

- Copy `.env.example` to `.env` and edit as needed.
- Ensure you have Python 3.x and Chrome installed.

### 3. Choose your development mode

#### Option A: Dev Container (Recommended)

1. Install [VS Code](https://code.visualstudio.com/) and the **Dev Containers** extension.
2. Install [Docker](https://www.docker.com/).
3. Open the project in VS Code and select "Reopen in Container".

#### Option B: GitHub Codespaces

1. Click "Code" > "Open with Codespaces" on GitHub.
2. Wait for the environment to be set up automatically.

#### Option C: Manual

```bash
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## ▶️ Running

### Local

```bash
python3 main.py
```

### Docker

```bash
docker build -t selenium-scraper .
docker run --env-file .env -p 3000:3000 selenium-scraper
```

### Production (Gunicorn)

```bash
gunicorn -w 2 -b 0.0.0.0:3000 --timeout 600 main:app
```

---

## 🔗 API Usage

### Authentication

All protected routes require the header:

```
Authorization: Bearer <VALID_TOKEN>
```

### Default Endpoints

| Method | Route      | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`        | Server health check                |
| GET    | `/sample`  | Example endpoint (modifiable)      |

#### Example with `curl`:

```bash
curl -H "Authorization: Bearer sample" http://localhost:3000/sample
```

---

## 🛠️ Customization & Extension

1. **Add your token and URL in `.env`.**
2. **Configure the base URL in `utils/config.py` if needed.**
3. **Create new endpoints in `main.py`.**
4. **Implement scraping logic in `actions/` and controllers in `controller/`.**
5. **Use utilities from `utils/` for logging, configuration, and helpers.**

---

## 🧩 Architecture & Flow

1. **main.py:** Defines endpoints and starts Flask.
2. **controller/**: Receives the request, validates, and calls the action.
3. **actions/**: Executes scraping logic (Selenium).
4. **utils/**: Configuration, helpers, and shared utilities.
5. **temp_downloads/**: Stores temporarily downloaded files.

---

## 🚢 Deployment

There are several recommended ways to deploy your scraper in a production or staging environment:

### 1. Gunicorn (Recommended for Production)

The project is ready to be served using [Gunicorn](https://gunicorn.org/), a robust WSGI HTTP server for Python web applications. This is the method used in the provided Dockerfile.

**To run with Gunicorn manually:**

```bash
gunicorn -w 2 -b 0.0.0.0:3000 --timeout 600 main:app
```

- `-w 2`: Number of worker processes (adjust as needed).
- `-b 0.0.0.0:3000`: Binds to all interfaces on port 3000.
- `--timeout 600`: Increases timeout for long scraping tasks.

### 2. Docker (Recommended for Consistency)

You can deploy the application using Docker, ensuring all dependencies and environment settings are consistent across environments.

**Build and run the container:**

```bash
docker build -t selenium-scraper .
docker run --env-file .env -p 3000:3000 selenium-scraper
```

### 3. Docker Compose (For Multi-Service and Volume Management)

The repository includes a `compose.yaml` file for [Docker Compose](https://docs.docker.com/compose/), which simplifies running the application with persistent storage

**To deploy with Docker Compose:**

```bash
docker compose up --build
```

#### Volumes in Compose

- `./logs:/app/logs`: Persists application logs on your host machine for easier debugging and auditing.
- `./temp_downloads:/app/temp_downloads`: Stores downloaded files outside the container, so you don't lose data on container restarts.

> **Tip:** You can customize the exposed ports and volume paths in `compose.yaml` as needed for your infrastructure.

---

## ⚙️ GitHub Actions CI/CD

This project includes a preconfigured GitHub Actions workflow for continuous integration and automated Docker image publishing. You can find the workflow files in `.github/workflows/`.

### Included Workflows

- **Test (`test.yml`):**
  - Runs on every push to `main` and on pull requests.
  - Builds the Docker image and starts the application using Docker Compose.
  - Ensures the application starts correctly in a containerized environment.
  - You can add your own test steps (e.g., API calls, integration tests) inside this workflow.

- **Docker Publish (`docker-publish.yml`):**
  - Triggers automatically after a successful run of the `Test` workflow.
  - Builds and pushes the Docker image to GitHub Container Registry (`ghcr.io`).
  - Uses repository secrets for sensitive environment variables (`STAGE`, `VALID_TOKEN`, `URL`).

### How to Customize

- **Add/Modify Tests:**
  - Edit `.github/workflows/test.yml`.
  - Uncomment and adapt the `Run tests` step to include your own test scripts or API checks.
  - Example:
    ```yaml
    - name: Run tests
      run: |
        curl -f http://localhost:5008/sample || exit 1
    ```

- **Change Environment Variables for CI/CD:**
  - Go to your repository's **Settings > Secrets and variables > Actions**.
  - Add or update secrets like `STAGE`, `VALID_TOKEN`, `URL` as needed.
  - These will be injected into the Docker image during the build and publish process.

> **⚠️ Important:**  
> If you publish the Docker image to a public registry, any environment variables (such as `STAGE`, `VALID_TOKEN`, `URL`) that are injected during the build process may be visible to anyone who pulls the image.  
> **Never use production secrets or sensitive tokens in public images.**  
> For private deployments, always use private registries and restrict access to your images.

- **Change Docker Registry or Image Name:**
  - Edit the `REGISTRY` and `IMAGE_NAME` variables in `.github/workflows/docker-publish.yml`.

- **Triggering the Publish Workflow:**
  - By default, the Docker image is published only after a successful run of the `Test` workflow.
  - You can change the trigger to run on other branches or events by editing the `on:` section.

### Example: Adding a Custom Test

To add a test that checks the `/sample` endpoint:

```yaml
# In .github/workflows/test.yml
- name: Run sample endpoint test
  run: |
    curl -H "Authorization: Bearer sample" http://localhost:5008/sample
```

> **Tip:** Adjust the port if you change the exposed port in `compose.yaml`.

---

## 🤖 Instrucciones personalizadas para GitHub Copilot

Este proyecto utiliza instrucciones personalizadas para Copilot desde [Ismola/personal-copilot-instructions](https://github.com/Ismola/personal-copilot-instructions).  
Cada vez que se inicia el devcontainer, se clonan y actualizan automáticamente en `.github/instructions`.

---

## 🐞 Troubleshooting

### Common error: `local variable 'driver' referenced before assignment`

- This may be due to incompatibility between Chrome and Chromedriver.
- Quick fix:
    1. Delete the drivers folder: `rm -rf ~/.wdm`
    2. Restart the environment.

### Other issues

- Ensure environment variables are correctly set.
- Check generated logs for more details.

---

## 📚 Resources & Bibliography

- [Selenium Python Docs](https://selenium-python.readthedocs.io/)
- [Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)
- [Selenium Tutorial (YouTube)](https://youtube.com/playlist?list=PLheIVUbpfWZ17lCcHnoaa1RD59juFR06C)

---

## 🤝 Contributions

Pull requests and suggestions are welcome! Please open an issue to discuss major changes.

---

## 📝 License

MIT License © Ismola

---
