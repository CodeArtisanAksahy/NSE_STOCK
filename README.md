# NSE_STOCK
# 📈 NSE Stock Data Pipeline

An end-to-end automated data pipeline that ingests live NSE stock prices, transforms them using dbt, stores them in Google BigQuery on GCP, enriches insights with Vertex AI, and visualises everything on a Streamlit dashboard.

---

## 🏗️ Architecture

```
Yahoo Finance API
        ↓
ingest_stocks.py  →  Google BigQuery (raw.stock_prices)
        ↓
dbt run  →  stg_stock_prices (view)  →  mart_stock_summary (table)
        ↓
Vertex AI (Gemini)  →  AI market commentary
        ↓
Streamlit Dashboard  →  http://localhost:8501
        ↓
Cron Job  →  Automated every weekday at 8:30 PM IST
```

---

## 🗂️ Project Structure

```
NSE_STOCK/
├── ingest_stocks.py          # Fetches NSE data & loads to BigQuery
├── dashboard.py              # Streamlit dashboard
├── run_pipeline.sh           # Shell script to run full pipeline
├── stock_pipeline/           # dbt project
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── sources.yml
│   │   │   └── stg_stock_prices.sql
│   │   └── marts/
│   │       └── mart_stock_summary.sql
│   └── profiles.yml
└── README.md
```

---

## 🧰 Tech Stack

| Layer | Tool |
|---|---|
| Data Ingestion | Python 3, yfinance |
| Cloud Warehouse | GCP BigQuery |
| File Storage | GCP Cloud Storage |
| Transformation | dbt Core |
| AI / GenAI | Vertex AI (Gemini Pro) |
| Visualisation | Streamlit + Plotly |
| Scheduler | macOS cron |
| Auth | GCP Service Account |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/NSE_STOCK.git
cd NSE_STOCK
```

### 2. Install dependencies

```bash
pip3 install yfinance pandas google-cloud-bigquery google-cloud-aiplatform streamlit plotly dbt-bigquery
```

### 3. Set up GCP authentication

Download your GCP Service Account key and set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/keys/gcp_service_account.json
```

### 4. Configure dbt profile

Add this to `~/.dbt/profiles.yml`:

```yaml
stock_pipeline:
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your-gcp-project-id
      dataset: stock_analytics
      keyfile: ~/keys/gcp_service_account.json
      threads: 1
  target: dev
```

### 5. Create BigQuery dataset and table

```sql
CREATE SCHEMA stock_analytics;

CREATE TABLE stock_analytics.stock_prices (
    stock_symbol  STRING,
    trade_date    DATE,
    open_price    FLOAT64,
    high_price    FLOAT64,
    low_price     FLOAT64,
    close_price   FLOAT64,
    volume        INT64,
    loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

---

## ▶️ Running the Pipeline

### Run ingestion

```bash
python3 ingest_stocks.py
```

### Run dbt transforms

```bash
cd stock_pipeline
dbt run
```

### Launch dashboard

```bash
streamlit run dashboard.py
```

### Run full pipeline in one command

```bash
bash run_pipeline.sh
```

---

## ⏰ Automating with Cron

Schedule the pipeline to run every weekday after NSE market close:

```bash
crontab -e
```

Add this line:

```
0 15 * * 1-5 /bin/bash ~/NSE_STOCK/run_pipeline.sh >> ~/NSE_STOCK/pipeline.log 2>&1
```

This runs at **3:00 PM UTC = 8:30 PM IST**, Monday to Friday.

---

## 📦 Stocks Tracked

| Ticker | Company |
|---|---|
| `RELIANCE.NS` | Reliance Industries |
| `TCS.NS` | Tata Consultancy Services |
| `INFY.NS` | Infosys |
| `HDFCBANK.NS` | HDFC Bank |
| `WIPRO.NS` | Wipro |

---

## 🤖 Vertex AI Integration

The pipeline uses **Gemini Pro on Vertex AI** to generate daily natural language market commentary based on the latest `daily_pct_change` values from the mart model. The summary is displayed directly on the Streamlit dashboard.

---

## 📄 dbt Models

| Model | Type | Description |
|---|---|---|
| `stg_stock_prices` | View | Cleans and standardises raw stock data |
| `mart_stock_summary` | Table | Calculates daily % price change using `LAG()` window function |

---

## 📝 License

MIT License. Free to use and modify.

---

Built by [Akshay Thakur](https://github.com/YOUR_USERNAME)
