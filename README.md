# Prometheus Occupation Exporter

This project is a custom Python tool for querying Prometheus time series data and exporting it to structured CSV files. It is designed for backend monitoring, reporting, and automation workflows. The system supports hourly resolution, retry logic, and structured logging.

## Project Structure

prometheus_ocupation/
├── app/
│ ├── config/ # Logging setup
│ ├── exceptions/ # Custom error classes
│ └── helpers/ # CSV read/write helpers
├── data/ # Output CSV files
├── logs/ # Application logs
├── src/
│ └── main.py # Main entry point
├── .env # Environment configuration (not committed)
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .gitignore # Ignored files and folders



## Features

- Query Prometheus using custom PromQL expressions
- Export time series to CSV with hourly granularity
- Retry logic with exception handling
- Environment-based configuration using `.env`
- Structured logging to both console and file
- Modular code with helpers and custom exception handling

## Requirements

- Python 3.8+
- Prometheus with HTTP access to `/api/v1/query_range`
- Access to Prometheus metric: `metric`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/prometheus_ocupation.git
cd prometheus_ocupation


python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

```

Edit .env with your desired values:

PROMETHEUS_URL=http://localhost:9090
QUERY=metric
CLIENT=client-name
START_MONTH=2024-06
END_MONTH=2025-04
STEP_HOURS=1

```bash
python3 src/main.py
```

The output CSV file will be saved in the data/ folder with a filename based on the client and date range.
Logging

Logs are saved to logs/app.log and streamed to the console. The logger is configured via app/config/logging.ini.
Customization

    To adjust logging: edit app/config/logging.ini

    To modify Prometheus retries or backoff: update fetch_data() in main.py

    To change output format: modify write_csv() in app/helpers/cs_rw.py

License

This project is private and proprietary. All rights reserved.


---

Let me know if you'd like a Spanish version, or to include a badge header (like "Python version", "Build passing", etc.) for a public repo.
