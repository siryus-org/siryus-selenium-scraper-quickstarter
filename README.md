# 🚀 Selenium Scraper Quickstarter

**Selenium Scraper Quickstarter** is a professional template for building robust and scalable web scrapers using Selenium and Flask, ready for local development, Docker containers, and cloud deployment.

[![Deploy](https://github.com/siryus-org/siryus-selenium-scraper-quickstarter/actions/workflows/deploy.yml/badge.svg)](https://github.com/siryus-org/siryus-selenium-scraper-quickstarter/actions/workflows/deploy.yml)

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
| `HEADLESS_MODE`    | Optional | `auto`, `True`, `False`                  | Controls if the browser is visible or headless                     |
| `LOG_LEVEL` | Optional | `INFO`, `DEBUG`, `WARNING` | JSON stdout logging level |

> **Note:** See `.env.example` for more details and recommendations.
> **Base URL:** Set `BASE_URL` in `.env` or pass `url=` to the shared browser helper.

---

## 🏁 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Ismola/selenium-scraper-quickstarter.git
cd selenium-scraper-quickstarter
```

### 2. Set up your environment

- Copy `.env.example` to `.env` and edit it as needed.
- Make sure you have Python 3.x and Google Chrome installed.
- **Set the base URL:** Set `BASE_URL` in `.env` to point to your target website.

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
python -m pip install -r requirements.txt
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

## ⚙️ CI/CD and Workflow Customization

- **Change environment variables for CI/CD:**
  - Go to **Settings > Secrets and variables > Actions** in your GitHub repository.
  - Add or update secrets like `STAGE`, `VALID_TOKEN` as needed.
  - These will be injected into the Docker image during the build and publish process.

> **⚠️ Important:**  
> If you publish the Docker image to a public registry, any environment variable (such as `STAGE`, `VALID_TOKEN`) injected during build may be visible to anyone who downloads the image.  
> **Never use production secrets or sensitive tokens in public images.**  
> For private deployments, always use private registries and restrict access to your images.

- **Change Docker registry or image name:**
  - Edit the `REGISTRY` and `IMAGE_NAME` variables in `.github/workflows/docker-publish.yml`.

- **Trigger the publish workflow:**
  - By default, the Docker image is published only after a successful run of the `Test` workflow.
  - You can change the trigger to run on other branches or events by editing the `on:` section.

> **Tip:** Adjust the port if you change the exposed port in `compose.yaml`.

---

## 🔗 API Usage

### Authentication

All protected routes require the header:

```curl
Authorization: Bearer <VALID_TOKEN>
```

### Default Endpoints

| Method | Route      | Description                        |
|--------|-----------|------------------------------------|
| GET    | `/`        | Server health check                |
| GET    | `/sample`  | Example endpoint (modifiable)      |

#### Example with `curl`

```bash
curl -H "Authorization: Bearer sample" http://localhost:3000/sample
```

---

## 🛠️ Customization & Extension

1. **Add your token in `.env`.**
2. **Set the base URL in `utils/config.py` by editing the `BASE_URL` constant.**
3. **Create new endpoints in `main.py`.**
4. **Implement scraping logic in `actions/` and controllers in `controller/`.**
5. **Use utilities from `utils/` for logging, configuration, and helpers.**

---

## 🧩 Architecture & Flow

1. **main.py:** Defines endpoints and starts Flask.
2. **controller/**: Receives the request, validates, and calls the action.
3. **actions/**: Executes scraping logic (Selenium).
4. **utils/**: Configuration, helpers, and shared utilities.  
   - **BASE_URL** is defined in `utils/config.py`.
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

- Application logs are JSON on stdout and can be collected by Alloy and viewed in Grafana via Loki.
- `./temp_downloads:/app/temp_downloads`: Stores downloaded files outside the container, so you don't lose data on container restarts.

> **Tip:** You can customize the exposed ports and volume paths in `compose.yaml` as needed for your infrastructure.

---

## ⚙️ GitHub Actions CI/CD

This project includes a preconfigured GitHub Actions workflow for continuous integration and automated Docker image publishing. You can find the workflow files in `.github/workflows/`.

### Included Workflows

- **Docker Smoke (`docker-smoke.yml`):**
  - Builds the Docker image and verifies that the application starts correctly using Docker Compose.
  - Performs a smoke test by accessing the root endpoint (`/`) to ensure the container responds.

- **CI Test Suite (`ci-test.yml`):**
  - Runs after the smoke test.
  - Installs dependencies and runs automated tests with `pytest` inside the Docker Compose environment.
  - Ensures the application passes tests before continuing the pipeline.

- **Docker Build & Publish (`docker-publish.yml`):**
  - Runs only if the previous workflows are successful.
  - Builds and publishes the Docker image to GitHub Container Registry (`ghcr.io`).
  - Uses environment variables and secrets configured in the repository.

> ⚙️ You can customize or extend these workflows by editing the files in `.github/workflows/` as needed for your CI/CD requirements.

## Shared scraper runtime

The Dockerfile and devcontainer use the rolling `latest` [selenium-scraper-runtime](https://github.com/Ismola/selenium-scraper-runtime) image. Logging, Prometheus metrics, browser setup and cleanup, and common element actions are installed from the runtime `main` branch. Rebuild with pull enabled to receive current shared code and browsers.

Use `selenium_scraper_runtime.browser` for `get_page`, `browser_session`, `get_wait`, and `close_driver`; use `selenium_scraper_runtime.elements` for `search_element`, `click_element`, `write_element`, and `hover_element`. Keep only site-specific selectors and workflows in `actions/`. `WEBDRIVER_MAX_LIFETIME` limits the lifetime of a local browser session, including when a worker dies before it can close the driver. Raise it in `.env` for legitimate jobs longer than 12 minutes. Gunicorn recycles API workers after a bounded number of requests (`GUNICORN_MAX_REQUESTS`, default 100) to limit long-term memory growth.

Application logs are JSON on stdout and include a `run_id`; every API response includes `X-Run-ID`. Alloy can collect the Docker logs and forward them to Loki for Grafana.

## 📈 Prometheus metrics

The API listens on port `3000`; Prometheus metrics are intentionally served by a
separate process on port `9090` at `/metrics`. The metrics port is bound to
`127.0.0.1` by the example Compose file. In a private Docker network it can be
scraped directly as `server:9090`.

Available application metrics include:

- `scraper_http_requests_total`: successful and failed calls by endpoint, method, and status.
- `scraper_http_request_duration_seconds`: request latency histogram.
- `scraper_http_requests_in_progress`: current API usage/concurrency.
- `scraper_unhandled_exceptions_total`: unhandled request exceptions.
- `scraper_build_info`: service identity and scrape readiness.

Set `SCRAPER_SERVICE_NAME` to a stable deployment name and change
`METRICS_PORT` if `9090` is already in use. Production startup also requires a
non-default `VALID_TOKEN`; the image refuses to start with `sample`.

```bash
curl http://127.0.0.1:9090/-/healthy
curl http://127.0.0.1:9090/metrics
```

---

## 🧪 Automated Testing

The project includes automated tests located in the `test/` folder, using `pytest` and Flask's test client.

### 📂 Test Structure

- `test/test_main.py`: Tests for the main endpoints defined in `main.py`.

### ▶️ How to run the tests

1. Install dependencies if you haven't already:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Run the tests:

   ```bash
   pytest --maxfail=1 --disable-warnings -v
   ```

> 💡 **Tip:** You can also run the tests automatically in the CI/CD flow with GitHub Actions.

### ✏️ How to modify or add tests?

- Edit or add files in the `test/` folder following the example in `test_main.py`.
- Use the Flask client to simulate HTTP requests and validate responses.
- To test new endpoints, create functions starting with `test_` and use the `client` fixture.
- See the [pytest documentation](https://docs.pytest.org/) for more options and best practices.

---

## 🤖 Custom instructions for GitHub Copilot

This project uses custom Copilot instructions from [Ismola/personal-copilot-instructions](https://github.com/Ismola/personal-copilot-instructions).  
Each time the devcontainer starts, they are cloned and updated automatically in `.github/instructions`.

---

## 🐞 Troubleshooting

### Browser startup errors

- Check the container logs for the specific driver error. The base image includes a matching Chromium and ChromeDriver. For local development, Selenium resolves the driver for the installed browser.

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
