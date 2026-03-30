# 🚚 Supply Chain Analytics — End-to-End ETL Pipeline with ML

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=for-the-badge&logo=github&logoColor=white)

---

## 📌 Project Overview

A complete **end-to-end data engineering and machine learning project** built on the DataCo Smart Supply Chain dataset (180,000+ records). This project simulates a real-world data pipeline — from raw data ingestion to a live Power BI dashboard — covering every stage a Data Analyst or Data Scientist is expected to handle.

> **"I deliberately removed data leakage features that inflated accuracy to 97%, and built an honest model at 62% using only pre-shipment data — because a model that works in production matters more than one that looks good on paper."**

---

## 🎯 Business Problem

Supply chain companies lose millions annually due to late deliveries — leading to customer dissatisfaction, refund costs, and damaged brand reputation. 

**This project answers:**
- Which shipping modes have the highest late delivery risk?
- Can we predict whether an order will be late *before* it ships?
- What months see the highest sales and delivery failures?

---

## 🗂️ Dataset

| Property | Details |
|----------|---------|
| **Source** | [DataCo Smart Supply Chain — Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) |
| **Records** | 180,519 rows |
| **Columns** | 53 features |
| **Period** | 2015 – 2018 |
| **Target Column** | `Late_delivery_risk` (0 = On-time, 1 = Late) |

---

## 🏗️ Pipeline Architecture

```
Raw CSV (180K records)
        │
        ▼
┌───────────────┐
│  extract.py   │  ← Load CSV with latin-1 encoding, schema validation
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ transform.py  │  ← Clean data, engineer features, encode categoricals
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   load.py     │  ← Push to PostgreSQL (dim_customers + fact_orders)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   model.py    │  ← Train Random Forest, export predictions CSV
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Power BI     │  ← Live dashboard connected to PostgreSQL
└───────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.13 |
| Data Processing | Pandas, NumPy |
| Database | PostgreSQL 16 + pgAdmin 4 |
| ORM / Connector | SQLAlchemy, psycopg2 |
| Machine Learning | Scikit-learn (Random Forest) |
| Visualization | Power BI Desktop |
| Version Control | Git + GitHub |

---

## 📁 Project Structure

```
supply-chain-etl-pipeline/
│
├── 📂 data/
│   ├── DataCoSupplyChainDataset.csv    ← raw dataset (not pushed to GitHub)
│   ├── clean_data.csv                  ← transformed data (gitignored)
│   └── predictions.csv                 ← ML model output
│
├── 📂 powerbi/
│   └── Dashboard_updated.pbix                  ← Power BI dashboard file
│
├── extract.py                          ← Stage 1: Extract
├── transform.py                        ← Stage 2: Transform
├── load.py                             ← Stage 3: Load to PostgreSQL
├── model.py                            ← Stage 4: ML Model
├── pipeline.py                         ← Master runner (runs all stages)
├── .gitignore
└── README.md
```

---

## 🔧 Feature Engineering

New columns created during transformation:

| Feature | Formula | Purpose |
|---------|---------|---------|
| `delay_days` | real_days − scheduled_days | Delivery delay measure |
| `profit_margin` | (profit / sales) × 100 | Profitability % |
| `order_month` | extracted from order_date | Seasonality analysis |
| `order_year` | extracted from order_date | Year-over-year trends |
| `shipping_enc` | Label encoded Shipping Mode | ML input feature |

---

## 🤖 Machine Learning Model

### Model: Random Forest Classifier

**Features used (pre-shipment only — no data leakage):**
- Days for shipment (scheduled)
- Shipping mode (encoded)
- Sales value
- Order item quantity
- Order month
- Profit margin

### Results

```
              precision    recall  f1-score   support

           0       0.58      0.58      0.58     16307
           1       0.66      0.65      0.65     19797

    accuracy                           0.62     36104
   macro avg       0.62      0.62      0.62     36104
weighted avg       0.62      0.62      0.62     36104
```

### ⚠️ Important Note on Data Leakage
An initial model using `delay_days` as a feature achieved **97% accuracy** — but this was due to **data leakage** (using post-shipment information to predict a pre-shipment outcome). After removing the leaky feature, the honest accuracy is **62%** — a realistic result for predicting delivery outcomes using only pre-shipment data.

---

## 📊 Key Business Insights

| Finding | Insight |
|---------|---------|
| 🔴 First Class shipping | Highest late delivery risk (~95%) |
| 🟡 Second Class shipping | Second highest risk (~85%) |
| 🟢 Standard Class | Lowest late delivery risk (~45%) |
| 📈 Peak sales month | January (3.5M revenue) |
| 📉 Lowest sales month | December (2.4M revenue) |
| ⚠️ Predicted late orders | 42.62% of all orders at risk |

---

## 🗄️ Database Schema (Star Schema)

```
         ┌─────────────────┐
         │  dim_customers  │
         │─────────────────│
         │ customer_id  PK │
         │ customer_name   │
         │ segment         │
         │ city            │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   fact_orders   │
         │─────────────────│
         │ order_id     PK │
         │ customer_id  FK │
         │ order_date      │
         │ sales           │
         │ profit          │
         │ delay_days      │
         │ late_risk       │
         │ shipping_mode   │
         └─────────────────┘
```

---

## 🚀 How to Run This Project

### Prerequisites
- Python 3.x installed
- PostgreSQL installed and running
- Power BI Desktop installed

### Step 1 — Clone the repository
```bash
git clone https://github.com/ektashirsulla26-source/supply-chain-etl-pipeline.git
cd supply-chain-etl-pipeline
```

### Step 2 — Install dependencies
```bash
pip install pandas scikit-learn xgboost sqlalchemy psycopg2-binary openpyxl
```

### Step 3 — Add the dataset
Download the dataset from Kaggle and place it in:
```
data/DataCoSupplyChainDataset.csv
```

### Step 4 — Configure PostgreSQL
Open `load.py` and update your credentials:
```python
DB = URL.create(
    drivername="postgresql",
    username="postgres",
    password="YOUR_PASSWORD",
    host="localhost",
    port=5432,
    database="supply_chain_db"
)
```

### Step 5 — Run the full pipeline
```bash
python pipeline.py
```

This runs all 4 stages automatically:
```
✓ Loaded 180519 rows and 53 columns
✓ Transform done. Shape: (180519, 57)
✓ dim_customers loaded!
✓ fact_orders loaded!
Training model... please wait
✓ Model saved!
✓ Predictions saved to data/predictions.csv
✓ Full pipeline complete!
```

### Step 6 — Open Power BI Dashboard
Open `powerbi/Dashboard.pbix` in Power BI Desktop → click Refresh

---

## 📈 Power BI Dashboard

The dashboard contains 1 page with 5 visuals:

| Visual | Description |
|--------|-------------|
| 📦 KPI Card | Total Orders: 180,519 |
| 💰 KPI Card | Total Revenue: $36.78M |
| ⏱️ KPI Card | Avg Delay: 0.57 days |
| 📊 Bar Chart | Late delivery risk by shipping mode |
| 📉 Line Chart | Monthly sales trend |
| 🍩 Donut Chart | Predicted late vs on-time orders |

---

## 🔮 Future Improvements

- [ ] Add weather API data to improve prediction accuracy
- [ ] Implement XGBoost for comparison
- [ ] Add SHAP explainability plots
- [ ] Schedule pipeline with Apache Airflow
- [ ] Deploy dashboard to Power BI Service (cloud)
- [ ] Add carrier performance history as a feature

---

## 👩‍💻 About the Author

**Ekta Shirsulla**
M.Sc. Statistics | Data Analyst | Aspiring Data Scientist

📧 ektashirsulla26@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/ekta-shirsulla)  
🐙 [GitHub](https://github.com/ektashirsulla26-source)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with ❤️ using Python, PostgreSQL, Scikit-learn and Power BI*
