# E-Commerce Customer & Revenue Analytics Warehouse



An end-to-end e-commerce analytics warehouse built using Python, SQL, dbt, DuckDB, and Power BI.



The project transforms raw e-commerce transaction data into tested analytical models and business-facing dashboards for customer, sales, product, and revenue analysis.



## Project Overview



This project builds a layered analytics warehouse from raw e-commerce data.



The workflow is:



Raw CSV Data → Python Data Loading → dbt Staging → Intermediate Transformation → Analytics Marts → Data Quality Audits → Power BI



The warehouse separates raw data, transformations, business logic, validation, and reporting so that analytical results can be traced through the pipeline.



## Tech Stack



\- Python

\- SQL

\- DuckDB

\- dbt

\- Power BI

\- Git / GitHub



## Dataset



The project uses the Brazilian E-Commerce Public Dataset by Olist.



The raw dataset contains information covering:



\- Customers

\- Orders

\- Order items

\- Payments

\- Reviews

\- Products

\- Sellers

\- Geolocation

\- Product category translations



Raw CSV files are intentionally excluded from Git because the complete source dataset is approximately 120 MB.



The pipeline expects the source files under:



`data/raw/`



## Warehouse Architecture



### 1. Raw Layer



The raw Olist CSV files are loaded into DuckDB without applying business transformations.



### 2. Staging Layer



The staging models standardize and prepare the raw source tables for downstream transformations.



Source tables include:



\- customers

\- geolocation

\- orders

\- order\_items

\- order\_payments

\- reviews

\- products

\- sellers

\- category\_translation



### 3. Intermediate Layer



The intermediate model enriches order-item records by combining:



\- Orders

\- Customers

\- Products

\- Sellers

\- Category translations



This creates an order-item-level analytical dataset.



### 4. Marts Layer



The warehouse contains three main analytical marts.



#### Customer Summary



Provides:



\- Total orders

\- Delivered orders

\- Total items

\- Product revenue

\- Freight

\- Total revenue

\- Average order value

\- First and last order dates

\- Customer lifetime days



#### Daily Sales



Provides:



\- Total orders

\- Total items

\- Product revenue

\- Freight

\- Total revenue

\- Average order value



#### Product Performance



Provides:



\- Total orders

\- Items sold

\- Product revenue

\- Freight

\- Total revenue

\- Average item price

\- Average freight value

\- Product and category attributes



## Revenue Definitions



\- \*\*Product revenue\*\* = item price only

\- \*\*Freight revenue\*\* = freight value

\- \*\*Total revenue\*\* = item price + freight value

\- \*\*Payment value\*\* = recorded customer payment amount



Payment value is kept as a separate financial measure rather than being treated as a direct reconciliation target for product revenue.



## Data Quality & Validation



The project includes dbt tests and custom validation queries covering model integrity and warehouse consistency.



The final dbt test run passed:



\- 59 data tests

\- 59 passed

\- 0 warnings

\- 0 errors



Additional reconciliation checks validate:



\- Raw → staging order counts

\- Staging → mart product revenue

\- Staging → mart total revenue

\- Orders without item records

\- Payment values

\- Data-quality exceptions



### Order Reconciliation



Verified warehouse figures include:



\- Raw orders: 99,441

\- Orders represented in order items: 98,666

\- Orders without items: 775

\- Product revenue: Rs 13,591,643.70

\- Freight: Rs 2,251,909.54

\- Payment value: Rs 16,008,872.12



The staging-to-mart product revenue reconciliation has a difference of Rs 0.00.



Orders without item records are separately audited rather than silently removed.



## Data Quality Audit



The audit model identifies orders without associated order-item records when their status is not expected to lack item records.



The current audit identifies three exceptions:



\- 2 invoiced orders

\- 1 shipped order



These records are retained and surfaced as data-quality exceptions rather than deleted.



## Power BI



The final Power BI dashboard provides business-facing analysis based on the warehouse marts.



The dashboard focuses on:



\- Sales performance

\- Customer analysis

\- Product performance

\- Revenue trends

\- KPI monitoring



The Power BI file is available under:



`power bi/Ecommerce\_Customer\_Revenue\_Analytics\_Final.pbix`



## Project Structure



```text

ecommerce-analytics-warehouse/

│

├── ecommerce\_analytics/

│   ├── models/

│   │   ├── staging/

│   │   ├── intermediate/

│   │   ├── marts/

│   │   └── audits/

│   ├── macros/

│   ├── tests/

│   ├── scripts/

│   └── dbt\_project.yml

│

├── scripts/

│   ├── load\_raw.py

│   └── reconcile\_orders.py

│

├── power bi/

│   └── Ecommerce\_Customer\_Revenue\_Analytics\_Final.pbix

│

├── data/

│   └── raw/

│

├── .gitignore

└── README.md

