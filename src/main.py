import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.exceptions.api_exceptions import MaxRetriesExceeded
from app.config.logging_setup import LoggerSetup
from app.helpers.cs_rw import write_csv
import time
import requests
from dotenv import load_dotenv
from datetime import datetime


# Internal modules

# === Logger configuration ===
logger = LoggerSetup.get_logger(__name__)


def load_config():
    """Load configuration from environment variables."""
    load_dotenv()

    config = {
        "prometheus_url": os.getenv("PROMETHEUS_URL"),
        "query": os.getenv("QUERY"),
        "client": os.getenv("CLIENT", "UNKNOWN").replace(" ", "-").upper(),
        "start_month": os.getenv("START_MONTH"),
        "end_month": os.getenv("END_MONTH"),
        "step_hours": int(os.getenv("STEP_HOURS", 1)),
    }

    config["step"] = str(config["step_hours"] * 3600)

    config["start_date"] = datetime.strptime(
        config["start_month"] + "-01", "%Y-%m-%d")
    config["end_date"] = datetime.strptime(
        config["end_month"] + "-01", "%Y-%m-%d")

    clean_range = (
        config["start_month"].replace("-", ""),
        config["end_month"].replace("-", ""),
    )
    config["output_csv"] = f"data/{config['client']}_{clean_range[0]}_{clean_range[1]}.csv"

    os.makedirs("data", exist_ok=True)
    return config


def fetch_data(prometheus_url, query, start_ts, end_ts, step, retries=3, delay=2):
    """Query Prometheus range data with retries."""
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(
                f"{prometheus_url}/api/v1/query_range",
                params={
                    "query": query,
                    "start": start_ts,
                    "end": end_ts,
                    "step": step,
                },
                timeout=10,
            )
            data = response.json()

            if data.get("status") != "success":
                raise ValueError(f"Bad response from Prometheus: {data}")

            results = data["data"]["result"]
            return results[0]["values"] if results else []

        except (requests.exceptions.RequestException, ValueError) as e:
            attempt += 1
            logger.warning(f"Attempt {attempt} failed: {e}")
            time.sleep(delay)

    logger.error(f"Max retries exceeded for {start_ts} → {end_ts}")
    raise MaxRetriesExceeded("Failed to fetch data after retries.")


def process_data(config):
    """Fetch and format all data from Prometheus month by month."""
    final_rows = []
    year = config["start_date"].year
    month = config["start_date"].month
    end_date = config["end_date"]

    while datetime(year, month, 1) <= end_date:
        start = datetime(year, month, 1)
        end = datetime(
            year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

        logger.info(f"Processing: {start.strftime('%Y-%m')}")

        values = fetch_data(
            config["prometheus_url"],
            config["query"],
            int(start.timestamp()),
            int(end.timestamp()),
            config["step"],
        )

        for ts, val in values:
            ts_dt = datetime.fromtimestamp(ts)
            date_str = ts_dt.strftime("%Y-%m-%d")
            hour_str = ts_dt.strftime("%H:%M")

            try:
                call_count = float(val)
            except ValueError:
                call_count = 0

            final_rows.append(
                {"date": date_str, "hour": hour_str, "call_count": call_count}
            )

        # Advance month
        month = 1 if month == 12 else month + 1
        year = year + 1 if month == 1 and start.month == 12 else year

    return final_rows


def main():
    config = load_config()
    try:
        data = process_data(config)

        if data:
            fieldnames = ["date", "hour", "call_count"]
            write_csv(config["output_csv"], data, fieldnames)
            logger.info(
                f" CSV saved to: {config['output_csv']} ({len(data)} rows)")
        else:
            logger.warning(" No data to write.")
    except MaxRetriesExceeded as e:
        logger.critical(f" Fatal error during data collection: {e}")


if __name__ == "__main__":
    main()
